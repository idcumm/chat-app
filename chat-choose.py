from tkinter import *
from threading import Thread
from tkinter.font import *


class App:
    def __init__(self, root):
        width = 1250
        height = 700
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.people_list_scrollbar = Scrollbar()
        self.people_list = Listbox(
            root, yscrollcommand=self.people_list_scrollbar.set, selectmode=SINGLE, font=Font(size=20), justify=CENTER)
        self.people_list.bind("<<ListboxSelect>>", self.select_person)
        self.people_list_scrollbar.config(command=self.people_list.yview)

        self.people_list.place(x=20, y=20, width=300, height=660)
        self.people_list_scrollbar.place(x=330, y=20, width=20, height=660)

        for i in people:
            self.people_list.insert(END, i)
        else:
            self.people_list.activate(1)

    def select_person(self, event=None):
        person_selected = self.people_list.curselection()[0]
        print(people[person_selected])


people = "Joan", "Miquel", "Ramón", "Josep"

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
