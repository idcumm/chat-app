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
        absolute_path = path.dirname(path.abspath(__file__))
        self.file_path = absolute_path + "/database/"
        self.file_path2 = absolute_path + "/database/"
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
        logger.info(f"Server directory: '{absolute_path}'")

        with open(self.file_path + "data.csv", "r", encoding="utf8") as file:
            self.data = []
            r = csv.reader(file)
            self.users = []

            for row in r:
                self.data.append(row)

        for i in self.data:
            if not (i[0] in self.users):
                self.users.append(i[0])
        #!######################3
        for i in self.users:
            for j in self.users:
                if i < j:
                    try:
                        open(self.file_path2 + f"{i}_{j}.db", "x", encoding="utf8", newline="")
                    except (FileExistsError, FileNotFoundError):
                        logger.debug(f"{i}_{j}.log already exists")
        #!######################3
        #!######################3
        thread.start()
        thread.join()
        #!##################3

    def accept_incoming_connections(self):
        while True:
            self.client, self.client_address = self.socket.accept()
            logger.info(f"{self.client_address} se ha conectado.")
            self.addresses[self.client] = self.client_address
            Thread(target=self.handle_client, args=(self.client,)).start()

    def handle_client(self, client, *args):
        print(self.users)
        self.command_send(client, "userlist", str(self.users))
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
                    logger.error(f"{KeyError}: {e}")
                    break

            if self.dictionary["type"] == "command":
                if self.dictionary["command"] == "login":
                    self.username = self.dictionary["user"]
                    self.password = self.dictionary["key"]
                    logger.debug("username: " + self.username)
                    logger.debug("password: " + self.password)
                    try:
                        with open(self.file_path + "data.csv", "r+", encoding="utf8", newline="") as file:
                            self.data = []
                            r = csv.reader(file)
                            login_state = 0

                            for row in r:
                                self.data.append(row)

                            for i in self.data:
                                if not (i[0] in self.users):
                                    self.users.append(i[0])

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
                        logger.error(f"{FileNotFoundError}: {e}")
                        self.command_send(client, "login_user_error")

                elif self.dictionary["command"] == "register":
                    self.username = self.dictionary["user"]
                    self.password = self.dictionary["key"]
                    try:
                        x = open(self.file_path + "data.csv", "x")
                        x.close()
                    except FileExistsError:
                        pass

                    with open(self.file_path + "data.csv", "r+", encoding="utf8", newline="") as file:
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

                elif self.dictionary["command"] == "usersel":
                    #!######################3
                    data = [self.dictionary["name"], self.dictionary["destinatary"]]
                    data.sort()
                    with open(
                        f"{self.file_path}{data[0]}_{data[1]}.db", "r"
                    ) as file:  # ? "a+" works for FileNotFoundError
                        msg_list = file.readlines()
                    self.command_send(client, "usersel", str(msg_list))
                    #! # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            elif self.dictionary["type"] == "broadcast":
                self.msg_send(self.dictionary["name"], self.dictionary["msg"], self.dictionary["destinatary"])

    def msg_send(self, name, msg, destinatary):
        dictionary = {"date": self.dictionary["date"], "name": name, "type": "broadcast", "msg": msg}
        for sock in self.clients:
            try:
                sock.send(str(dictionary).encode("utf8"))
            except ConnectionResetError as e:
                logger.error(f"{ConnectionResetError}: {e}")
        self.history.append(dictionary)
        data = [name, destinatary]
        data.sort()
        with open(f"{self.file_path}{data[0]}_{data[1]}.db", "a") as file:
            file.write(dictionary + "\n")

    def command_send(self, client: socket, command: str, arg: str = ""):
        if command == "history":
            dictionary = {"type": "command", "command": command, "history": arg}
        elif command == "userlist":
            dictionary = {"type": "command", "command": command, "users": arg}
        elif command == "usersel":
            dictionary = {"type": "command", "command": command, "msg_list": arg}
        else:
            dictionary = {"type": "command", "command": command}
        client.send(str(dictionary).encode("utf8"))


# ==========>> MAIN CODE <<========== #


HOST = ""
PORT = 33000

if __name__ == "__main__":
    logger = logging.getLogger()
    server = Server()

    server.socket.close()
