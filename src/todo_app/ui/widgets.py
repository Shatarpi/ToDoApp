import customtkinter as ctk
from todo_app.ui import themes

DEFAULT_THEME = "default"


def confirmation_print():
    """Just to show that the button works"""
    print("This works - But you need to assign a command to it!")



# --- PROJECT BUTTON ---
class ProjectButton(ctk.CTkButton):
    """
    The button that gets created whenever a project is created. Stores various other information such as project name, which tabs/categories it got etc.
    """
    def __init__(self, master, theme, set_view, project_data, **kwargs):

        # Store the incoming function
        self.set_view = set_view

        # Store the incoming project data so each button stores it's unique data
        self.project_data = project_data
        
        defaults = {
            "height": 75,
            "width": 130,
            "border_width": 1,
            "corner_radius": 15,
            "text": self.project_data.project_name,
            "font": ctk.CTkFont(size=16, weight="bold"),
            "command": lambda: self.set_view("tabs", self.project_data),
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
        "fg_color": theme["main"],
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


        # Create the text that goes in the frame
        no_tabs_label = ctk.CTkLabel(
            master = self,
            text = "No categories exist yet",
            font = ("", 48, "bold"),
            text_color = "#404040"
            
        )


        # Place it in the new frame
        no_tabs_label.grid(row=1, column=1)





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
        


# --- TABS FOOTER ---
class TabsFooter (ctk.CTkFrame):
    def __init__(self, master, theme, on_back_click, on_add_click, theme_select, **kwargs):
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


        # Create the error text that appears when category doesn't have a name
        self.error_text = ctk.CTkLabel(
            master = self,
            text = "", # Text is added when an error arises
            font = ("", 16),
            text_color = "#be4d4d"
        )

        self.error_text.grid(row=0, column=2, pady=0, padx=0)

        # Add a "back" button
            # Get settings for a default button
        default_theme = themes.get_theme("Default")

        self.button_back = SquareButton(
            master = self,
            text = "<",
            command = on_back_click,
            theme = default_theme,
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
            text = "+",
            command = on_add_click,
            theme = theme,
        )

        # Add it to the grid
        self.button_add.grid(row=1, column=4, pady=0, padx=0)
        




# --- FUNCTIONS ---

    # Footer functions/methods

        # Hide parts of UI when no tabs exist
    def show_ui(self, show):
        if show == True:
            self.theme_selector_frame.grid()
        else:
            self.theme_selector_frame.grid_remove()



        # Method/function for updating the theme
    def update_theme(self, new_theme):
        self.button_add.update_theme(new_theme)
        self.option_menu.configure(
            fg_color = new_theme["main"],
            button_color = new_theme["accent"],
            button_hover_color = new_theme["hover"],
            dropdown_fg_color = new_theme["main"]
        )
