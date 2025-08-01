"""The projects view module that lists the available projects"""

import tkinter as tk
import customtkinter as ctk
from todo_app.ui import widgets as ui
from todo_app.ui import themes
from todo_app.core import data as data

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR


# --- MAIN UI/LANDING "PAGE" CLASS ---
class ProjectsView(ctk.CTkFrame):
    """Main class"""

    def __init__(self, master, **kwargs):
    # Self: When this/a ProjectClass 'object' is created/instanced, it will
    # automatically call the __init__ method and pass itself as the first and 
    # argument/self.
    # This only happens when for functions inside a class, not for functions
    # outside a class.  

        # Get the settings for the default theme
        self.default_theme = themes.get_theme("Default")

        # Create an empty list that will store all the project OBJECTS
        self.all_projects = []

        # Set start variables for placing projects in order
        self.current_projects_row = 0
        self.current_projects_column = 0

        # Start value for checking if projects exist
        self.projects_exists = False

        defaults = {
            "fg_color": MAIN_FRAME_COLOR
        }

        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        # (Analogy: order the car chassi with the new specifications)
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
            command = self.open_add_project,
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
        


        # --- REMOVE PROJECTS BUTTON ---
            # Create the "remove project" button
        self.button_remove_project = ui.SquareButton(
            master = self.add_remove_frame,
            text = "-",
            # ADD COMMAND HERE
            theme = self.default_theme,
            border_color = "#6E2B2B",
        )

        self.button_remove_project.grid(row=0, column=1, padx=25, pady=20)
        


        # --- SHOW/HIDE THE CORRECT UI ELEMENTS AT LAUNCH ---

        if self.projects_exists == False:
            # Hide the grid of projects
            self.projects_grid.grid_remove()
            # Show the "No projects" frame/text
            self.no_projects_frame.grid()
            # Hide the "Remove projects button"
            self.button_remove_project.grid_remove()
        
        else:
            # Show the grid of projects
            self.projects_grid.grid()
            # Hide the "No projects" frame/text
            self.no_projects_frame.grid_remove()
            # Show the "Remove projects button"
            self.button_remove_project.grid()


# --- FUNCTIONS/METHODS ---

    # Change the view/page
        # Function that just calls the function in main.py
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data )



    # "ADD PROJECT" POPUP/DIALOG BOX

    # Open the "Add project" popup/dialog window
    def open_add_project(self):

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
        elif input_text == "" or None:
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

                # Create the project button
            project_button = ui.ProjectButton(
                master = self.projects_grid.projects_grid,
                theme = self.default_theme,
                set_view = lambda *args: self.set_view("tabs", project),
                project_data = project # Send the data about the project to this button
            )

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
            

            # Set projects exists to true and show the window
            self.projects_exists = True

            # Show the grid of projects
            self.projects_grid.grid()
            # Hide the "No projects" frame/text
            self.no_projects_frame.grid_remove()
            # Show the "Remove projects button"
            self.button_remove_project.grid()











