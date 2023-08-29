from tkinter import *
from time import sleep

def lab():
    global blue_label
    global x
    blue_label.destroy()
    blue_label = Label(root, text=x)
    blue_label.pack()
    x += 1
x = 1
root = Tk()
root.geometry("300x250")
button = Button(root, text="X", command=lab)
button.pack()
blue_label = Label(root, text='0')
blue_label.pack()
root.mainloop()