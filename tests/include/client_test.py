from tkinter import *
from threading import Thread
from tkinter.font import *
from time import sleep
from os import path


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
            root,
            yscrollcommand=self.people_list_scrollbar.set,
            selectmode=SINGLE,
            font=Font(size=20),
            justify=CENTER,
        )
        self.my_msg = StringVar()
        self.entry_field = Entry(root, textvariable=self.my_msg, font=Font(size=15))
        self.msg_text_list_scrollbar = Scrollbar(root)
        self.msg_text_list = Text(root, yscrollcommand=self.msg_text_list_scrollbar.set)

        self.people_list.bind("<<ListboxSelect>>", self.select_person)
        self.people_list_scrollbar.config(command=self.people_list.yview)
        self.my_msg.set("")
        self.msg_text_list["borderwidth"] = "1px"
        self.msg_text_list["font"] = Font(size=15)
        self.msg_text_list.tag_config("right", justify="right")
        self.msg_text_list.tag_config("center", justify="center")
        self.msg_text_list.configure(state="disabled")

        self.entry_field.bind("<Return>", self.msg_send)
        self.entry_field.focus_set()

        self.people_list.place(x=20, y=20, width=300, height=660)
        self.people_list_scrollbar.place(x=330, y=20, width=20, height=660)
        self.msg_text_list_scrollbar.place(x=1220, y=10, width=20, height=640)

        everyone = list()
        for i in people:
            everyone.append(i)
        else:
            everyone.append(username)
        for i in everyone:
            for j in everyone:
                if i < j:
                    try:
                        open(f"{file_path}\{i}_{j}.log", "x", encoding="utf8", newline="")
                    except FileExistsError:
                        print(f"{i}_{j}.log already exists")
        for i in people:
            self.people_list.insert(END, i)

    def select_person(self, event=None):
        self.person_selected = self.people_list.curselection()[0]
        if username < people[self.person_selected]:
            command = f'/setchat "{username}", "{people[self.person_selected]}"'
        else:
            command = f'/setchat "{people[self.person_selected]}", "{username}"'
        sleep(0.1)
        self.serv_recvv(command)

    def msg_send(self, event=None):
        self.msg_text_list.configure(state="normal")
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.msg_text_list.insert(END, msg + "\n")
        self.msg_text_list.yview(END)
        self.msg_text_list.configure(state="disabled")
        with open(
            f"{file_path}\{self.person1}_{self.person2}.log",
            "a",
            encoding="utf8",
            newline="",
        ) as file:
            file.write(msg + "\n")

    def serv_recvv(self, x):
        print(x)
        self.person1, self.person2 = eval(x[9:])
        self.msg_text_list.place(x=380, y=10, width=830, height=640)
        self.entry_field.place(x=380, y=660, width=800, height=30)
        with open(
            f"{file_path}\{self.person1}_{self.person2}.log",
            "r",
            encoding="utf8",
            newline="",
        ) as file:
            f = file.readlines()
            self.msg_text_list.configure(state="normal")
            self.msg_text_list.delete("1.0", END)
            for line in f:
                self.msg_text_list.insert(END, line)
            self.msg_text_list.yview(END)
            self.msg_text_list.configure(state="disabled")


people = "persona1", "persona2", "guillem", "jan"
username = "persona0"
absolute_path = path.dirname(path.abspath(__file__))
file_path = absolute_path + "/logs"

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
