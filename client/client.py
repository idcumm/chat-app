# # # # TODO fer que el chat tingui missatges privats
# # # # TODO simular un atac informatic al servidor
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# TODO posar dia i hora en missatges
# TODO que no surti la consola al obrir client.pyw
# TODO millorar el print de la consola
# TODO Quan la aplicció no tingui focus i revi un misatge, faigi ping i ficar l'icono tronja
# TODO Que detecti el nom del ultim misatge i si es el mateix que no escrigui el nom.
# TODO fer funcio tot allo que es repeteix molt
# TODO millorar notification
# TODO en comptes que els errors s'eliminin i es crein, que nomes es cambii el text i ya
# TODO fer separacio de misatges per persona (2 misatges duna persona seguits, sense doble espai, i altres ab doble espai)
# -=-=-=- devesaguillem@gmail.com se ha unido! -=-=-=-

#                                              - - - - devesaguillem@gmail.com - - - -
#                                              (00:00) Hola chicos!
#                                              (00:00) Como estan? Espero que Muy Bien
#
# - - - - devesapere@gmail.com - - - -
# (00:01) Mal
#
#                                              - - - - devesaguillem@gmail.com - - - -
#                                              (00:02) Por?
#
# ==========>> MODULE IMPORT <<========== #


import tkinter.font as tkFont
import base64
import hashlib
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from os import popen
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from win10toast import ToastNotifier


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class App:
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
        self.msg_entry["font"] = tkFont.Font(family="Sitka Small", size=15)
        self.msg_entry["fg"] = "#ffffff"
        self.msg_entry["justify"] = "left"
        self.msg_entry["relief"] = "sunken"
        self.msg_entry.place(x=380, y=660, width=800, height=30)

        self.msg_list = Text(root, yscrollcommand=self.msg_scrollbar.set)
        self.msg_scrollbar.config(command=self.msg_list.yview)
        self.msg_list["bg"] = "#282424"
        self.msg_list["borderwidth"] = "1px"
        self.msg_list["font"] = tkFont.Font(family="Sitka Small", size=15)
        self.msg_list["fg"] = "#ffffff"
        self.msg_list.place(x=380, y=10, width=830, height=640)
        self.msg_list.tag_config("right", justify="right")
        self.msg_list.tag_config("center", justify="center")

        # msg_send_button
        self.msg_send_button = Button(root, text="Enviar", command=self.msg_send)
        self.msg_send_button["anchor"] = "se"
        self.msg_send_button["bg"] = "#282424"
        self.msg_send_button["font"] = tkFont.Font(family="Sitka Small", size=10)
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

    def receive(self):
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                if "/login" == msg:
                    root.title(f"Chatt app - Logged as {self.username}")
                    self.login_root.destroy()
                    self.msg_entry.focus_set()
                elif "/history" in msg:
                    self.history = msg[9:]
                    if not self.history == [""]:
                        self.history = eval(self.history)
                        self.onAdd("1.0", self.history, True)
                elif "/login_user_error" == msg:
                    self.login_error(2)
                elif "/login_password_error" == msg:
                    self.login_error(3)
                elif "/register" == msg:
                    self.login(self.user_entry_var.get(), self.key_entry_var.get())
                elif "/register_error" == msg:
                    self.login_error(4)
                elif "/quit" == msg:
                    client_socket.close()
                    root.quit()
                else:
                    msg = eval(msg)
                    self.onAdd(END, msg)
                    self.notification()

            except OSError:
                print(OSError)
                client_socket.close()
                root.quit()
                exit()

    def msg_send(self, event=None):
        msg = self.msg_entry_var.get()
        if not msg == "":
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

    def onAdd(self, position, x, self_messages=False, local=False):
        self.msg_list.configure(state="normal")
        if local == False:
            x["name"] = self.decrypt(x["name"])
            x["msg"] = self.decrypt(x["msg"])

            self.last_name = x["name"]
            self.last_message = x["msg"]

        if x["type"] == "broadcast":
            if x["name"] == self.username:
                if self_messages == True:
                    self.msg_list.insert(
                        position,
                        f'{x["name"]}: {x["msg"]} ({x["date"]})\n\n',
                        "right",
                    )
            else:
                self.msg_list.insert(
                    position, f'({x["date"]}) {x["name"]}: {x["msg"]}\n\n'
                )
        # elif x["type"] == "join":
        #     self.msg_list.insert(
        #         position, f'{x["name"]} se ha unido al chat!\n\n', "center")
        # elif x["type"] == "leave":
        #     self.msg_list.insert(
        #         position, f'{x["name"]} se ha ido del chat!\n\n', "center")
        self.msg_list.configure(state="disabled")
        self.msg_list.yview(END)

    def login(self, user, key, event=None):
        self.username = user
        if len(user) > 20 or len(key) > 20:
            self.login_error(1)
        elif len(user) == 0 or len(key) == 0:
            self.login_error(0)
        else:
            user = self.encrypt(user)
            key = self.encrypt(key)
            msg = f'"{user}", "{key}"'
            self.command_send(f"/login {msg}")

    def register(self, user, key, event=None):
        if len(user) > 20 or len(key) > 20:
            self.login_error(1)
        elif len(user) == 0 or len(key) == 0:
            self.login_error(0)
        else:
            user = self.encrypt(user)
            key = self.encrypt(key)
            msg = f'"{user}", "{key}"'
            self.command_send(f"/register {msg}")

    def login_error(self, x):
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

    def command_send(self, msg, event=None):
        client_socket.send(msg.encode("utf8"))

    def on_closing(self, event=None):
        self.command_send("/quit")
        exit()

    def encrypt(self, raw):
        if not raw == "":
            raw = pad(raw.encode(), 16)
            cipher = AES.new(KEY, AES.MODE_ECB)
            return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")
        else:
            return ""

    def decrypt(self, enc):
        if not enc == "":
            enc = base64.b64decode(enc)
            cipher = AES.new(KEY, AES.MODE_ECB)
            return unpad(cipher.decrypt(enc), 16).decode("utf-8", "ignore")
        else:
            return ""

    def focus_out(self, event=None):
        self.focus = False

    def focus_in(self, event=None):
        self.focus = True

    def notification(self):
        if NOTIFICATIONS == True:
            if self.focus == False:
                n.show_toast(
                    "Chat app",
                    f"{self.last_name}: {self.last_message}",
                    duration=5,
                    threaded=True,
                )


# ==========>> MAIN CODE <<========== #


if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    n = ToastNotifier()
    HOST = "127.0.0.1"  # "127.0.0.1"
    PORT = 33000
    ADDR = (HOST, PORT)
    BUFSIZ = 1024

    NOTIFICATIONS = True
    KEY = "pswrd"
    KEY = hashlib.sha256(KEY.encode()).digest()

    popen("title ClientSocket")

    client_socket.connect(ADDR)

    root = Tk()
    app = App(root)
    receive_thread = Thread(target=app.receive)
    receive_thread.start()
    root.mainloop()
