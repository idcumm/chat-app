import socket

if __name__ == "__main__":
    # Defining Socket
    host = "127.0.0.1"
    port = 8080
    totalclient = int(input("Enter number of clients: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(totalclient)
    # Establishing Connections
    connections = []
    print("Initiating clients")
    for i in range(totalclient):
        conn = sock.accept()
        connections.append(conn)
        print("Connected with client", i + 1)

    fileno = 0
    idx = 0
    for conn in connections:
        # Receiving File Data
        idx += 1
        data = conn[0].recv(1024).decode()

        if not data:
            continue
        # Creating a new file at server end and writing the data
        while data:
            filename = "output" + str(fileno) + ".txt"
            fileno = fileno + 1
            fo = open(filename, "w")
            if not data:
                break
            else:
                fo.write(data)
                print()
                print("Receiving file from client", idx)
                print()
                print("Received successfully! New filename is:", filename)
                fo.close()
                data = conn[0].recv(1024).decode()

    # Closing all Connections
    for conn in connections:
        conn[0].close()
