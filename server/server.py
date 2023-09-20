# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system
import csv
import logging
from datetime import datetime
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


def accept_incoming_connections():
    global client_address
    while True:
        client, client_address = SERVER.accept()
        logger.info(f"{client_address} se ha conectado.")
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    global client_address
    global history

    while True:
        try:
            msg = client.recv(BUFSIZ).decode("utf8")
        except ConnectionResetError:
            client.close()
            try:
                del clients[client]
                broadcast(name, "leave")
                logger.info(f"{client_address} se ha ido.")
                break
            except KeyError:
                logger.error(KeyError)
                break

        try:
            logger.info(name + ": " + msg)
        except UnboundLocalError:
            logger.info(f"{client_address}: {msg}")

        if "/login" in msg:
            username, password = eval(msg[7:])
            logger.debug("username: " + username)
            logger.debug("password: " + password)
            try:
                with open(
                    "database\data.csv", "r+", encoding="utf8", newline=""
                ) as file:
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
                                    break

                            else:
                                login_state = 3

                    if login_state == 1:
                        name = username
                        clients[client] = name
                        client.send("/login".encode("utf8"))
                        for i in reversed(history):
                            client.send(("/history " + str(i)).encode("utf8"))
                            sleep(0.05)
                        broadcast(name, "join")
                        # msg = f"%s se ha unido al chat! {client_address}" % name
                        # print(msg)

                    elif login_state == 2:
                        client.send("/login_password_error".encode("utf8"))

                    elif login_state == 3:
                        client.send("/login_user_error".encode("utf8"))

            except FileNotFoundError:
                logger.error(FileNotFoundError)
                client.send("/login_user_error".encode("utf8"))

        elif "/register" in msg:
            username, password = eval(msg[10:])
            try:
                x = open("database\data.csv", "x")
                x.close()
                logger.error(FileExistsError)

            except FileExistsError:
                pass

            with open("database\data.csv", "r+", encoding="utf8", newline="") as file:
                data = []
                w = csv.writer(file)
                r = csv.reader(file)
                user_in_use = False

                for row in r:
                    data.append(row)

                if not data:
                    w.writerow([username, password])
                    client.send("/register".encode("utf8"))
                else:
                    for i in data:
                        if username == i[0]:
                            user_in_use = True
                            client.send("/register_error".encode("utf8"))
                            break
                    if not user_in_use:
                        w.writerow([username, password])
                        client.send("/register".encode("utf8"))
        elif "/quit" in msg:
            client.send("/quit".encode("utf8"))
            client.close()
            try:
                del clients[client]
                broadcast(name, "leave")
                logger.info(f"{client_address} se ha ido.")
                break
            except KeyError:
                logger.error(KeyError)
                break

        else:
            broadcast(name, "broadcast", msg=msg)


def broadcast(prefix, type, msg=""):
    global history

    for sock in clients:
        try:
            date = datetime.now().strftime("%H:%M")
            dict = {"date": date, "type": type, "name": prefix, "msg": msg}
            sock.send(str(dict).encode("utf8"))
        except ConnectionResetError:
            logger.error(ConnectionResetError)
    date = datetime.now().strftime("%H:%M")
    dict = {"date": date, "type": type, "name": prefix, "msg": msg}
    history.append(dict)


if __name__ == "__main__":
    logger = logging.getLogger()
    clients = {}
    addresses = {}
    history = []

    logging.basicConfig(format="[%(levelname)s] > %(message)s")

    logger.setLevel(logging.DEBUG)

    HOST = ""
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    system("title ServerSocket")

    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    print("         ---- Server online! ----\n")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
