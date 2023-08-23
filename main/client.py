# TODO make the app so it not only has group chat, dm's too
# TODO arreglar history chat duplication glitch
# TODO arreglar leave chat
# TODO fer log.log de history chat i cargarlo cada cop que sobra
# ==========>> DEFINITION OF FUNCTIONS <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter.font as tkFont
from os import system
import csv
from time import sleep


# ==========>> ASSIGNATION OF VARIABLES <<========== #


if __name__ == "__main__":
    system("title ClientSocket")

HOST = "192.168.1.29"
PORT = 33000
ADDR = (HOST, PORT)

BUFSIZ = 1024


# ==========>> DEFINITION OF FUNCTIONS <<========== #


def ventana_inicio():
    global ventana_principal
    pestas_color = "DarkGrey"
    ventana_principal = Toplevel(top)
    # ventana_principal.focus_force()
    ventana_principal.geometry("300x250")  # DIMENSIONES DE LA VENTANA
    ventana_principal.title("Login con tkinter")  # TITULO DE LA VENTANA
    Label(
        ventana_principal,
        text="Escoja su opción",
        bg="LightGreen",
        width="300",
        height="2",
        font=("Calibri", 13),
    ).pack()  # ETIQUETA CON TEXTO
    Label(ventana_principal, text="").pack()
    Button(
        ventana_principal,
        text="Acceder",
        height="2",
        width="30",
        bg=pestas_color,
        command=login,
    ).pack()  # BOTÓN "Acceder"
    Label(ventana_principal, text="").pack()
    Button(
        ventana_principal,
        text="Registrarse",
        height="2",
        width="30",
        bg=pestas_color,
        command=registro,
    ).pack()  # BOTÓN "Registrarse".
    Label(ventana_principal, text="").pack()
    ventana_principal.mainloop()


