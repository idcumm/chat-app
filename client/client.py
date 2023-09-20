# # # # TODO fer que el chat tingui missatges privats
# # # # TODO simular un atac informatic al servidor
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# bubbl.us
# TODO posar dia i hora en missatges
# TODO que no surti la consola al obrir client.pyw
# TODO millorar el print de la consola
# TODO Quan la aplicció no tingui focus i revi un misatge, faigi ping i ficar l'icono tronja
# TODO fer funcio tot allo que es repeteix molt
# TODO millorar notification
# TODO fer separacio de misatges per persona (nom a dalt, 2 misatges duna persona seguits, sense doble espai, i altres ab doble espai)
# ==========>> MODULE IMPORT <<========== #


import base64
import hashlib
import logging
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import font
from os import popen
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from win10toast import ToastNotifier
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class App:
    """Used to initialize the main chatting application"""

    def __init__(self, root):
        # window
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
        root.bind("<FocusOut>", self.focus_out)
        root.bind("<FocusIn>", self.focus_in)

        # msg_entry_var
        self.msg_entry_var = StringVar()
        self.msg_entry_var.set("")

        # msg_scrollbar
        self.msg_scrollbar = Scrollbar(
            root,
            activebackground="#282424",
            bg="#282424",
            highlightbackground="#282424",
            highlightcolor="#282424",
            troughcolor="#282424",
        )
        self.msg_scrollbar.place(x=1220, y=10, width=20, height=640)

        # msg_entry
        self.msg_entry = Entry(root, textvariable=self.msg_entry_var)
        self.msg_entry.bind("<Return>", self.msg_send)
        self.msg_entry.focus_set()
        self.msg_entry["borderwidth"] = "1px"
        self.msg_entry["bg"] = "#282424"
        self.msg_entry["font"] = font.Font(family="Sitka Small", size=15)
        self.msg_entry["fg"] = "#ffffff"
        self.msg_entry["justify"] = "left"
        self.msg_entry["relief"] = "sunken"
        self.msg_entry.place(x=380, y=660, width=800, height=30)

        # msg_list
        self.msg_list = Text(
            root,
            yscrollcommand=self.msg_scrollbar.set,
            bg="#282424",
            borderwidth="1px",
            font=font.Font(family="Sitka Small", size=15),
            fg="#ffffff",
        )
        self.msg_scrollbar.config(command=self.msg_list.yview)
        self.msg_list.place(x=380, y=10, width=830, height=640)
        self.msg_list.tag_config("right", justify="right")
        self.msg_list.tag_config("center", justify="center")

        # people_list
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
            justify=CENTER,
            bg="#282424",
            borderwidth="1px",
            fg="#ffffff",
        )
        self.people_list.bind("<<ListboxSelect>>", self.select_person)
        self.people_scrollbar.config(command=self.people_list.yview)
        self.people_list.place(x=10, y=10, width=330, height=680)
        self.people_scrollbar.place(x=350, y=10, width=20, height=680)

        # msg_send_button
        self.msg_send_button = Button(root, text="Enviar", command=self.msg_send)
        self.msg_send_button["anchor"] = "se"
        self.msg_send_button["bg"] = "#282424"
        self.msg_send_button["font"] = font.Font(family="Sitka Small", size=10)
        self.msg_send_button["fg"] = "#ffffff"
        self.msg_send_button["justify"] = "center"
        self.msg_send_button.place(x=1190, y=660, width=50, height=30)

        self.login_root = Frame(root)
        self.user_entry_var = StringVar()
        self.key_entry_var = StringVar()

        Label(
            self.login_root,
            text="\n\n\n\n\n\n\n\n",
            width="300",
        ).pack()

        Label(
            self.login_root,
            text="Introduzca el nombre de usuario y la contraseña\n",
            font=("Calibri", 13),
        ).pack()

        Label(self.login_root, text="Nombre de usuario *", font=("Calibri", 13)).pack()

        self.user_entry = Entry(
            self.login_root,
            width="30",
            font=("Calibri", 13),
            textvariable=self.user_entry_var,
        )
        self.user_entry.focus_set()
        self.user_entry.bind(
            "<Return>",
            lambda event: self.login(
                self.user_entry_var.get(), self.key_entry_var.get()
            ),
        )
        self.user_entry.pack()

        Label(self.login_root, text="Contraseña *", font=("Calibri", 13)).pack()

        self.key_entry = Entry(
            self.login_root,
            width="30",
            font=("Calibri", 13),
            textvariable=self.key_entry_var,
            show="*",
        )
        self.key_entry.bind(
            "<Return>",
            lambda event: self.login(
                self.user_entry_var.get(), self.key_entry_var.get()
            ),
        )
        self.key_entry.pack()

        Label(self.login_root, text="").pack()

        Button(
            self.login_root,
            text="Login",
            width="20",
            bg="DarkGrey",
            command=lambda: self.login(
                self.user_entry_var.get(), self.key_entry_var.get()
            ),
            font=("Calibri", 13),
        ).pack()

        Label(self.login_root, text="").pack()

        Button(
            self.login_root,
            text="Register",
            width="20",
            bg="DarkGrey",
            command=lambda: self.register(
                self.user_entry_var.get(), self.key_entry_var.get()
            ),
            font=("Calibri", 13),
        ).pack()

        self.Error_label = Label(
            self.login_root,
            text="\n",
            font=("Calibri", 13),
        )
        self.Error_label.pack()

        self.login_root.pack(side=LEFT, fill=BOTH)

    def connect(self):
        while True:
            try:
                ADDR = (HOST, PORT)
                client_socket.connect(ADDR)
                receive_thread.start()
                break
            except ConnectionRefusedError:
                for i in reversed(range(5)):
                    logger.debug(f"Trying to connect: {i+1} seconds remaining")
                    sleep(1)

    def select_person(self, *args):
        pass

    def receive(self):
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                if msg == "/login":
                    root.title(f"Chatt app - Logged as {self.username}")
                    self.login_root.destroy()
                    self.msg_entry.focus_set()
                elif msg[:8] == "/history":
                    self.history = msg[9:]
                    if self.history:
                        self.history = eval(self.history)
                        self.onAdd("1.0", self.history, True)
                elif msg == "/login_user_error":
                    self.login_error(2)
                elif msg == "/login_password_error":
                    self.login_error(3)
                elif msg == "/register":
                    self.login(self.user_entry_var.get(), self.key_entry_var.get())
                elif msg == "/register_error":
                    self.login_error(4)
                elif msg == "/quit":
                    client_socket.close()
                    root.quit()
                else:
                    dict = eval(msg)
                    self.onAdd(END, dict)
                    self.notification()

            except OSError:
                print(OSError)
                client_socket.close()
                root.quit()
                exit()

    def on_closing(self, *args):
        root.quit()
        client_socket.close()

    def msg_send(self, *args):
        msg = self.msg_entry_var.get()
        if msg:
            self.msg_entry_var.set("")
            date = datetime.now().strftime("%H:%M")
            dict = {
                "date": date,
                "type": "broadcast",
                "name": self.username,
                "msg": msg,
            }
            self.onAdd(END, dict, True, True)
            msg = self.encrypt(msg)
            try:
                client_socket.send(msg.encode("utf8"))
            except OSError:
                print(OSError)

    def command_send(self, msg: str):
        client_socket.send(msg.encode("utf8"))

    def onAdd(self, pos: str, x: dict, self_msg: bool = False, local: bool = False):
        self.msg_list.configure(state="normal")
        if not local:
            x["name"] = self.decrypt(x["name"])
            x["msg"] = self.decrypt(x["msg"])

            self.last_name = x["name"]
            self.last_message = x["msg"]

        if x["type"] == "broadcast":
            if x["name"] == self.username:
                if self_msg:
                    self.msg_list.insert(
                        pos,
                        f'{x["name"]}: {x["msg"]} ({x["date"]})\n\n',
                        "right",
                    )
            else:
                self.msg_list.insert(pos, f'({x["date"]}) {x["name"]}: {x["msg"]}\n\n')
        # elif x["type"] == "join":
        #     self.msg_list.insert(
        #         pos, f'{x["name"]} se ha unido al chat!\n\n', "center")
        # elif x["type"] == "leave":
        #     self.msg_list.insert(
        #         pos, f'{x["name"]} se ha ido del chat!\n\n', "center")
        self.msg_list.configure(state="disabled")
        self.msg_list.yview(END)

    def login(self, user: str, key: str, *args):
        self.username = user
        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not user or not key:
            self.login_error(0)
        else:
            user = self.encrypt(user)
            key = self.encrypt(key)
            msg = f'"{user}", "{key}"'
            self.command_send(f"/login {msg}")

    def register(self, user: str, key: str):
        if (len(user) or len(key)) > 20:
            self.login_error(1)
        elif not user or not key:
            self.login_error(0)
        else:
            user = self.encrypt(user)
            key = self.encrypt(key)
            msg = f'"{user}", "{key}"'
            self.command_send(f"/register {msg}")

    def login_error(self, x: int):
        if x == 0:
            self.Error_label.config(
                text="\nEl usuario y/o la contraseña no pueden estar en blanco."
            )
        elif x == 1:
            self.Error_label.config(
                text="\nEl usuario y la contraseña deben ser inferiores a 20 carácteres."
            )
        elif x == 2:
            self.Error_label.config(text="\nUsuario no encontrado.")
        elif x == 3:
            self.Error_label.config(text="\nContraseña incorrecta.")
        elif x == 4:
            self.Error_label.config(
                text="\nEste nombre de usuario y/o contraseña no están disponibles"
            )

    def encrypt(self, str: str) -> str:
        """Returns an AES-Base 64 encrypted version of the input.

        Args:
            str (str): String to be encrypted.

        Returns:
            str: Encrypted version of the string.
        """
        if str:
            str = pad(str.encode(), 16)
            cipher = AES.new(KEY, AES.MODE_ECB)
            return base64.b64encode(cipher.encrypt(str)).decode("utf-8", "ignore")
        else:
            return ""

    def decrypt(self, str: str) -> str:
        """Returns an AES-Base 64 decrypted version of the encrypted input.

        Args:
            str (str): Encrypted string to be decrypted.

        Returns:
            str: Decrypted version of the encrypted string.
        """
        if str:
            str = base64.b64decode(str)
            cipher = AES.new(KEY, AES.MODE_ECB)
            return unpad(cipher.decrypt(str), 16).decode("utf-8", "ignore")
        else:
            return ""

    def focus_out(self, *args):
        self.focus = False

    def focus_in(self, *args):
        self.focus = True

    def notification(self):
        if NOTIFICATIONS:
            if not self.focus:
                n.show_toast(
                    "Chat app",
                    f"{self.last_name}: {self.last_message}",
                    duration=5,
                    threaded=True,
                )


# ==========>> MAIN CODE <<========== #


LOGGING_LEVEL = logging.DEBUG
NOTIFICATIONS = True
KEY = "pswrd"
HOST = "127.0.0.1"
PORT = 33000


if __name__ == "__main__":
    logger = logging.getLogger()
    client_socket = socket(AF_INET, SOCK_STREAM)
    n = ToastNotifier()
    root = Tk()
    app = App(root)
    receive_thread = Thread(target=app.receive)
    connect = Thread(target=app.connect)

    BUFSIZ = 1024
    KEY = hashlib.sha256(KEY.encode()).digest()

    logger.setLevel(LOGGING_LEVEL)
    popen("title ClientSocket")
    logging.basicConfig(format="[%(levelname)s] > %(message)s")
    connect.start()
    root.mainloop()
