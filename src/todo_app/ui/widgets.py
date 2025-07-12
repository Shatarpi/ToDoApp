import customtkinter as ctk
from todo_app.ui import themes

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR

DEFAULT_THEME = "default"


def confirmation_print():
    """Just to show that the button works"""
    print("This works - But you need to assign a command to it!")



# --- PRIMARY BUTTON ---
class PrimaryButton(ctk.CTkButton):
    """
    A custom primary button that inherits from CTkButton.
    It sets default styling for the application, which can be overridden.
    """
    def __init__(self, master, theme, **kwargs):
        
        defaults = {
            "height": 40,
            "width": 160,
            "font": ctk.CTkFont(size=14),
            "command": confirmation_print,
            "fg_color": theme["button_fg_color"],
            "hover_color": theme["button_hover_color"],
            "text_color": theme["button_text_color"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)



# --- TAB BUTTON ---

class TabsButton(ctk.CTkButton):
    """
    The buttons above the scrollable frame, acting as folder tabs
    """
    def __init__(self, master, theme, **kwargs):
        
        defaults = {
            "height": 40,
            "width": 120,
            "font": ctk.CTkFont(size=14),
            "command": confirmation_print,
            "fg_color": theme["button_tab_fg_color"],
            "hover_color": theme["button_tab_fg_color"],
            "text_color": theme["button_text_color"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)



# --- TABS/CATEOGRY BAR ---
class TabsCategories (ctk.CTkFrame):
    def __init__(self, master, theme, **kwargs):

        defaults = {
            "height": 60,
            "fg_color": "transparent"
        }

        defaults.update(kwargs)

        super().__init__(master=master,**defaults)


        # Add a test button to the navigation bar
        tester = TabsButton(
             master = self,
             text = "A test tab",
             theme = theme,
             corner_radius = 0
         )

        tester.grid(row=0, column=0, pady=(10, 0), padx=10)


# --- TABS BODY / LIST OF TO-DO's ---
class TabsBody(ctk.CTkScrollableFrame):
    """
    The main/big frame that holds all the to-do items
    """
    def __init__ (self, master, theme, **kwargs):

        defaults = {
            "height": 200,
            "width": 250,
            "fg_color": theme["scrollableFrame_fg_color"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)



# --- TABS/CATEOGRY BAR ---
class TabsFooter (ctk.CTkFrame):
    def __init__(self, master, theme, on_back_click, **kwargs):

        defaults = {
            "height": 60,
            "fg_color": "transparent"
        }

        defaults.update(kwargs)

        super().__init__(master=master,**defaults)

        # Configure the grid columns that the buttons are placed in
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Add a "back" button
            # Get settings for a default button
        default_theme = themes.get_theme("default")

            # Create the back button
        button_back = PrimaryButton(
             master = self,
             text = "Back",
             theme = default_theme,
             command = on_back_click # Use function input as arg in __init__
         )

        # Add it to the grid
        button_back.grid(row=0, column=0, pady=0, padx=0, sticky="w")


        # Add an "add" button
        button_add = PrimaryButton(
             master = self,
             text = "Add",
             theme = theme
             # ADD COMMAND HERE
         )

        # Add it to the grid
        button_add.grid(row=0, column=1, pady=0, padx=0)
        
    
        # Create the option menu that lets user select color theme
        option_menu = ctk.CTkOptionMenu(
            master=self,
            fg_color = theme["scrollableFrame_fg_color"],
            button_color = "black",
            values = ["option 1", "option2"],
        )

        option_menu.grid(row=0, column=2, pady=0, padx=0, sticky="e")