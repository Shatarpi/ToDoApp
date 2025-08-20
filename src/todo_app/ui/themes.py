# Define the main background color for all views
MAIN_FRAME_COLOR = "#202020"

# Function for returning settings based on themes
def get_theme(theme):
    """Returns the a dictionary with settings for the requested theme"""

    # Define settings for different themes
    default_theme = {
        "main" : "#303030",
        "active_category" : "#404040", # Temp color
        "accent" : "#404040",
        "hover" : "#606060",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }

    red_theme = {
        "main" : "#352929",
        "active_category" : "#493030",
        "accent" : "#ad5050",
        "hover" : "#bb7171",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }

    green_theme = {
        "main" : "#3B5541",
        "active_category" : "#3C6946",
        "accent" : "#43852f",
        "hover" : "#77a369",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }

    blue_theme = {
        "main" : "#3B4155",
        "active_category" : "#3A4569",
        "accent" : "#4173be",
        "hover" : "#7194c9",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }

    yellow_theme = {
        "main" : "#52553B",
        "active_category" : "#595E36",
        "accent" : "#858b2c",
        "hover" : "#989c55",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }

    purple_theme = {
        "main" : "#4E3B55",
        "active_category" : "#593964",
        "accent" : "#8648a3",
        "hover" : "#ad7dc4",
        "text" : "#DADADA",
        "checkbox_border" : "#9C3939",
        "checkbox_hover" : "#C4C4C4",
        "checkbox_done" : "#349e31"
    }


    if theme == "Default":
        return default_theme
    
    elif theme == "Red":
        return red_theme

    elif theme == "Green":
        return green_theme

    elif theme == "Blue":
        return blue_theme
    
    elif theme == "Yellow":
        return yellow_theme
    
    elif theme == "Purple":
        return purple_theme