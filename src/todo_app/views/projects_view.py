"""The projects view module that lists the available projects"""

import tkinter as tk
import customtkinter as ctk
from todo_app.ui import widgets as ui
from todo_app.ui import themes
from todo_app.core import data as data
from todo_app.core import storage

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR


# --- MAIN UI/LANDING "PAGE" CLASS ---
class ProjectsView(ctk.CTkFrame):
    """Main class"""

    def __init__(self, master, loaded_data, **kwargs):
    # Self: When this/a ProjectClass 'object' is created/instanced, it will
    # automatically call the __init__ method and pass itself as the first and 
    # argument/self.
    # This only happens when for functions inside a class, not for functions
    # outside a class.  

        # Get the settings for the default theme
        self.default_theme = themes.get_theme("Default")


        # Unpack the dictionary and create a 'project' object from it
            # Create new list variable (self.all_projects[])
            # Inside [] we create a project object (data.Project)
            # which will hold the data that gets unpacked (**data)..
            # .. for every data/item in the loaded_data list of dictionaries

            # Basically a for loop inside the [], ie do this for every item in loaded_data
        self.all_projects = [data.Project(**data) for data in loaded_data]


        # Create an empty list that will store all the project BUTTONS
        self.all_project_buttons = []


        # Set start variables for placing projects in order
        self.current_projects_row = 0
        self.current_projects_column = 0

        # Start value for checking if projects exist
            # If the list constains projects
        if self.all_projects:
            self.projects_exists = True
        else:
            self.projects_exists = False

        defaults = {
            "fg_color": MAIN_FRAME_COLOR
        }

        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        super().__init__(master, **defaults)

        # Fix main grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)



        # --- NO PROJECTS FRAME / TEXT ---
            # If there are no projects, this text will show

            # Create the frame that will hold the text
        self.no_projects_frame = ui.NoProjectsFrame(
            master = self,
        )
        
            # Place it in the main projects view grid
        self.no_projects_frame.grid(row=0, column=0)



        # --- LIST / GRID OF PROJECTS ---
            # If there are projects, this frame/grid will show

            # Create widget / frame
        self.projects_grid = ui.ProjectsGrid(
            master = self
        )

            # Place it in the main projects view grid
        self.projects_grid.grid(row=0, column=0)



        # --- 'ADD/REMOVE PROJECT' BUTTONS ---

            # Create the frame that holds the add/remove project buttons and error text
        self.add_remove_frame = ctk.CTkFrame(
            master = self,
            fg_color = "transparent"
        )

            # Add it/new frame to the projects view frame 
        self.add_remove_frame.grid(row=1, column=0, padx=20, pady=20)

            # Fix it's configuration
        self.add_remove_frame.grid_rowconfigure(0, weight=1)
        self.add_remove_frame.grid_columnconfigure(0, weight=1)
        self.add_remove_frame.grid_columnconfigure(1, weight=1)



            # Create the "add project" button
        self.button_add_project = ui.SquareButton(
            master = self.add_remove_frame,
            text = "+",
            command = self.add_project,
            theme = self.default_theme,
            border_color = "#416E2B",
        )

        self.button_add_project.grid(row=0, column=0, padx=25, pady=20)

        # Create the frame that holds the error/warning text
        self.error_text_frame = ctk.CTkFrame(
            master = self,
            border_width = 1,
            border_color = "#da3232"
        )

            # Create the error text that appears when project doesn't have a name
        self.error_text = ctk.CTkLabel(
            master = self.error_text_frame,
            text = "", # Text is added when an error arises
            font = ("", 16),
            text_color = "#da3232"
        )

        # Add the text to the error text frame
        self.error_text.grid(row=1, column=0, padx=20, pady = 10)
        


        # Remove projects button
            # Create the "remove project" button
        self.button_remove_project = ui.SquareButton(
            master = self.add_remove_frame,
            text = "-",
            command = self. remove_project,
            theme = self.default_theme,
            border_color = "#6E2B2B",
        )

        self.button_remove_project.grid(row=0, column=1, padx=25, pady=20)
        


        # Show/hide the correct UI elements at launch
        self.update_ui()


    # --- FUNCTIONS/METHODS ---

    # CHANGE THE VIEW/PAGE
        # Function that just calls the function in main.py
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data)



    # "ADD PROJECT" POPUP/DIALOG BOX
    def add_project(self):

        dialog = ctk.CTkInputDialog(
            title = "Add new project",
            text = "Project name:",
            fg_color = MAIN_FRAME_COLOR,
            button_fg_color = self.default_theme["accent"],
            button_hover_color = self.default_theme["hover"]
        )

        # Position the dialog box
            # Makes sure the dialogs contents are fully arranged and ready before doing anything else.
        dialog.update_idletasks()

            # Get cursor position
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

            # Offset popup window from cursor
            # Manually figured out the size of the popup and hardcoded in offsets
        pos_x = pointer_x - 175 # Remove half of width from pos x
        pos_y = pointer_y - 100 # Remove half of height from pos y
    

            # Set the dialog position
        dialog.geometry(f"+{pos_x}+{pos_y}")

        # After 200 milliseconds, apply the icon to the window
        # (Ctk applies its own after ~150ms so we have to wait until after that)
        dialog.after(200, lambda: dialog.iconbitmap("D:/Projects/Programming/ToDoApp/src/todo_app/assets/icon_main.ico"))


        # Hide the error text/frame.
        self.error_text_frame.grid_remove()


        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but project is missing name
        elif input_text == "" or input_text is None:
            self.error_text.configure(text = "Project needs a name!")

            # Show the error frame/text
            self.error_text_frame.grid(row=2, column=0, padx=20, pady=(0, 20))


        # Else create a new project button.
        else:

            # Check if a project with that name already exists
            for project in self.all_projects:
                if project.project_name == input_text:

                    # Change the error text
                    self.error_text.configure(text = "A project with that name already exists!")
                    
                    # Show the error frame/text
                    self.error_text_frame.grid(row=2, column=0, padx=20, pady=(0, 20))
                    
                    # Stop the entire project creation function.
                    return


                # Create a project data object
            project = data.Project(
                name = input_text
            )

                # Add the project to the list variable of projects
            self.all_projects.append(project)

            self.update_ui()


    # "REMOVE PROJECT" POPUP
    def remove_project(self):

        def remove_confirmation(selected_project):

            ui.ConfirmationPopup(
                master = main,
                thing_to_delete = f"project: '{selected_project.project_name}",
                on_yes_click = lambda: on_yes(selected_project)
            )


        def on_yes(project):

            # Remove the project from the list of projects
            self.all_projects.remove(project)

            self.update_ui()

            # Destroy the popup to close it
            main.destroy()


        # Create a top level/popup window
        main = ctk.CTkToplevel(
            master = self
        )

        main.title("My To-Do manager")

        # Configure its grid
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Create the main frame that goes in the window
        frame = ctk.CTkFrame(master = main, fg_color = "transparent")

        # Place the frame in the window
        frame.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)
        
        # Configure the new frames grid
        frame.grid_columnconfigure(0, weight=1)

        # Add a label to the top of the frame
        label = ctk.CTkLabel(master = frame, text = "Which project to delete?")

        label.grid(row = 0, column = 0, pady = 30, sticky = "ew")

        # Set the first row a button/project will be on
        row = 1

        # For every project, create a button
        for project in self.all_projects:
            
            button = ctk.CTkButton(
                master = frame,
                text = project.project_name,
                fg_color = self.default_theme["accent"],
                hover_color = "#be2c2c",
                border_width = 1,
                # NO COMMAND HERE
                )
            
            # Since the command references the button itself, we need to assign the command after the button has been fully created.
            button.configure(command=lambda p=project: remove_confirmation(p))

            # Place it in the frame
            button.grid(row=row, column = 0, pady = 10, padx = 50, sticky = "ew")

            # Increment up the row counter
            row +=1

        # Position the dialog box
            # Makes sure the dialogs contents are fully arranged and ready before doing anything else.
        main.update_idletasks()

            # Get cursor position
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

        # Offset popup window from cursor
            # Manually figured out the size of the popup and hardcoded in offsets
        pos_x = pointer_x - 175 # Remove half of width from pos x
        pos_y = pointer_y - 100 # Remove half of height from pos y
    

            # Set the dialog position
        main.geometry(f"+{pos_x}+{pos_y}")

        # After 200 milliseconds, apply the icon to the window
            # (Ctk applies its own after ~150ms so we have to wait until after that)
        main.after(200, lambda: main.iconbitmap("D:/Projects/Programming/ToDoApp/src/todo_app/assets/icon_main.ico"))


        # After 250 milliseconds, set focus to the popup window
        main.after(250, lambda: main.focus())



    # UDPATE / REFRESH THE UI
    def update_ui(self):

        # Delete every button
        for button in self.all_project_buttons[:]: # Using duplicate list here
            button.destroy()

        # If list of projects contains projects
        if self.all_projects:

            # Show the grid of projects
            self.projects_grid.grid()
            # Hide the "No projects" frame/text
            self.no_projects_frame.grid_remove()
            # Show the "Remove projects button"
            self.button_remove_project.grid()

            # Reset counters
            self.current_projects_row = 0
            self.current_projects_column = 0

            # Go through all of the projects
            for project in self.all_projects:

                # Create the project button
                project_button = ui.ProjectButton(
                    master = self.projects_grid.projects_grid,
                    theme = self.default_theme,
                    command = lambda p=project: self.set_view("tabs", p),
                    project_data = project # Send the data about the project to this button
                )

                # Add the button to the list of buttons
                self.all_project_buttons.append(project_button)

                # Add the button to the grid
                project_button.grid(
                    row = self.current_projects_row,
                    column = self.current_projects_column,
                    padx=20,
                    pady=(10, 10)
                    )
                
                
                # Increment up the counters
                    # If we are not currently on the last column, increment it
                if self.current_projects_column < 2:
                    self.current_projects_column += 1

                    # If we are on the last column, increase to row counter and reset column counter
                else:
                    self.current_projects_row += 1
                    self.current_projects_column = 0

        # If no projects exist
        else:
            # Hide the grid of projects
            self.projects_grid.grid_remove()
            # Show the "No projects" frame/text
            self.no_projects_frame.grid()
            # Hide the "Remove projects button"
            self.button_remove_project.grid_remove()

            
