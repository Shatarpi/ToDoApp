"""The tabs view module that shows the tabs/categories and to-do items in each project"""

import customtkinter as ctk
import tkinter as tk
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
        self.active_project = None # Stores active project object
        self.active_category = None # Stores active category object
        
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
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 0)
        
        self.grid_columnconfigure(0, weight=1)



        # --- HEADER WITH PROJECT NAME ---
            # Create the frame (and text)
        self.header = ui.TabsHeader(
            master = self,
        )
            # Place it in the TabsView grid
        self.header.grid(row=0, column=0, pady = (0, 30))



        # --- NO TABS FRAME (WHEN CATEGORIES DOESN'T EXIST) ---
            # Create widget / frame
        self.no_tabs_exist = ui.NoTabsFrame(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )

        # Place it in 'TabsView's grid
        self.no_tabs_exist.grid(row=2, column=0, padx=50, pady=80, sticky="nsew")



        # --- TOP ROW OF BUTTONS/TABS ---

        # Create the category bar
        self.tabs = ui.TabsCategories(
            master = self,
            theme = self.theme_settings # Use returned dictionary as argument
        )

        # Place it in 'TabsView's grid
        self.tabs.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="nsew")



        # --- FOOTER/BOTTOM ROW OF BUTTONS ---
        
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
        self.footer.grid(row=3, column=0, padx=20, pady=(60, 20), sticky="nsew")


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



        # --- HIDE UI ELEMENTS AT LAUNCH ---

        if self.categories_exists == False:
            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide the theme selector dropdown (and label)
            self.footer.show_ui(False)

            # Show the "no tabs exist" frame/text
            self.no_tabs_exist.grid()





    # --- FUNCTIONS/METHODS ---

    # LOAD PROJECT - changes UI elements based on which project whas selected
    def load_project(self, project_data):

        # Initialize active category VAR
        self.active_category = None

        self.active_project = project_data # Store the project data
        self.header.set_text(project_data) # Tell the header widget to change it's text to display the correct project name

        # Hide the error text/frame
        self.error_text_frame.grid_remove()


        # If there was an active category from previous project
        if self.active_category is not None:
            # Remove it's body/to-do list from the main grid
            self.category_components[self.active_category.category_name]["body"].grid_remove()


        # Remove the old category components (tab/button and body/frame) from the GUI
        for category_name, components in self.category_components.items():
            components["tab"].destroy()
            components["body"].destroy()

        # Clear the main dictionary
        self.category_components = {}

        # Reset variables
        self.active_category = None
        self.current_tab_column = 0

        # Check if the active projects does NOT have any categories
        if not self.active_project.categories:
            
            # Set the status variable
            self.categories_exist = False

            # Hide the top row of button/tabs
            self.tabs.grid_remove()
            # Hide the theme selector dropdown (and label)
            self.footer.show_ui(False)
            # Set dropdown value
            self.footer.set_dropdown("Default")

            # Set the footer theme (mainly for the add button)
            self.footer.update_theme(themes.get_theme("Default"))


            # Show the "no tabs exist" frame/text
            self.no_tabs_exist.grid(row=2, column=0, padx=50, pady=80, sticky="nsew")

        # If list DOES have categories
        else:

            # Loop through the categories in the project
            for category_object in self.active_project.categories:
                
                    
                    # CREATE A TAB BUTTON
                category_button = ui.TabsButton(
                    master = self.tabs,
                    theme = category_object.theme_settings,
                    text = category_object.category_name,
                    command = lambda name = category_object.category_name: self.change_category(name) # The button stores the category name as argument for it's command.
                )

                    # Add button to grid/row of tab buttons
                category_button.grid(
                    row = 0,
                    column = self.current_tab_column,
                    padx = 5
                )

                    # Increment up the counter so next button goes in the next column
                self.current_tab_column += 1


                    # CREATE BODY / TO-DO LIST

                    # Create the "body"/scrollable frame that holds the to-do items
                body = ui.TabsBody(
                    master = self,
                    on_add_click = self.open_add_item,
                    theme = category_object.theme_settings
                )

                    # DON'T ADD THE BODY TO THE GRID HERE, THE CHANGE CATEGORY FUNCTION DOES THAT

                    # Store the components of that category in a dictionary
                self.category_components[category_object.category_name] = {
                    "tab": category_button,
                    "body": body,
                    "data": category_object
                }


            # Change status
            self.categories_exists = True

            # Update the UI

                # Hide the "no tabs exist" frame/text
            self.no_tabs_exist.grid_remove()

                # Show frame with tabs/buttons/categories
            self.tabs.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="nsew")

            # show the theme selector dropdown (and label)
            self.footer.show_ui(True)
            
            # Store the first category in the project as a VAR
            first_category = self.active_project.categories[0].category_name

            # Change the category to the first category in the project
            self.change_category(first_category)



    # SET VIEW (back button, goes back to projects_view)
    def set_view(self, to_view, project_data):
        self.master.set_view(to_view, project_data)



    # CHANGE CATEGORY
    def change_category(self, to_category):

        # Loop through the active projects categories (objects)
        for category in self.active_project.categories:

            # If category objects name matches name we want to switch to
            if category.category_name == to_category:
                
                # Update what is considered the active category with new object
                self.active_category = category

                # Get the theme settings from it
                settings = self.active_category.theme_settings

                # Update the footer with the new settings
                self.footer.update_theme(settings)

                # Set the theme selector/dropdown to use the category's theme.
                self.footer.set_dropdown(self.active_category.theme_name)

                # Once found and updated, exit the loop
                break

        # Make sure the active category got updated
        if self.active_category is not None:

            # Loop through the dictionary of category COMPONENTS (buttons/frames/bodies)
            for category_name, category_component in self.category_components.items():

                # Store the category tab/button
                tab = category_component["tab"]

                # Store the body/frame/list of to-dos
                body = category_component["body"]

                # Get/store the categories theme settings
                theme_settings = category_component["data"].theme_settings

                # Store font object (which contains the settings) for the buttons text
                font_object = tab.cget("font")

                # If category name IS the same as the category we want to be active
                if category_name == self.active_category.category_name:

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

                    # Store the to-do items that already exist in the frame, in a list
                    old_items = body.todo_frame.winfo_children()
                    
                    # Go through the list and delete the items (because we re-add them later)
                    for item in old_items:
                        item.destroy()

                    # Add it to the main grid
                    body.grid(row=2, column=0, padx=20, sticky="nsew")

                    # Initialize the counter for the to-do items
                    row = 0

                    # For every to-do item in the active category
                    for item in self.active_category.todo_items:

                        # Convert the true/false state stored in the to-do items data object to a tkinter boolean
                        checkbox_state_var = tk.BooleanVar(value = item.is_checked)

                        # Create the to-do item/checkbox UI widget
                        self.todo_item = ui.ToDoItem(
                            master = body.todo_frame,
                            theme = theme_settings,
                            text = item.text,
                            variable = checkbox_state_var,
                            command = lambda i=self.data_item, v=checkbox_state_var: self.checkbox_clicked(i, v)
                        )

                        # Add the stored to-do object to the scrollable frame
                        self.todo_item.grid(row=row, column = 0, sticky = "w", padx=20, pady = 5)

                        # Increment the row counter
                        row += 1

                # If category name is NOT the same as the category we want to be active
                else:
                    
                    # Hide the stored "body" from the UI.
                    body.grid_remove()

                    # Change the font object so it's bold text
                    font_object.configure(weight = "normal")
                    font_object.configure(size = 14)
                    
                    # Set tab/button to use the non-active color
                    tab.configure(
                        fg_color = theme_settings["main"],
                        hover_color = theme_settings["active_category"],
                        font = font_object,
                        height = 40
                        )



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
        dialog.after(200, lambda: dialog.iconbitmap("D:/Projects/Programming/ToDoApp/src/todo_app/assets/icon_main.ico"))

        # Hide the error text/frame
        self.error_text_frame.grid_remove()



        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but category is missing name
        elif input_text == "" or None:

            # Set the error text
            self.error_text.configure(text = "Category needs a name!")
            
            # Show the error frame/text
            self.error_text_frame.grid(row=3, column=0, padx=20, pady=(0, 20))



        # CREATE NEW CATEGORY
        else:


            # Check if category name is already being used
            for existing_category in self.active_project.categories:
                if existing_category.category_name == input_text:

                    # Set the error text
                    self.error_text.configure(text = "Name is taken")
                    
                    # Show the error frame/text
                    self.error_text_frame.grid(row=3, column=0, padx=20, pady=(0, 20))

                    return
                

            # Set warning/error text to be nothing if a project was successfully created.
            self.error_text.configure(text = "")

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

            
            # Change status
            if self.categories_exists == False:
                self.categories_exists = True
            

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
                padx = 3
            )

                # Increment up the counter so next button goes in the next column
            self.current_tab_column += 1


            # CREATE BODY / TO-DO LIST

                # Create the "body"/scrollable frame that holds the to-do items
            body = ui.TabsBody(
                master = self,
                on_add_click = self.open_add_item,
                theme = self.theme_settings # Use returned dictionary as argument
            )


            # Store the components of that category in a dictionary
            self.category_components[input_text] = {
                "tab": category_button,
                "body": body,
                "data": category
            }

            # Show the row of tabs at the top
            self.tabs.grid()

            # Show extra UI elements in the footer
            self.footer.show_ui(True)

            # Change the category to the newly created one to show the rest and make it active
            self.change_category(input_text)


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
            if index == None:
                self.categories_exists = False

                # Hide the row of tabs at the top
                self.tabs.grid_remove()

                # Hide extra UI elements in the footer
                self.footer.show_ui(False)

                # Show the "no categories exists" frame
                self.no_tabs_exist.grid(row=2, column=0, padx=50, pady=80, sticky="nsew")

            else:
                # Change to the new category
                self.change_category(new_category.category_name)





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
        dialog.after(200, lambda: dialog.iconbitmap("D:/Projects/Programming/ToDoApp/src/todo_app/assets/icon_main.ico"))



        # When popup/dialog is closed (Either OK, CANCEL or X)
        input_text = dialog.get_input()

        # If dialog is closed with Cancel or X
        if input_text == None:
            pass

        # Else if dialog is closed with OK, but item is missing name
        elif input_text == "" or None:
            self.error_text.configure(text = "To-do item needs a name!")


        # CREATE NEW TO-DO ITEM
        else:

            # Create the to-do item/checkbox OBJECT
            self.data_item = data.Todo(
                text = input_text,
            )
            
            # Add item to active category's self.todo_items = [] list
            self.active_category.todo_items.append(self.data_item)

            # Get/store the active categories frame that items go in
            body = self.category_components[self.active_category.category_name]["body"]

            # Get current theme settings
            theme_settings = self.active_category.theme_settings

            # Convert the true/false state stored in the to-do items data object to a tkinter boolean
            checkbox_state_var = tk.BooleanVar(value = self.data_item.is_checked)

            # Create a frame that will act as a row for each item with buttons etc.

            self.item_frame = ctk.CTkFrame(
                master = body.todo_frame,
                fg_color = "transparent"
            )

            # Create the to-do item/checkbox UI widget
            self.todo_item = ui.ToDoItem(
                master = self.item_frame,
                theme = theme_settings,
                text = input_text,
                variable = checkbox_state_var,
                command = lambda i=self.data_item, v=checkbox_state_var: self.checkbox_clicked(i, v)
            )

            # data_item = self.data_item
            # item_frame = self.item_frame
            

            # Create a delete button that will be next to the to-do item
            self.button_delete_todo = ui.SquareButton(
                master = self.item_frame,
                text = "X",
                width = 25,
                height = 25,
                font = ("", 12, "normal"),
                theme = theme_settings,
                corner_radius = 5,
                command = lambda i=self.data_item, v=self.item_frame: self.delete_todo_confirmation(i,v)
            )


            # Store length of list = which row it ends up on
            row = len(self.active_category.todo_items)

            # Place the frame/row in the scrollable frame, on the row that is equal to the total amount of to-do items that exist
            self.item_frame.grid(row = row, column = 0, sticky = "ew")

            # Place the delete and to-do in frame that acts as a row
            self.button_delete_todo.grid(row=0, column = 0, sticky = "w", padx=(10, 10), pady = 5)

            self.todo_item.grid(row=0, column = 1, sticky = "w", pady = 5)



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

            frame.destroy()
