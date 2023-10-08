from customtkinter import *
from CTkListbox import *


class App:
    """Used to initialize the main chatting application"""

    def __init__(self, root):
        set_appearance_mode("System")
        set_default_color_theme("dark-blue")
        # root
        root.title("Chatt app")
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

        # initialize
        self.msg_entry_var = StringVar()
        self.msg_entry = CTkEntry(root, width=755, height=30, justify="left", textvariable=self.msg_entry_var)
        self.msg_list = CTkTextbox(root, width=855, height=640, font=("default", 20))
        self.people_list = CTkListbox(root, width=340, height=670, justify="center", font=("default", 20))
        self.msg_send_button = CTkButton(root, width=90, height=30, text="Enviar")

        # config
        self.msg_entry_var.set("")
        self.msg_list.configure(state="disabled")
        self.msg_entry.focus_set()

        # binds
        self.msg_entry.bind("<Return>", self.msg_send)
        self.people_list.bind("<<ListboxSelect>>", self.select_person)

        # place & pack
        self.people_list.pack(padx=10, pady=10, anchor="nw", side=LEFT)
        self.msg_list.pack(padx=0, pady=10, anchor="nw")
        self.msg_entry.pack(padx=0, pady=0, anchor="nw", side=LEFT)
        self.msg_send_button.pack(padx=10, pady=0, anchor="nw")

        # other
        self.msg_list.configure(state="normal")
        for i in range(100):
            self.msg_list.insert(END, f"{i}\n")
            self.people_list.insert(END, f"{i}")
        else:
            self.msg_list.configure(state="disabled")

    def msg_send(self):
        pass

    def select_person(self):
        pass


if __name__ == "__main__":
    root = CTk()
    app = App(root)
    root.mainloop()
