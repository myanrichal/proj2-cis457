# Python TCP Client A
import json
import socket
import time
import threading
import ftplib

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer




def init_message():
    message = {
        "MessageType": "init",
        "Info":
            {"user": user,
             "connectionSpeed": connection,
             "hostname": hostname,
             "portNumber": portU}
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
    for m in range(len(data)):
        print(data[m])
    return data


def send_file():
    message = {
        "MessageType": "file",
        "fileName": filename,
        "Info": "contents of file"
    }
    f = open(filename, 'r')
    loader = f.read(1024)
    message["Info"] = loader
    tcpClient.send(json.dumps(message).encode('utf-8'))
    data_p = tcpClient.recv(BUFFER_SIZE)
    data = json.loads(data_p.decode('utf-8'))
    print(data)


def end():
    message = {
        "MessageType": "exit",
        "user": user
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
def retrieve(ftp, name):
    try:
        localfile = open(name, 'wb')
        ftp.retrbinary('RETR '+name, localfile.write, 1024)
        localfile.close()
        print("File Retrieved \n\n")
    except IOError:
        print("Failure to retrieve file\n\n")
    except ftplib.all_errors:
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
    ftp = ftplib.FTP('')
    ftp.connect(ip, int(p))
    ftp.login()
    return ftp


if __name__ == "__main__":

    authorizer = DummyAuthorizer()
    fileMatches = []
    response = input("Are you client A or B?")
    if response.upper() == "A":
        print("Welcome client A\n")
        client = 1
        hostname = "127.0.0.2"
        portU = 8021
        user = "clientA"
        connection = "ethernet"
        filename = "clientA.txt"
    else:
        print("Welcome client B\n")
        client = 2
        hostname = "127.0.0.3"
        portU = 7021
        user = "clientB"
        connection = "T1"
        filename = "clientB.txt"

    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer((hostname, portU), handler)
    print("Thread for local server starting...")
    # start the thread for the local ftp server to transmit files
    thread_server=threading.Thread(target=server.serve_forever).start()

    if user == "clientA":
        authorizer.add_user("user", "12345", "C:/Users/JD/Desktop/CIS457/proj2-cis457/clientA", perm="elradfmw")
        authorizer.add_anonymous("C:/Users/JD/Desktop/CIS457/proj2-cis457/clientA", perm="elradfmw")

    else:
        authorizer.add_user("user", "12345", "C:/Users/JD/Desktop/CIS457/proj2-cis457/clientB", perm="elradfmw")
        authorizer.add_anonymous("C:/Users/JD/Desktop/CIS457/proj2-cis457/clientB", perm="elradfmw")

    host_centralServer = "localhost"
    port_centralServer = 2019
    BUFFER_SIZE = 1000

    print("Trying to connect to central server..\n")
    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClient.connect((host_centralServer, port_centralServer))

    time.sleep(1)

    init_message()
    send_file()
    userInput = getinput()
    while userInput != '3':
        correctMap = None

        if userInput == '1':
            fileMatches = search_file(input("\tEnter filename to search for: "))

        elif userInput == '2':
            # implement ftp client to retrieve from other chadster client
            r_filename = input("Which filename would you like to get?")

            for i in range(len(fileMatches)):
                match = fileMatches[i]
                if r_filename == match["filename"]:
                    correctMap = match
            if correctMap is None:
                print("File name not found, try search function again")
            else:
                m_fileName = correctMap["filename"]
                m_hostname = correctMap["hostname"]
                m_port = correctMap["portNumber"]

                ftp_connection = None
                try:
                    ftp_connection = create_client(m_hostname, m_port)
                    retrieve(ftp_connection, r_filename)
                    ftp_connection.quit()

                except ftplib.all_errors:
                    print("Could not connect to server, try again\n")
                    ftp_connection = None

        # fileMatches = []
        userInput = getinput()

    end()
    server.close()
