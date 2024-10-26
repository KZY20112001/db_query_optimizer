import psycopg

def connect(host='localhost', port='5432',dbname='Project2',user='postgres',password='root'):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
    except psycopg.OperationalError as e:
        print("Error: Could not connect to the PostgreSQL server.")
        print(e)
        return
    
    cur = conn.cursor()
    return cur

def close_connection(conn: psycopg.Connection, cur: psycopg.Cursor):
    conn.close()
    cur.close()
    return

def sql_query(cur, query, explain=False):
    if explain:
        sql_query = f"EXPLAIN (FORMAT JSON) {query}"
    try:
            cur.execute(sql_query)
            result = cur.fetchone()
    except Exception as e:
        print(f"Error: Could not execute the query.")
        print(e)
        result = None
    return result