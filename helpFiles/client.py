# Python TCP Client A
import socket
import json
import time


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
    l = f.read(1024)
    message["Info"] = (l)
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


host = socket.gethostname()
port = 2004
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
