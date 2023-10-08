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
        root.resizable(width=False, height=False)

        # initialize
        self.login_root = CTkFrame(root)
        self.user_entry_var = StringVar()
        self.key_entry_var = StringVar()
        self.user_entry = CTkEntry(
            self.login_root,
            width=200,
            textvariable=self.user_entry_var,
        )
        self.key_entry = CTkEntry(
            self.login_root,
            width=200,
            textvariable=self.key_entry_var,
            show="*",
        )
        self.Error_label = CTkLabel(self.login_root, text="\n", width=2000)

        CTkLabel(self.login_root, text="\n\n\n\n\n\n\n\n").pack()
        CTkLabel(self.login_root, text="Introduzca el nombre de usuario y la contraseña\n", font=("Roboto", 24)).pack()
        CTkLabel(self.login_root, text="Nombre de usuario *").pack()
        self.user_entry.pack()
        CTkLabel(self.login_root, text="Contraseña *").pack()
        self.key_entry.pack()
        CTkLabel(self.login_root, text="").pack()
        CTkButton(
            self.login_root,
            text="Login",
            command=lambda: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        ).pack()
        CTkLabel(self.login_root, text="").pack()
        CTkButton(
            self.login_root,
            text="Register",
            command=lambda: self.register(self.user_entry_var.get(), self.key_entry_var.get()),
        ).pack()
        self.Error_label.pack()
        self.login_root.pack(side=LEFT, fill=BOTH)


if __name__ == "__main__":
    root = CTk()
    app = App(root)
    root.mainloop()
