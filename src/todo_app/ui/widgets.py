import customtkinter as ctk
from todo_app.ui import themes

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


        # Add a test button to the navigation bar
        self.testButton = TabsButton(
            master = self,
            text = "A test tab",
            theme = theme,
            corner_radius = 0
         )

        self.testButton.grid(row=0, column=0, pady=(10, 0), padx=10)

    # Method/function for updating the theme
    # Since the frame is always transparent, just call the buttons own update function to to update that.
    def update_theme(self, new_theme):
        self.testButton.update_theme(new_theme)


# --- TABS BODY / LIST OF TO-DO's ---
class TabsBody(ctk.CTkScrollableFrame):
    """
    The main/big frame that holds all the to-do items
    """
    def __init__ (self, master, theme, **kwargs):

        defaults = {
            "height": 200,
            "width": 250,
            "fg_color": theme["main"]
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)

    # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.configure(
            fg_color = new_theme["main"],
            )
        


# --- FOOTER ---
class TabsFooter (ctk.CTkFrame):
    def __init__(self, master, theme, on_back_click, theme_select, **kwargs):
        # on_back_click and theme_select_callback are arguments where functions are passed from tabs_view.py

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
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)

        # Add a "back" button
            # Get settings for a default button
        default_theme = themes.get_theme("Default")

            # Create the back button
        self.button_back = PrimaryButton(
            master = self,
            width = 45,
            height = 45,
            text = "<",
            font = ("", 26),
            theme = default_theme,
            command = on_back_click # "on_back_click" is a function passed through inits argument
         )

        # Add it to the grid
        self.button_back.grid(row=0, column=0, pady=0, padx=0, sticky="w")



        # Create the theme selector label/button

        # Create the frame that holds the dropdown label and menu
        self.theme_selector_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        # Put this frame in the far right footer column
        self.theme_selector_frame.grid(row=0, column=2, pady=0, padx=0, sticky="e")

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




        # Add an "add" button
        self.button_add = PrimaryButton(
            master = self,
            width = 50,
            height = 40,
            text = "+",
            font = ("", 34, "bold"),
            theme = theme
            # ADD COMMAND HERE
         )

        # Add it to the grid
        self.button_add.grid(row=0, column=4, pady=0, padx=0)
        



# --- FUNCTIONS ---

    # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.button_add.update_theme(new_theme)
        self.option_menu.configure(
            fg_color = new_theme["main"],
            button_color = new_theme["accent"],
            button_hover_color = new_theme["hover"],
            dropdown_fg_color = new_theme["main"]
        )
