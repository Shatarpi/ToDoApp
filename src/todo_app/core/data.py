

# --- PROJECT ---
class Project():
    """
    The object that stores the data/information about a project
    """
    def __init__(self, name,):
        self.project_name = name # Holds the name of the project
        self.categories = [] # Holds all of the category objects



class Category():
    """
    The object that stores the data/information about a category
    """

    def __init__(self, name, theme_name, theme_settings):
        self.category_name = name
        self.theme_name = theme_name
        self.theme_settings = theme_settings
        self.todo_items = []


class Todo():
    """
    The object that stores the data/information about an indvidual to do item
    """
    def __init__(self, text):
        self.text = text
        self.is_checked = False