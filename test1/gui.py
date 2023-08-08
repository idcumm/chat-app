from tkinter import *

window = Tk()
window.title("Chat app")
window.geometry("900x500")

Label1 = Label(window, text="Escriba su mensaje:")
Label1.pack()


def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    Label1.config(text="Provided Input: " + inp)


inputtxt = Text(window, height=1, width=20)
inputtxt.pack(side=BOTTOM)

printButton = Button(window, text="Print", command=printInput)
printButton.pack(side=BOTTOM)

window.mainloop()
