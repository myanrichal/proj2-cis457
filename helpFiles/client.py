# Python TCP Client A
import json
import socket
import time
import threading

import pyftpdlib.authorizers
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def threaded_local_server():
    handler = FTPHandler
    handler.authorizer = pyftpdlib.authorizers.DummyAuthorizer
    server = FTPServer(("127.0.0.1", 8021), handler)
    server.serve_forever()
    print("Will this ever print?")


def init_message():
    message = {
        "MessageType": "init",
        "Info":
            {"user": "clientA",
             "connectionSpeed": "ethernet",
             "hostname": "host",
             "portNumber": "port"}
    }
    tcpClient.send(json.dumps(message).encode('utf-8'))
    data_p = tcpClient.recv(BUFFER_SIZE)
    data = json.loads(data_p.decode('utf-8'))
    print(data)


def search_file(search_key):
    message = {
            "MessageType": "search",
            "searchKey": search_key
            }
    tcpClient.send(json.dumps(message).encode('utf-8'))
    data_p = tcpClient.recv(BUFFER_SIZE)
    data = json.loads(data_p.decode('utf-8'))
    print(data)


def send_file():
    message = {
        "MessageType": "file",
        "fileName": "clientA.txt",
        "Info": "contents of file"
    }
    f = open("clientA.txt", 'r')
    loader = f.read(1024)
    message["Info"] = loader
    tcpClient.send(json.dumps(message).encode('utf-8'))
    data_p = tcpClient.recv(BUFFER_SIZE)
    data = json.loads(data_p.decode('utf-8'))
    print(data)


def end():
    message = {
        "MessageType": "exit",
        "user": "clientA"
        }
    tcpClient.send(json.dumps(message).encode('utf-8'))
    data_p = tcpClient.recv(BUFFER_SIZE)
    data = json.loads(data_p.decode('utf-8'))
    print(data)
    tcpClient.close()


def getinput():
    return input("Enter 1 for Search\nEnter 2 for retrieve\nEnter 3 to exit\n")


# Retrieve a file from the server
# param - ftp connection
def retrieve(ftp):
    filename = input("Enter filename of file to retrieve: ")
    # create file to store retrieved data in
    try:
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR '+filename, localfile.write, 1024)
        localfile.close()
        print("File Retrieved \n\n")
    except IOError:
        print("Failure to retrieve file\n\n")
    except pyftpdlib.all_errors:
        print("Error: ftp error \n")


# Function to get FTP connection information from user
# return IP of server and port number
def welcome():
    print("Welcome to FTP client app\n")
    s_name = input("Please enter the server name: ")
    p_number = input("please enter the port number: ")
    return s_name, p_number


# Create client connection to server
# Param - IP and port of server
# return ftp connection
# To Do: Add try/catch for connection
def create_client(ip, p):
    ftp = pyftpdlib.FTP('')
    ftp.connect(ip, int(p))
    ftp.login()

    return ftp


if __name__ == "__main__":
    # initialize things that are important
    threading.Thread(target=threaded_local_server, args=[]).start()
    print("Thread for local server started")

    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", "C:/Users/chadm/Desktop/ftp", perm="elradfmw")
    authorizer.add_anonymous("C:/Users/chadm/Desktop/ftp", perm="elradfmw")

    host = socket.gethostname()
    port = 2004
    BUFFER_SIZE = 2000

    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClient.connect((host, port))

    time.sleep(1)

    init_message()
    send_file()

    userInput = getinput()
    while userInput != '3':
        if userInput == '1':
            search_file(input("\tEnter filename: "))

        elif userInput == '2':
            # implement ftp client to retrieve from other chadster client

            ftp_connection = None
            while ftp_connection is None:
                server_name, port_number = welcome()
                try:
                    ftp_connection = create_client(server_name, port_number)
                except pyftpdlib.all_errors:
                    print("Could not connect to server, try again\n")
                    ftp_connection = None

            retrieve(ftp_connection)

        userInput = getinput()

    end()
