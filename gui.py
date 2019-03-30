from tkinter import *


class Chadster:
    def __init__(self, master):
        self.master = master
        master.title("Chadster Host")

        #Connection Box
        #row 1
        #row 2
        entry_serverHostName = Entry(master)
        entry_port = Entry(master)
        button_connect = Button(master, text="Connect")
        #row 3
        entry_username = Entry(master)
        entry_hostname = Entry(master)

        option_speed = StringVar(master)
        option_speed.set("one")
        entry_speed = OptionMenu(master, option_speed, "one", "two", "three")
        #row 4
        #skip
        #row 5
        entry_keyword = Entry(master)
        button_search = Button(master, text="Search")
        listbox_files = Listbox(master)
        listbox_files.insert(1, 'this')
        listbox_files.insert(2, 'that')
        

        entry_command = Entry(master)
        button_go = Button(master, text="Go")



        greet_button = Button(master, text="Greet", command=self.greet)
        close_button = Button(master, text="Close", command=master.quit)

        #connection
        #row 1
        Label(master, text="Connection").grid(row=1, column=2)
        #row 2
        Label(master, text="Server HostName").grid(row=2, column=1)
        entry_serverHostName.grid(row=2, column=2)
        Label(master, text="Port").grid(row=2, column=3)
        entry_port.grid(row=2, column=4)
        button_connect.grid(row=2, column=6)
        #row 3
        Label(master, text="Username").grid(row=3, column=1)
        entry_username.grid(row=3, column=2)
        Label(master, text="HostName").grid(row=3, column=3)
        entry_hostname.grid(row=3, column=4)
        Label(master, text="Speed").grid(row=3, column=5)
        entry_speed.grid(row=3, column=6)
        #row 4
        #skip
        Label(master, text=" ").grid(row=4, column=1)
        #row 5
        Label(master, text="Search").grid(row=5, column=2)
        #row 6
        Label(master, text="Keyword").grid(row=6, column=1)
        entry_keyword.grid(row=6, column=2)
        button_search.grid(row=6, column=4)
        #row 7
        listbox_files.grid(row=7, column=2)
        #row 8
        #skip
        Label(master, text=" ").grid(row=8, column=1)
        #row 9
        Label(master, text="FTP").grid(row=9, column=2)
        #row 10
        Label(master, text="Enter Command").grid(row=10, column=1)
        entry_command.grid(row=10, column=2)
        button_go.grid(row=10, column=4)



        

        close_button.grid(row=12, column=6)

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = Chadster(root)
root.mainloop()