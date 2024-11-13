
# text shown in the top right to guide the user
default_text = "Click a node (operator) to get all the relevant info! Extra comments are provided for mismatching costs."

# css for the info box
css = """            #info-box {
                position: absolute;
                top: 20px;
                right: 20px;
                background-color: white;
                border: 1px solid black;
                padding: 10px;
            }
"""

# html to add our info box
div = f'            <div id="info-box">{default_text}</div>'

# js to handle click events for updating the info box
js = f"""                  
                function updateInfoBox(content) {{
                    var infoBox = document.getElementById('info-box');
                    infoBox.innerHTML = content;
                  }}
 
                network.on('click', function(properties) {{
                    console.log("HERE"); 
                    if(properties.nodes.length > 0) {{
                        var nodeId = properties.nodes[0];
                        var clickedNode = nodes.get(nodeId);
                        console.log("Node here:");
                        console.log(clickedNode);
                        updateInfoBox(clickedNode.type);
                    }} else {{
                        updateInfoBox("{default_text}");
                    }}
                  }});
"""

