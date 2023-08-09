from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import random
from time import sleep

system("title ServerSocket")


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Escrive tu nombre", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    # name = client.recv(BUFSIZ).decode("utf8")
    name = "User_" + str(random.randint(100000, 999999))
    welcome = "Bienvenido %s" % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s se ha unido al chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        console_print = str(bytes(name, "utf8") + bytes(": ", "utf8") + msg)
        print(console_print[2:-1])

        if msg != bytes("{quit}", "utf8"):
            if bytes("{setname}", "utf8") in msg:
                name = str(msg)[11:-1]
                welcome = "Has cambiado tu nombre a %s" % name
                client.send(bytes(welcome, "utf8"))
                clients[client] = name
            else:
                broadcast(msg, name + ": ")
        else:
            # client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s se ha ido del chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ""
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
