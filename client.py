from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from os import system
from time import sleep

system("title ClientSocket")

# HOST = "127.0.0.1"
HOST = "192.168.1.29"
PORT = 33000


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

# ---------------------------------------------------------------

my_msg = tkinter.StringVar()
my_msg.set("")


scrollbar = tkinter.Scrollbar(top)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field["borderwidth"] = "1px"
entry_field["fg"] = "#333333"
entry_field["justify"] = "left"
entry_field["relief"] = "sunken"
entry_field.place(x=10, y=460, width=500, height=30)


msg_list = tkinter.Listbox(top, yscrollcommand=scrollbar.set)
msg_list["borderwidth"] = "1px"
msg_list["fg"] = "#333333"
msg_list["justify"] = "left"
msg_list.place(x=10, y=10, width=570, height=440)


send_button = tkinter.Button(top, text="Enviar", command=send)
send_button["anchor"] = "se"
send_button["bg"] = "#f0f0f0"
send_button["fg"] = "#000000"
send_button["justify"] = "center"
send_button.place(x=520, y=460, width=50, height=30)


top.protocol("WM_DELETE_WINDOW", on_closing)

# ---------------------------------------------------------------

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
