# ==========>> DEFINITION OF FUNCTIONS <<========== #


from tkinter import *
import os
import csv


# ==========>> DEFINITION OF FUNCTIONS <<========== #


def ventana_inicio():
    global ventana_principal
    pestas_color = "DarkGrey"
    ventana_principal = Tk()
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
    entrada_nombre = Entry(
        ventana_registro, textvariable=nombre_usuario
    )  # ESPACIO PARA INTRODUCIR EL NOMBRE.
    entrada_nombre.pack()
    etiqueta_clave = Label(ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(
        ventana_registro, textvariable=clave, show="*"
    )  # ESPACIO PARA INTRODUCIR LA CONTRASEÑA.
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
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="Contraseña * ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show="*")
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(
        ventana_login, text="Acceder", width=10, height=1, command=verifica_login
    ).pack()


def verifica_login():
    exit = False
    csvfile = []
    usuario1 = verifica_usuario.get()
    clave1 = verifica_clave.get()
    search = [usuario1, clave1]

    entrada_login_usuario.delete(0, END)
    entrada_login_clave.delete(0, END)

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    for i in csvfile:
        if search == i:
            exit = True
            Label(
                ventana_principal,
                text="Login completado con éxito",
                fg="green",
                font=("calibri", 11),
            ).pack()
            ventana_login.destroy()
            break
    if not exit == True:
        no_usuario()


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
    Label(ventana_no_registro, text="Este nombre de usuario ya está en uso.").pack()
    Button(
        ventana_no_registro, text="OK", command=borrar_no_registro
    ).pack()  # EJECUTA "borrar_no_registro()"


def borrar_no_usuario():
    ventana_no_usuario.destroy()


def borrar_no_registro():
    ventana_no_registro.destroy()


def registro_usuario():
    usuario_info = nombre_usuario.get()
    clave_info = clave.get()
    towrite = [usuario_info, clave_info]

    entrada_nombre.delete(0, END)
    entrada_clave.delete(0, END)

    csvfile = []
    user_in_use = False

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    search = towrite[0]

    for i in csvfile:
        if search in i:
            user_in_use = True
            no_registro()
            break

    if user_in_use == False:
        csvfile.append(towrite)
        Label(
            ventana_principal,
            text="Registro completado con éxito",
            fg="green",
            font=("calibri", 11),
        ).pack()
        ventana_registro.destroy()

    with open("data.csv", "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csvfile)


# ==========>> MAIN CODE <<========== #


if __name__ == "__main__":
    ventana_inicio()
