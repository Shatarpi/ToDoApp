"""The tabs view module that shows the tabs/categories and to-do items in each project"""

import customtkinter as ctk
from todo_app.ui import widgets as ui
from todo_app.ui import themes

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR

# --- MAIN CLASS ---
class TabsView(ctk.CTkFrame):
    """Main class"""

    # --- MAIN FRAME THAT HOLDS THE OTHER ELEMENTS ---

    # __init__ is called when an object/instance of this is created
    def __init__(self, master, **kwargs):

        # Set start value of the active/selected project
        self.active_project = None

        # Set start theme
        selected_theme = "Default"

        # Get the theme settings
        self.theme_settings = themes.get_theme(selected_theme)

        # Start value for checking if tabs exist
        self.tabs_exists = False

        # Set defaults for the main frame
        defaults = {
            "fg_color": MAIN_FRAME_COLOR
        }
        
        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        # (Analogy: order the car chassi with the new specifications)
        super().__init__(master, **defaults)

        # Configure the internal grid in this view/frame 
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 0)
        
        self.grid_columnconfigure(0, weight=1)



        # --- HEADER WITH PROJECT NAME ---
            # Create the frame (and text)
        self.header = ui.TabsHeader(
            master = self,
        )
            # Place it in the TabsView grid
        self.header.grid(row=0, column=0)



        # --- NO TABS FRAME (WHEN CATEGORIES DOESN'T EXIST) ---
            # Create widget / frame
        self.no_tabs_exist = ui.NoTabsFrame(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )

        # Place it in 'TabsView's grid
        self.no_tabs_exist.grid(row=1, column=0, padx=50, pady=80, sticky="nsew")



        # --- TOP ROW OF BUTTONS/TABS ---

        # Create the category bar
        self.tabs = ui.TabsCategories(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )

        # Place it in 'TabsView's grid
        self.tabs.grid(row=0, column=0, padx=20, pady=(40, 0), sticky="nsew")



        # --- BODY / TO-DO LIST ---

        # Create the "body"/scrollable frame that holds the to-do items
        self.body = ui.TabsBody(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )
        # Place it in 'TabsView's grid
        self.body.grid(row=1, column=0, padx=20, sticky="nsew")



        # --- FOOTER/BOTTOM ROW OF BUTTONS ---
        
        # Create footer that contains the back, add etc. buttons
        self.footer = ui.TabsFooter (
            master = self,
            theme = self.theme_settings, # Use returned dictionary as argument
            on_back_click = lambda: self.set_view("projects", None),
            theme_select = self.set_theme, # Send the "set_theme" function to the new instance
            on_add_click = self.open_add_category
        )
        # Place it in 'TabsView's grid
        self.footer.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")



        # --- SHOW/HIDE THE CORRECT UI ELEMENTS AT LAUNCH ---

        if self.tabs_exists == False:
            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide the body / frame that holds to-do items
            self.body.grid_remove()
            # Hide the theme selector dropdown (and label)
            self.footer.show_ui(False)

            # Show the "no tabs exist" frame/text
            self.no_tabs_exist.grid()
        
        else:
            # Show the grid of projects
            self.tabs.grid()
            # Show the "Remove projects button"
            self.body.grid()
            # Show the theme selector dropdown (and label)
            self.footer.show_ui(True)

            # Hide the "no tabs exist" frame/text
            self.no_tabs_exist.grid_remove()



    # --- FUNCTIONS/METHODS ---


    # Load project - changes UI elements based on which project whas selected
    def load_project(self, project_data):
        self.active_project = project_data # Store the project data
        self.header.set_text(project_data) # Tell the header widget to change it's text to display the correct project name


    # Set view (back button, goes back to projects_view)
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data)

    # Updates/changes the theme of a tab
    def set_theme(self, selected_theme_name):
        new_theme = themes.get_theme(selected_theme_name)

        self.tabs.update_theme(new_theme)
        self.body.update_theme(new_theme)
        self.footer.update_theme(new_theme)



    # "ADD PROJECT" POPUP/DIALOG BOX

    # Open the "Add project" popup/dialog window
    def open_add_category(self):
        dialog = ctk.CTkInputDialog(
            title = "Add new category",
            text = "Category name:",
            fg_color = MAIN_FRAME_COLOR,
            button_fg_color = self.theme_settings["accent"],
            button_hover_color = self.theme_settings["hover"]
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



        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but project is missing name
        elif input_text == "" or None:
            self.footer.error_text.configure(text = "Category needs a name!")

        # Else create a new project button.
        else:
            # Set text to be nothing if a project was successfully created.
            self.footer.error_text.configure(text = "")
            print("New category created!")