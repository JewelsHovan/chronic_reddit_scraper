// Add this near the top with other variable declarations
let i = 0;  // Counter for generating unique IDs
let root; // Add this at the top with other variables
let posts = [];
let currentPost = null;

// Update the margin settings for better spacing
const margin = {top: 20, right: 380, bottom: 20, left: 100};
const totalWidth = window.innerWidth - 40;
const totalHeight = window.innerHeight * 0.85; // Slightly reduced to prevent overflow
const width = totalWidth - margin.left - margin.right;
const height = totalHeight - margin.top - margin.bottom;

// Create a container for the comment panel - now we just append it as is
// Since #tree-container is position:relative, these absolute coords are relative to it.
const commentPanel = d3.select("#tree-container")
    .append("div")
    .attr("class", "comment-panel");

// Create the SVG container with zoom support
const svg = d3.select("#tree-container")
    .append("svg")
    .attr("width", totalWidth)
    .attr("height", totalHeight)
    .call(d3.zoom().on("zoom", (event) => {
        g.attr("transform", event.transform);
    }))
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Add viewBox for better scaling
svg.attr("viewBox", [
    0,  // Start from 0 since we're using container centering
    0,
    totalWidth,
    totalHeight
]);

// Background rectangle for zoom
svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("fill", "none")
    .attr("pointer-events", "all");

const g = svg.append("g");

// Tree layout
let isHorizontal = true;
const tree = d3.tree()
    .size([height, width])
    .separation((a, b) => (a.parent == b.parent ? 1.5 : 2.5)); // Adjusted separation

