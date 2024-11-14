
# text shown in the top right to guide the user
default_text = "Click a node (operator) to get all the relevant info! Extra comments are provided for mismatching costs."

# css for the info box
css = """           
            #info-box {
                position: absolute;
                top: 20px;
                right: 20px;
                background-color: white;
                border: 1px solid black;
                padding: 10px;
            }
"""

# html to add our info box
div = f'<div id="info-box">{default_text}</div>'

list = f'''
    <h2>Select Items</h2>

    <button>Show Selected Items</button>
'''
# js to handle click events for updating the info box
js = f"""       
                const joins = ["Hash Join", "Merge Join", "Nested Loop Join"]; 
                
                function updateInfoBox(content) {{
                    let infoBox = document.getElementById('info-box');
                    infoBox.innerHTML = content;
                  }}
 
                network.on('click', function(properties) {{
                    if(properties.nodes.length > 0) {{
                        let nodeId = properties.nodes[0];
                        let clickedNode = nodes.get(nodeId);
                        let type = clickedNode.type;
                        let lastWord = type.split(" ")[type.split(" ").length - 1]; 
                        if (lastWord === "Join"){{
                            console.log("JOIN: ", type);
                        }}
                        updateInfoBox(type)
                            
                    }} else {{
                        updateInfoBox("{default_text}");
                    }}
                  }});
"""

