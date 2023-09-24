# ==========>> MODULE IMPORT <<========== #


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, path
import csv
import logging
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
                self.dictionary = eval(client.recv(self.BUFSIZ).decode("utf8"))
                logger.debug(self.dictionary)
            except ConnectionResetError:
                client.close()
                try:
                    del self.clients[client]
                    # self.msg_send(self.dictionary["name"], "leave")
                    logger.info(f"{self.client_address} se ha ido.")
                    break
                except KeyError as e:
                    logger.error(e)
                    break

            if self.dictionary["type"] == "command":
                if self.dictionary["command"] == "login":
                    self.username = self.dictionary["user"]
                    self.password = self.dictionary["key"]
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
                                self.clients[client] = self.dictionary["name"]
                                self.command_send(client, "login")
                                for i in reversed(self.history):
                                    self.command_send(client, "history", str(i))
                                    sleep(0.05)
                                # self.msg_send(self.dictionary["name"], "join")
                                # msg = f"%s se ha unido al chat! {client_address}" % name
                                # print(msg)
                            elif login_state == 2:
                                self.command_send(client, "login_password_error")
                            elif login_state == 3:
                                self.command_send(client, "login_user_error")
                    except FileNotFoundError as e:
                        logger.error(e)
                        self.command_send(client, "login_user_error")

                elif self.dictionary["command"] == "register":
                    self.username = self.dictionary["user"]
                    self.password = self.dictionary["key"]
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
                            self.command_send(client, "register")
                        else:
                            for i in self.data:
                                if self.username == i[0]:
                                    user_in_use = True
                                    self.command_send(client, "register_error")
                                    break
                            if not user_in_use:
                                w.writerow([self.username, self.password])
                                self.command_send(client, "register")
                # elif self.dictionary["command"] == "quit":
                #     client.send("/quit".encode("utf8"))
                #     client.close()
                #     try:
                #         del self.clients[client]
                #         logger.info(f"{self.client_address} se ha ido.")
                #         break
                #     except KeyError as e:
                #         logger.error(e)
                #         break
            elif self.dictionary["type"] == "broadcast":
                self.msg_send(self.dictionary["name"], self.dictionary["msg"])

    def msg_send(self, name, msg):
        dictionary = {"date": self.dictionary["date"], "name": name, "type": "broadcast", "msg": msg}
        for sock in self.clients:
            try:
                sock.send(str(dictionary).encode("utf8"))
            except ConnectionResetError as e:
                logger.error(e)
        self.history.append(dictionary)

    def command_send(self, client: socket, command: str, history: str = ""):
        if command != "history":
            dictionary = {"type": "command", "command": command}
        else:
            dictionary = {"type": "command", "command": command, "history": history}
        client.send(str(dictionary).encode("utf8"))


# ==========>> MAIN CODE <<========== #


HOST = ""
PORT = 33000

if __name__ == "__main__":
    logger = logging.getLogger()
    server = Server()

    server.socket.close()
