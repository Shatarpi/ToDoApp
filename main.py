"""Main file for the To-Do manager"""

import sys
import os
import customtkinter as ctk
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from todo_app.views.projects_view import ProjectsView
from todo_app.views.category_view import TabsView
from todo_app.core import storage
from todo_app.core.utils import resource_path




# --- MAIN APPLICATION CLASS ---
class App(ctk.CTk):
    """Main application class"""

    def __init__(self):
        super().__init__()

        loaded_data = storage.load_data()



        # --- DEFAULT WINDOW SETTINGS ---

        # Window title
        self.iconbitmap(resource_path("src/todo_app/assets/icon_main.ico"))
        self.title("My To-Do manager")
        
        # Define the starting size of the main application
        app_width = 750
        app_height = 750

        # Use normal Tkinter to get the monitor size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Get center of monitor
        pos_x = (screen_width // 2) - (app_width // 2)
        pos_y = (screen_height // 2) - (app_height // 2)

        # Create window at the center of the screen by entering "<width>x<height>+<x_pos>+<y_pos>"
        self.geometry(str(app_width)+"x"+str(app_height)+"+"+str(pos_x)+"+"+str(pos_y))


        # --- GRID SETTINGS ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # --- VIEWS ---
        # Create an empty dictionary to hold the views
        self.views = {}

        # --- Projects view ---
            # Create a variable that acts as the instance/object of the ProjectsView class. When variable is created/defined, so is an instance/object.
        self.projects_view = ProjectsView(
            master=self,
            loaded_data = loaded_data
            )

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
        self.set_view("projects", None)


        # --- Define what happens when program is closed (with X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)





    # --- FUNCTIONS / METHODS ---

    def save(self):

        # Get/store a list of all the projects
        all_projects = self.projects_view.all_projects

        # Initialize the list of dictionaries that will be saved out
        save_dicts = []

        # Go over all projects and create dictionaries of all of them.
        # Calling the projects "to_dict" method in turn calls the category's "to_dict" method and so on, resulting in a top level dictionary that contains several layers of dictionaries.
        for project in all_projects:
            project_dict = project.to_dict()

            save_dicts.append(project_dict)

        # Save the list of dictionaries to the file
        storage.save_data(save_dicts)



    # Function for toggling views/pages
    def set_view(self, view_name, project_data):
        # Check if the view (key) is in the views dictionary
        if view_name in self.views:

            # Store the actual view we want to switch to
            target_view = self.views[view_name]

            # If we are going to "Tabs View"
            if view_name == "tabs" and project_data is not None:
                # Go into tabs view and call the internal function/method to let it load the project data/information.
                target_view.load_project(project_data)

            # Regardless of which view we're going to, raise/show it.
            target_view.tkraise()

        # Else if view is not found, print error
        else:
            print(f"ERROR: View '{view_name}' not found")



    # When the program closes (with X)
    def on_closing(self):

        # Save the data
        self.save()
        
        # Actually destroy the window
        self.destroy()



# --- RUN THE APPLICATION ---

if __name__ == "__main__":
    # Create an instance of the App class
    app = App()

    # Loop it/show it (the application) until the user closes it
    app.mainloop()

    