//iteractive graph code
const JOIN_METHODS = ["Hash Join", "Merge Join", "Nested Loop", "Partitionwise Join", "Parallel Hash Join"]; 

const SCAN_METHODS = [
    "Seq Scan",
    "Index Scan",
    "Bitmap Scan",
    "Index Only Scan",
    "TID Scan",
];




function updateInfoBox(content) {
    let infoBox = document.getElementById('info-box');
    infoBox.innerHTML = content;
}

function showAlternatives(type, list) {
    let alternatives = list.filter(item => item !== type);

    let ulHtml = '<h3>Alternative Plans</h3> <ul>';

    alternatives.forEach(item => {
        ulHtml += `<li>${item}</li>`; 
    });

    ulHtml += '</ul>'; 
    return ulHtml;
}

function getJoinDetails(type){
    switch (type) {
        case "Hash Join":
           return `
                <h2>Hash Join</h2>
                <p>Efficient for large datasets, using hashing to reduce comparisons.</p>
            `;
        case "Merge Join":
            return `
                <h2>Merge Join</h2>
                <p>Best for sorted datasets, requiring both inputs to be ordered.</p>
            `;
        case "Nested Loop":
            return `
                <h2>Nested Loop</h2>
                <p>Suitable for smaller datasets or when an index is used on the inner table.</p>
            `;
        case "Partitionwise Join":
            return `
                <h2>Partitionwise Join</h2>
                <p>Optimizes joins on partitioned tables by processing each partition individually. Effective when both tables are partitioned in a compatible way.</p>
            `;
        case "Parallel Hash Join":
            return `
                <h2>Parallel Hash Join</h2>
                <p>Uses multiple CPU cores to speed up hash join operations, especially beneficial for large tables. Requires adequate parallel configuration.</p>
            `;
        
        default:
            return "<p>Unknown Join Type.</p>";
    }
}


function getScanDetails(type) {
    switch (type) {
        case "Seq Scan":
            return `
                <h2>Seq Scan (Sequential Scan)</h2>
                <p>Reads the entire table row by row. Best used when no indexes exist or when scanning a large portion of the table.</p>
            `;
        case "Index Scan":
            return `
                <h2>Index Scan</h2>
                <p>Uses an index to find matching rows quickly. Efficient when querying a small subset of the table with an appropriate index.</p>
            `;
        case "Bitmap Scan":
            return `
                <h2>Bitmap Scan</h2>
                <p>Combines an index with a bitmap to mark relevant rows, then retrieves them in bulk. Useful when many rows need to be accessed, reducing random I/O.</p>
            `;
        case "Index Only Scan":
            return `
                <h2>Index Only Scan</h2>
                <p>Retrieves data directly from the index without accessing the main table, provided the index contains all required columns. Ideal for queries where data is fully visible in the index.</p>
            `;
        case "TID Scan":
            return `
                <h2>TID Scan (Tuple ID Scan)</h2>
                <p>Fetches rows based on their physical storage locations (tuple IDs). Used for precise row access when the row location is known, but less common in general querying.</p>
            `;
        default:
            return "<p>Unknown Scan Type.</p>";
    }
}
network.on('click', function(properties) {
    if(properties.nodes.length > 0) {
        let nodeId = properties.nodes[0];
        let clickedNode = nodes.get(nodeId);
        let type = clickedNode.type;

        if (JOIN_METHODS.includes(type)){
            
            let joinDetails = getJoinDetails(type);
            joinDetails += showAlternatives(type,JOIN_METHODS);
            
            updateInfoBox(joinDetails); 
        } else if (SCAN_METHODS.includes(type)){
           
            let joinDetails = getScanDetails(type);
            joinDetails+= showAlternatives(type, SCAN_METHODS); 
            updateInfoBox(joinDetails)
        }
        else updateInfoBox(type);
                
    } else {
        const default_text = "Click a node (operator) to get quick info!";
        updateInfoBox(`${default_text}`);
    }   
});