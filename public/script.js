/**
 * Configuration Module
 * @module config
 * @description Defines the configuration settings for the visualization, including dimensions, styling, and behavior.
 */
const config = {
    // Margin settings for the visualization area
    margin: { top: 20, right: 380, bottom: 20, left: 100 },
    // Computes the total width of the SVG element based on the window size
    get totalWidth() { return window.innerWidth - 40; },
    // Computes the total height of the SVG element based on the window size
    get totalHeight() { return window.innerHeight * 0.85; },
    // Computes the usable width for the tree layout, considering margins
    get width() { return this.totalWidth - this.margin.left - this.margin.right; },
    // Computes the usable height for the tree layout, considering margins
    get height() { return this.totalHeight - this.margin.top - this.margin.bottom; },
    // Duration for transitions in milliseconds
    transitionDuration: 750,
    // Radius of the nodes in the tree
    nodeRadius: 8,
    // Function to calculate the stroke width of links based on depth
    linkStrokeWidth: (d) => Math.max(1.5, 4 - d.target.depth * 0.5),
    // Offset for the tooltip position
    tooltipOffset: 10,
    // Width of the comment panel
    commentPanelWidth: 350,
    // Height of the comment panel, dynamically calculated based on viewport height
    commentPanelHeight: 'calc(85vh - 40px)',
    // Left margin for comment items in the comment panel
    commentItemMarginLeft: 20,
    // Default fill color for nodes
    defaultNodeFill: "#2378ae",
    // Fill color for reply nodes
    replyNodeFill: "#ff7f0e",
    // Stroke color for links
    linkStrokeColor: "#666",
    // Opacity for link strokes
    linkStrokeOpacity: 0.9,
    // Stroke color for nodes
    nodeStrokeColor: "#fff",
    // Stroke width for nodes
    nodeStrokeWidth: 2,
    // Text color
    textColor: "#333",
    // Font size for text elements
    fontSize: "12px",
    // Flag to control the visibility of author names
    nameVisibility: true,
};

/**
 * Data Handling Module
 * @module dataModule
 * @description Handles the loading and transformation of post data from a JSON file.
 */
const dataModule = {
    // Array to store loaded posts
    posts: [],
    // Currently selected post
    currentPost: null,
    /**
     * Transforms the raw post data into a hierarchical structure suitable for tree visualization.
     * @param {Object} post - The post object containing post details and comments.
     * @returns {Object} The root node of the hierarchical data.
     */
    transformData: function(post) {
        const rootNode = {
            thing_id: post.post_id,
            depth: 0,
            parent_id: null,
            author: post.author,
            text: post.content,
            action_id: post.post_id,
            more_replies: null,
            replies: post.comments.map(comment => ({
                ...comment,
                depth: comment.depth + 1,
                parent_id: comment.depth === 0 ? post.post_id : comment.parent_id
            }))
        };
        return rootNode;
    },
    /**
     * Loads post data from a JSON file.
     * @async
     * @returns {Promise<Array>} A promise that resolves to an array of post objects.
     */
    loadPosts: async function() {
        try {
            this.posts = await d3.json("posts_data_20241217_000658.json");
            return this.posts;
        } catch (error) {
            console.error("Error loading posts:", error);
            return [];
        }
    }
};

/**
 * Tree Layout Module
 * @module treeModule
 * @description Handles the layout and rendering of the tree visualization using D3.js.
 */
