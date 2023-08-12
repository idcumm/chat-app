from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from os import system

system("title ClientSocket")

# HOST = "127.0.0.1"
HOST = "192.168.1.29"
PORT = 33000

ADDR = (HOST, PORT)

BUFSIZ = 1024


def setname():
    global my_name
    msg = my_name.get()
    my_msg.set("{setname}" + msg)
    send()


def openNewWindow():
    global my_name
    settings = tkinter.Toplevel(top)
    settings.title("Settings")
    settings.geometry("200x200")

    my_name = tkinter.StringVar()
    my_name.set("")

    text = tkinter.Label(settings, text="Escribe tu nombre:")
    text.pack()

    entry_name = tkinter.Entry(settings, textvariable=my_name)
    entry_name.bind("<Return>", send)
    entry_name.pack()

    set_name = tkinter.Button(settings, text="Apply", command=setname)
    set_name.pack()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


# ---------------------------------------------------------------


top = tkinter.Tk()
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


# ---------------------------------------------------------------


my_msg = tkinter.StringVar()
my_msg.set("")

scrollbar = tkinter.Scrollbar(top)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field["borderwidth"] = "1px"
entry_field["bg"] = "#282424"
entry_field["fg"] = "#ffffff"
entry_field["justify"] = "left"
entry_field["relief"] = "sunken"
entry_field.place(x=10, y=460, width=500, height=30)

msg_list = tkinter.Listbox(top, yscrollcommand=scrollbar.set)
msg_list["bg"] = "#282424"
msg_list["borderwidth"] = "1px"
msg_list["fg"] = "#ffffff"
msg_list["justify"] = "left"
msg_list.place(x=10, y=50, width=560, height=400)

send_button = tkinter.Button(top, text="Enviar", command=send)
send_button["anchor"] = "se"
send_button["bg"] = "#282424"
send_button["fg"] = "#ffffff"
send_button["justify"] = "center"
send_button.place(x=520, y=460, width=50, height=30)

config_button = tkinter.Button(top, text="Settings", command=openNewWindow)
config_button["anchor"] = "nw"
config_button["bg"] = "#282424"
config_button["fg"] = "#ffffff"
config_button["justify"] = "center"
config_button.place(x=10, y=10, width=50, height=30)

top.protocol("WM_DELETE_WINDOW", on_closing)


# ---------------------------------------------------------------


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


if __name__ == "__main__":
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
