'''
This handles the import/export of the data, meaning it saves the existing projects/categories/to-do items so that it doesn't have to be recreated everytime the program is launched.
'''

import json
import os
import appdirs


# Get and create path to C:\Users\[YourUsername]\AppData\Local\ToDoApp\
DATA_DIR = appdirs.user_data_dir("ToDoApp")

# Add "data.json" to the end of the path created above
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def save_data(all_projects_data):
    """Saves the projects data to a JSON file."""

    # Create the folder(s) if it/they dont exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Write the data to the JSON file
        # open the file in "write" mode and store the file as an object called f
    with open(DATA_FILE, "w") as f:
        # Write json style text, using infor stored in all_projects_data, to the object f
        json.dump(all_projects_data, f, indent=4)





def load_data():
    """Loads projects data from a JSON file."""

    # If data file doesn't exist, return an empty list
    if not os.path.exists(DATA_FILE):
        return []
    
    # If file does exist, open it in read mode
    with open(DATA_FILE, "r") as f:

        # Load/read the data and return it. This is being returned as a list/array of dictionaries. Each dictionary is a seperate project.
        return json.load(f)