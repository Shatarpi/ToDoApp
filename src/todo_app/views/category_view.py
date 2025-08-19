"""The tabs view module that shows the tabs/categories and to-do items in each project"""

import customtkinter as ctk
import tkinter as tk
from todo_app.ui import widgets as ui
from todo_app.ui import themes
from todo_app.core import data as data
from todo_app.core.utils import resource_path

# Import the main frame color for all frames
from todo_app.ui.themes import MAIN_FRAME_COLOR

# --- MAIN CLASS ---
class TabsView(ctk.CTkFrame):
    """Main class"""

# MAIN FRAME THAT HOLDS THE OTHER ELEMENTS
    # __init__ is called when an object/instance of this is created
    def __init__(self, master, **kwargs):

        # Set start value of the active/selected project/category
        self.active_project = None # Stores active project object
        self.active_category = None # Stores active category object
        
        # Set start theme
        selected_theme = "Default"

        # Get the theme settings
        self.theme_settings = themes.get_theme(selected_theme)

        # Create empty dict that later holds info about categories that exist
        self.category_components = {}

        # Set start counter for the tab buttons
        self.current_tab_column = 0

        # Set defaults for the main frame
        defaults = {
            "fg_color": MAIN_FRAME_COLOR
        }
        
        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        super().__init__(master, **defaults)

        # Configure the internal grid in this view/frame 
        self.grid_rowconfigure(0, weight = 0) # Header
        self.grid_rowconfigure(1, weight = 0) # Category tabs
        self.grid_rowconfigure(2, weight = 1) # Body/frame that holds to-do's
        self.grid_rowconfigure(3, weight = 0) # Error message
        self.grid_rowconfigure(4, weight = 0) # Footer
        
        self.grid_columnconfigure(0, weight=1)



        # HEADER WITH PROJECT NAME
            # Create the frame (and text)
        self.header = ui.TabsHeader(
            master = self,
        )
            # Place it in the TabsView grid
        self.header.grid(row=0, column=0, pady = (0, 30))



        # 'NO CATEGORIES EXIST' FRAME
            # Create widget / frame
        self.no_tabs_exist = ui.NoTabsFrame(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )


        # TOP ROW OF BUTTONS/TABS
            # Create the category bar
        self.tabs = ui.TabsCategories(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )


        # ERROR FRAME
            # Create the main frame that holds the error elements
        self.error_main_frame = ctk.CTkFrame(
            master = self,
            fg_color = "transparent"
        )

            # Add it to the main grid
        self.error_main_frame.grid(row=3, column=0, pady = 20)

            # Create the frame that holds the error/warning text
        self.error_text_frame = ctk.CTkFrame(
            master = self.error_main_frame,
            border_width = 1,
            border_color = "#da3232"
        )
            # Add it to the main frame
        self.error_text_frame.grid(row=0, column=0)

            # Create the error text that appears when e.g., name is taken
        self.error_text = ctk.CTkLabel(
            master = self.error_text_frame,
            text = "", # Text is added when an error arises
            font = ("", 16),
            text_color = "#da3232"
        )

            # Add the text to the error text frame
        self.error_text.grid(row=0, column=0, padx=20, pady = 10)


        # FOOTER/BOTTOM ROW OF BUTTONS
        
            # Create footer that contains the back, add etc. buttons
        self.footer = ui.TabsFooter (
            master = self,
            theme = self.theme_settings, # Use returned dictionary as argument
            on_back_click = lambda: self.set_view("projects", None),
            theme_select = self.set_theme, # Send the "set_theme" function to the new instance
            on_add_click = self.open_add_category,
            on_remove_click = self.delete_category_confirmation
        )
            # Place it in 'TabsView's grid
        self.footer.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")



        # HIDE UI ELEMENTS AT LAUNCH
        self.update_ui()



    # --- FUNCTIONS/METHODS ---

    # LOAD PROJECT - changes UI elements based on which project whas selected
    def load_project(self, project_data):


        # If there was an active category from previous project
        if self.active_category is not None:
            # Remove it's body/to-do list from the main grid
            self.category_components[self.active_category.category_name]["body"].grid_remove()


        # Reset variables
        self.active_category = None
        self.current_tab_column = 0


        # Remove the old category components (tab/button and body/frame) from the GUI
        for category_name, components in self.category_components.items():
            components["tab"].destroy()
            components["body"].destroy()


        # Clear the main dictionary
        self.category_components = {}

        self.active_project = project_data # Store the project data
        self.header.set_text(project_data) # Tell the header widget to change it's text to display the correct project name

        # If project has categories, set the first one to be active
        if self.active_project.categories:
            self.active_category = self.active_project.categories[0]

        # Build UI stuff for each category
        for category in self.active_project.categories:
            self.create_category_components(category)


        # Update the UI
        self.update_ui()



    # CREATE UI COMPONENTS (TAB BUTTON, BODY)
    def create_category_components(self, category):
            
            # CREATE A TAB BUTTON
            category_button = ui.TabsButton(
                master = self.tabs,
                theme = self.theme_settings,
                text = category.category_name,
                command = lambda: self.change_category(category.category_name) # The button stores the category name (input_text) as argument for it's command.
            )

            # CREATE BODY / TO-DO LIST
                # Create the "body"/scrollable frame that holds the to-do items
            body = ui.TabsBody(
                master = self,
                on_add_click = self.open_add_item,
                theme = self.theme_settings # Use returned dictionary as argument
            )


            # Store the components of that category in a dictionary
            self.category_components[category.category_name] = {
                "tab": category_button,
                "body": body,
                "data": category
            }



    def create_todo_item(self, object, master):
        
        # Get current theme settings
        theme_settings = self.active_category.theme_settings

        # Convert the true/false state stored in the to-do items data object to a tkinter boolean
        checkbox_state_var = tk.BooleanVar(value = object.is_checked)

        # Get/store the default theme
        default_theme = themes.get_theme("Default")


        # Create a frame that will act as a row for each item with buttons etc.
        self.item_frame = ctk.CTkFrame(
            master = master,
            fg_color = "transparent"
        )

        # Create a delete button that will be next to the to-do item
        self.button_delete_todo = ui.SquareButton(
            master = self.item_frame,
            text = "X",
            width = 25,
            height = 25,
            font = ("", 12, "normal"),
            theme = default_theme,
            corner_radius = 5,
            command = lambda i=object, v=self.item_frame: self.delete_todo_confirmation(i,v)
        )

        self.button_delete_todo.grid(column = 0, row = 0)


        # Create the to-do item/checkbox UI widget
        self.todo_item = ui.ToDoItem(
            master = self.item_frame,
            theme = theme_settings,
            text = object.text,
            variable = checkbox_state_var,
            command = lambda i=object, v=checkbox_state_var: self.checkbox_clicked(i, v)
        )
        
        self.todo_item.grid(column = 1, row = 0, padx = (20, 0))

        
        return self.item_frame



    # UPDATES THE UI (shows/hides button etc on the grid)
    def update_ui(self, error_text=None): # Set argument default value to None

        # NO ACTIVE PROJECT - Hide everything, sort of.
        if self.active_project == None:

            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide UI elements in footer (theme selector, remove button etc.)
            self.footer.show_ui(False)



        # IF CATEGORIES DOES NOT EXIST
        elif not self.active_project.categories:

            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide UI elements in footer (theme selector, remove button etc.)
            self.footer.show_ui(False)
            # Set dropdown value
            self.footer.set_dropdown("Default")
            # Set the footer theme
            self.footer.update_theme(themes.get_theme("Default"))

            # Show the "no tabs exist" frame/text
            self.no_tabs_exist.grid(row=2, column=0, padx=50, pady=80, sticky="nsew")


        # IF CATEGORIES EXIST
        else:
            
            # Add the tab buttons to the top row
                # Initialize the counter for the tabs/buttons
            tab_column = 0

            # Go through all the categories in the project
            for category in self.active_project.categories:

                # Get the theme settings for it
                theme_settings = category.theme_settings

                # Get the current categories UI components
                components = self.category_components[category.category_name]
                body = components["body"]
                tab = components["tab"]

                # Store font object (which contains the settings) for the buttons text
                font_object = tab.cget("font")
                
                # Grid the tab button
                tab.grid(row=0, column = tab_column, padx = 5)


                # ACTIVE CATEGORY
                    # If category is the active category, and names match
                if self.active_category and self.active_category == category:

                    # Update the footer with the new settings
                    self.footer.update_theme(theme_settings)

                    # Set the theme selector/dropdown to use the category's theme.
                    self.footer.set_dropdown(self.active_category.theme_name)
                    
                    # Change the font object so it's bold and larger
                    font_object.configure(weight = "bold")
                    font_object.configure(size = 16)

        
                    # Change the tab/button to use the active color
                    tab.configure(
                        fg_color = theme_settings["active_category"],
                        hover_color = theme_settings["active_category"],
                        font = font_object,
                        height = 50
                        )

                    # Change the frame that holds items to use the active color
                    body.todo_frame.configure(fg_color = theme_settings["active_category"])

                    # Add the body frame to the main grid
                    body.grid(row=2, column=0, padx=20, sticky="nsew")

                    # Store the to-do items that already exist in the frame, in a list
                    old_items = body.todo_frame.winfo_children()
                    
                    # Go through the list and delete the items (because we re-add them later)
                    for item in old_items:
                        item.destroy()

                    # Initialize the counter for the to-do items
                    row = 0

                    # For every to-do item in the active category
                    for item in self.active_category.todo_items:

                        # If it's the first item, increase the padding on top to create a gap between tab buttons and the first to-do item.
                        if row == 0:
                            pad_top = 30
                        else:
                            pad_top = 5
                        
                        # Create the to do item
                        new_todo_item = self.create_todo_item(item, body.todo_frame)

                        # Add the new to-do object to the scrollable frame
                        new_todo_item.grid(row=row, column = 0, sticky = "w", padx = 5, pady = (pad_top, 5))

                        # Increment the row counter
                        row += 1




                # If category name is NOT the same as the category we want to be active
                else:
                    
                    # Hide the stored "body" from the UI.
                    body.grid_remove()

                    # Change the font object so it's normal text
                    font_object.configure(weight = "normal")
                    font_object.configure(size = 14)
                    
                    # Set tab/button to use the non-active color
                    tab.configure(
                        fg_color = theme_settings["main"],
                        hover_color = theme_settings["active_category"],
                        font = font_object,
                        height = 40
                        )


                    # Increment the counter
                tab_column += 1


            # HIDE "NO CATEGORIES EXIST" ELEMENTS
                # Hide the "no categories exist" frame/text
            self.no_tabs_exist.grid_remove()

                # Show frame with tabs/buttons/categories
            self.tabs.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="nsew")


            # Show additional footer elements (dropdown, remove button etc.)
            self.footer.show_ui(True)
            


        # ERROR MESSAGE
            # If there is an error to show
        if error_text is not None:
                # Change the text to be what we want
            self.error_text.configure(text = error_text)

                # Grid the frame that holds the text
            self.error_text_frame.grid(row = 0)
        
            # If there is no error to show, hide the frame that holds the text
        else:
            self.error_text_frame.grid_remove()
            


    # SET VIEW (back button, goes back to projects_view)
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data)



    # CHANGE CATEGORY
    def change_category(self, to_category):

        # Loop through the active projects categories
        for category in self.active_project.categories:

            # If category objects name matches name we want to switch to
            if category.category_name == to_category:
                
                # Update what is considered the active category
                self.active_category = category

                # Update the UI
                self.update_ui()

                # Once found and updated, abort
                break


    # UPDATES / CHANGES THE THEME OF A TAB
    def set_theme(self, selected_theme_name):
        

        # Check if we have an active category
        if self.active_category is not None:
            
            # Store the new theme NAME in the category object
            self.active_category.theme_name = selected_theme_name

            # Get and store the new theme SETTINGS in the category object
            self.active_category.theme_settings = themes.get_theme(selected_theme_name)

            # Go into category_components (which holds all the dictionaries of stored widgets per category), get the dictionary that is our current category, then get the button associated with it's "tab" key.
            active_button_object = self.category_components[self.active_category.category_name]["tab"]
            
            active_body_object = self.category_components[self.active_category.category_name]["body"]

            # Get the new theme settings from the category object and store in local variable
            new_theme = self.active_category.theme_settings

            # Feed the new tab/button object for the active category to the update theme method
            active_button_object.update_theme(new_theme)
            active_body_object.update_theme(new_theme)
            self.footer.update_theme(new_theme)

            # Change category as an easy way to make it "active" and get it to use the active colors
            self.change_category(self.active_category.category_name)

            # Save all the data to file
            self.master.save()
            
        # If there is no active category
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
        dialog.after(200, lambda: dialog.iconbitmap(resource_path("src/todo_app/assets/icon_main.ico")))

        # Refresh UI to remove potential error text
        self.update_ui()

        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but category is missing name
        elif input_text == "" or None:

            # Update UI to show error text
            self.update_ui("Category needs a name!")



        # CREATE NEW CATEGORY
        else:

            # Check if category name is already being used
            for existing_category in self.active_project.categories:
                if existing_category.category_name == input_text:
                    
                    # Update UI to show error text
                    self.update_ui("Name is taken")
                    return

            # Reset theme settings back to default theme
            self.theme_settings = themes.get_theme("Default")

            # Create a category data object
            category = data.Category(
                name = input_text,
                theme_name = "Default",
                theme_settings = self.theme_settings
            )

            # Set newly created category as the active one
            self.active_category = category
            
            # Add the category object to list of categories inside the project instance (from data.py) 
            self.active_project.categories.append(self.active_category)

            # Create the tab button and body that will hold to-do items
            self.create_category_components(category)

            # Save all the data to file
            self.master.save()

            # Update the UI so they are displayed
            self.update_ui()
            


    def delete_category_confirmation(self):

        # Store the name of the active category
        category_name = self.active_category.category_name


        # Open up the popup/confirmation window
        ui.ConfirmationPopup(master = self,thing_to_delete = f"category '{category_name}'", on_yes_click = lambda: delete_category())

        
        # Function that the "yes" button in the popup calls 
        def delete_category():

            # Initialize the category we want to switch to
            new_category = None

            # Store category's index in list of categories
            index = self.active_project.categories.index(self.active_category)

            # If it's the first category in the list
            if index == 0:
                # Check if there is a category after it
                if index +1 < len(self.active_project.categories):
                    # If it does, increment the index
                    index += 1
                else:
                    # If no categories will exists after this has been deleted, set VAR to None
                    index = None

            else:
                index -= 1   

            # If index IS None, then there is no category to switch to
            if index != None:
                # Store the new category we want to change to
                new_category = self.active_project.categories[index]


            # Store the tab/button as a variable
            button = self.category_components[self.active_category.category_name]["tab"]

            # Remove the tab/button
            button.destroy()
            
            # Store the body/scrollable frame as a variable
            body = self.category_components[self.active_category.category_name]["body"]

            # Remove the body/scrollable frame
            body.destroy()

            # Remove the category from the UI components dictionary as well
            self.category_components.pop(self.active_category.category_name, None)

            # Remove the active category object from the active projects list of categories
            self.active_project.categories.remove(self.active_category)

            # Switch to a new category
                # If index is None, then there is no category left to switch to
            if index != None:

                # Change to the new category
                self.change_category(new_category.category_name)

            # Save all the data to file
            self.master.save()

            # Update the UI
            self.update_ui()



    # "ADD ITEM" POPUP/DIALOG BOX
    def open_add_item(self):
        dialog = ctk.CTkInputDialog(
                title = "Add to-do",
                text = "What do you need to do?:",
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
        dialog.after(200, lambda: dialog.iconbitmap(resource_path("src/todo_app/assets/icon_main.ico")))


        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but item is missing name
        elif input_text == "":
            
            # Display the error text
            self.update_ui("To-do item needs a name!")

        # CREATE NEW TO-DO ITEM
        else:

            # Store the body which will be the items master
            body = self.category_components[self.active_category.category_name]["body"]

            # Create the to-do item/checkbox OBJECT
            data_item = data.Todo(
                text = input_text,
            )

            # Add new data item to active categories list of to-do's
            self.active_category.todo_items.append(data_item)

            # Save all the data to file
            self.master.save()

            # Update the UI to place/grid the new item
            self.update_ui()



    # WHEN A CHECKBOX IS CLICKED
    def checkbox_clicked(self, checkbox, tk_boolean):

        # Input is tkinters custom boolean, were we "get" it's actual value and store it in our own variable
        current_state_bool = tk_boolean.get()

        # Use the checkbox item/data object that was passed through, and change its internal "is_checked" value
        checkbox.is_checked = current_state_bool



    # DELETE TO-DO ITEM POPUP
    def delete_todo_confirmation(self, data_to_delete, ui_to_delete):

        ui.ConfirmationPopup(master = self, thing_to_delete = "to-do", on_yes_click = lambda: delete_item(data_to_delete, ui_to_delete))

        
        # Function that the "yes" button in the popup calls
        def delete_item(data, frame):

            self.active_category.todo_items.remove(data)

            # Save all the data to file
            self.master.save()

            frame.destroy()
