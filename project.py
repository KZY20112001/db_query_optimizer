import interface
import sv_ttk
from tkinter import ttk, Tk
from preprocessing import DBConnection
import os
import logging


logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Main tkinter window
root = Tk()
root.resizable(width=False, height=False)
root.title("QEP Explainer")


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


login_frame = ttk.Frame(root)
app_frame = ttk.Frame(root)


login_frame.grid(row=0, column=0, sticky="nsew")
app_frame.grid(row=0, column=0, sticky="nsew")

# create both frames
login = interface.Login(login_frame, app_frame)
app = interface.App(app_frame, login_frame)


interface.set_window_size(login_frame, interface.LOGIN_SIZE, True)
login_frame.tkraise()


sv_ttk.set_theme("dark")


root.mainloop()

# Function to get user input from GUI (interface.py)
def get_query_from_gui():
    query = app.query_input.get("1.0", "end-1c")  
    return query


def execute_query_and_get_qep(query: str):
    conn = DBConnection()
    connect_result = conn.connect_to_db()
    if connect_result != "":
        print(f"Error connecting to the database: {connect_result}")
        return None

    # Fetching original QEP for the query
    print("Fetching original QEP...")
    original_qep = conn.fetch_qep(query)
    if not original_qep:
        print("Error fetching QEP.")
        return None

    print("Original QEP fetched successfully.")
    log_output("Original QEP fetched successfully.")
    return original_qep


def generate_modified_sql_and_aqp(query: str, modified_qep):

    modified_query = query  
    print(f"Modified query: {modified_query}")
    log_output(f"Modified query: {modified_query}")
    

    conn = DBConnection()
    modified_aqp = conn.fetch_qep(modified_query)  
    return modified_query, modified_aqp


def compare_qep_and_aqp_costs(original_qep, modified_aqp):
    original_cost = original_qep[0]["Total Cost"]  
    modified_cost = modified_aqp[0]["Total Cost"]

    print(f"Original QEP cost: {original_cost}")
    print(f"Modified AQP cost: {modified_cost}")
    log_output(f"Original QEP cost: {original_cost}")
    log_output(f"Modified AQP cost: {modified_cost}")
    
    cost_difference = float(modified_cost) - float(original_cost)
    return cost_difference

# Function to display results in the GUI 
def display_results_in_gui(original_qep, modified_aqp, cost_difference):
    interface.VIZ.new_viz(original_qep)  
    interface.VIZ.new_viz(modified_aqp)  

  
    app.add_status(f"Cost difference: {cost_difference}")
    print(f"Cost difference: {cost_difference}")
    log_output(f"Cost difference: {cost_difference}")


def log_output(message: str):
    logging.info(message)


def main():
    
    query = get_query_from_gui()

   
    original_qep = execute_query_and_get_qep(query)
    if not original_qep:
        return

    
    modified_query, modified_aqp = generate_modified_sql_and_aqp(query, original_qep)
    if not modified_aqp:
        return

   
    cost_difference = compare_qep_and_aqp_costs(original_qep, modified_aqp)

    
    display_results_in_gui(original_qep, modified_aqp, cost_difference)

if __name__ == "__main__":
    main()
