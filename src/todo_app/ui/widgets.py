# A portion of this code was written with the help of an AI tool to help with debugging and explaining/teaching new concepts while the logic and structure were my own.

import customtkinter as ctk

DEFAULT_THEME = "default"


def confirmation_print():
    """Just to show that the button works"""
    print("This works - But you need to assign a command to it!")


# --- PROJECT BUTTON ---
class ProjectButton(ctk.CTkButton):
    """
    The button that gets created whenever a project is created. Stores various other information such as project name, which tabs/categories it got etc.
    """
    def __init__(self, master, theme, command, project_data, **kwargs):

        # Store the incoming project data so each button stores it's unique data
        self.project_data = project_data
        
        defaults = {
            "height": 75,
            "width": 130,
            "border_width": 1,
            "corner_radius": 15,
            "text": self.project_data.project_name,
            "font": ctk.CTkFont(size=16, weight="bold"),
            "command": command,
            "fg_color": theme["accent"],
            "hover_color": theme["hover"],
            "text_color": theme["text"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)

    # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.configure(
            fg_color = new_theme["accent"],
            hover_color = new_theme["hover"],
            text_color = new_theme["text"]
            )
        



# --- SQUARE BUTTON ----
class SquareButton(ctk.CTkButton):
    def __init__(self, master, theme, **kwargs):
        """
        Square button, used for add/remove/back etc. Usually with just a "+" or "<"
        """
        defaults = {
            "height": 60,
            "width": 60,
            "text": "#",
            "font": ctk.CTkFont(size=24, weight="bold"),
            "corner_radius": 15,
            "border_width": 2,
            "border_color": "#707070",
            "command": confirmation_print,
            "fg_color": theme["accent"],
            "hover_color": theme["hover"],
            "text_color": theme["text"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)

    def update_theme(self, new_theme):
        self.configure(
            fg_color = new_theme["accent"],
            hover_color = new_theme["hover"],
            text_color = new_theme["text"]
            )



# --- CONFIRMATION POPUP ---

class ConfirmationPopup(ctk.CTkToplevel):
    def __init__(self, master, thing_to_delete, on_yes_click):
        """
        The popup window used for confirmation when e.g., deleting a category, item etc.
        """

        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master)

        self.title("Confirmation")
        self.geometry("350x150")

            # Position the dialog box
            # Makes sure the dialogs contents are fully arranged and ready before doing anything else.
        self.update_idletasks()

            # Get cursor position
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

            # Offset popup window from cursor
            # Manually figured out the size of the popup and hardcoded in offsets
        pos_x = pointer_x - 175 # Remove half of width from pos x
        pos_y = pointer_y - 100 # Remove half of height from pos y
    

            # Set the dialog position
        self.geometry(f"+{pos_x}+{pos_y}")

        # After 200 milliseconds, apply the icon to the window
        # (Ctk applies its own after ~150ms so we have to wait until after that)
        self.after(200, lambda: self.iconbitmap("D:/Projects/Programming/ToDoApp/src/todo_app/assets/icon_main.ico"))


        # After 250 milliseconds, set focus to the popup window
        self.after(250, lambda: self.focus())


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)



        label = ctk.CTkLabel(
            master = self,
            text = f"Delete this {thing_to_delete}?"
        )

        label.grid(column=0, row=0)


        button = ctk.CTkButton(
            master = self,
            text = "Yes",
            fg_color = "#404040",
            hover_color = "#606060",
            command = lambda: (on_yes_click(), self.destroy())
        )

        button.grid(column = 0, row = 1)



# --- TABS VIEW HEADER ---

class TabsHeader (ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """
        This will just display the current project you are in
        """

        defaults = {
            "fg_color": "transparent"
        }
    
        defaults.update(kwargs)

        super().__init__(master=master, **defaults)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(
            master = self,
            text = "Testing",
            font = ("", 24, "bold"),
            text_color = "#707070"
            )
        
        self.header.grid(row=0, column=0, pady=(20, 0))


    # Sets the text/label to the projects name
    def set_text(self, project_data):
        self.header.configure(
            text = project_data.project_name,
        )



# --- NO PROJECTS FRAME / TEXT ---
    # If there are no projects, this text will show

class NoProjectsFrame(ctk.CTkFrame):
    """The frame and text that shows when no projects exists"""

    def __init__(self, master, **kwargs):
        # Create the frame that holds the text
        defaults = {
        "fg_color": "#252525",
        "border_width": 1,
        "border_color": "#505050"
        }


        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)

        super().__init__(master=master, **defaults)

        # Configure the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)


        # Create the big text
        no_projects_label = ctk.CTkLabel(
            master = self,
            text = "No projects exist yet",
            font = ("", 48),
            text_color = "#404040"
        )

        # Place it in the no_projects_frame
        no_projects_label.grid(row=0, column=0, padx=40, pady=40)



