


# Define the main background color for all views
MAIN_FRAME_COLOR = "#202020"

# Function for returning settings based on themes
def get_theme(theme):
    """Returns the a dictionary with settings for the requested theme"""

    # Define settings for different themes
    default_theme = {
        "button_fg_color": "#404040",
        "button_hover_color": "#606060",
        "button_text_color": "#EBEBEB",
        "button_tab_fg_color": "#454545", # Same as scrollable frame
        "button_tab_hover_color": "#606060",
        "scrollableFrame_fg_color": "#454545"

    }

    blue_theme = {
        "button_fg_color": "#2373eb",
        "button_hover_color": "#7ca7e7",
        "button_text_color": "#DADADA",
        "button_tab_fg_color": "#3B4155", # Same as scrollable frame
        "button_tab_hover_color": "#565E7A",
        "scrollableFrame_fg_color": "#3B4155",
    }

    red_theme = {
        "button_fg_color": "#c53737",
        "button_hover_color": "#b86161",
        "button_text_color": "#DADADA",
        "button_tab_fg_color": "#352929", # Same as scrollable frame
        "button_tab_hover_color": "#685050",
        "scrollableFrame_fg_color": "#352929"
    }

    if theme == "default":
        return default_theme

    elif theme == "blue":
        return blue_theme

    elif theme == "red":
        return red_theme