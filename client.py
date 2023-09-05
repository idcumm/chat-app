# # # # TODO fer que el chat tingui missatges privats
# # # # TODO simular un atac informatic al servidor
# # # # TODO fer el encriptatge
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# TODO fer tot en un sol idioma
# TODO posar dia i hora en missatges
# TODO que no surti la consola al obrir client.pyw
# TODO millorar el print de la consola
# TODO Quan la aplicció no tingui focus i revi un misatge, faigi ping i ficar l'icono tronja
# TODO Que detecti el nom del ultim misatge i si es el mateix que no escrigui el nom.
# TODO fer funcio tot allo que es repeteix molt
# TODO fer separacio de misatges per persona (2 misatges duna persona seguits, sense doble espai, i altres ab doble espai)
# -=-=-=- devesaguillem@gmail.com se ha unido! -=-=-=-

# - - - - devesaguillem@gmail.com - - - -
# (00:00) Hola chicos!
# (00:00) Como estan? Espero que Muy Bien
#
# - - - - devesapere@gmail.com - - - -
# (00:01) Mal
#
# - - - - devesaguillem@gmail.com - - - -
# (00:02) Por?
#
# ==========>> DEFINITION OF FUNCTIONS <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter.font as tkFont
from os import system
from functools import partial
from datetime import datetime


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class App:
    def __init__(self, top):
        global my_msg
        global msg_list
        global scrollbar
        global entry_field
        global send_button
        global top_login
        global verifica_usuario
        global verifica_clave

        # window
        top.title("Chatt app")
        width = 1250
        height = 700
        screenwidth = top.winfo_screenwidth()
        screenheight = top.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        top.geometry(alignstr)
        top.resizable(width=False, height=False)
        top.configure(bg="#282424")
        top.protocol("WM_DELETE_WINDOW", on_closing)

        # my_msg
        my_msg = StringVar()
        my_msg.set("")

        # scrollbar
        scrollbar = Scrollbar(
            top,
            activebackground="#282424",
            bg="#282424",
            highlightbackground="#282424",
            highlightcolor="#282424",
            troughcolor="#282424",
        )
        scrollbar.place(x=1220, y=10, width=20, height=640)

        # entry_field
        entry_field = Entry(top, textvariable=my_msg)
        entry_field.bind("<Return>", msg_send)
        entry_field.focus_set()
        entry_field["borderwidth"] = "1px"
        entry_field["bg"] = "#282424"
        ft = tkFont.Font(family="Times", size=15)
        entry_field["font"] = ft
        entry_field["fg"] = "#ffffff"
        entry_field["justify"] = "left"
        entry_field["relief"] = "sunken"
        entry_field.place(x=380, y=660, width=800, height=30)

        msg_list = Text(top, yscrollcommand=scrollbar.set)
        scrollbar.config(command=msg_list.yview)
        msg_list["bg"] = "#282424"
        msg_list["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=15)
        msg_list["font"] = ft
        msg_list["fg"] = "#ffffff"
        msg_list.place(x=380, y=10, width=830, height=640)
        msg_list.tag_config("right", justify="right")
        msg_list.tag_config("center", justify="center")

        # send_button
        send_button = Button(top, text="Enviar", command=msg_send)
        send_button["anchor"] = "se"
        send_button["bg"] = "#282424"
        ft = tkFont.Font(family="Times", size=10)
        send_button["font"] = ft
        send_button["fg"] = "#ffffff"
        send_button["justify"] = "center"
        send_button.place(x=1190, y=660, width=50, height=30)

        top_login = Frame(top)
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

        Label(top_login, text="Nombre de usuario *", font=("Calibri", 13)).pack()

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
            command=lambda: login(verifica_usuario.get(), verifica_clave.get()),
            font=("Calibri", 13),
        ).pack()

        Label(top_login, text="").pack()

        Button(
            top_login,
            text="Register",
            width="20",
            bg="DarkGrey",
            command=lambda: register(verifica_usuario.get(), verifica_clave.get()),
            font=("Calibri", 13),
        ).pack()

        top_login.pack(side=LEFT, fill=BOTH)


def login(usuario, clave, event=None):
    global username
    username = usuario
    if len(usuario) > 20 or len(clave) > 20:
        login_lenght_error()
    else:
        msg = f'"{usuario}", "{clave}"'
        command_send("/login " + msg)


def register(usuario, clave, event=None):
    if len(usuario) > 20 or len(clave) > 20:
        login_lenght_error()
    else:
        msg = f'"{usuario}", "{clave}"'
        command_send("/register " + msg)


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


def onAdd(place, text, tag=None):
    global msg_list
    msg_list.configure(state="normal")
    msg_list.insert(place, text + "\n\n", tag)
    msg_list.configure(state="disabled")
    msg_list.yview(place)


def receive():
    global history
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if "/login" == msg:
                top.title(f"Chatt app - Logged as {username}")
                top_login.destroy()
                entry_field.focus_set()
            elif "/history" in msg:
                history = eval(msg[9:])
                if not history == [""]:
                    for i in history:
                        # i = eval(i)
                        if i["type"] == "broadcast":
                            if i["name"] == username:
                                msg = f'{i["name"]}: {i["msg"]} ({i["date"]})'
                                onAdd(END, msg, "right")
                            else:
                                msg = f'({i["date"]}) {i["name"]}: {i["msg"]}'
                                onAdd(END, msg)
                        elif i["type"] == "join" or i["type"] == "leave":
                            msg = f'{i["name"]} {i["msg"]}'
                            onAdd(END, msg, "center")
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
                top.quit()
            else:
                msg = eval(msg)
                if msg["type"] == "broadcast":
                    if not msg["name"] == username:
                        msg = f'({msg["date"]}) {msg["name"]}: {msg["msg"]}'
                        onAdd(END, msg)
                elif msg["type"] == "join" or msg["type"] == "leave":
                    msg = f'{msg["name"]} {msg["msg"]}'
                    onAdd(END, msg, "center")

        except OSError:  # Possibly client has left the chat.
            print(OSError)
            client_socket.close()
            top.quit()
            exit()


def msg_send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")
    date = datetime.now().strftime("%H:%M")
    msg = f"{username}: {msg} ({date})"
    onAdd(END, msg, "right")
    try:
        client_socket.send(msg.encode("utf8"))
    except OSError:
        print(OSError)


def command_send(msg, event=None):
    client_socket.send(msg.encode("utf8"))


def on_closing(event=None):
    command_send("/quit")
    exit()


# ==========>> MAIN CODE <<========== #


client_socket = socket(AF_INET, SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 33000
ADDR = (HOST, PORT)
BUFSIZ = 1024

if __name__ == "__main__":
    system("title ClientSocket")

    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    top = Tk()
    app = App(top)
    top.mainloop()
