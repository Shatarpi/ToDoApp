# TO-DO MANAGER

#### Video Demo: https://www.youtube.com/watch?v=eaoq801UmdU
#### Description:
My project is a somewhat basic and classic to-do app, mainly tailored towards how I needed it to behave in my own day-to-day work.
The difference is that instead of having individual to-do lists scattered around, OR, a really long one that should handle every case, my app is designed to group and organize them. First by project (which can be e.g., a new program you are coding, what needs to be done on the car or similar), followed by categories that live inside each project. Which, if we continue with the same examples, can for example be (in the "car" project) "Engine", "Body", "Seats" and so on, all of which contain to-do lists of their own related to their category.

Besides this, it also allows for color coding, auto-saves any changes, and is packaged as a standalone app on the desktop, meaning it doesn't have to be launched through a terminal or similar.

I chose to do the entire project in Python as that is the language I want to dive deeper into (planning on taking CS50p after this!). Besides default Python, the library that was most extensively used was "customtkinter", (which is based on Pythons own "tkinter" library) which allowed me to fairly easily create a simple yet modern looking UI.
<br>
<br>



# Files & folders
In the project folder there various files and folder, not too many though so it should be somewhat easy to get a grasp on what is happening:
<br>
<br>



## main.py ##
This is the "Launch pad" of the application. It sets up and handles the main application window, switching views (from project view to category view and back), saving and similar.
This is the only Python file that is outside the src/todo_app folder structure.
<br>
<br>


## \src\todo_app\ ##
Most of the project files lives in this folder.

### \assets\ ###
This was meant to hold any icons, images and similar. I only ended up with a single icon, used for the main application window (as seen in the toolbar/desktop/top left corner of the application window).

#### icon_main.ico ####
The only icon used, seen in the toolbar/desktop, and top left corner of the application window.
<br>
<br>



### \core\ ###
This folder contains python files that deal with the fundamental structure of the application.

#### data.py ####
This contains the core classes that everything builds on, such as a project, category and to-do class.

#### storage.py ####
Creates the needed folders and reads/writes a json file in order to properly save data between sessions.

#### utils.py ####
Only contains a single function that returns the path the icon.
<br>
<br>



### \ui\ ###
Contains files that manages the color scheme(s) of everything and custom UI classes for the times where I wanted to deviate from the default customtkinter buttons etc.

#### themes.py ####
Basically just a bunch of similar dictionaries that contain various color codes, mainly used when switching the theme of a category.

#### widgets.py ####
Contains all the classes for specific UI elements, such as the project buttons, default square button, the tabs/categories and more.
<br>
<br>



### \views\ ###
Only consists of two files, yet where most of the work was done. These files are responsible for each of the 2 views the user can toggle between:
- The initial "projects" view where you see all the projects you have created.
- The "category" view, which is what you see when you "go into"/click on a project to see it's categories and to-do items.

#### projects_view.py ####
Handles the landing "page", loads existing projects, lets the user add new or remove projects, deals with the dialog/popups, refreshing the UI and similar.

#### category_view.py: ####
Handles the view after you click on a project, it loads in any existing categories and to-do items tied to that project, handles the logic for adding/removing both categories and to-do items and similar.
<br>
<br>



### Configuration files ###

The configuration files are in a few places, mostly directly in the project folder.

#### requirements.txt ####
This lists all the libraries used, which version they have etc.

#### .gitignore ####
This tells git what folder and files to ignore when comitting/pushing the project up to github.
<br>
<br>

# Design choices & challenges
When I got started I didn't know what to build, I only knew it had be with Python as that is my preferred language.
I was also interested in moving away from command line programs and learn how to create typical desktop applications. This got me looking into UI libraries, and while there are a couple of them out there, I landed on 'customtkinter' as it provided a modern look out of the box, a solid written documentation and multiple videos I could use as reference.

The workflow of going from Project to Category to To-Do was a bit of a no-brainer for me as that was how I already structured my notes in my day to day work, and works well for quickly being able to jump between lots of them when you deal with multiple things at once.

In terms of designing the actual code, I wish I had started with a different mindset. To be fair, not being experienced did play a role here, but, looking back, I realize I should have started out, for example, by creating classes for various things, compared to how I did it. I created something, realized I needed 1 more of it so I copied the code, then after a while realized I had copied the same code around and now had to transfer it to being a class (or helper function or similar) instead of doing it properly right away.
Lets just say, having to restructure lots of code every time I wanted to implement a new feature took a lot of time.
<br>
<br>

# Acknowledgements
This project was built with the help of an AI/LLM (gemini). It was used to provide guidance on things like:
- Learning concepts
- Code and folder structure
- Debugging
- Best practices
- Configuration files (.gitignore, requirements.txt)
- Git commands and workflow


I really liked how the CS50 duck/AI behaved/helped you out, so I repeatedly instructed the AI to act as a teacher, not to give me code that I could simply copy/paste, but instead explain things and nudge me in the right direction, similar to the CS50 duck. After all, I want to learn.

It also proved really useful for explaining new concepts in a way that I could understand, which would otherwise have taken a really long time.

