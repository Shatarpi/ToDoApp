
# Define the main background color for all views
MAIN_FRAME_COLOR = "#202020"

# Function for returning settings based on themes
def get_theme(theme):
    """Returns the a dictionary with settings for the requested theme"""

    # Define settings for different themes
    default_theme = {
        "main" : "#303030",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#404040",
        "hover" : "#606060",
        "text" : "#DADADA"
    }

    red_theme = {
        "main" : "#352929",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#ad5050",
        "hover" : "#bb7171",
        "text" : "#DADADA"
    }

    green_theme = {
        "main" : "#3B5541",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#43852f",
        "hover" : "#77a369",
        "text" : "#DADADA"
    }

    blue_theme = {
        "main" : "#3B4155",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#4173be",
        "hover" : "#7194c9",
        "text" : "#DADADA"
    }

    yellow_theme = {
        "main" : "#52553B",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#858b2c",
        "hover" : "#989c55",
        "text" : "#DADADA"
    }

    purple_theme = {
        "main" : "#4E3B55",
        "secondary" : "#FF00DD", # Temp color
        "accent" : "#8648a3",
        "hover" : "#ad7dc4",
        "text" : "#DADADA"
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