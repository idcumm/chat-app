# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import random
import csv
from datetime import datetime
from time import sleep

system("title ServerSocket")
history = []


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
    global history

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
                        # welcome = "Bienvenido %s" % name
                        # client.send(bytes(welcome, "utf8"))
                        clients[client] = name
                        client.send(bytes("{history}" + str(history), "utf8"))
                        sleep(0.2)
                        msg = "%s se ha unido al chat!" % name
                        broadcast(bytes(msg, "utf8"))

                        break
                if not exit == True:
                    client.send(bytes("{no_usuario}", "utf8"))
            elif bytes("{register}", "utf8") in msg:
                towrite = str(msg)[12:-1].split()

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
                        break

                if user_in_use == False:
                    csvfile.append(towrite)
                    client.send(bytes("{register}", "utf8"))
                else:
                    client.send(bytes("{no_register}", "utf8"))

                with open("data.csv", "w", encoding="UTF8", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(csvfile)

            else:
                broadcast(msg, name + ": ")
                console_print = str(bytes(name, "utf8") + bytes(": ", "utf8") + msg)
                print(console_print[2:-1])
        else:
            msg = "%s se ha ido del chat." % name
            broadcast(bytes(msg, "utf8"))
            console_print = str(
                bytes(name, "utf8") + bytes(": ", "utf8") + bytes(msg, "utf8")
            )
            print(console_print[2:-1])
            sleep(0.2)
            # try:
            #     client.send(bytes("{quit}", "utf8"))
            # except ConnectionResetError:
            #     continue
            client.close()
            del clients[client]
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    global history
    """Broadcasts a message to all the clients."""

    for sock in clients:
        date = datetime.now().strftime("%H:%M")
        try:
            sock.send(bytes("(" + date + ") " + prefix, "utf8") + msg)
        except ConnectionResetError:
            print("ConnectionResetError")
        history.append(bytes("(" + date + ") " + prefix, "utf8") + msg)
        # print(history)


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
