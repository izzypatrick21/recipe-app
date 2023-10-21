import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from numpy import random

bg_color   = "#4B0082"
fg_color   = "#ffffff"
dark_color = "#000000"

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM sqlite_schema WHERE type='table'; ")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables) - 1)

    # fetch ingredients
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()
  
    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    ingredients = []

    for i in table_records:
        name    = i[1]
        qty     = i[2]
        unit    = i[3]
    
        custom_str = qty + " " + unit + " of " + name
        ingredients.append(custom_str)

    return title, ingredients


def loadMainFrame():
    clear_widgets(frame = recipeFrame)
    mainFrame.tkraise()

    mainFrame.pack_propagate(False)

    # logo widget
    logo_widget = tk.Label(mainFrame, bg=bg_color)
    logo_widget.logo_image = ImageTk.PhotoImage(file="assets/recipe_logo.png")  
    logo_widget.config(image=logo_widget.logo_image)
    logo_widget.pack()

    # guide widget
    guide_text = tk.Label(mainFrame, text="Ready for your random recipe?", 
                        bg=bg_color, fg=fg_color, font=("TkMenuFont", 14))
    guide_text.pack()

    # button widget
    shuffle_button = tk.Button(mainFrame, text="SHUFFLE", cursor="hand2", 
                            font=("TkHeadingFont", 18), bg=fg_color, fg=dark_color, 
                            activebackground="grey", activeforeground="black", 
                            command=lambda : loadRecipeFrame())
    shuffle_button.pack(pady=20)


def loadRecipeFrame():
    clear_widgets(frame = mainFrame)
    recipeFrame.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    # logo widget
    logo_widget = tk.Label(recipeFrame, bg=bg_color)
    logo_widget.logo_image = ImageTk.PhotoImage(file="assets/recipe_logo_bottom.png")  
    logo_widget.config(image=logo_widget.logo_image)
    logo_widget.pack(pady=20)

    # title widget
    title_wg = tk.Label(recipeFrame, text=title, bg=bg_color, fg=fg_color, font=("TkHeadingFont", 20))
    title_wg.pack(pady=25)

    for i in ingredients:
        tk.Label(recipeFrame, text=i, bg="#1f0036", fg=fg_color, font=("TkMenuFont", 12)).pack(fill="both", padx=20)

    back_btn = tk.Button(recipeFrame, text="Back", cursor="hand2", font=("TkHeadingFont", 18), bg=fg_color, fg=dark_color, 
                            activebackground="grey", activeforeground="black", command=lambda : loadMainFrame())
    back_btn.pack(pady=20)

# initiallize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

# create the main frame
mainFrame = tk.Frame(root, width=500, height=600, bg=bg_color)
recipeFrame = tk.Frame(root, bg=bg_color)

for frame in (mainFrame, recipeFrame):
    frame.grid(row=0, column=0, sticky="nesw")


loadMainFrame()

# run app
root.mainloop()
