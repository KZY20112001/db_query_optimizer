import psycopg2

# class responsible for handling connecting to db server and handling the queries
class DBConnection(): 
    def __init__(self) -> None: 
        self.connection = None
    
    def isConnected(self) -> bool: 
        return self.connection is not None and not self.connection.closed
    
    def connect_to_db(self, dbname:str = "tpch", user:str = "postgres", password:str = "admin", host:str ="localhost", port:str = "5432") -> str:
        self.disconnect_from_db()
        try: 
            conn = psycopg2.connect(
                database=dbname,   
                user=user,
                password=password,  
                host=host,  
                port=port          
            )
            self.connection = conn
            self.connection.autocommit = True
            return ""
        except Exception as e: 
            return "Error in connecting to the database: " + str(e)
        
    def disconnect_from_db(self) -> None:
        if self.isConnected(): 
            self.connection.close()


    def fetch_qep(self, query:str):
        if not self.isConnected():
            return 
        
        cur = self.connection.cursor()
        cur.execute(f"EXPLAIN (FORMAT JSON) {query}")
        qep = cur.fetchall()
        cur.close()

        return qep[0][0][0]["Plan"]

    def fetch_qep_node_only(self, query:str):
        if not self.isConnected():
            return 
        
        cur = self.connection.cursor()
        cur.execute(f"EXPLAIN (FORMAT JSON, costs false, timing false, verbose false, buffers false) {query}")
        qep = cur.fetchall()
        cur.close()

        return qep[0][0][0]["Plan"]

    # this function modifies the query execution plan based on the modifiers provided
    def modify_qep(self, query: str, modifiers: dict[str]):
        if not self.isConnected():
            return 
        cur = self.connection.cursor()
        # Apply each modifier (e.g., set enable_hashjoin, enable_mergejoin)
        for modifier, value in modifiers.items():
            if not value:
                cur.execute(f"SET {modifier} = off;")
                print(f"SET {modifier} = off")
        # Run the EXPLAIN with the modified settings
        cur.execute(f"EXPLAIN (FORMAT JSON) {query}")
        qep = cur.fetchall()
        # Reset the executed modifiers
        cur.execute("RESET ALL;")
        cur.close()
        return qep[0][0][0]["Plan"]
    
    def plan_outline(self, dict, lvl=0):
        indent = "    " * lvl
        print(f"{indent}- Node Type: {dict.get('Node Type')}")
        if 'Join Type' in dict:
            print(f"{indent}  Join Type: {dict.get('Join Type')}")
        if 'Relation Name' in dict:
            print(f"{indent}  Relation Name: {dict.get('Relation Name')}")
        if 'Alias' in dict:
            print(f"{indent}  Alias: {dict.get('Alias')}")
        if 'Index Name' in dict:
            print(f"{indent}  Index Name: {dict.get('Index Name')}")
        if 'Filter' in dict:
            print(f"{indent}  Filter: {dict.get('Filter')}")
        if 'Plans' in dict:
            for sub_node in dict.get('Plans'):
                self.plan_outline(sub_node, lvl + 1)
        else:
            return

