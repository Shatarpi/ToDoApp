"""The tabs view module that shows the tabs/categories in each project"""

import customtkinter as ctk
from todo_app.ui import widgets as ui



# --- TABS/CATEGORY VIEW/CLASS ---
class TabsView(ctk.CTkFrame):
    """Main class"""

    # __init__ is called when an object/instance of this is created
    def __init__(self, master, **kwargs):

        defaults = {
            "fg_color": "#640664"
        }
        
        # Allow instantiation arguments to override the defaults
        defaults.update(kwargs)

        # (Analogy: order the car chassi with the new specifications)
        super().__init__(master, **defaults)

        test_button = ui.PrimaryButton(
            master=self,
            text="Switch to projects view",
            command=lambda: self.set_view("projects")
        )

        test_button.grid(row=0, column=0, padx=20, pady=20)



    def set_view(self, to_view):
        self.master.show_view(to_view)
