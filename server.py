# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import csv
from datetime import datetime
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


def accept_incoming_connections():
    global client_address
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} se ha conectado.")
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    global client_address
    global history

    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        try:
            print(name + ": " + msg)
        except UnboundLocalError:
            print(f"{client_address}: {msg}")
        if "/login" in msg:
            username, password = msg[7:].split()
            try:
                with open("data.csv", "r+", encoding="utf8", newline="") as file:
                    data = []
                    r = csv.reader(file)
                    login_state = 0

                    for row in r:
                        data.append(row)

                    if not data:
                        login_state = 3

                    else:
                        for i in data:
                            if i[0] == username:
                                if i[1] == password:
                                    login_state = 1
                                    break

                                else:
                                    login_state = 2

                            else:
                                login_state = 3

                    if login_state == 1:
                        name = username
                        clients[client] = name
                        client.send(bytes("/login", "utf8"))
                        client.send(bytes("/history" + " " + str(history), "utf8"))
                        sleep(0.2)
                        msg = f"%s se ha unido al chat!" % name
                        broadcast(msg)
                        msg = f"%s se ha unido al chat! {client_address}" % name
                        print(msg)

                    elif login_state == 2:
                        client.send(bytes("/login_password_error", "utf8"))

                    elif login_state == 3:
                        client.send(bytes("/login_user_error", "utf8"))

                    else:
                        print("Unknown error")
            except FileNotFoundError:
                print(FileNotFoundError)
                client.send(bytes("/login_user_error", "utf8"))

        elif "/register" in msg:
            username, password = msg[10:].split()
            try:
                print(FileExistsError)
                x = open("data.csv", "x")
                x.close()
            except FileExistsError:
                pass
            with open("data.csv", "r+", encoding="utf8", newline="") as file:
                data = []
                w = csv.writer(file)
                r = csv.reader(file)
                user_in_use = False

                for row in r:
                    data.append(row)

                if not data:
                    w.writerow([username, password])
                    client.send(bytes("/register", "utf8"))
                else:
                    for i in data:
                        if username == i[0]:
                            user_in_use = True
                            client.send(bytes("/register_error", "utf8"))
                            break
                    if not user_in_use:
                        w.writerow([username, password])
                        client.send(bytes("/register", "utf8"))
        elif "/quit" in msg:
            client.send(bytes("/quit", "utf8"))
            client.close()
            try:
                del clients[client]
                msg = f"%s se ha ido del chat." % name
                broadcast(msg)
                msg = f"%s se ha ido del chat. {client_address}" % name
                print(msg)
                break
            except KeyError:
                print(KeyError)
                break

        else:
            broadcast(msg, name + ": ")


def broadcast(msg, prefix=""):  # prefix is for name identification.
    global history
    date = datetime.now().strftime("%H:%M")
    for sock in clients:
        try:
            sock.send(bytes("(" + date + ") " + prefix + msg, "utf8"))
        except ConnectionResetError:
            print(ConnectionResetError)
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
