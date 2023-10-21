import tkinter as tk
from PIL import ImageTk, Image

# initiallize app
root = tk.Tk()
root.title("Recipe Picker")
# root.eval("tk::PlaceWindow . center")

# create the main frame
mainFrame = tk.Frame(root, width="500", height="600", bg="#4B0082")
mainFrame.grid(row="0", column="0")

x = root.winfo_screenwidth() // 2
y = int(root.winfo_screenheight() * 0.1)
root.geometry("500x600+" + str(x) + "+" + str(y))

# mainFrame widgets
logo_image = ImageTk.PhotoImage(file="assets/recipe_logo.png")
logo_widget = tk.Label(mainFrame, image=logo_image, bg="#4B0082")
logo_widget.image = logo_image
logo_widget.pack()

# run app
root.mainloop()
