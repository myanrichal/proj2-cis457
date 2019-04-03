# proj2-cis457
This project is composed of 2 main files: client.py and server.py

Clinet.py hosts an ftp server and connects to a centralized server. 

Server.py hosts an TCP server and allows multiple clients to connect. 

How the program works:

The current configuration of the program looks for files in the current directory. It is assumed there is a file in each directory titled clientA.txt and clientB.txt. These files state which files the client has and a description about the files. These files should also be present in the current directory. 

Client.py assumes there are 2 clients, A and B, and their information is already stored. The program will ask if you are A or B and assign information based on client name. Upon picking A or B the client will sign in with the centralized server and send the sever its file descriptions file. The client then has the option to search for a file description, retrieve a file, or quit. To search for a file the user enters a keyword they are interested. The server will return file information about any description that matches the word. The user can then use this list to retrieve a certain file. The retrieve functions uses the other clients FTP server to retrieve a file. Upon exit, all client information relating to the client in the centralized server is erased. 

Server.py always looks for new clients. Upon the addition of a new client the server spawns a new thread to deal with the client. If the client quits, the conenction and thread are closed. 