import platform
import os
import networkx as nx
import webbrowser
import whatif
from typing import List
from tkinter import ttk, Tk, Text, Toplevel, IntVar
from pyvis.network import Network

from preprocessing import DBConnection
from constants import ImageMapper
# responsible for visualing a QEP that has been explained

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Load raw JavaScript content from the external file for handling interactive graph
js = load_file("web/script.js")
css = load_file("web/info_box.css")
info_html = load_file("web/info_box.html")

class Visualizer():
    def new_viz(self, plan: dict, out_file: str = "QEP.html") -> None:
        # initialize graph
        graph = nx.DiGraph()

        self.node_id = 0
        self.imagemap = {}

        # populate graph
        self.add_nodes_and_edges(graph, plan, 0)

        # the multipartite layout has strict layers, which we can use to tell 
        # pyvis how to arrange the graph to resemble a tree-like structure/flow
        # this goes from left to right by default (higher 'subset' or layer values go the rightmost)
        # left to right instead of up to down to make better use of the aspect ratios of laptop/PC displays
        pos = nx.multipartite_layout(graph)

        # with physics off pyvis defaults to the given coordinates for each node
        net = Network('1080px', '1920px', directed=True)
        net.toggle_drag_nodes(False)
        net.toggle_physics(False)

        for node in list(graph.nodes(data="label")):
             # change highlight color for each node
            color = {
                "border": "#000000",
                "background": "#FFFFFF",
                "highlight": {
                    "border": "#000000",
                    "background": "#E6ECF5"
                }
            }
            type = node[1].split('\n')[0]
            # uses the saved info for each networkX node and passes it to pyvis.Network node
            # the multipartite layout is used here to arrange the nodes
            img = f"img/{self.imagemap[node[0]]}"
            net.add_node(node[0], label=node[1], type=type, x = pos[node[0]][0] * 1500, y = pos[node[0]][1] * 1500, shape="circularImage", image=img, borderWidth = 1.5, borderWidthSelected = 2, color=color, size=25)
        
        # add edges connecting the nodes
        for edge in graph.edges:
            net.add_edge(edge[0], edge[1], color="black", width = 2, chosen=False, arrowStrikethrough=False)

        # pyvis generates the html file with interactive elements for us
        output_file = out_file
        html_content = self.modify_html(net.generate_html().splitlines())
        with open(output_file, "w") as f:
            f.write(html_content)

        # force launch it
        absolute_path = os.path.join(os.getcwd(), output_file)
        webbrowser.open(f"file://{absolute_path}")
        
    
    # responsible for assigning values to each node and layering them
    def add_nodes_and_edges(self, graph: nx.DiGraph, plan: dict, subset: int, parent=None) -> None:
        self.node_id += 1

        # use image mapper to get the icon and text
        label = plan["Node Type"]
        img = "ex_unknown.svg"
        if label in ImageMapper:
            if callable(ImageMapper[label]):
                img = (ImageMapper[label](plan))["image"]
            else:
                img = ImageMapper[label]["image"]

        # extra info from the plan itself 
        label += f"\nStartup Cost: {plan['Startup Cost']}\nTotal Cost: {plan['Total Cost']}\n{plan['Plan Rows']} {'row' if plan['Plan Rows'] == 1 else 'rows'}"
        self.imagemap[self.node_id] = img

        graph.add_node(self.node_id, subset=subset, label=label)
        if parent:
            # plan is top down but graph should be bottom up. edge goes from child to parent node
            graph.add_edge(self.node_id, parent)
        if "Plans" in plan:
            # add children and reduce subset layer to position then below
            parent_id = self.node_id
            for child_plan in plan["Plans"]:
                self.add_nodes_and_edges(graph, child_plan, subset-1, parent_id)

    # function to add our custom css, html and js
    def modify_html(self, html: List[str]) -> str:
        iter = enumerate(html)
        index = 0
        line = ""

        # add css before the end of the <style> tag
        while "</style>" not in line:
            index, line = next(iter)
        
        html.insert(index, css)

        # add html after the main div
        while '<div id="mynetwork"' not in line:
            index, line = next(iter)
        
        html.insert(index+1, info_html)
        
        # add right js before we return to override any other behaviour 
        while 'return network;' not in line:
            index, line = next(iter)
        
        html.insert(index, js)

        return '\n'.join(html)

# responsible to changing window size when switching frames
def set_window_size(frame: ttk.Frame, size: tuple, refresh: bool = False) -> None:
    root:Tk = frame.master
    width, height = size
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    dark_title_bar(root, refresh)

# forces a dark title bar on Windows 10/11 to match the app's dark theme
# adapted from https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
# and https://stackoverflow.com/questions/77215242/i-am-trying-to-change-the-title-bar-color-of-my-tkinter-application-using-the-fo
def dark_title_bar(window: Tk, refresh: bool) -> None:
    if platform.system() == "Windows":
        from ctypes import windll, c_int, byref, sizeof
        window.update()
        set_window_attribute = windll.dwmapi.DwmSetWindowAttribute
        get_parent = windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        set_window_attribute(hwnd, 19, byref(c_int(2)), sizeof(c_int))

        if platform.release() == "10" and refresh:
            refresh = False
            window.withdraw()
            window.deiconify()
 
