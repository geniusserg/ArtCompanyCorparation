from tkinter import *
import driver
import ui

log = None
pas = None
root = None
con = None
label_list = None
database = None


def trigger_refresh(event):
    global con
    global label_list
    if label_list is not None:
        for i in label_list:
            i.destroy()
    label_list = []
    db_data = driver.output_databases(con)
    for i in range(len(db_data)):
        if db_data[i] == 'postgres' or db_data[i] == 'template0' or db_data[i] == 'template1':
            continue
        l_db = Button(text=db_data[i], bg="yellow")
        l_db.place(x=10, y=100 + i * 25)
        l_db.bind('<Button-3>', trigger_delete)
        l_db.bind('<Button-1>', trigger_connect)
        label_list.append(l_db)


def trigger_delete(event):
    global login
    global password
    res = driver.delete_database("postgres", log, pas)
    if res == 1:
        print('cant successfully delete database')


def trigger_create(event):
    global login
    global password
    res = driver.create_database(event.widget.cget("text"), log, pas)
    trigger_refresh(None)
    if res == 1:
        print('cant successfully create database')


def trigger_connect(event):
    global root
    global log
    global pas
    res = ui.main(event.widget.cget("text"), log, pas, root)
    if res == 1:
        print('cant successfully connect to database')


def main(login, password, entry_root):
    entry_root.destroy()
    global root
    global log
    global pas
    log=login
    pas=password
    root = Tk()
    global con
    try:
        con = driver.connect_database('postgres', login, password)
    except:
        return 1
    root.geometry("490x400+30+30")
    label_welcome = Label(text="Welcome to Paint Company Inc. databases manager", font=3, bg="yellow")
    label_welcome.place(x=0, y=0)
    label_create_db = Label(text='Create DataBase enter name')
    label_create_db.place(x=30, y=30)
    database = Entry(root)
    database.place(x=10, y=50)
    database.bind('<Return>', trigger_create)
    button_refresh = Button(text="refresh list of available databases", bg="red")
    button_refresh.place(x=10, y=70)
    button_refresh.bind('<Button-1>', trigger_refresh)
    root.mainloop()
