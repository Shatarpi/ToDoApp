import customtkinter as ctk

def confirmation_print():
    """Just to show that the button works"""
    print("This works - But you need to assign a command to it!")


class PrimaryButton(ctk.CTkButton):
    """
    A custom primary button that inherits from CTkButton.
    It sets default styling for the application, which can be overridden.
    """
    def __init__(self, master, **kwargs):
        # Define the default styles for this button
        defaults = {
            "height": 40,
            "width": 160,
            "font": ctk.CTkFont(size=14),
            "command": confirmation_print,  # Default command to execute on click
        }

        # Allow user-provided arguments to override the defaults
        defaults.update(kwargs)
        
        # Call the parent class's __init__ method with the master and combined arguments
        super().__init__(master=master, **defaults)