const treeModule = {
    // The root node of the tree
    root: null,
    // Flag to indicate if the layout is horizontal or vertical
    isHorizontal: true,
    // D3 tree layout function
    tree: d3.tree()
        .separation((a, b) => (a.parent == b.parent ? 1.5 : 2.5)),
    /**
     * Updates the layout of the tree visualization.
     * @param {Object} svg - The D3 selection of the SVG element.
     * @param {Object} g - The D3 selection of the main 'g' element within the SVG.
     */
    updateLayout: function(svg, g) {
        // Set the size of the tree layout based on orientation
        this.tree.size(this.isHorizontal ? [config.height, config.width * 0.8] : [config.width, config.height * 0.6]);
        // Compute the tree layout
        let treeData = this.tree(this.root);

        // Create or select the links group
        const linksGroup = g.selectAll(".links-group").data([null]);
        linksGroup.enter().append("g").attr("class", "links-group");

        // Create or select the nodes group
        const nodesGroup = g.selectAll(".nodes-group").data([null]);
        nodesGroup.enter().append("g").attr("class", "nodes-group");

        // Update links
        const links = g.select(".links-group").selectAll(".link").data(treeData.links());
        links.exit().remove();

        // Enter new links
        const linkEnter = links.enter().append("path").attr("class", "link");
        // Merge and transition links
        linkEnter.merge(links)
            .transition()
            .duration(config.transitionDuration)
            .attr("d", this.isHorizontal
                ? d3.linkHorizontal().x(d => d.y).y(d => d.x)
                : d3.linkVertical().x(d => d.x).y(d => d.y))
            .style("stroke", config.linkStrokeColor)
            .style("stroke-width", config.linkStrokeWidth)
            .style("stroke-opacity", config.linkStrokeOpacity)
            .style("fill", "none");

        // Update nodes
        const nodes = g.select(".nodes-group").selectAll(".node").data(treeData.descendants());
        nodes.exit().remove();

        // Enter new nodes
        const nodeEnter = nodes.enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => this.isHorizontal ? `translate(${d.y},${d.x})` : `translate(${d.x},${d.y})`)
            .on("mouseover", function(event, d) {
                // Show tooltip on mouseover
                tooltipModule.showTooltip(event, d);
            })
            .on("mouseout", function() {
                // Hide tooltip on mouseout
                tooltipModule.hideTooltip();
            })
            .on("click", function(event, d) {
                // Update comment chain on node click
                commentPanelModule.updateCommentChain(d);
            });

        // Add circles to new nodes
        nodeEnter.append("circle")
            .attr("r", config.nodeRadius)
            .style("fill", d => d.depth === 0 ? config.defaultNodeFill : config.replyNodeFill)
            .style("stroke", config.nodeStrokeColor)
            .style("stroke-width", config.nodeStrokeWidth);

        // Add text to new nodes
        nodeEnter.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -13 : 13)
            .attr("text-anchor", d => d.children ? "end" : "start")
            .style("fill", config.textColor)
            .style("font-size", config.fontSize);

        // Update text content and visibility
        nodes.select("text")
            .merge(nodeEnter.select("text"))
            .text(d => {
                if (d.depth === 0 || !d.children) {
                    return d.data.author;
                }
                return "";
            })
            .attr("visibility", config.nameVisibility ? "visible" : "hidden");

        // Merge and transition nodes
        nodes.merge(nodeEnter)
            .transition()
            .duration(config.transitionDuration)
            .attr("transform", d => this.isHorizontal ? `translate(${d.y},${d.x})` : `translate(${d.x},${d.y})`);
    }
};

/**
 * Tooltip Module
 * @module tooltipModule
 * @description Manages the display and content of the tooltip that appears on node hover.
 */
const tooltipModule = {
    // The tooltip element
    tooltip: d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0),
    /**
     * Shows the tooltip with information about the hovered node.
     * @param {Object} event - The mouse event.
     * @param {Object} d - The data of the hovered node.
     */
    showTooltip: function(event, d) {
        this.tooltip.transition().duration(200).style("opacity", .9);
        this.tooltip.html(`
            <strong>${d.data.author}</strong><br/>
            ${d.depth === 0
                ? ` <small>Original Post</small><hr/>${d.data.text.substring(0, 100)}...`
                : ` <small>Depth: ${d.data.depth}</small><br/>${d.data.text.substring(0, 100)}...`
            }
        `)
        .style("left", (event.pageX + config.tooltipOffset) + "px")
        .style("top", (event.pageY - 28) + "px");
    },
    /**
     * Hides the tooltip.
     */
    hideTooltip: function() {
        this.tooltip.transition().duration(500).style("opacity", 0);
    }
};

/**
 * Comment Panel Module
 * @module commentPanelModule
 * @description Manages the display of the comment chain for the selected node.
 */
const commentPanelModule = {
    // The comment panel element
    commentPanel: d3.select("#tree-container").append("div").attr("class", "comment-panel"),
    /**
     * Updates the comment panel to display the comment chain of the clicked node.
     * @param {Object} node - The clicked node.
     */
    updateCommentChain: function(node) {
        const chain = [];
        let current = node;
        // Traverse up the tree to build the comment chain
        while (current) {
            chain.unshift(current.data);
            current = current.parent;
        }

        // Clear the comment panel
        this.commentPanel.html("");
        // Add a title to the comment panel
        this.commentPanel.append("h3").attr("class", "comment-panel-title").text("Comment Thread");

        // Add each comment to the panel
        chain.forEach((comment, index) => {
            const commentDiv = this.commentPanel.append("div")
                .attr("class", "comment-item")
                .style("margin-left", (index * config.commentItemMarginLeft) + "px");

            commentDiv.append("div").attr("class", "comment-author").text(comment.author);
            commentDiv.append("div").attr("class", "comment-text").text(comment.text);

            // Add a separator between comments
            if (index < chain.length - 1) {
                commentDiv.append("div").attr("class", "comment-separator");
            }
        });
    }
};

/**
 * UI Interaction Module
 * @module uiModule
 * @description Handles the setup and interaction of UI elements like the post selector, toggle buttons, and window resize.
 */
