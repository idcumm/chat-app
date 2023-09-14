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
            for j in people:
                if i < j:
                    try:
                        open(f'chat-choose\_{i}_{j}_.log', "x", encoding="utf8", newline="")
                    except FileExistsError:
                        print(f"_{i}_{j}_.log already exists")
            self.people_list.insert(END, i)
        else:
            self.people_list.activate(1)
            

    def select_person(self, event=None):
        person_selected = self.people_list.curselection()[0]
        command = f'/setchat "{username}", "{people[person_selected]}"'
        serv_recvv(command)


people = "Joan", "Miquel", "Ramón", "Josep"
username = "Guillem"

def serv_recvv(x):
    person1, person2 = eval(x[9:])
    print(person1, person2)
    # try:
    #     with open(f'chat-choose\_{person1}_{person2}_.log', "w", encoding="utf8", newline="") as file:
    #         data = []
            
        
    # except:
    #     try:
    #         with open(f'chat-choose\_{person1}_{person2}_.log', "r+", encoding="utf8", newline="") as file:
    #             data = []
            
    #     except:
    #         try:
    #             with open(f'chat-choose\_{person2}_{person1}_.log', "r+", encoding="utf8", newline="") as file:
    #                 data = []
    #         except:
    #             print('error')
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
