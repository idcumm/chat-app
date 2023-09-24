# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, path
import csv
import logging
from datetime import datetime
from time import sleep


# ==========>> DEFINITION OF FUNCTIONS <<========== #


class Server:
    def __init__(self):
        self.absolute_path = path.dirname(path.abspath(__file__))
        self.file_path = self.absolute_path + "/database/data.csv"
        thread = Thread(target=self.accept_incoming_connections)
        self.clients = {}
        self.addresses = {}
        self.history = []
        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.socket.bind(ADDR)
        self.socket.listen(5)
        logging.basicConfig(format="[%(levelname)s] > %(message)s")
        logger.setLevel(logging.DEBUG)
        system("title ServerSocket")
        logger.info("---- Server online! ----")
        logger.info(f"Server directory: '{self.absolute_path}'")
        thread.start()
        thread.join()

    def accept_incoming_connections(self):
        while True:
            self.client, self.client_address = self.socket.accept()
            logger.info(f"{self.client_address} se ha conectado.")
            self.addresses[self.client] = self.client_address
            Thread(target=self.handle_client, args=(self.client,)).start()

    def handle_client(self, client, *args):
        while True:
            try:
                msg = client.recv(self.BUFSIZ).decode("utf8")
            except ConnectionResetError:
                client.close()
                try:
                    del self.clients[client]
                    self.broadcast(name, "leave")
                    logger.info(f"{self.client_address} se ha ido.")
                    break
                except KeyError as e:
                    logger.error(e)
                    break

            try:
                logger.info(name + ": " + msg)
            except UnboundLocalError:
                logger.info(f"{self.client_address}: {msg}")

            if "/login" in msg:
                self.username, self.password = eval(msg[7:])
                logger.debug("username: " + self.username)
                logger.debug("password: " + self.password)
                try:
                    with open(self.file_path, "r+", encoding="utf8", newline="") as file:
                        self.data = []
                        r = csv.reader(file)
                        login_state = 0

                        for row in r:
                            self.data.append(row)

                        if not self.data:
                            login_state = 3
                        else:
                            for i in self.data:
                                if i[0] == self.username:
                                    if i[1] == self.password:
                                        login_state = 1
                                        break
                                    else:
                                        login_state = 2
                                        break
                                else:
                                    login_state = 3

                        if login_state == 1:
                            name = self.username
                            self.clients[client] = name
                            client.send("/login".encode("utf8"))
                            for i in reversed(self.history):
                                client.send(("/history " + str(i)).encode("utf8"))
                                sleep(0.05)
                            self.broadcast(name, "join")
                            # msg = f"%s se ha unido al chat! {client_address}" % name
                            # print(msg)
                        elif login_state == 2:
                            client.send("/login_password_error".encode("utf8"))
                        elif login_state == 3:
                            client.send("/login_user_error".encode("utf8"))
                except FileNotFoundError as e:
                    logger.error(e)
                    client.send("/login_user_error".encode("utf8"))
            elif "/register" in msg:
                self.username, self.password = eval(msg[10:])
                try:
                    x = open(self.file_path, "x")
                    x.close()
                except FileExistsError:
                    pass

                with open(self.file_path, "r+", encoding="utf8", newline="") as file:
                    self.data = []
                    w = csv.writer(file)
                    r = csv.reader(file)
                    user_in_use = bool()

                    for row in r:
                        self.data.append(row)

                    if not self.data:
                        w.writerow([self.username, self.password])
                        client.send("/register".encode("utf8"))
                    else:
                        for i in self.data:
                            if self.username == i[0]:
                                user_in_use = True
                                client.send("/register_error".encode("utf8"))
                                break
                        if not user_in_use:
                            w.writerow([self.username, self.password])
                            client.send("/register".encode("utf8"))
            elif "/quit" in msg:
                client.send("/quit".encode("utf8"))
                client.close()
                try:
                    del self.clients[client]
                    self.broadcast(name, "leave")
                    logger.info(f"{self.client_address} se ha ido.")
                    break
                except KeyError as e:
                    logger.error(e)
                    break
            else:
                self.broadcast(name, "broadcast", msg=msg)

    def broadcast(self, prefix, type, msg=""):
        date = datetime.now().strftime("%H:%M")
        for sock in self.clients:
            try:
                dict = {"date": date, "type": type, "name": prefix, "msg": msg}
                sock.send(str(dict).encode("utf8"))
            except ConnectionResetError as e:
                logger.error(e)
        dict = {"date": date, "type": type, "name": prefix, "msg": msg}
        self.history.append(dict)


# ==========>> MAIN CODE <<========== #


HOST = ""
PORT = 33000

if __name__ == "__main__":
    logger = logging.getLogger()
    server = Server()

    server.socket.close()
