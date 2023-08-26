# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import random
import csv
from datetime import datetime
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


def accept_incoming_connections():
    global client_address
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se ha conectado." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    global client_address
    global history

    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if "{login}" in msg:
            exit = False
            csvfile = []
            search = msg[7:].split()
            with open("data.csv", "r") as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    csvfile.append(row)

            for i in csvfile:
                if search == i:
                    exit = True
                    client.send(bytes("{connect}", "utf8"))
                    name = search[0]
                    clients[client] = name
                    client.send(bytes("{history}" + str(history), "utf8"))
                    sleep(0.2)
                    msg = f"%s se ha unido al chat!" % name
                    broadcast(msg)
                    msg = f"%s se ha unido al chat! {client_address}" % name
                    print(msg)

                    break
            if not exit == True:
                client.send(bytes("{no_usuario}", "utf8"))
        elif "{register}" in msg:
            towrite = msg[10:].split()

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
        elif "{quit}" in msg:
            msg = f"%s se ha ido del chat." % name
            broadcast(msg)
            msg = f"%s se ha ido del chat. {client_address}" % name
            print(msg)
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            break
        else:
            broadcast(msg, name + ": ")
            print(name + ": " + msg)


def broadcast(msg, prefix=""):  # prefix is for name identification.
    global history
    for sock in clients:
        date = datetime.now().strftime("%H:%M")
        try:
            sock.send(bytes("(" + date + ") " + prefix + msg, "utf8"))
        except ConnectionResetError:
            print("Error: ConnectionResetError 2")
    history.append(bytes("(" + date + ") " + prefix + msg, "utf8"))


clients = {}
addresses = {}
history = []

system("title ServerSocket")

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
