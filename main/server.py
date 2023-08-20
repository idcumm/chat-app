# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import random
import csv

system("title ServerSocket")


def set_name(x):
    csvfile = []
    in_i = False

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    search = x[0]

    for i in csvfile:
        if search in i:
            in_i = True
            index = csvfile.index(i)
            csvfile[index] = x
            break

    if in_i == False:
        csvfile.append(x)

    with open("data.csv", "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csvfile)


def assign_name(x):
    csvfile = []
    name = None

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    search = x

    for i in csvfile:
        if search in i:
            name = i[1]
            # print(f"{search} = {name}")
            break
    return name


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    global client_address
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Escrive tu nombre", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    global client_address

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            # if bytes("{setname}", "utf8") in msg:
            #     name = str(msg)[11:-1]
            #     welcome = "Has cambiado tu nombre a %s" % name
            #     client.send(bytes(welcome, "utf8"))
            #     clients[client] = name
            #     towrite = [client_address[0], name]
            #     set_name(towrite)
            if bytes("{login}", "utf8") in msg:
                exit = False
                csvfile = []
                search = str(msg)[9:-1].split()
                with open("data.csv", "r") as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                        csvfile.append(row)

                for i in csvfile:
                    if search == i:
                        exit = True
                        client.send(bytes("{connect}", "utf8"))
                        name = search[0]
                        welcome = "Bienvenido %s" % name
                        client.send(bytes(welcome, "utf8"))
                        msg = "%s se ha unido al chat!" % name
                        broadcast(bytes(msg, "utf8"))
                        clients[client] = name

                        break
                if not exit == True:
                    client.send(bytes("{no_usuario}", "utf8"))

                pass
            else:
                broadcast(msg, name + ": ")
                console_print = str(bytes(name, "utf8") + bytes(": ", "utf8") + msg)
                print(console_print[2:-1])
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