# --- LIST / GRID OF PROJECTS ---
    # If there are projects, this frame/grid will show
    
class ProjectsGrid(ctk.CTkFrame):
    """The frame/grid of projects/buttons"""

    def __init__(self, master, **kwargs):
        # Create the frame that holds the text
        defaults = {
        "fg_color": "#252525",
        "border_width": 1,
        "border_color": "#505050"
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)

        super().__init__(master=master, **defaults)

        # Configure the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # HEADER FRAME (with the "Projects:" text)
        self.projects_header = ctk.CTkFrame(
            master = self,
            fg_color = "transparent",
        )

            # Place it in the projects frame
        self.projects_header.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            # Fix it's configuration
        self.projects_header.grid_rowconfigure(0, weight=1)
        self.projects_header.grid_rowconfigure(1, weight=1)
        self.projects_header.grid_columnconfigure(0, weight=1)
    

            # Create a header at the top of the new frame
        projects_label = ctk.CTkLabel(
            master = self.projects_header,
            text = "Projects:",
            text_color = "#707070",
            font = ("", 18, "bold"),
        )

            # Place the it in the frame that will contain all the projects
        projects_label.grid(row=0, column=0, pady=(10, 0))



        # GRID FRAME (that holds the project buttons)
        self.projects_grid = ctk.CTkFrame(
            master = self,
            fg_color = "transparent",
        )

            # Place it in the projects frame
        self.projects_grid.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

            # Fix it's configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        


# --- NO TABS / CATEGORIES FRAME ---

class NoTabsFrame(ctk.CTkFrame):
    """The frame and text that shows when no tabs inside a project exists"""

    def __init__(self, master, theme, **kwargs):
        # Create the frame that holds the text
        defaults = {
        "fg_color": "#252525",
        "border_width": 1,
        "border_color": "#505050"
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)

        super().__init__(master=master, **defaults)

        # Configure the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)


        # Create the text that goes in the frame
        no_tabs_label = ctk.CTkLabel(
            master = self,
            text = "No categories exist yet",
            font = ("", 48, "bold"),
            text_color = "#404040"
            
        )

        # Place it in the new frame
        no_tabs_label.grid(row=1, column=1, sticky = "nsew")



# --- TAB BUTTON ---

class TabsButton(ctk.CTkButton):
    """
    The buttons above the scrollable frame, acting as folder tabs
    """
    def __init__(self, master, theme, **kwargs):
        
        defaults = {
            "height": 40,
            "width": 120,
            "corner_radius": 0,
            "font": ctk.CTkFont(size=14),
            # No need for a command as it already exists from creating the button in tabs_view.py
            "fg_color": theme["main"],
            "hover_color": theme["main"], # "main" to prevent hover effect
            "text_color": theme["text"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)


    # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.configure(
            fg_color = new_theme["main"],
            hover_color = new_theme["main"],
            text_color = new_theme["text"]
            )



# --- TABS/CATEOGRY BAR ---
class TabsCategories (ctk.CTkFrame):
    def __init__(self, master, theme, **kwargs):

        defaults = {
            "height": 60,
            "fg_color": "transparent"
        }

        defaults.update(kwargs)

        super().__init__(master=master,**defaults)

    # Method/function for updating the theme
    # Frame is always transparent, just call the buttons own update function. Button comes from "get active category" in tabs_view
    def update_theme(self, button, new_theme):
        button.update_theme(new_theme)



# --- TABS BODY / LIST OF TO-DO's ---
class TabsBody(ctk.CTkFrame):
    """
    The main/big frame that holds all the to-do items
    """
    def __init__ (self, master, theme, on_add_click, **kwargs):

        defaults = {
            "width": 250,
            "fg_color": "transparent"
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)

         # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.todo_frame = ctk.CTkScrollableFrame(
            master = self,
            #height = 200,
            width = 250,
            fg_color = theme["main"]
        )

        self.todo_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx = 0, pady = 0)

        

        self.button_add = SquareButton(
            master = self,
            width = 35,
            height = 60,
            text = "Add item",
            font = ("", 16, "bold"),
            command = on_add_click,
            theme = theme
        )

        self.button_add.grid(row=1, column=1, pady=(20,0))



# --- BODY FUNCTIONS ---

    # Method/function for updating the theme
    def update_theme(self, new_theme):

        # Update the scrollable frame color
        self.todo_frame.configure(
            fg_color = new_theme["main"]
            )
        
        # Update the add button colors
        self.button_add.configure(
            fg_color = new_theme["accent"],
            hover_color = new_theme["hover"],
        )


