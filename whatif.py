import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",  
        database="tpch",   
        user="admin",
        password="admin",  
        port=5432          
    )
    return conn

def fetch_qep(query):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}")
    qep = cur.fetchall()
    cur.close()
    conn.close()
    return qep


# this function modifies the query execution plan based on the modifiers provided
def modify_qep(query, modifiers):
    print("These are the modifiers:")
    for modifier in modifiers:
        print(modifier)
    conn = connect_to_db()
    cur = conn.cursor()
    # Apply each modifier (e.g., set enable_hashjoin, enable_mergejoin)
    for modifier in modifiers:
        cur.execute(f"SET {modifier};")
    # Run the EXPLAIN with the modified settings
    cur.execute(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}")
    qep = cur.fetchall()
    # Reset the executed modifiers
    cur.execute("RESET ALL;")
    cur.close()
    conn.close()
    return qep


# Example usage:
query = "SELECT * FROM orders WHERE o_orderkey = 1;"
qep = fetch_qep(query)
modifiers = ["enable_hashjoin = off", "enable_mergejoin = on"]
aqep = modify_qep(query, modifiers)
print("Query Execution Plan:")
print(qep)
print("Modified Query Execution Plan:")
print(aqep)

''' 
What the stats represent: 
Node Type: The type of operation being performed at this step in the execution plan.
Parallel Aware: Indicates whether the operation is aware of parallel execution.
Async Capable: Indicates whether the operation can be performed asynchronously.
Scan Direction: Indicates the direction of the scan on the index
Index Name: The name of the index being used for the scan
Relation Name: The name of the table being scanned
Alias: The alias for the table used in the query 
Startup Cost: The estimated cost (in arbitrary units) to start returning the first row.
Total Cost: The estimated total cost to process the entire query. 
Plan Rows: The estimated number of rows PostgreSQL expects this step to return. 
Plan Width: The estimated average size (in bytes) of a row returned by this operation. 
Actual Startup Time: The actual time (in milliseconds) PostgreSQL took to start returning the first row of this step.
Actual Total Time: The actual total time taken by this step to complete execution. 
Actual Rows: The actual number of rows returned by this step. 
Actual Loops: The number of times this step was executed (important in case of nested loops). 
Index Cond: The condition used by the index to filter rows. 
Rows Removed by Index Recheck: The number of rows that were removed during a recheck of the index. This occurs when PostgreSQL needs to confirm that the indexed condition matches the query condition.
Planning Time: The time PostgreSQL spent planning the execution of the query (in milliseconds).
Triggers: If any triggers (procedural code that gets executed automatically) were executed during the query, this section would list them.
Execution Time: The total time taken to execute the entire query, including all steps.
'''