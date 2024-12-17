// Add this near the top with other variable declarations
let i = 0;  // Counter for generating unique IDs
let root; // Add this at the top with other variables

// Remove fixed margins and use relative sizing
const margin = {top: 5, right: 380, bottom: 5, left: 200};
const totalWidth = window.innerWidth - 40; // Account for container margin
const totalHeight = window.innerHeight * 0.9; // 90vh equivalent
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
    .size([height, width * 0.8])
    .separation((a, b) => (a.parent == b.parent ? 2 : 3));

// Tooltip
const tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// Move updateLayout outside and declare it before use
function updateLayout() {
    // Update tree dimensions based on orientation
    tree.size(isHorizontal ? [height, width * 0.6] : [width, height * 0.6]);
    let treeData = tree(root);

    // Recalculate bounds for new layout
    const nodes = treeData.descendants();
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    
    nodes.forEach(d => {
        if (d.x < x0) x0 = d.x;
        if (d.x > x1) x1 = d.x;
        if (d.y < y0) y0 = d.y;
        if (d.y > y1) y1 = d.y;
    });

    // Update viewBox for new layout
    svg.transition()
        .duration(750)
        .attr("viewBox", [
            isHorizontal ? (y0 - margin.left) : (x0 - margin.left),
            isHorizontal ? (x0 - margin.top) : (y0 - margin.top),
            isHorizontal ? ((y1 - y0) + margin.left + margin.right) : ((x1 - x0) + margin.left + margin.right),
            isHorizontal ? ((x1 - x0) + margin.top + margin.bottom) : ((y1 - y0) + margin.top + margin.bottom)
        ]);

    // Update links
    let links = g.selectAll(".link")
        .data(treeData.links());

    links.enter()
        .append("path")
        .attr("class", "link")
        .merge(links)
        .transition()
        .duration(750)
        .attr("d", isHorizontal 
            ? d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x)
            : d3.linkVertical()
                .x(d => d.x)
                .y(d => d.y))
        .style("stroke-width", d => Math.max(1, 3 - d.target.depth * 0.5));

    links.exit().remove();

    // Update nodes
    const nodeUpdate = g.selectAll(".node")
        .data(treeData.descendants());

    // Handle node positions
    nodeUpdate.enter()
        .append("g")
        .attr("class", "node")
        .merge(nodeUpdate)
        .transition()
        .duration(750)
        .attr("transform", d => isHorizontal 
            ? `translate(${d.y},${d.x})` 
            : `translate(${d.x},${d.y})`);

    // Update text labels
    g.selectAll(".node text")
        .transition()
        .duration(750)
        .attr("x", d => {
            if (isHorizontal) {
                return d.children ? -13 : 13;
            } else {
                return 0;
            }
        })
        .attr("y", d => {
            if (isHorizontal) {
                return 0;
            } else {
                return d.children ? -13 : 13;
            }
        })
        .attr("text-anchor", d => {
            if (isHorizontal) {
                return d.children ? "end" : "start";
            } else {
                return "middle";
            }
        })
        .style("opacity", d => d.parent === null || !d.children ? 1 : 0);

    nodeUpdate.exit().remove();
}

// Load and process data
d3.json("comments_t3_1hflkkb_20241216_211002.json").then(data => {
    root = d3.hierarchy(data[0], d => d.replies);
    let treeData = tree(root);

    // Dynamic centering after initial layout
    const initialNodes = treeData.descendants();
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    
    initialNodes.forEach(d => {
        if (d.x < x0) x0 = d.x;
        if (d.x > x1) x1 = d.x;
        if (d.y < y0) y0 = d.y;
        if (d.y > y1) y1 = d.y;
    });

    // Adjust viewBox to fit all nodes
    svg.attr("viewBox", [
        y0 - margin.left, 
        x0 - margin.top, 
        (y1 - y0) + margin.left + margin.right, 
        (x1 - x0) + margin.top + margin.bottom
    ]);

    render(treeData);

    function render(treeData) {
        // Links
        let links = g.selectAll(".link")
            .data(treeData.links());

        links.enter()
            .append("path")
            .attr("class", "link")
            .merge(links)
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x))
            .style("stroke-width", d => Math.max(1, 3 - d.target.depth * 0.5));

        links.exit().remove();

        // Nodes
        let nodeSelection = g.selectAll(".node")
            .data(treeData.descendants(), d => d.id || (d.id = ++i));

        const nodeEnter = nodeSelection.enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`);

        nodeEnter.append("circle")
            .attr("r", d => Math.max(4, 8 - d.depth * 1))
            .attr("fill", d => d.children ? "#fff" : "#69b3a2")
            .attr("stroke", "#2378ae")
            .attr("stroke-width", 2)
            .on("mouseover", function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("r", d => Math.max(6, 10 - d.depth * 1))
                    .attr("fill", "#ff8c00");

                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);

                tooltip.html(`
                    <strong>${d.data.author}</strong><br/>
                    <small>Depth: ${d.data.depth}</small>
                `)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");

                updateCommentChain(d);
            })
            .on("mouseout", function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("r", d => Math.max(4, 8 - d.depth * 1))
                    .attr("fill", d => d.children ? "#fff" : "#69b3a2");

                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });

        nodeEnter.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -13 : 13)
            .style("text-anchor", d => d.children ? "end" : "start")
            .style("font-size", d => Math.max(10, 14 - d.depth) + "px")
            .style("fill", "#2378ae")
            .style("opacity", d => d.parent === null || !d.children ? 1 : 0)
            .text(d => d.data.author);

        nodeSelection.exit().remove();
    }
});

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