# --- TO DO ITEM ---
class ToDoItem(ctk.CTkCheckBox):
    """
    To-do item checkboxes
    """

    def __init__(self, master, text, theme, variable, command, **kwargs):

        defaults = {
            "text" : text,
            "fg_color" : theme["checkbox_done"],
            "hover_color" : theme["checkbox_hover"],
            "border_color" : theme["checkbox_border"],
            "font" : ctk.CTkFont(size=16),
            "variable" : variable,
            "command" : command
        }

        defaults.update(kwargs)

        super().__init__(master=master, **defaults)
        


# --- TABS FOOTER ---
class TabsFooter (ctk.CTkFrame):
    def __init__(self, master, theme, on_back_click, on_add_click, on_remove_click, theme_select, **kwargs):
        # on_back_click and theme_select_callback are arguments where functions are passed from tabs_view.py

        defaults = {
            "height": 60,
            "fg_color": "transparent"
        }

        defaults.update(kwargs)

        super().__init__(master=master,**defaults)


        # Configure the grid columns that the buttons are placed in
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)


        # Add a "back" button

        self.button_back = SquareButton(
            master = self,
            width = 40,
            height = 45,
            text = "<",
            command = on_back_click,
            theme = theme,
        )

            # Add it to the grid
        self.button_back.grid(row=1, column=0, pady=0, padx=0, sticky="w")


        # Create the theme selector label and button

            # Create the frame that holds the dropdown label and menu
        self.theme_selector_frame = ctk.CTkFrame(master=self, fg_color="transparent")

            # Put this frame in the center column
        self.theme_selector_frame.grid(row=1, column=2, pady=0, padx=0, sticky="e")

            # Create the dropdown/theme selector label
        theme_label = ctk.CTkLabel(
            master = self.theme_selector_frame, # Master is the new frame that's in the footers far right column 
            text = "Theme:",
            font = ("", 16)
        )

            # Put the label in the first internal column
        theme_label.grid(row=0, column=0, padx=(0, 10))


        # Create the dropdown menu

            # Store the function that was passed through the __init__ so we can access it later.
            # The "theme_select" (right) acts as a delivery man, delivering the function to the instance's own variable ("self.theme_select") then leaves. They don't need to be called the same.
        self.theme_select = theme_select
    
        # Create the option menu that lets user select color theme
        self.option_menu = ctk.CTkOptionMenu(
            master = self.theme_selector_frame, # Master is the new frame that's in the footers far right column
            fg_color = theme["main"],
            button_color = theme["accent"],
            button_hover_color = theme["hover"],
            dropdown_fg_color = theme["main"],
            dropdown_hover_color = theme["hover"],
            height = 40,
            values = ["Default", "Red", "Green", "Blue", "Yellow", "Purple"],
            command = self.theme_select # use the function passed through the __init__ with the selected option (e.g., "red" or "blue") as arguments to that function.
        )

        # Put the label in the second internal column
        self.option_menu.grid(row=0, column=1, pady=0, padx=0)

        
        # Create the "add" button
        self.button_add = SquareButton(
            master = self,
            width = 40,
            height = 45,
            text = "+",
            border_color = "#416E2B",
            command = on_add_click,
            theme = theme,
        )

        # Add it to the grid
        self.button_add.grid(row=1, column=4, pady=0, padx=0)
        
        # Create the "remove" button
        self.button_remove = SquareButton(
            master = self,
            width = 40,
            height = 45,
            text = "-",
            border_color = "#6E2B2B",
            command = on_remove_click,
            theme = theme,
        )

        # DON'T add remove button to grid by default, only when category exists
        
        


# --- FOOTER FUNCTIONS ---

    # Hide parts of UI when no tabs exist
    def show_ui(self, show):
        if show == True:
            self.theme_selector_frame.grid()
            self.button_remove.grid(row=1, column=5, pady=0, padx=10)
        else:
            self.theme_selector_frame.grid_remove()
            self.button_remove.grid_remove()


    # Change the dropdown item (from e.g., "Red" to "Default")
    def set_dropdown(self, value):
        if hasattr(self, 'option_menu'):
            self.option_menu.set(value)
        else:
            print("Warning: theme_selector_dropdown not found in TabsFooter.") 



        # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.option_menu.configure(
            fg_color = new_theme["main"],
            button_color = new_theme["accent"],
            button_hover_color = new_theme["hover"],
            dropdown_fg_color = new_theme["main"],
            dropdown_hover_color = new_theme["hover"]
        )
