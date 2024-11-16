//iteractive graph code
const JOIN_METHODS = ["Hash Join", "Merge Join", "Nested Loop"]; 

const SCAN_METHODS = [
    "Seq Scan",
    "Index Scan",
    "Bitmap Heap Scan",
    "Bitmap Index Scan", 
    "Index Only Scan",
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
        
        case "Bitmap Index Scan":
            return `
                <h2>Bitmap Index Scan</h2>
                <p>Creates a bitmap (a compressed list of row locations) based on an index to identify matching rows for a specific condition. 
                This operation is efficient for finding rows that match one or more conditions, especially when many rows meet the criteria.
                It doesn’t retrieve the rows directly but rather marks their locations.</p>
                <p>Useful for large datasets or queries with multiple conditions, as it reduces the need for random I/O.</p>
            `;
        
        case "Bitmap Heap Scan":
            return `
                <h2>Bitmap Heap Scan</h2>
                <p>Uses the bitmap created by the Bitmap Index Scan to efficiently retrieve only the relevant rows from the table.
                By accessing marked blocks of rows, this scan minimizes unnecessary I/O, making it faster to load large numbers of matched rows.</p>
                <p>Often used together with Bitmap Index Scan for large datasets to optimize disk access and performance.</p>
            `;

        case "Index Only Scan":
            return `
                <h2>Index Only Scan</h2>
                <p>Retrieves data directly from the index without accessing the main table, provided the index contains all required columns. Ideal for queries where data is fully visible in the index.</p>
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