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

        # Define which theme we want
        theme_settings = themes.get_theme("red")

        # Set defaults for the main frame
        defaults = {
            "fg_color": MAIN_FRAME_COLOR
        }
        
        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        # (Analogy: order the car chassi with the new specifications)
        super().__init__(master, **defaults)

        # Configure the internal grid in this view/frame 
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(0, weight=1)



        # --- TOP ROW OF BUTTONS/TABS ---

        # Create the category bar
        tabs_frame = ui.TabsCategories(
            master=self,
            theme=theme_settings # Use returned dictionary as argument
        )

        # Place it in 'TabsView's grid
        tabs_frame.grid(row=0, column=0, padx=20, pady=(40, 0), sticky="nsew")



        # --- BODY / TO DO LIST ---

        # Create the "body"/scrollable frame that holds the to-do items
        body = ui.TabsBody(
            master=self,
            theme = theme_settings # Use returned dictionary as argument
        )
        # Place it in 'TabsView's grid
        body.grid(row=1, column=0, padx=20, sticky="nsew")





       # Create footer that contains the back, add etc. buttons
        body = ui.TabsFooter (
            master=self,
            theme = theme_settings, # Use returned dictionary as argument
            on_back_click = lambda: self.set_view("projects"),
        )
        # Place it in 'TabsView's grid
        body.grid(row=2, column=0, padx=20, pady=40, sticky="nsew")




    def set_view(self, to_view):
        self.master.show_view(to_view)
