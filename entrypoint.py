from tkinter import *
import driver
import ui
import database_entry
root = None
login = None
password = None


def trigger_install(event):
    global login
    global password
    if driver.install_functions_create_delete_db(login.get(), password.get()) == 0:
        event.widget.configure(bg="green")
        print("Successfully installed")
    else:
        print("cannot install application. Please, contact to admin")
        event.widget.configure(bg="red")

def trigger_auth(event):
    global root
    global login
    global password
    res = database_entry.main(login.get(), password.get(), root)
    if res == 1:
        print('cant successfully connect to database')

if __name__ == "__main__":
    root = Tk()
    root.geometry("490x200+30+30")
    label_welcome = Label(text="Welcome to Paint Company Inc. databases manager", font=3, bg="yellow")
    label_welcome.place(x=0, y=0)
    login_label = Label(text="login:")
    login_label.place(x=10, y=30)
    login = Entry(root)
    login.place(x=10, y=50)
    password = Entry(root, show="*")
    pass_label = Label(text="password:")
    pass_label.place(x=10, y=80)
    password.place(x=10, y=100)
    auth = Button(text="GO!", bg="red", font=3)
    auth.place(x=10, y=120)
    auth.bind('<Button-1>', trigger_auth)
    install = Button(text="Install application on database (You should be superuser to do it!)")
    install.place(x=10, y=160)
    install.bind('<Button-1>', trigger_install)
    root.mainloop()
