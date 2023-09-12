# # # # TODO fer que el chat tingui missatges privats
# # # # TODO simular un atac informatic al servidor
# TODO treure "tots" els globals i posar self.
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# TODO fer tot en un sol idioma
# TODO posar dia i hora en missatges
# TODO que no surti la consola al obrir client.pyw
# TODO millorar el print de la consola
# TODO Quan la aplicció no tingui focus i revi un misatge, faigi ping i ficar l'icono tronja
# TODO Que detecti el nom del ultim misatge i si es el mateix que no escrigui el nom.
# TODO fer funcio tot allo que es repeteix molt
# TODO millorar notification
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
        global my_msg
        global msg_list
        global scrollbar
        global entry_field
        global send_button
        global top_login
        global verifica_usuario
        global verifica_clave

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
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.bind('<FocusOut>', focus_out)
        root.bind('<FocusIn>', focus_in)

        # my_msg
        my_msg = StringVar()
        my_msg.set("")

        # scrollbar
        scrollbar = Scrollbar(
            root,
            activebackground="#282424",
            bg="#282424",
            highlightbackground="#282424",
            highlightcolor="#282424",
            troughcolor="#282424",
        )
        scrollbar.place(x=1220, y=10, width=20, height=640)

        # entry_field
        entry_field = Entry(root, textvariable=my_msg)
        entry_field.bind("<Return>", msg_send)
        entry_field.focus_set()
        entry_field["borderwidth"] = "1px"
        entry_field["bg"] = "#282424"
        entry_field["font"] = tkFont.Font(family="Times", size=15)
        entry_field["fg"] = "#ffffff"
        entry_field["justify"] = "left"
        entry_field["relief"] = "sunken"
        entry_field.place(x=380, y=660, width=800, height=30)

        msg_list = Text(root, yscrollcommand=scrollbar.set)
        scrollbar.config(command=msg_list.yview)
        msg_list["bg"] = "#282424"
        msg_list["borderwidth"] = "1px"
        msg_list["font"] = tkFont.Font(family="Times", size=15)
        msg_list["fg"] = "#ffffff"
        msg_list.place(x=380, y=10, width=830, height=640)
        msg_list.tag_config("right", justify="right")
        msg_list.tag_config("center", justify="center")

        # send_button
        send_button = Button(root, text="Enviar", command=msg_send)
        send_button["anchor"] = "se"
        send_button["bg"] = "#282424"
        send_button["font"] = tkFont.Font(family="Times", size=10)
        send_button["fg"] = "#ffffff"
        send_button["justify"] = "center"
        send_button.place(x=1190, y=660, width=50, height=30)

        top_login = Frame(root)
        verifica_usuario = StringVar()
        verifica_clave = StringVar()

        Label(
            top_login,
            text="\n\n\n\n\n\n\n\n",
            width="300",
        ).pack()

        Label(
            top_login,
            text="Introduzca el nombre de usuario y la contraseña\n",
            font=("Calibri", 13),
        ).pack()

        Label(top_login, text="Nombre de usuario *",
              font=("Calibri", 13)).pack()

        entry_usuario = Entry(
            top_login,
            width="30",
            font=("Calibri", 13),
            textvariable=verifica_usuario,
        )
        entry_usuario.focus_set()
        entry_usuario.bind(
            "<Return>",
            lambda event: login(verifica_usuario.get(), verifica_clave.get()),
        )
        entry_usuario.pack()

        Label(top_login, text="Contraseña *", font=("Calibri", 13)).pack()

        entry_contrasena = Entry(
            top_login,
            width="30",
            font=("Calibri", 13),
            textvariable=verifica_clave,
            show="*",
        )
        entry_contrasena.bind(
            "<Return>",
            lambda event: login(verifica_usuario.get(), verifica_clave.get()),
        )
        entry_contrasena.pack()

        Label(top_login, text="").pack()

        Button(
            top_login,
            text="Login",
            width="20",
            bg="DarkGrey",
            command=lambda: login(verifica_usuario.get(),
                                  verifica_clave.get()),
            font=("Calibri", 13),
        ).pack()

        Label(top_login, text="").pack()

        Button(
            top_login,
            text="Register",
            width="20",
            bg="DarkGrey",
            command=lambda: register(
                verifica_usuario.get(), verifica_clave.get()),
            font=("Calibri", 13),
        ).pack()

        top_login.pack(side=LEFT, fill=BOTH)


def login(usuario, clave, event=None):
    global username
    username = usuario
    if len(usuario) > 20 or len(clave) > 20:
        login_lenght_error()
    else:
        usuario = encrypt(usuario)
        clave = encrypt(clave)
        msg = f'"{usuario}", "{clave}"'
        command_send(f"/login {msg}")