# window sizes and global variables
LOGIN_SIZE = (400, 375)
APP_SIZE = (600, 700)
VIZ = Visualizer()
db_connection = DBConnection()
# responsible for making the login frame
class Login:
    def __init__(self, root:ttk.Frame, app_frame:ttk.Frame) -> None:
        self.app_frame = app_frame
        
        # 2 equi-width columns
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.header_label=ttk.Label(root, justify="center", text="Connect to PostgreSQL")
        self.header_label.grid(row=0,column=0,padx=10,pady=10)

        # Database name input
        db_label=ttk.Label(root, justify="center", text="Name:")
        db_label.grid(row=1,column=0)

        self.db_input=ttk.Entry(root, justify="center")
        self.db_input.insert("end", "tpch")
        self.db_input.grid(row=1,column=1,pady=5,padx=10)

        # DB server username input
        user_label=ttk.Label(root, justify="center", text="User:")
        user_label.grid(row=2,column=0)

        self.user_input=ttk.Entry(root, justify="center")
        self.user_input.insert("end", "postgres")
        self.user_input.grid(row=2,column=1,pady=5,padx=10)

        # DB server password input
        pw_label=ttk.Label(root, justify="center", text="Password:")
        pw_label.grid(row=4,column=0)

        self.pw_input=ttk.Entry(root, justify="center", show="*")
        self.pw_input.grid(row=4,column=1,pady=5,padx=10)

        # DB server host input
        host_label=ttk.Label(root, justify="center", text="Host")
        host_label.grid(row=3,column=0)

        self.host_input=ttk.Entry(root, justify="center")
        self.host_input.insert("end", "localhost")
        self.host_input.grid(row=3,column=1,pady=5,padx=10)

        # DB server port input
        port_label=ttk.Label(root, justify="center", text="Port:")
        port_label.grid(row=5,column=0)

        self.port_input=ttk.Entry(root, justify="center")
        self.port_input.insert("end", "5432")
        self.port_input.grid(row=5,column=1,pady=5,padx=10)

        # connect button
        connect_btn=ttk.Button(root, text="Connect", command=self.connect_btn_command)
        connect_btn.grid(row=6,column=0,pady=10)
        
        # disabled to prevent editing
        self.error_label = Text(root, height=4, state="disabled")
        self.error_label.grid(row=7,column=0,columnspan=2,pady=5,sticky="nsew")

        self.root = root
    
    # enables the error label, changes the value and disables again to prevent editing
    def set_error(self, text:str) -> None:
        self.error_label["state"] = "normal"
        self.error_label.delete(1.0,"end")
        self.error_label.insert("end",text)
        self.error_label["state"] = "disabled"

    def connect_btn_command(self) -> None:
        # open connection
        connect_res = db_connection.connect_to_db(dbname=self.db_input.get(), user=self.user_input.get(), password=self.pw_input.get(), host=self.host_input.get(), port=self.port_input.get())

        # show result
        # an empty result means no error, move to the app frame
        if connect_res == "":
            self.set_error("Connected successfully") 
            set_window_size(self.app_frame, APP_SIZE)
            self.app_frame.tkraise()

        else:  
            self.set_error(connect_res) 