// Tooltip
const tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// Move updateLayout outside and declare it before use
function updateLayout() {
    // Update tree dimensions based on orientation
    tree.size(isHorizontal ? [height, width * 0.8] : [width, height * 0.6]);
    let treeData = tree(root);

    // Create a group for links that will be rendered first
    const linksGroup = g.selectAll(".links-group").data([null]);
    linksGroup.enter()
        .append("g")
        .attr("class", "links-group");

    // Create a group for nodes that will be rendered on top
    const nodesGroup = g.selectAll(".nodes-group").data([null]);
    nodesGroup.enter()
        .append("g")
        .attr("class", "nodes-group");

    // Update links (now specifically in the links group)
    const links = g.select(".links-group")
        .selectAll(".link")
        .data(treeData.links());

    links.exit().remove();

    const linkEnter = links.enter()
        .append("path")
        .attr("class", "link");

    linkEnter.merge(links)
        .transition()
        .duration(750)
        .attr("d", isHorizontal 
            ? d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x)
            : d3.linkVertical()
                .x(d => d.x)
                .y(d => d.y))
        .style("stroke", "#666")
        .style("stroke-width", d => Math.max(1.5, 4 - d.target.depth * 0.5))
        .style("stroke-opacity", 0.9)
        .style("fill", "none");

    // Update nodes (now specifically in the nodes group)
    const nodes = g.select(".nodes-group")
        .selectAll(".node")
        .data(treeData.descendants());

    nodes.exit().remove();

    // Handle entering nodes
    const nodeEnter = nodes.enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => isHorizontal 
            ? `translate(${d.y},${d.x})`
            : `translate(${d.x},${d.y})`)
        .on("mouseover", function(event, d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html(`
                <strong>${d.data.author}</strong><br/>
                ${d.depth === 0 
                    ? `<small>Original Post</small><hr/>${d.data.text.substring(0, 100)}...` 
                    : `<small>Depth: ${d.data.depth}</small><br/>${d.data.text.substring(0, 100)}...`
                }
            `)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function() {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("click", function(event, d) {
            updateCommentChain(d);
        });

    // Add circles to nodes
    nodeEnter.append("circle")
        .attr("r", 8)
        .style("fill", d => d.depth === 0 ? "#2378ae" : "#ff7f0e")
        .style("stroke", "#fff")
        .style("stroke-width", 2);

    // Add text for new nodes
    nodeEnter.append("text")
        .attr("dy", ".35em")
        .attr("x", d => d.children ? -13 : 13)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .style("fill", "#333")
        .style("font-size", "12px");

    // Update BOTH new and existing text elements
    nodes.select("text")  // Update existing
        .merge(nodeEnter.select("text"))  // Merge with new
        .text(d => {
            if (d.depth === 0 || !d.children) {
                return d.data.author;
            }
            return "";
        });
    
    // Add this new attribute to control text visibility
    nodes.select("text")
        .attr("visibility", showNames ? "visible" : "hidden");

    // Update existing nodes position
    nodes.merge(nodeEnter)
        .transition()
        .duration(750)
        .attr("transform", d => isHorizontal 
            ? `translate(${d.y},${d.x})`
            : `translate(${d.x},${d.y})`);
}

// Add this transformation function
function transformData(post) {
    // Create root node from post
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
}

// Replace the existing data loading section
d3.json("posts_data_20241217_000658.json").then(postsData => {
    posts = postsData;
    
    // Create post selector
    d3.select(".header")
        .append("select")
        .attr("id", "post-selector")
        .style("margin-left", "20px")
        .style("padding", "5px")
        .style("font-size", "16px")
        .on("change", function() {
            const selectedPost = posts.find(p => p.post_id === this.value);
            visualizePost(selectedPost);
        });
    
    // Populate selector
    d3.select("#post-selector")
        .selectAll("option")
        .data(posts)
        .enter()
        .append("option")
        .attr("value", d => d.post_id)
        .text(d => d.title || `Post ${d.post_id}`);
    
    // Visualize first post
    if (posts.length > 0) {
        visualizePost(posts[0]);
    }
}).catch(error => {
    console.error("Error loading posts:", error);
});

// Add this new function
function visualizePost(post) {
    currentPost = post;
    const transformedData = transformData(post);
    
    // Update root and tree
    root = d3.hierarchy(transformedData, d => d.replies);
    
    // Reset zoom
    svg.transition().duration(750).call(
        d3.zoom().transform,
        d3.zoomIdentity
    );
    
    // Update visualization
    updateLayout();
}


// Update comment chain function remains the same
function updateCommentChain(node) {
    const chain = [];
    let current = node;
    while (current) {
        chain.unshift(current.data);
        current = current.parent;
    }

    // Clear existing content
    d3.select(".comment-panel").html("");

    // Add title
    d3.select(".comment-panel").append("h3")
        .attr("class", "comment-panel-title")
        .text("Comment Thread");

    chain.forEach((comment, index) => {
        const commentDiv = d3.select(".comment-panel").append("div")
            .attr("class", "comment-item")
            .style("margin-left", (index * 20) + "px");

        commentDiv.append("div")
            .attr("class", "comment-author")
            .text(comment.author);

        commentDiv.append("div")
            .attr("class", "comment-text")
            .text(comment.text);

        if (index < chain.length - 1) {
            commentDiv.append("div")
                .attr("class", "comment-separator");
        }
    });
}

// Add this instead
d3.select("#toggle-button")
    .on("click", () => {
        isHorizontal = !isHorizontal;
        updateLayout();
    });

// Add this new button
let showNames = true;
d3.select("#tree-container")
    .append("button")
    .attr("id", "toggle-names-button")
    .style("position", "fixed")
    .style("bottom", "5vh")
    .style("right", "625px")
    .style("z-index", "1000")
    .style("padding", "12px 24px")
    .style("background-color", "#2378ae")
    .style("color", "white")
    .style("border", "none")
    .style("border-radius", "5px")
    .style("cursor", "pointer")
    .style("font-family", "Arial, sans-serif")
    .style("font-size", "16px")
    .style("box-shadow", "0 2px 4px rgba(0,0,0,0.2)")
    .style("transition", "background-color 0.3s ease, transform 0.2s ease")
    .text("Toggle Names")
    .on("click", () => {
        showNames = !showNames;
        updateLayout();
    });

// Add window resize handler
window.addEventListener('resize', () => {
    const newWidth = window.innerWidth - 40;
    const newHeight = window.innerHeight * 0.85;
    
    svg.attr("width", newWidth)
       .attr("height", newHeight);
    
    width = newWidth - margin.left - margin.right;
    height = newHeight - margin.top - margin.bottom;
    
    tree.size([height, width]);
    updateLayout();
});
