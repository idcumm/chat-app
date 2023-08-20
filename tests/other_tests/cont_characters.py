# Import the required libraries
from tkinter import *
from PIL import Image, ImageTk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")


def show_msg(event):
    label["text"] = "Sale Up to 50% Off!"


# Create a label widget
label = Label(win, text="Press Enter Key", font="TkMenuFont 20")
label.pack(pady=30)

# Bind the Enter Key to the window
win.bind("<Return>", show_msg)

win.mainloop()
