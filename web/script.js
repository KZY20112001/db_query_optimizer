const JOIN_METHODS = ["Hash Join", "Merge Join", "Nested Loop"]; 

const SCAN_METHODS = [
    "Seq Scan",
    "Index Scan",
    "Bitmap Heap Scan",
    "Index Only Scan",
    "Tid Scan",
    "Foreign Scan",
    "Custom Scan",
    "Materialized View Scan"
];




function updateInfoBox(content) {
    let infoBox = document.getElementById('info-box');
    infoBox.innerHTML = content;
}

function showAlternatives(type, list) {
    let alternatives = list.filter(item => item !== type);

    let ulHtml = '<h3>Alternative</h3> <ul>';

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
        case "Bitmap Heap Scan":
            return `
                <h2>Bitmap Heap Scan</h2>
                <p>Uses a bitmap to track matching rows from the index and then fetches the rows from the table. Efficient for complex queries with multiple conditions.</p>
            `;
        case "Index Only Scan":
            return `
                <h2>Index Only Scan</h2>
                <p>Reads the data directly from the index without accessing the table, which improves performance when all needed columns are in the index.</p>
            `;
        case "Tid Scan":
            return `
                <h2>Tid Scan</h2>
                <p>Accesses rows directly by their internal tuple ID (TID). Useful when rows are identified by their ctid value.</p>
            `;
        case "Foreign Scan":
            return `
                <h2>Foreign Scan</h2>
                <p>Used for scanning data from foreign tables or external data sources via a foreign data wrapper.</p>
            `;
        case "Materialized View Scan":
            return `
                <h2>Materialized View Scan</h2>
                <p>Scans data from a materialized view, which stores precomputed results to avoid recalculating them on every query.</p>
            `;
        case "Custom Scan":
            return `
                <h2>Custom Scan</h2>
                <p>A user-defined scan that can be used to implement custom behaviors or scan strategies, often used in extensions.</p>
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
        const default_text = "Click a node (operator) to get all the relevant info! Extra comments are provided for mismatching costs."
        updateInfoBox(`${default_text}`);
    }   
});