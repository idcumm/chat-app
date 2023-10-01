# bubbl.us
# * millorar tot el procediment
# * Aplicar tcp method (enviar info per files)
# * Crear data.csv al __init__
# * que es crei el b64.db al enviar missatge, no tots al principi
# TODO posar dia i hora en missatges
# TODO fer funcio tot allo que es repeteix molt
# TODO millorar notification
# TODO que no es repeteixi el nom mes dun missatge seguit
# TODO fer que es pugui fer resize
# TODO fer autologin


# ==========>> MODULE IMPORT <<========== #


import base64
import hashlib
import logging
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import font
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from win10toast import ToastNotifier
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class App:
    """Used to initialize the main chatting application"""

    def __init__(self, root):
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
        root.configure(bg="#282424")
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # initialize
        font_1 = font.Font(family="Helvetica", size=15)
        font_2 = font.Font(family="Calibri", size=15)

        self.msg_entry_var = StringVar()
        self.msg_scrollbar = Scrollbar(
            root,
            activebackground="#282424",
            bg="#282424",
            highlightbackground="#282424",
            highlightcolor="#282424",
            troughcolor="#282424",
        )
        self.msg_entry = Entry(
            root,
            textvariable=self.msg_entry_var,
            borderwidth="1px",
            bg="#282424",
            font=font_1,
            fg="#ffffff",
            justify="left",
            relief="sunken",
        )
        self.msg_list = Text(
            root,
            yscrollcommand=self.msg_scrollbar.set,
            bg="#282424",
            borderwidth="1px",
            font=font_1,
            fg="#ffffff",
        )
        self.people_scrollbar = Scrollbar(
            activebackground="#282424",
            bg="#282424",
            highlightbackground="#282424",
            highlightcolor="#282424",
            troughcolor="#282424",
        )
        self.people_list = Listbox(
            root,
            yscrollcommand=self.people_scrollbar.set,
            selectmode=SINGLE,
            font=font.Font(size=20),
            justify="center",
            bg="#282424",
            borderwidth="1px",
            fg="#ffffff",
        )
        self.msg_send_button = Button(
            root,
            text="Enviar",
            command=self.msg_send,
            bg="#282424",
            font=font.Font(family="Helvetica", size=10),
            fg="#ffffff",
            justify="center",
        )
        self.login_root = Frame(root)
        self.user_entry_var = StringVar()
        self.key_entry_var = StringVar()
        self.user_entry = Entry(
            self.login_root,
            width="30",
            font=font_2,
            textvariable=self.user_entry_var,
        )
        self.key_entry = Entry(
            self.login_root,
            width="30",
            font=font_2,
            textvariable=self.key_entry_var,
            show="*",
        )
        self.Error_label = Label(self.login_root, text="\n", font=font_2, width="300")

        # config
        self.msg_entry_var.set("")
        self.msg_scrollbar.config(command=self.msg_list.yview)
        self.msg_list.tag_config("right", justify="right")
        self.people_scrollbar.config(command=self.people_list.yview)
        self.user_entry.focus_set()

        # binds
        self.msg_entry.bind("<Return>", self.msg_send)
        self.people_list.bind("<<ListboxSelect>>", self.select_person)
        self.user_entry.bind(
            "<Return>",
            lambda event: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        )
        self.key_entry.bind(
            "<Return>",
            lambda event: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
        )
        root.bind("<FocusOut>", self.focus_out)
        root.bind("<FocusIn>", self.focus_in)

        # place and pack
        self.msg_scrollbar.place(x=1220, y=10, width=20, height=640)
        self.people_list.place(x=10, y=10, width=330, height=680)
        self.people_scrollbar.place(x=350, y=10, width=20, height=680)
        self.msg_send_button.place(x=1190, y=660, width=50, height=30)
        Label(self.login_root, text="\n\n\n\n\n\n\n\n").pack()
        Label(self.login_root, text="Introduzca el nombre de usuario y la contraseña\n", font=font_2).pack()
        Label(self.login_root, text="Nombre de usuario *", font=font_2).pack()
        self.user_entry.pack()
        Label(self.login_root, text="Contraseña *", font=font_2).pack()
        self.key_entry.pack()
        Label(self.login_root, text="").pack()
        Button(
            self.login_root,
            text="Login",
            width="20",
            bg="DarkGrey",
            command=lambda: self.login(self.user_entry_var.get(), self.key_entry_var.get()),
            font=font_2,
        ).pack()
        Label(self.login_root, text="").pack()
        Button(
            self.login_root,
            text="Register",
            width="20",
            bg="DarkGrey",
            command=lambda: self.register(self.user_entry_var.get(), self.key_entry_var.get()),
            font=font_2,
        ).pack()
        self.Error_label.pack()
        self.login_root.pack(side=LEFT, fill=BOTH)

        # other
        logger.setLevel(LOGGING_LEVEL)
        logging.basicConfig(format="[%(levelname)s] > %(message)s")

        connect = Thread(target=self.connect)
        connect.start()

    def connect(self):
        self.must_close = False
        while True:
            try:
                ADDR = (HOST, PORT)
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.connect(ADDR)
                receive_thread = Thread(target=self.receive)
                receive_thread.start()
                logger.info(f"Connected succesfully")
                break
            except (ConnectionRefusedError, OSError):
                for i in reversed(range(5)):
                    logger.debug(f"Trying to connect: {i+1} seconds remaining")
                    sleep(1)
                    if self.must_close:
                        break
            finally:
                if self.must_close:
                    break

    def receive(self):
        while True:
            try:
                dictionary = eval(self.socket.recv(BUFSIZ).decode("utf8"))
                logger.debug(f"Received: {dictionary}")
                if dictionary["type"] == "command":
                    if dictionary["command"] == "login":
                        root.title(f"Chatt app - Logged as {self.username}")
                        self.login_root.destroy()
                        self.users.remove(self.username)
                        for i in self.users:
                            if i != self.username:
                                self.people_list.insert(END, i)
                        self.msg_entry.focus_set()
                    elif dictionary["command"] == "history":
                        self.history = dictionary["history"]
                        if self.history:
                            self.history = eval(self.history)
                            self.onAdd("1.0", self.history, True)
                    elif dictionary["command"] == "login_user_error":
                        self.login_error(2)
                    elif dictionary["command"] == "login_password_error":
                        self.login_error(3)
                    elif dictionary["command"] == "register":
                        self.login(self.user_entry_var.get(), self.key_entry_var.get())
                    elif dictionary["command"] == "register_error":
                        self.login_error(4)
                    # elif dictionary["command"] == "quit":
                    #     self.socket.close()
                    #     root.quit()
                    elif dictionary["command"] == "userlist":
                        self.users = []
                        for i in eval(dictionary["users"]):
                            i = self.decrypt(i)
                            self.users.append(i)
                    elif dictionary["command"] == "usersel":
                        dictionary["msg_list"] = self.decrypt(str(dictionary["msg_list"]))
                        logger.debug(i)
                        self.onAdd("1.0", eval(dictionary["msg_list"]), True)
                if dictionary["type"] == "broadcast":
                    self.onAdd(END, dictionary)
                    self.notification()
            except OSError as e:
                if self.must_close:
                    break
                logger.error(e)
                self.socket.close()
                connect = Thread(target=self.connect)
                connect.start()
                break
            if self.must_close:
                break

    def select_person(self, *args):
        self.msg_entry.place(x=380, y=660, width=800, height=30)
        self.msg_list.place(x=380, y=10, width=830, height=640)
        self.person_selected = self.people_list.curselection()[0]
        self.msg_list.configure(state="normal")
        self.msg_list.delete("1.0", END)
        self.msg_list.configure(state="disabled")
        self.command_send("usersel", self.users[self.person_selected])

    def on_closing(self, *args):
        root.quit()
        self.must_close = True
        self.socket.close()

    def msg_send(self, *args):
        msg = self.msg_entry_var.get()
        self.msg_entry_var.set("")
        if msg:
            dictionary = {
                "date": datetime.now().strftime("%H:%M"),
                "name": self.username,
                "type": "broadcast",
                "msg": msg,
                "destinatary": self.users[self.person_selected],
            }
            self.onAdd(END, dictionary, True, True)

            dictionary["date"] = self.encrypt(dictionary["date"])
            dictionary["name"] = self.encrypt(dictionary["name"])
            dictionary["msg"] = self.encrypt(dictionary["msg"])
            dictionary["destinatary"] = self.encrypt(dictionary["destinatary"])

            try:
                self.socket.send(str(dictionary).encode("utf8"))
                logger.debug(f"Sent: {dictionary}")
            except OSError as e:
                logger.error(e)

    def command_send(self, command: str, arg1: str = "", arg2: str = ""):
        if command == "usersel":
            dictionary = {
                "date": datetime.now().strftime("%H:%M"),
                "name": self.username,
                "type": "command",
                "command": command,
                "destinatary": arg1,
            }
            dictionary["destinatary"] = self.encrypt(dictionary["destinatary"])
        else:
            dictionary = {
                "date": datetime.now().strftime("%H:%M"),
                "name": self.username,
                "type": "command",
                "command": command,
                "user": arg1,
                "key": arg2,
            }
            dictionary["user"] = self.encrypt(dictionary["user"])
            dictionary["key"] = self.encrypt(dictionary["key"])

        dictionary["date"] = self.encrypt(dictionary["date"])
        dictionary["name"] = self.encrypt(dictionary["name"])

        self.socket.send(str(dictionary).encode("utf8"))
        logger.debug(f"Sent: {dictionary}")

    def onAdd(self, pos: str, dictionary: dict, self_msg: bool = False, local: bool = False):
        self.msg_list.configure(state="normal")
        if not local:
            dictionary["name"] = self.decrypt(dictionary["name"])
            dictionary["msg"] = self.decrypt(dictionary["msg"])
            dictionary["date"] = self.decrypt(dictionary["date"])
            logger.info(dictionary)

            self.last_name = dictionary["name"]
            self.last_message = dictionary["msg"]

        if dictionary["name"] == self.username:
            if self_msg:
                self.msg_list.insert(
                    pos,
                    f'{dictionary["name"]}: {dictionary["msg"]} ({dictionary["date"]})\n\n',
                    "right",
                )
        else:
            self.msg_list.insert(pos, f'({dictionary["date"]}) {dictionary["name"]}: {dictionary["msg"]}\n\n')
        self.msg_list.configure(state="disabled")
        self.msg_list.yview(END)

    def login(self, user: str, key: str, *args):
        self.username = user
        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not (user and key):
            self.login_error(0)
        else:
            self.command_send("login", user, key)

    def register(self, user: str, key: str):
        self.username = user
        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not (user and key):
            self.login_error(0)
        else:
            self.command_send("register", user, key)

    def login_error(self, x: int):
        if x == 0:
            self.Error_label.config(text="\nEl usuario y/o la contraseña no pueden estar en blanco.")
            logger.debug("login_blank_error")
        elif x == 1:
            self.Error_label.config(text="\nEl usuario y la contraseña deben ser inferiores a 20 carácteres.")
            logger.debug("login_length_error")
        elif x == 2:
            self.Error_label.config(text="\nUsuario no encontrado.")
            logger.debug("login_user_error")
        elif x == 3:
            self.Error_label.config(text="\nContraseña incorrecta.")
            logger.debug("login_password_error")
        elif x == 4:
            self.Error_label.config(text="\nEste nombre de usuario y/o contraseña no están disponibles")
            logger.debug("register_error")

    def encrypt(self, strg: str) -> str:
        """Returns an AES-Base 64 encrypted version of the input.

        Args:
            str (str): String to be encrypted.

        Returns:
            str: Encrypted version of the string.
        """
        strg = str(strg)
        if str:
            str2 = pad(strg.encode(), 16)
            cipher = AES.new(KEY, AES.MODE_ECB)
            return base64.b64encode(cipher.encrypt(str2)).decode("utf-8", "ignore")
        else:
            return ""

    def decrypt(self, strg: str) -> str:
        """Returns an AES-Base 64 decrypted version of the encrypted input.

        Args:
            str (str): Encrypted string to be decrypted.

        Returns:
            str: Decrypted version of the encrypted string.
        """
        strg = str(strg)
        if strg:
            str2 = base64.b64decode(strg)
            cipher = AES.new(KEY, AES.MODE_ECB)
            try:
                return unpad(cipher.decrypt(str2), 16).decode("utf-8", "ignore")
            except ValueError:
                return strg
        else:
            return ""

    def focus_out(self, *args):
        self.focus = False

    def focus_in(self, *args):
        self.focus = True

    def notification(self):
        if NOTIFICATIONS:
            if not self.focus:
                notification.show_toast(
                    "Chat app",
                    f"{self.last_name}: {self.last_message}",
                    duration=5,
                    threaded=True,
                )


# ==========>> MAIN CODE <<========== #


LOGGING_LEVEL = logging.DEBUG
NOTIFICATIONS = True
KEY = "1234"
HOST = "127.0.0.1"
PORT = 33000


if __name__ == "__main__":
    logger = logging.getLogger()
    notification = ToastNotifier()
    root = Tk()
    app = App(root)

    BUFSIZ = 1024
    KEY = hashlib.sha256(KEY.encode()).digest()

    root.mainloop()