def registro():
    global ventana_registro
    ventana_registro = Toplevel(ventana_principal)
    # ventana_registro.focus_force()
    ventana_registro.title("Registro")
    ventana_registro.geometry("300x250")

    global nombre_usuario
    global clave
    global entrada_nombre
    global entrada_clave
    nombre_usuario = (
        StringVar()
    )  # DECLARAMOS "string" COMO TIPO DE DATO PARA "nombre_usuario"
    clave = StringVar()  # DECLARAMOS "sytring" COMO TIPO DE DATO PARA "clave"

    Label(ventana_registro, text="Introduzca datos", bg="LightGreen").pack()
    Label(ventana_registro, text="").pack()
    etiqueta_nombre = Label(ventana_registro, text="Nombre de usuario * ")
    etiqueta_nombre.pack()
    entrada_nombre = Entry(ventana_registro, textvariable=nombre_usuario)
    entrada_nombre.focus_set()
    entrada_nombre.bind("<Return>", registro_usuario)
    entrada_nombre.pack()
    etiqueta_clave = Label(ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(
        ventana_registro, textvariable=clave
    )  # ESPACIO PARA INTRODUCIR LA CONTRASEÑA.
    entrada_clave.bind("<Return>", registro_usuario)
    entrada_clave.pack()
    Label(ventana_registro, text="").pack()
    Button(
        ventana_registro,
        text="Registrarse",
        width=10,
        height=1,
        bg="LightGreen",
        command=registro_usuario,
    ).pack()  # BOTÓN "Registrarse"


def login():
    global ventana_login
    ventana_login = Toplevel(ventana_principal)
    # ventana_login.focus_force()
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry("300x250")
    Label(ventana_login, text="Introduzca nombre de usuario y contraseña").pack()
    Label(ventana_login, text="").pack()

    global verifica_usuario
    global verifica_clave

    verifica_usuario = StringVar()
    verifica_clave = StringVar()

    global entrada_login_usuario
    global entrada_login_clave

    Label(ventana_login, text="Nombre usuario * ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable=verifica_usuario)
    entrada_login_usuario.focus_set()
    entrada_login_usuario.bind("<Return>", verifica_login)
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="Contraseña * ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show="*")
    entrada_login_clave.bind("<Return>", verifica_login)
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(
        ventana_login, text="Acceder", width=10, height=1, command=verifica_login
    ).pack()


def verifica_login(event=None):
    usuario1 = verifica_usuario.get()
    clave1 = verifica_clave.get()

    msg = f"{usuario1} {clave1}"
    my_msg.set("{login}" + msg)
    send()


def no_usuario():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel(ventana_login)
    ventana_no_usuario.title("ERROR")
    ventana_no_usuario.geometry("250x100")
    Label(ventana_no_usuario, text="Usuario o contraseña incorrecta.").pack()
    Button(
        ventana_no_usuario, text="OK", command=borrar_no_usuario
    ).pack()  # EJECUTA "borrar_no_usuario()"


def no_registro():
    global ventana_no_registro
    ventana_no_registro = Toplevel(ventana_registro)
    ventana_no_registro.title("ERROR")
    ventana_no_registro.geometry("250x100")
    Label(
        ventana_no_registro,
        text="Este nombre de usuario y/o contraseña \n no están disponibles",
    ).pack()
    Button(
        ventana_no_registro, text="OK", command=borrar_no_registro
    ).pack()  # EJECUTA "borrar_no_registro()"


def borrar_no_usuario():
    ventana_no_usuario.destroy()


def borrar_no_registro():
    ventana_no_registro.destroy()


def registro_usuario(event=None):
    usuario_info = nombre_usuario.get()
    clave_info = clave.get()
    towrite = [usuario_info, clave_info]

    for i in towrite:
        if " " in i:
            no_spaces = False
            entrada_nombre.delete(0, END)
            entrada_clave.delete(0, END)
            no_registro()
            break
        else:
            no_spaces = True
    if no_spaces == True:
        msg = f"{usuario_info} {clave_info}"
        my_msg.set("{register}" + msg)
        send()


def receive():
    global user_loged
    global history
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if "{connect}" in str(msg):
                ventana_principal.destroy()
                user_loged = True
            elif "{history}" in str(msg):
                history = str(msg)[12:-2].split("', b'")
                print(history)
                if not history == [""]:
                    for i in history:
                        msg_list.insert(END, i)
            elif "{no_usuario}" in str(msg):
                no_usuario()
            elif "{register}" in str(msg):
                Label(
                    ventana_principal,
                    text="Registro completado con éxito",
                    fg="green",
                    font=("calibri", 11),
                ).pack()
                ventana_registro.destroy()
            elif "{no_register}" in str(msg):
                no_registro()
            else:
                msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    global user_loged
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")
    if user_loged == True:
        client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()
    if "{login}" in msg:
        client_socket.send(bytes(msg, "utf8"))
    if "{register}" in msg:
        client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()
    sleep(0.2)
    exit()


# ==========>> MAIN CODE <<========== #


client_socket = socket(AF_INET, SOCK_STREAM)

top = Tk()
my_msg = StringVar()
scrollbar = Scrollbar(top)
entry_field = Entry(top, textvariable=my_msg)
msg_list = Listbox(top, yscrollcommand=scrollbar.set)
send_button = Button(top, text="Enviar", command=send)

if __name__ == "__main__":
    user_loged = False
    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    top.title("Chatter")

    width = 600
    height = 500
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

    my_msg.set("")

    scrollbar.pack(side=RIGHT, fill=Y)

    entry_field.bind("<Return>", send)
    entry_field.focus_set()
    entry_field["borderwidth"] = "1px"
    entry_field["bg"] = "#282424"
    ft = tkFont.Font(family="Times", size=15)
    entry_field["font"] = ft
    entry_field["fg"] = "#ffffff"
    entry_field["justify"] = "left"
    entry_field["relief"] = "sunken"
    entry_field.place(x=10, y=460, width=500, height=30)

    msg_list["bg"] = "#282424"
    msg_list["borderwidth"] = "1px"
    ft = tkFont.Font(family="Times", size=15)
    msg_list["font"] = ft
    msg_list["fg"] = "#ffffff"
    msg_list["justify"] = "left"
    msg_list.place(x=10, y=10, width=560, height=440)

    send_button["anchor"] = "se"
    send_button["bg"] = "#282424"
    ft = tkFont.Font(family="Times", size=10)
    send_button["font"] = ft
    send_button["fg"] = "#ffffff"
    send_button["justify"] = "center"
    send_button.place(x=520, y=460, width=50, height=30)

    top.protocol("WM_DELETE_WINDOW", on_closing)
    ventana_inicio()
    mainloop()
