const joins = ["Hash Join", "Merge Join", "Nested Loop"]; 

function updateInfoBox(content) {
    let infoBox = document.getElementById('info-box');
    infoBox.innerHTML = content;
}

network.on('click', function(properties) {
    if(properties.nodes.length > 0) {
        let nodeId = properties.nodes[0];
        let clickedNode = nodes.get(nodeId);
        let type = clickedNode.type;
        if (joins.includes(type)){
            console.log("JOIN: ", type);
            joinDetails = `
                <h3>Merge Join</h3>
                <p>Best for sorted datasets, requires both inputs to be ordered.</p>
                <ul>
                <li>Requires sorted inputs</li>
                <li>Efficient for ordered data</li>
                </ul>
                        <button onclick="alert('More on Merge Join')">Learn More</button>
            `;
            updateInfoBox(joinDetails)
        } else updateInfoBox(type);
                
    } else {
        const default_text = "Click a node (operator) to get all the relevant info! Extra comments are provided for mismatching costs."
        updateInfoBox(`${default_text}`);
    }   
});