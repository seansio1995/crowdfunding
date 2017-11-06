from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E

class reports:
    def __init__(self, master):
        self.master = master

class Login:
    def __init__(self, master):
        self.master = master
        master.title("File Download application")

        self.username_entry = ''
        self.password_entry = ''


        self.label1 = Label(master, text="File Download Login")
        self.label2 = Label(text="Username")
        self.label3 = Label(master, text="Password")
        vcmd = master.register(self.validate_user) # we have to wrap the command
        self.entry_user = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        vcmd1 = master.register(self.validate_pass) # we have to wrap the command
        self.entry_pass = Entry(master, validate="key", validatecommand=(vcmd1, '%P'))

        self.login_button = Button(master, text="Login", command=self.login)


        self.entry_user.grid(row=1, column=6, columnspan=10,sticky=E+W)
        self.entry_pass.grid(row=2, column=6, columnspan=10,sticky=E+W)
        self.login_button.grid(row = 3,column = 5,columnspan = 10)
        self.label3.grid(row=1, column = 0)
        self.label2.grid(row=2, column = 0)
        self.label1.grid(row=0,column = 5, columnspan = 10, sticky = W+E)

    def validate_user(self, new_text):
        if not new_text: # the field is being cleared
            self.username_entry = ''
            return True

        try:
            self.username_entry = new_text
            return True
        except ValueError:
            return False

    def validate_pass(self, new_text):
        if not new_text: # the field is being cleared
            self.password_entry = ''
            return True

        try:
            self.password_entry = new_text
            return True
        except ValueError:
            return False

    def login(self):
        #if statement checking if entered login information is correct
        root = Tk()
        my_gui = reports(root)
        root.mainloop()

root = Tk()
my_gui = Login(root)
root.mainloop()
