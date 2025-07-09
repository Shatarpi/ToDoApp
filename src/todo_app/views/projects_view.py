"""The projects view module that lists the available projects"""

import tkinter as tk
import customtkinter as ctk
from todo_app.ui import widgets as ui




# --- MAIN UI/LANDING "PAGE" CLASS ---
class ProjectsView(ctk.CTkFrame):
    """Main class"""

    # Constructor (Analogy: configure order for the car chassi)
    # __init__ is called when an object/instance of this is created
    def __init__(self, master, **kwargs):
    # Self: When this/a ProjectClass 'object' is created/instanced, it will
    # automatically call the __init__ method and pass itself as the first and 
    # argument/self.
    # This only happens when for functions inside a class, not for functions
    # outside a class.  

        # (Analogy: Add seats to the car chassi)
        defaults = {
            "fg_color": "#066413"
        }

        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        # (Analogy: order the car chassi with the new specifications)
        super().__init__(master, **defaults)

        header = ctk.CTkLabel(master=self, text="My Test label")
        header.grid(row=0, column=0, padx=20, pady=20)


        test_button = ui.PrimaryButton(
            master = self,
            text = "Switch to tabs view",
            # use 'lambda' to to create a mini/anonymous function, this
            # prevents the command from running when script is being executed/# application is started.
            command = lambda: self.set_view("tabs")
        )
        test_button.grid(row=0, column=0, padx=20, pady=20)

        button_add_project = ui.PrimaryButton(
            master = self,
            text = "Add project",
            command = self.open_add_project
        )
        button_add_project.grid(row=1, column=3, padx=20, pady=20)


        button_print = ui.PrimaryButton(
            master = self,
            text = "Print button",
            command = self.print
        )
        button_print.grid(row=2, column=0, padx=20, pady=20)




# --- FUNCTIONS ---


    # TEMP FUNCTION - Lets a button print something
    def print(self):
        cursor_x = tk.Tk.winfo_pointerx(self)
        cursor_y = tk.Tk.winfo_pointery(self)
        print("Cursor X: ", cursor_x, "Cursor Y: ", cursor_y)



    # Change the view/page
    def set_view(self, to_view):
        self.master.show_view(to_view)


    # Open the "Add project" popup/dialog window
    def open_add_project(self):
        dialog = ctk.CTkInputDialog(
            text="Project name:",
            title="Add new project",
            fg_color="#202020"
        )

        # --- POSITIONING THE DIALOG ---
        # Makes sure the dialogs contents are fully arranged and ready before doing anything else.
        dialog.update_idletasks()

        # Get cursor position
        pointer_x = self.winfo_pointerx()
        pointer_y = self.winfo_pointery()

        # Offset window from cursor
        # Manually figured out the size of the popup and hardcoded in offsets
        pos_x = pointer_x - 175 # Remove half of width from pos x
        pos_y = pointer_y - 100 # Remove half of height from pos y
    

        # Set the dialog position
        dialog.geometry(f"+{pos_x}+{pos_y}")


        # --- END POSITIONING ---

        input_text = dialog.get_input()


        print("Input text: ", input_text)