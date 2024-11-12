
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
js = f"""                  function updateInfoBox(content) {{
                    var infoBox = document.getElementById('info-box');
                    infoBox.innerHTML = content.replace(/\\n/g, "<br>");
                  }}

                  network.on('click', function(properties) {{
                    if(properties.nodes.length > 0) {{
                        var nodeId = properties.nodes[0];
                        var clickedNode = nodes.get(nodeId);
                        updateInfoBox(clickedNode.explanation);
                    }} else {{
                        updateInfoBox("{default_text}");
                    }}
                  }});
"""

# stolen from https://github.com/pgadmin-org/pgadmin4/blob/master/web/pgadmin/static/js/Explain/ImageMapper.js
# this will help create a similar UI to that of pgAdmin
ImageMapper = {
    'Aggregate': {'image': 'ex_aggregate.svg', 'image_text': 'Aggregate'},
    'Append': {'image': 'ex_append.svg', 'image_text': 'Append'},
    'Bitmap Index Scan': lambda data: {'image': 'ex_bmp_index.svg', 'image_text': data['Index Name']},
    'Bitmap Heap Scan': lambda data: {'image': 'ex_bmp_heap.svg', 'image_text': data['Relation Name']},
    'BitmapAnd': {'image': 'ex_bmp_and.svg', 'image_text': 'Bitmap AND'},
    'BitmapOr': {'image': 'ex_bmp_or.svg', 'image_text': 'Bitmap OR'},
    'CTE Scan': {'image': 'ex_cte_scan.svg', 'image_text': 'CTE Scan'},
    'Function Scan': {'image': 'ex_result.svg', 'image_text': 'Function Scan'},
    'Foreign Scan': {'image': 'ex_foreign_scan.svg', 'image_text': 'Foreign Scan'},
    'Gather': {'image': 'ex_gather_motion.svg', 'image_text': 'Gather'},
    'Gather Merge': {'image': 'ex_gather_merge.svg', 'image_text': 'Gather Merge'},
    'Group': {'image': 'ex_group.svg', 'image_text': 'Group'},
    'GroupAggregate': {'image': 'ex_aggregate.svg', 'image_text': 'Group Aggregate'},
    'Hash': {'image': 'ex_hash.svg', 'image_text': 'Hash'},
    'Hash Join': lambda data: {
        'image': 'ex_join.svg' if not data['Join Type'] else
                 ('ex_hash_anti_join.svg' if data['Join Type'] == 'Anti' else
                  'ex_hash_semi_join.svg' if data['Join Type'] == 'Semi' else
                  'ex_hash.svg'),
        'image_text': 'Join' if not data['Join Type'] else
                      ('Hash Anti Join' if data['Join Type'] == 'Anti' else
                       'Hash Semi Join' if data['Join Type'] == 'Semi' else
                       'Hash ' + data['Join Type'] + ' Join'),
    },
    'HashAggregate': { 'image': 'ex_aggregate.svg','image_text': 'Hash Aggregate'},
    'Index Only Scan': lambda data: {'image': 'ex_index_only_scan.svg', 'image_text': data['Index Name']},
    'Index Scan': lambda data: {'image': 'ex_index_scan.svg', 'image_text': data['Index Name']},
    'Index Scan Backword': {'image': 'ex_index_scan.svg', 'image_text': 'Index Backward Scan'},
    'Limit': {'image': 'ex_limit.svg', 'image_text': 'Limit'},
    'LockRows': {'image': 'ex_lock_rows.svg', 'image_text': 'Lock Rows'},
    'Materialize': {'image': 'ex_materialize.svg', 'image_text': 'Materialize'},
    'Merge Append': {'image': 'ex_merge_append.svg', 'image_text': 'Merge Append'},
    'Merge Join': lambda data: {
        'image': 'ex_merge_anti_join.svg' if data['Join Type'] == 'Anti' else
                 'ex_merge_semi_join.svg' if data['Join Type'] == 'Semi' else
                 'ex_merge.svg',
        'image_text': 'Merge Anti Join' if data['Join Type'] == 'Anti' else
                      'Merge Semi Join' if data['Join Type'] == 'Semi' else
                      'Merge ' + data['Join Type'] + ' Join',
    },
    'ModifyTable': lambda data: {
        'image': 'ex_insert.svg' if data['Operation'] == 'Insert' else
                 'ex_update.svg' if data['Operation'] == 'Update' else
                 'ex_delete.svg' if data['Operation'] == 'Delete' else
                 'ex_merge.svg' if data['Operation'] == 'Merge' else None,
        'image_text': 'Insert' if data['Operation'] == 'Insert' else
                      'Update' if data['Operation'] == 'Update' else
                      'Delete' if data['Operation'] == 'Delete' else
                      'Merge' if data['Operation'] == 'Merge' else None,
    },
    'Named Tuplestore Scan': {'image': 'ex_named_tuplestore_scan.svg','image_text': 'Named Tuplestore Scan',},
    'Nested Loop': lambda data: {
        'image': 'ex_nested_loop_anti_join.svg' if data['Join Type'] == 'Anti' else
                 'ex_nested_loop_semi_join.svg' if data['Join Type'] == 'Semi' else
                 'ex_nested.svg',
        'image_text': 'Nested Loop Anti Join' if data['Join Type'] == 'Anti' else
                      'Nested Loop Semi Join' if data['Join Type'] == 'Semi' else
                      'Nested Loop ' + data['Join Type'] + ' Join',
    },
    'ProjectSet': {'image': 'ex_projectset.svg','image_text': 'ProjectSet'},
    'Recursive Union': {'image': 'ex_recursive_union.svg', 'image_text': 'Recursive Union'},
    'Result': {'image': 'ex_result.svg', 'image_text': 'Result'},
    'Sample Scan': {'image': 'ex_scan.svg', 'image_text': 'Sample Scan'},
    'Scan': {'image': 'ex_scan.svg', 'image_text': 'Scan'},
    'Seek': {'image': 'ex_seek.svg', 'image_text': 'Seek'},
    'SetOp': lambda data: {
    'image': 'ex_setop.svg' if data['Strategy'] != "Hashed" else ( 
             'ex_hash_setop_intersect_all.svg' if data['Command'] == 'Intersect All' else
             'ex_hash_setop_intersect.svg' if data['Command'].startswith('Intersect') else
             'ex_hash_setop_except_all.svg' if data['Command'] == 'Except All' else
             'ex_hash_setop_except.svg' if data['Command'].startswith('Except') else
             'ex_hash_setop_unknown.svg' if data['Strategy'] == 'Hashed' else None ),
    'image_text': 'SetOp' if data['Strategy'] != "Hashed" else ( 
                  'Hashed Intersect All' if data['Command'] == 'Intersect All' else
                  'Hashed Intersect' if data['Command'].startswith('Intersect') else
                  'Hashed Except All' if data['Command'] == 'Except All' else
                  'Hash Except' if data['Command'].startswith('Except') else
                  'Hashed SetOp Unknown' if data['Strategy'] == 'Hashed' else None ),
    },
    'Seq Scan': lambda data: {'image': 'ex_scan.svg', 'image_text': data['Relation Name']},
    'Subquery Scan': {'image': 'ex_subplan.svg', 'image_text': 'SubQuery Scan'},
    'Sort': {'image': 'ex_sort.svg', 'image_text': 'Sort'},
    'Tid Scan': {'image': 'ex_tid_scan.svg', 'image_text': 'Tid Scan'},
    'Table Function Scan': {'image': 'ex_table_func_scan.svg', 'image_text': 'Table Function Scan'},
    'Unique': {'image': 'ex_unique.svg', 'image_text': 'Unique'},
    'Values Scan': {'image': 'ex_values_scan.svg', 'image_text': 'Values Scan'},
    'WindowAgg': {'image': 'ex_window_aggregate.svg', 'image_text': 'Window Aggregate'},
    'WorkTable Scan': { 'image': 'ex_worktable_scan.svg', 'image_text': 'WorkTable Scan'},
}