const uiModule = {
    /**
     * Sets up the post selector dropdown.
     * @param {Array} posts - The array of post objects.
     * @param {Function} visualizePost - The function to call when a post is selected.
     */
    setupPostSelector: function(posts, visualizePost) {
        // Append the select element to the header
        d3.select(".header")
            .append("select")
            .attr("id", "post-selector")
            .style("margin-left", "20px")
            .style("padding", "5px")
            .style("font-size", "16px")
            .on("change", function() {
                // Find the selected post and visualize it
                const selectedPost = posts.find(p => p.post_id === this.value);
                visualizePost(selectedPost);
            });

        // Add options to the select element
        d3.select("#post-selector")
            .selectAll("option")
            .data(posts)
            .enter()
            .append("option")
            .attr("value", d => d.post_id)
            .text(d => d.title || `Post ${d.post_id}`);
    },
    /**
     * Sets up the toggle layout button.
     * @param {Function} updateLayout - The function to call to update the tree layout.
     */
    setupToggleLayoutButton: function(updateLayout) {
        // Add a click listener to the toggle layout button
        d3.select("#toggle-button").on("click", () => {
            treeModule.isHorizontal = !treeModule.isHorizontal;
            updateLayout();
        });
    },
    /**
     * Sets up the toggle names button.
     * @param {Function} updateLayout - The function to call to update the tree layout.
     */
    setupToggleNamesButton: function(updateLayout) {
        // Append the toggle names button to the tree container
        d3.select("#tree-container")
            .append("button")
            .attr("id", "toggle-names-button")
            .text("Toggle Names")
            .on("click", () => {
                // Toggle the name visibility flag and update the layout
                config.nameVisibility = !config.nameVisibility;
                updateLayout();
            });
    },
    /**
     * Sets up the window resize handler.
     * @param {Object} svg - The D3 selection of the SVG element.
     * @param {Function} updateLayout - The function to call to update the tree layout.
     */
    setupResizeHandler: function(svg, updateLayout) {
        // Add an event listener for window resize
        window.addEventListener('resize', () => {
            // Calculate new dimensions
            const newWidth = window.innerWidth - 40;
            const newHeight = window.innerHeight * 0.85;

            // Update SVG dimensions
            svg.attr("width", newWidth).attr("height", newHeight);

            // Update config dimensions
            config.width = newWidth - config.margin.left - config.margin.right;
            config.height = newHeight - config.margin.top - config.margin.bottom;

            // Update tree size and layout
            treeModule.tree.size([config.height, config.width]);
            updateLayout();
        });
    }
};

/**
 * Main Module
 * @module mainModule
 * @description Initializes the application, sets up the SVG, loads data, and sets up UI interactions.
 */
const mainModule = {
    // The SVG element
    svg: null,
    // The main 'g' element within the SVG
    g: null,
    /**
     * Initializes the application.
     * @async
     */
    init: async function() {
        // Initialize SVG and main 'g' element
        this.svg = d3.select("#tree-container")
            .append("svg")
            .attr("width", config.totalWidth)
            .attr("height", config.totalHeight)
            .call(d3.zoom().on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            }))
            .append("g")
            .attr("transform", `translate(${config.margin.left},${config.margin.top})`);

        // Set the viewBox attribute for responsive scaling
        this.svg.attr("viewBox", [0, 0, config.totalWidth, config.totalHeight]);
        // Add a background rectangle to the SVG
        this.svg.append("rect")
            .attr("width", config.width)
            .attr("height", config.height)
            .attr("fill", "none")
            .attr("pointer-events", "all");

        // Append the main 'g' element to the SVG
        this.g = this.svg.append("g");

        // Load posts and setup UI
        const posts = await dataModule.loadPosts();
        if (posts.length > 0) {
            uiModule.setupPostSelector(posts, this.visualizePost.bind(this));
            this.visualizePost(posts[0]);
        }

        // Setup UI interactions
        uiModule.setupToggleLayoutButton(treeModule.updateLayout.bind(treeModule, this.svg, this.g));
        uiModule.setupToggleNamesButton(treeModule.updateLayout.bind(treeModule, this.svg, this.g));
        uiModule.setupResizeHandler(this.svg, treeModule.updateLayout.bind(treeModule, this.svg, this.g));
    },
    /**
     * Visualizes the selected post.
     * @param {Object} post - The selected post object.
     */
    visualizePost: function(post) {
        // Set the current post and transform the data
        dataModule.currentPost = post;
        const transformedData = dataModule.transformData(post);
        // Create a D3 hierarchy from the transformed data
        treeModule.root = d3.hierarchy(transformedData, d => d.replies);

        // Reset the zoom and transition to the new layout
        this.svg.transition().duration(config.transitionDuration).call(
            d3.zoom().transform,
            d3.zoomIdentity
        );

        // Update the tree layout
        treeModule.updateLayout(this.svg, this.g);
    }
};

// Initialize the application
mainModule.init();