# responsible for creating the app frame            
class App():
    def __init__(self, root:ttk.Frame, login_frame:ttk.Frame) -> None:
        self.login_frame = login_frame
        
        # 3 equi-width columns
        root.grid_columnconfigure(0, weight=1, uniform="buttons")
        root.grid_columnconfigure(1, weight=1, uniform="buttons")
        root.grid_columnconfigure(2, weight=1, uniform="buttons")

        # the 2nd row (explain input) will expand/shrink to fit into the window
        root.grid_rowconfigure(1, weight=1)

        header_label = ttk.Label(root, justify="left", text="Enter one query at a time and click 'Generate' to generate a visualization. This will launch an interactable graph in your browser", wraplength=450)
        disconnect_btn = ttk.Button(root, text="Disconnect", command=self.disconnect_btn_command)

        # alignment for label and disconnect button
        header_label.grid(row=0, column=0, padx=10, pady=5, columnspan=3, sticky="w")
        disconnect_btn.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        # query_input assigned to the flexible row
        self.query_input = Text(root, height=25, highlightthickness=1, highlightbackground = "white", highlightcolor= "white")
        self.query_input.grid(row=1,column=0, columnspan=3 ,pady=5, sticky="nsew")

        # Generate QEP/AQP button
        generate_btn = ttk.Button(root, text="Generate", command=self.generate_btn_command)
        generate_btn.grid(row=2, column=1, pady=5, padx=10, sticky="nsew")

        # Set Join Button
        set_join_btn = ttk.Button(root, text="Select Join for AQP", command=self.select_join_btn_command)
        set_join_btn.grid(row=2, column=0)

        # Set Scan Button
        set_scan_btn = ttk.Button(root, text="Select Scan for AQP", command=self.select_Scan_btn_command)
        set_scan_btn.grid(row=2, column=2)

        # disabled to prevent editing
        self.status = Text(root, height=20, state="disabled")
        self.status.grid(row=3,column=0,columnspan=3, pady=5,sticky="nsew")
    
    # clears the status box
    def clear_status(self) -> None:
        self.status["state"] = "normal"
        self.status.delete(1.0,"end")
        self.status["state"] = "disabled"
    
    # appends to the status box. handles newlines automatically
    def add_status(self, status) -> None:
        self.status["state"] = "normal"
        self.status.insert("end", "\n" + status)
        self.status.yview_moveto(1.0)
        self.status["state"] = "disabled"

    # handle disconnect
    def disconnect_btn_command(self) -> None:
        # since tkinter Frames aren't created from scratch everytime, they need to be returned to the initial state
        self.clear_status()
        self.query_input.delete(1.0,"end")
        
        db_connection.disconnect_from_db()

        set_window_size(self.login_frame, LOGIN_SIZE)
        self.login_frame.tkraise()
    

        # clear any existing status info
        self.clear_status()
    
    def select_join_btn_command(self) -> None:
        join_window = Toplevel()
        join_window.title("Select Join Type")
        join_text = ["hash join", "merge join", "nested loop join"]
        selected_join = IntVar(value=join_text[0])


        # Add a label for instructions
        label = ttk.Label(join_window, text="Select the type of join:")
        label.pack(pady=10)
        # Create radio buttons for each join option
        for index, option in enumerate(join_text):
            radio_btn = ttk.Radiobutton(
                join_window,
                text=option,
                value=index,
                variable=selected_join
            )
            radio_btn.pack(anchor="w", padx=20)

        confirm_btn = ttk.Button(join_window, text="Confirm", command=lambda: confirm_selection(selected_join.get()))
        confirm_btn.pack(pady=10)
        
        def confirm_selection(selection):
            join_options = ["enable_hashjoin", "enable_mergejoin", "enable_nestloop"]
            selected_value = join_options[selection]
            self.add_status("Selected Join: " + selected_value)
            for key in join_options:
                if key != selected_value:
                    whatif.query_settings[key] = False
                else:
                    whatif.query_settings[key] = True
            join_window.destroy()
            return
    
    def select_Scan_btn_command(self) -> None:
        scan_window = Toplevel()
        scan_window.title("Select Scan Type")
        scan_text = ["bitmap scan", "index scan", "index only scan", "seq scan"]
        selected_scan = IntVar(value=scan_text[0])


        # Add a label for instructions
        label = ttk.Label(scan_window, text="Select the type of scan:")
        label.pack(pady=10)
        # Create radio buttons for each join option
        for index, option in enumerate(scan_text):
            radio_btn = ttk.Radiobutton(
                scan_window,
                text=option,
                value=index,
                variable=selected_scan
            )
            radio_btn.pack(anchor="w", padx=20)

        confirm_btn = ttk.Button(scan_window, text="Confirm", command=lambda: confirm_selection(selected_scan.get()))
        confirm_btn.pack(pady=10)

        def confirm_selection(selection):
            join_options = ["enable_bitmapscan", "enable_indexscan", "enable_indexonlyscan", "enable_seqscan"]
            selected_value = join_options[selection]
            self.add_status("Selected Scan: " + selected_value)
            for key in join_options:
                if key != selected_value:
                    whatif.query_settings[key] = False
                else:
                    whatif.query_settings[key] = True
            scan_window.destroy()
            return
        

    # generate graph
    def generate_btn_command(self) -> None:

        # we pass add_status to this function so it can use it internally to update the status as it goes on
        query_res = db_connection.fetch_qep(query=self.query_input.get("1.0",'end-1c'))
        aqp_res = db_connection.modify_qep(query=self.query_input.get("1.0",'end-1c'), modifiers=whatif.query_settings)

        qep_stats, aqp_stats, difference = whatif.compare_qp(query_res,aqp_res)        
        
        if aqp_stats is not None or difference is not None:
            self.add_status('\n')
            self.add_status(qep_stats)
            self.add_status(aqp_stats)
            self.add_status(difference)
            self.add_status('\n')
            VIZ.new_viz(plan=query_res, out_file="QEP.html")
            VIZ.new_viz(plan=aqp_res, out_file="AQP.html")
        else:
            self.add_status("No modification made")
            self.add_status(qep_stats)
            self.add_status('\n')
    
            VIZ.new_viz(plan=query_res, out_file="QEP.html")
        
        whatif.reset_settings(whatif.query_settings)
            