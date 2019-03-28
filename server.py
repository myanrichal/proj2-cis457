# CIS457 Project 2
# Server.py
# Program to create a multi-threaded TCP server
# Server will accept multiple clients and listens for certain messages to search for files

import socket
import threading
import json
import ast


# Multithreaded Python server
class ThreadedServer(object):

    # set up server
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((self.ip, self.port))

    # listen for clients
    def listen(self):
        self.tcpServer.listen(5)
        while True:
            try:
                client, address = self.tcpServer.accept()
                print("[+] New server socket thread started for :" + str(address))

                client.settimeout(60)
                # add each client to new thread
                threading.Thread(target=self.listenToClient, args=(client, address)).start()
            except socket.error:
                print("Error: could not connect to client")

    # thread to deal with client communication
    def listenToClient(self, client, address):
        while True:
            try:
                data_packed = client.recv(2048)
            except socket.error:
                print("Error, could not receive from client: ", address)
                client.close()
                return
            # look for valid return message
            if data_packed != b'':
                try:
                    data = json.loads(data_packed.decode('utf-8'))
                except ValueError:
                    print("Error with JSON decode")
                    return
                # add User to List with info
                if "init" == data["MessageType"]:
                    # message should already be in correct form, append to list
                    users_list.append(data["Info"])
                    return_message = {"Result": "Success"}
                    print("Update user List: ", users_list)

                # add file with file descriptions
                elif "file" == data["MessageType"]:
                    # create file for new file to be downloaded to
                    f = open(data["fileName"], 'w+')
                    # write transmitted data
                    f.write(data["Info"])
                    f.close()

                    # open description file and copy to array of dictionaries
                    str_file = open(data["fileName"]).read()
                    json_file = ast.literal_eval(str_file)
                    files = json_file["files"]
                    for i in range(len(files)):
                        file_description = files[i]
                        info = {"fileName": file_description["fileName"],
                                "fileDescription": file_description["fileDescription"],
                                "user": json_file["user"]}
                        file_list.append(info)
                    return_message={"Result": "Success"}
                    print("Update File List: ", file_list)
                # search for word in file descriptions
                elif "search" == data["MessageType"]:
                    search_word = data["searchKey"]
                    matching_files = []
                    # loop through files
                    for i in range(len(file_list)):
                        file = file_list[i]
                        description = file["fileDescription"]
                        # search for word in description
                        if search_word in description:
                            user_name = file["user"]
                            # loop for user information if match found
                            for a in range(len(users_list)):
                                users = users_list[a]
                                if user_name == users["user"]:
                                    keep = {"filename": file["fileName"],
                                            "hostname": users["hostname"],
                                            "connectionSpeed": users["connectionSpeed"],
                                            "portNumber":users["portNumber"]
                                            }
                                    matching_files.append(keep)
                    # array of dictionaries for matching file, [] if no match
                    return_message = matching_files

                # client wants to disconnect
                elif "exit" == data["MessageType"]:
                    remove_user = data["user"]
                    count = 0
                    # remove from file information
                    while count < (len(file_list)):
                        file = file_list[count]
                        user = file["user"]
                        if user == remove_user:
                            del (file_list[count])
                            count = 0
                        else:
                            count = count + 1
                    # remove from user list
                    for i in range(len(users_list)):
                        use = users_list[i]
                        if remove_user == use["user"]:
                            del users_list[i]
                    print("Update File List: ", file_list)
                    print("Update User List: ", users_list)
                    return_message = {"Result": "Success"}

                else:
                    return_message = {"Result": "Error"}
                # send response
                try:
                    client.send(json.dumps(return_message).encode('utf-8'))
                except ValueError:
                    print("Error: Can't send response..")
                    client.send(json.dumps({"Result": "Error"}).encode('utf-8'))


# Multithreaded Python server : TCP Server Socket Program
TCP_IP = '127.0.0.1'
TCP_PORT = 2019

# store user information
users_list = []
# store file information
file_list = []
ThreadedServer('', TCP_PORT).listen()

