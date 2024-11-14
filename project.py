import interface
import sv_ttk
from tkinter import ttk, Tk




def main():

    # Main tkinter window
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("What-If Analyzer")


    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    login_frame = ttk.Frame(root)
    app_frame = ttk.Frame(root)

    interface.Login(login_frame, app_frame)
    interface.App(app_frame, login_frame)
    interface.set_window_size(login_frame, interface.LOGIN_SIZE, True)
    login_frame.grid(row=0, column=0, sticky="nsew")
    app_frame.grid(row=0, column=0, sticky="nsew")


    login_frame.tkraise()


    sv_ttk.set_theme("dark")


    root.mainloop()

   
if __name__ == "__main__":
    main()
