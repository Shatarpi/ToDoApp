# A portion of this code was written with the help of an AI tool to help with debugging and explaining/teaching new concepts while the logic and structure were my own.


'''
These are the different objects that store data. E.g., the project class/object stores information about it's name and which categories it contains.
'''

# --- PROJECT ---
class Project():
    """
    The object that stores the data/information about a project
    """
    def __init__(self, name, categories=None):
        self.project_name = name # Holds the name of the project

        # If categories data exists, convert it into a list of Category objects
        if categories is not None:
            self.categories = [Category(**cat_data) for cat_data in categories]
        else:
            self.categories = []


    # Convert the project to a dictionary so it can be saved out as json
    def to_dict(self):

        # Initialize the list that will hold all the category dictionaries
        category_dicts = []

        # For every category, create a dict of it and add it to a new list
        for category in self.categories:
            category_dict = category.to_dict()
            category_dicts.append(category_dict)

        # Return a dictionary
        return {
        "name": self.project_name,
        "categories": category_dicts
        }



class Category():
    """
    The object that stores the data/information about a category
    """

    def __init__(self, name, theme_name, theme_settings, todo_items=None):
        self.category_name = name
        self.theme_name = theme_name
        self.theme_settings = theme_settings
        
        # If todo_items data exists, convert it into a list of Todo objects
        if todo_items is not None:
            self.todo_items = [Todo(**todo_data) for todo_data in todo_items]
        else:
            self.todo_items = []

    # Convert the category to a dictionary so it can be saved out as json
    def to_dict(self):

        # Initialize the list that will hold all the todo dictionaries
        todo_dicts = []

        # For every to_do item, create a dict of it and add it to a new list
        for todo in self.todo_items:
            todo_dict = todo.to_dict()
            todo_dicts.append(todo_dict)

        # Return a dictionary
        return {
        "name": self.category_name,
        "theme_name": self.theme_name,
        "theme_settings": self.theme_settings,
        "todo_items": todo_dicts
        }



class Todo():
    """
    The object that stores the data/information about an indvidual to do item
    """
    def __init__(self, text, is_checked=False):
        self.text = text
        self.is_checked = is_checked


    # Convert the todo item to a dictionary so it can be saved out as json
    def to_dict(self):
        return {
            "text": self.text,
            "is_checked": self.is_checked
        }