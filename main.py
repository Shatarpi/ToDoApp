"""Main file for the To-Do manager"""

import sys
import os
import customtkinter as ctk
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from todo_app.views.projects_view import ProjectsView
from todo_app.views.tabs_view import TabsView


# --- MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    """Main application class"""

    def __init__(self):
        super().__init__()

        # --- DEFAULT WINDOW SETTINGS ---
        # Window size
        self.geometry("750x450")
        # Window title
        self.iconbitmap("src/todo_app/assets/icon.ico")
        self.title("My To-Do manager")


        # --- GRID SETTINGS ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # --- VIEWS ---
        # Create an empty dictionary to hold the views
        self.views = {}

        # --- Projects view ---
        # Create a variable that acts as the instance/object of the ProjectsView class. When variable is created/defined, so is an instance/object.
        self.projects_view = ProjectsView(master=self) 

        # Place the new view instance/object on the grid to make it visible
        self.projects_view.grid(row=0, column=0, sticky="nsew")

        # Create a dictionary key/value (string to object/instance) item
        self.views["projects"] = self.projects_view

        # --- Tabs view ---
        # (same setup as "Projects view")
        self.tabs_view = TabsView(master=self) 
        self.tabs_view.grid(row=0, column=0, sticky="nsew")
        self.views["tabs"] = self.tabs_view




        # --- Initial view when launching the program ---
        self.show_view("projects")



    # Function for toggling views/pages
    def show_view(self, view_name):
        # Check if the view (key) is in the views dictionary
        if view_name in self.views:
            # If true, get the instance (value) matching the key and raise that.
            self.views[view_name].tkraise()
        else:
            print(f"ERROR: View '{view_name}' not found")

# --- RUN THE APPLICATION ---

if __name__ == "__main__":
    # Create an instance of the App class
    app = App()

    # Loop it/show it (the application) until the user closes it
    app.mainloop()

    