def register(usuario, clave, event=None):
    if len(usuario) > 20 or len(clave) > 20:
        login_lenght_error()
    else:
        usuario = encrypt(usuario)
        clave = encrypt(clave)
        msg = f'"{usuario}", "{clave}"'
        command_send(f"/register {msg}")


def login_lenght_error():
    global top_login
    global Error
    try:
        Error.destroy()
    except NameError:
        print(NameError)
    Error = Label(
        top_login,
        text="\nEl usuario y la contraseña deben ser inferiores a 20 carácteres.",
        font=("Calibri", 13),
    )
    Error.pack()


def login_user_error():
    global top_login
    global Error
    try:
        Error.destroy()
    except NameError:
        print(NameError)
    Error = Label(
        top_login,
        text="\nUsuario no encontrado.",
        font=("Calibri", 13),
    )
    Error.pack()


def login_password_error():
    global top_login
    global Error
    try:
        Error.destroy()
    except NameError:
        print(NameError)
    Error = Label(
        top_login,
        text="\nContraseña incorrecta.",
        font=("Calibri", 13),
    )
    Error.pack()


def register_error():
    global top_login
    global Error
    try:
        Error.destroy()
    except NameError:
        print(NameError)
    Error = Label(
        top_login,
        text="\nEste nombre de usuario y/o contraseña no están disponibles",
        font=("Calibri", 13),
    )
    Error.pack()


def onAdd(position, x, self_messages=False, local=False):
    global last_name
    global last_message
    msg_list.configure(state="normal")
    if local == False:
        x['name'] = decrypt(x['name'])
        x['msg'] = decrypt(x['msg'])

        last_name = x['name']
        last_message = x['msg']

    if x["type"] == "broadcast":
        if x["name"] == username:
            if self_messages == True:
                msg_list.insert(
                    position,
                    f'{x["name"]}: {x["msg"]} ({x["date"]})\n\n',
                    "right",
                )
        else:
            msg_list.insert(
                position, f'({x["date"]}) {x["name"]}: {x["msg"]}\n\n')
    elif x["type"] == "join":
        msg_list.insert(
            position, f'{x["name"]} se ha unido al chat!\n\n', "center")
    elif x["type"] == "leave":
        msg_list.insert(
            position, f'{x["name"]} se ha ido del chat!\n\n', "center")
    msg_list.configure(state="disabled")
    msg_list.yview(END)


def receive():
    global history
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if "/login" == msg:
                root.title(f"Chatt app - Logged as {username}")
                top_login.destroy()
                entry_field.focus_set()
            elif "/history" in msg:
                history = msg[9:]
                if not history == [""]:
                    history = eval(history)
                    onAdd('1.0', history, True)
            elif "/login_user_error" == msg:
                login_user_error()
            elif "/login_password_error" == msg:
                login_password_error()
            elif "/register" == msg:
                login(verifica_usuario.get(), verifica_clave.get())
            elif "/register_error" == msg:
                register_error()
            elif "/quit" == msg:
                client_socket.close()
                root.quit()
            else:
                msg = eval(msg)
                onAdd(END, msg)
                notification()

        except OSError:
            print(OSError)
            client_socket.close()
            root.quit()
            exit()


def msg_send(event=None):
    msg = my_msg.get()
    if not msg == "":
        my_msg.set("")
        date = datetime.now().strftime("%H:%M")
        msg_ = {"date": date, "type": "broadcast", "name": username, "msg": msg}
        onAdd(END, msg_, True, True)
        msg = encrypt(msg)
        try:
            client_socket.send(msg.encode("utf8"))
        except OSError:
            print(OSError)


def command_send(msg, event=None):
    client_socket.send(msg.encode("utf8"))


def on_closing(event=None):
    command_send("/quit")
    exit()


def encrypt(raw):
    if not raw == "":
        raw = pad(raw.encode(), 16)
        cipher = AES.new(KEY, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")
    else:
        return ""


def decrypt(enc):
    if not enc == "":
        enc = base64.b64decode(enc)
        cipher = AES.new(KEY, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc), 16).decode("utf-8", "ignore")
    else:
        return ""


def focus_out(*args):
    global focus
    focus = False


def focus_in(*args):
    global focus
    focus = True


def notification():
    global focus
    if NOTIFICATIONS == True:
        if focus == False:
            n.show_toast("Chat app",
                         f"{last_name}: {last_message}",
                         duration=5,
                         threaded=True)

# ==========>> MAIN CODE <<========== #


if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    n = ToastNotifier()
    HOST = "127.0.0.1"  # "127.0.0.1"
    PORT = 33000
    ADDR = (HOST, PORT)
    BUFSIZ = 1024

    NOTIFICATIONS = True
    KEY = 'password'
    KEY = hashlib.sha256(KEY.encode()).digest()

    popen("title ClientSocket")

    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    root = Tk()
    app = App(root)
    root.mainloop()
