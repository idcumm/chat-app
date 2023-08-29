# TODO make the app so it not only has group chat, dm's too
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# TODO fer verificar i register amb def ver(user, password): in no amb user.get()
# TODO fer tot un sol idioma
# TODO arreglar register
# TODO fer autoscroll
# TODO fer si data.csv no existe, el crea
# ==========>> DEFINITION OF FUNCTIONS <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter.font as tkFont
from os import system


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class App:
    def __init__(self, top):
        global my_msg
        global msg_list
        global scrollbar
        global entry_field
        global send_button

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
        entry_field.bind("<Return>", send)
        entry_field.focus_set()
        entry_field["borderwidth"] = "1px"
        entry_field["bg"] = "#282424"
        ft = tkFont.Font(family="Times", size=15)
        entry_field["font"] = ft
        entry_field["fg"] = "#ffffff"
        entry_field["justify"] = "left"
        entry_field["relief"] = "sunken"
        entry_field.place(x=380, y=660, width=800, height=30)

        msg_list = Listbox(top, yscrollcommand=scrollbar.set)
        scrollbar.config(command=msg_list.yview)
        msg_list["bg"] = "#282424"
        msg_list["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=15)
        msg_list["font"] = ft
        msg_list["fg"] = "#ffffff"
        msg_list["justify"] = "left"
        msg_list.place(x=380, y=10, width=830, height=640)

        # send_button
        send_button = Button(top, text="Enviar", command=send)
        send_button["anchor"] = "se"
        send_button["bg"] = "#282424"
        ft = tkFont.Font(family="Times", size=10)
        send_button["font"] = ft
        send_button["fg"] = "#ffffff"
        send_button["justify"] = "center"
        send_button.place(x=1190, y=660, width=50, height=30)

        ventana_inicio()


def ventana_inicio():
    global top_login
    global verifica_usuario
    global verifica_clave

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
        lambda: login(verifica_usuario.get(), verifica_clave.get()),
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
        lambda: login(verifica_usuario.get(), verifica_clave.get()),
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
    list = [usuario, clave]
    if " " in usuario or usuario == "":
        no_spaces = False
        login_user_error()
    elif " " in clave or clave == "":
        no_spaces = False
        login_password_error()
    else:
        no_spaces = True

    if no_spaces == True:
        msg = f"{usuario} {clave}"
        my_msg.set("{login}" + msg)
        send()


def register(usuario, clave, event=None):
    list = [usuario, clave]

    for i in list:
        if " " in i or i == "":
            no_spaces = False
            register_error()
            break
        else:
            no_spaces = True
    if no_spaces == True:
        msg = f"{usuario} {clave}"
        my_msg.set("{register}" + msg)
        send()


def login_user_error():
    global top_login
    Label(top_login, text="Usuario no encontrado.").pack()


def login_password_error():
    global top_login
    Label(top_login, text="Contraseña incorrecta.").pack()


def register_error():
    global top_login
    Label(
        top_login,
        text="Este nombre de usuario y/o contraseña \n no están disponibles",
    ).pack()


def receive():
    global user_loged
    global history
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if "{login}" in msg:
                top_login.destroy()
                entry_field.focus_set()
                user_loged = True
            elif "{history}" in msg:
                history = msg[12:-2].split("', b'")
                if not history == [""]:
                    for i in history:
                        msg_list.insert(END, i)
            elif "{login_user_error}" in msg:
                login_user_error()
            elif "{login_password_error}" in msg:
                login_password_error()
            elif "{register}" in msg:
                login(verifica_usuario.get(), verifica_clave.get())
            elif "{register_error}" in msg:
                register_error()
            elif "{quit}" in msg:
                client_socket.close()
                top.quit()
            else:
                msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            print("Error: OSError 1")
            client_socket.close()
            top.quit()
            exit()


def send(event=None):  # event is passed by binders.
    global user_loged
    msg = my_msg.get()
    my_msg.set("")
    if user_loged == False:
        if "{quit}" in msg or "{login}" in msg or "{register}" in msg:
            client_socket.send(bytes(msg, "utf8"))
    elif user_loged == True:
        try:
            client_socket.send(bytes(msg, "utf8"))
        except OSError:
            print("Error: OSError 2")


def on_closing(event=None):
    my_msg.set("{quit}")
    send()
    exit()


# ==========>> MAIN CODE <<========== #


client_socket = socket(AF_INET, SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 33000
ADDR = (HOST, PORT)

BUFSIZ = 1024

if __name__ == "__main__":
    system("title ClientSocket")
    user_loged = False

    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    top = Tk()
    app = App(top)
    top.mainloop()

    exit()
