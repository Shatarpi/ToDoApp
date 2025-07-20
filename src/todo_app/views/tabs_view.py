"""The tabs view module that shows the tabs/categories and to-do items in each project"""

import customtkinter as ctk
from todo_app.ui import widgets as ui
from todo_app.ui import themes
from todo_app.core import data as data

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR

# --- MAIN CLASS ---
class TabsView(ctk.CTkFrame):
    """Main class"""

    # --- MAIN FRAME THAT HOLDS THE OTHER ELEMENTS ---

    # __init__ is called when an object/instance of this is created
    def __init__(self, master, **kwargs):

        # Set start value of the active/selected project/category
        self.active_project = None
        self.active_category = None

        # Set start theme
        selected_theme = "Default"

        # Get the theme settings
        self.theme_settings = themes.get_theme(selected_theme)

        # Create empty dict that later holds info about categories that exist
        self.category_components = {}

        # Start value for checking if tabs exist
        self.categories_exists = False

        # Set start counter for the tab buttons
        self.current_tab_column = 0

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



        # --- HIDE UI ELEMENTS AT LAUNCH ---

        if self.categories_exists == False:
            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide the theme selector dropdown (and label)
            self.footer.show_ui(False)

            # Show the "no tabs exist" frame/text
            self.no_tabs_exist.grid()



    # --- FUNCTIONS/METHODS ---


    # Load project - changes UI elements based on which project whas selected
    def load_project(self, project_data):
        self.active_project = project_data # Store the project data
        self.header.set_text(project_data) # Tell the header widget to change it's text to display the correct project name


    # Set view (back button, goes back to projects_view)
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data)

        

    # Change category
    def change_category(self, to_category):

        # Update what is considered the active category
        self.active_category = to_category

        # Loop through the dictionary of category COMPONENTS (buttons/frames/bodies)
        for category_name, category_component in self.category_components.items():
            # if category name IS the same as the category we want to be active
            if category_name == to_category:
                # Add the body/frame/list of to-dos to the main grid
                category_component["body"].grid(row=1, column=0, padx=20, 
                                                sticky="nsew")
                
            # Otherwise hide the stored "body" from the UI.
            else:
                category_component["body"].grid_remove()

        # Loop through the list of of categories in the PROJECT object (which holds name, theme settings etc.)
        for category_object in self.active_project.categories:

            # # if category name IS the same as the category we want to be active 
            if category_object.name == to_category:
                
                # Get the theme settings from it
                settings = category_object.theme_settings

                # Update the footer with the new settings
                self.footer.update_theme(settings)

                # Once found and updated, exit the loop
                break



    # Updates/changes the theme of a tab
    def set_theme(self, selected_theme_name):
        

        # Check if we have an active category
        if self.active_category is not None:
            
            # Get the theme settings
            new_theme = themes.get_theme(selected_theme_name)

            # Find the active category OBJECT and update its theme_settings
            active_category_object = None

            # Loop through the categories store in the active project
            for category_object in self.active_project.categories:

                # If the name of the category matches the active categories name
                if category_object.name == self.active_category:

                    # Store the category OBJECT that matches
                    active_category_object = category_object
                    break
            
            # Store the new settings in the stored OBJECT
            if active_category_object:
                active_category_object.theme_settings = new_theme


            # Go into category_components (which holds all the dictionaries of stored widgets par category), get the dictionary that is our current category, then get the button associated with it's "tab" key.
            active_button_object = self.category_components[self.active_category]["tab"]
            
            active_body_object = self.category_components[self.active_category]["body"]

            # Feed the new tab/button object for the active category to the update theme method
            active_button_object.update_theme(new_theme)
            active_body_object.update_theme(new_theme)
            self.footer.update_theme(new_theme)

            # Update the category OBJECTs theme setting
            

        else:
            print("No active category - Can't change theme!")



    # "ADD CATEGORY" POPUP/DIALOG BOX

    # Open the "Add category" popup/dialog window
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

        # Else if dialog is closed with OK, but category is missing name
        elif input_text == "" or None:
            self.footer.error_text.configure(text = "Category needs a name!")


        # --- CREATE NEW CATEGORY ---
        else:
            # Set text to be nothing if a project was successfully created.
            self.footer.error_text.configure(text = "")

            # Reset theme settings back to default theme
            self.theme_settings = themes.get_theme("Default")

            # Create a category data object
            category = data.Category(
                name = input_text,
                theme_settings = self.theme_settings
            )
            
            # Add the category object to list of categories inside the project instance (from data.py) 
            self.active_project.categories.append(category)
            


            # CREATE A TAB BUTTON
            category_button = ui.TabsButton(
                master = self.tabs,
                theme = self.theme_settings,
                text = input_text,
                command = lambda: self.change_category(input_text) # The button stores the category name (input_text) as argument for it's command.
            )

                # Add button to grid/row of tab buttons
            category_button.grid(
                row = 0,
                column = self.current_tab_column,
                padx = 5
            )

                # Increment up the counter so next button goes in the next column
            self.current_tab_column += 1


            # --- CREATE BODY / TO-DO LIST ---

                # Create the "body"/scrollable frame that holds the to-do items
            body = ui.TabsBody(
                master = self,
                theme = self.theme_settings # Use returned dictionary as argument
            )


            # Store the components of that category in a dictionary
            self.category_components[input_text] = {
                "tab": category_button,
                "body": body
            }

                # Add body/frame to the 'TabsView's grid
            body.grid(row=1, column=0, padx=20, sticky="nsew")


                # Change status
            if self.categories_exists == False:
                self.categories_exists = True

                # Set newly created category as the active one
            self.active_category = input_text


            # Update the UI

                # Hide the "no tabs exist" frame/text
            self.no_tabs_exist.grid_remove()

                # Frame with tabs/buttons/categories
            self.tabs.grid()

            # Loop through and hide the non-active "bodies"/frames with to-do items
                # category_name and category_components are temporary variables. "category_component", in each loop, contains both "tab" = the object/button we stored, AND "body" = the body/frame we stored
            for category_name, category_component in self.category_components.items():
                # if category name IS the same as the active category
                if category_name == self.active_category:
                    # do nothing
                    pass
                # Otherwise hide the stored "body" from the UI.
                else:
                    category_component["body"].grid_remove()

                # Show the theme selector dropdown (and label)
            self.footer.show_ui(True)

            # Update the footers theme to be the default theme 
            self.footer.update_theme(self.theme_settings)
