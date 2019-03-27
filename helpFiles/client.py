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


def getinfo():
    remote = input("Enter IP address of remote client: ")
    local = input("Enter IP address of local client: ")

    return remote, local


if __name__ == "__main__":
    threading.Thread(target=threaded_local_server, args=[]).start()
    print("Thread started")

    remote_ip, local_ip = getinfo()

    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", "C:/Users/chadm/Desktop/ftp", perm="elradfmw")
    authorizer.add_anonymous("C:/Users/chadm/Desktop/ftp", perm="elradfmw")

    host = local_ip
    port = 8021
    BUFFER_SIZE = 2000

    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClient.connect((host, port))

    init_message()
    time.sleep(2)
    send_file()
    time.sleep(1)
    search_file("hello")
    time.sleep(2)
    search_file("test")
    time.sleep(3)
    search_file("nothing")
    time.sleep(3)

    end()


