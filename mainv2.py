# Equivalent to the script in main.py but here I used class
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from numpy import random


class RecipePicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Picker")
        self.root.geometry("500x700")
        self.root.eval("tk::PlaceWindow . center")

        self.bg_color = "#4B0082"
        self.fg_color = "#ffffff"
        self.dark_color = "#000000"

        self.recipe_logo = ImageTk.PhotoImage(file="assets/recipe_logo.png")
        self.recipe_logo_bottom = ImageTk.PhotoImage(
            file="assets/recipe_logo_bottom.png"
        )

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainFrame = tk.Frame(self.root, bg=self.bg_color)
        self.recipeFrame = tk.Frame(self.root, bg=self.bg_color)

        for frame in (self.mainFrame, self.recipeFrame):
            frame.grid(row=0, column=0, sticky="nesw")

        self.load_frame1()

    def clear_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def fetch_db(self):
        connection = sqlite3.connect("data/recipes.db")
        cursor = connection.cursor()
        cursor.execute(" SELECT * FROM sqlite_schema WHERE type='table'; ")
        all_tables = cursor.fetchall()

        idx = random.randint(0, len(all_tables) - 1)

        table_name = all_tables[idx][1]
        cursor.execute("SELECT * FROM " + table_name + ";")
        table_records = cursor.fetchall()

        connection.close()
        return table_name, table_records

    def pre_process(self, table_name, table_records):
        title = table_name[:-6]
        title = "".join([char if char.islower() else " " + char for char in title])

        ingredients = [
            f"{record[2]} {record[3]} of {record[1]}" for record in table_records
        ]
        return title, ingredients

    def load_frame1(self):
        self.clear_widgets(self.recipeFrame)
        self.mainFrame.tkraise()

        logo_widget = tk.Label(self.mainFrame, bg=self.bg_color, image=self.recipe_logo)
        logo_widget.pack()

        guide_text = tk.Label(
            self.mainFrame,
            text="Ready for your random recipe?",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("TkMenuFont", 14),
        )
        guide_text.pack()

        shuffle_button = tk.Button(
            self.mainFrame,
            text="SHUFFLE",
            cursor="hand2",
            font=("TkHeadingFont", 18),
            bg=self.fg_color,
            fg=self.dark_color,
            command=self.load_frame2,
        )
        shuffle_button.pack(pady=20)

    def load_frame2(self):
        self.clear_widgets(self.mainFrame)
        self.recipeFrame.tkraise()

        table_name, table_records = self.fetch_db()
        title, ingredients = self.pre_process(table_name, table_records)

        logo_widget = tk.Label(
            self.recipeFrame, bg=self.bg_color, image=self.recipe_logo_bottom
        )
        logo_widget.pack(pady=20)

        title_wg = tk.Label(
            self.recipeFrame,
            text=title,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("TkHeadingFont", 20),
        )
        title_wg.pack(pady=25)

        for ingredient in ingredients:
            tk.Label(
                self.recipeFrame,
                text=ingredient,
                bg="#1f0036",
                fg=self.fg_color,
                font=("TkMenuFont", 12),
            ).pack(fill="both", padx=20)

        back_btn = tk.Button(
            self.recipeFrame,
            text="Back",
            cursor="hand2",
            font=("TkHeadingFont", 18),
            bg=self.fg_color,
            fg=self.dark_color,
            command=self.load_frame1,
        )
        back_btn.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipePicker(root)
    root.mainloop()
