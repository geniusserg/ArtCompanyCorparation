from tkinter import *
import driver

con = None
table_frame  =None
current_table =0
current_row=0
little_frame=None
input_frame=None
insert_args=[]
args=[]
header=[]

def trigger_little_panel(event):
    global little_frame
    global current_row
    global input_frame
    global header
    global insert_args
    if little_frame  is not None:
        for i in little_frame.grid_slaves():
            i.destroy()
        little_frame.destroy()
    little_frame = Frame()
    little_frame.configure(width=350, height=300, bg="blue")
    little_frame.place(x=400, y=300)
    current_row = event.widget.cget("text")
    delete_button = Button(little_frame, text='Delete ID '+str(current_row), font=2, bg="red")
    delete_button.bind('<Button-1>', trigger_delete)
    delete_button.place(x=0, y=0)
    header = []
    insert_args=[]
    if current_table == "pictures":
        header = ["Name", "Artist", "Price"]
    if current_table == "orders":
        header = ["Picture ID", "Address ID"]
    if current_table == "delivery":
        header = ["Address", "Price"]
    for i in range(len(header)):
        find_label = Label(little_frame, text=header[i] + ":")
        find_entry = Entry(little_frame)
        find_entry.place(x=70, y=40 + 22 * i)
        find_label.place(x=0, y=40 + 22 * i)
        insert_args.append(find_entry)
    accept_button = Button(little_frame,text="update row "+str(current_row))
    accept_button.place(x=0, y=110)
    accept_button.bind('<Button-1>', trigger_update)

def create_table(data, table):
    global current_table
    current_table = table
    global table_frame
    global little_frame
    global input_frame
    if table_frame is not None:
        for i in table_frame.grid_slaves():
            i.destroy()
        table_frame.destroy()
        table_frame = None
    if little_frame is not None:
        for i in little_frame.grid_slaves():
            i.destroy()
        little_frame.destroy()
        little_frame = None
    if input_frame is not None:
        for i in input_frame.grid_slaves():
            i.destroy()
        input_frame.destroy()
        input_frame = None
    table_frame = Frame()
    table_frame.configure(width=400, height=700, bg="white")
    table_frame.place(x=0, y=0)
    header=[]
    if table == "pictures":
        header = ["ID", "Name", "Artist", "Price"]
    if table == "orders":
        header = ["ID", "Picture ID", "Address ID", "Price"]
    if table == "delivery":
        header = ["ID", "Address", "Price"]
    for i in range(len(header)):
        l = Label( table_frame)
        l.configure(width=56 // len(header), height=1, bg="red", text=str(header[i]))
        l.place(x=i*(400 // len(header)), y=0)
    for i in range(0,len(data)):
        b_id = Button(table_frame)
        b_id.configure(width=56 // len(data[i]), height=1, bg="white", text=str(data[i][0]))
        b_id.bind('<Button-1>', trigger_little_panel)
        b_id.place(x=0, y=(i+1)*20)
        for j in range(1, len(data[i])):
            l = Label( table_frame)
            l.configure(width=56//len(data[i]), height=1, bg="white", text=str(data[i][j]))
            l.place(x=j*(400 // len(header)), y=(i+1)*20)
    input_table()

def input_table():
    global con
    global current_table
    global input_frame
    global insert_args
    input_frame = Frame()
    input_frame.configure(width=250, height=130, bg="white")
    input_frame.place(x=400, y=120)
    header = []
    if current_table == "pictures":
        header = ["ID", "Name", "Artist", "Price"]
    if current_table == "orders":
        header = ["ID", "Picture ID", "Address ID"]
    if current_table == "delivery":
        header = ["ID", "Address", "Price"]
    insert_args = []
    for i in range(len(header)):
        find_label = Label(input_frame, text=header[i]+":")
        find_entry = Entry(input_frame)
        find_entry.place(x=60, y=10+20*i)
        find_label.place(x=0, y=10+20*i)
        insert_args.append(find_entry)
    accept_button = Button(input_frame,text="insert into "+current_table)
    accept_button.place(x=0, y=100)
    accept_button.bind('<Button-1>', trigger_insert)


def trigger_delete(event):
    global con
    global current_table
    global current_row
    driver.delete_row(con, current_table, current_row)
    create_table(driver.output_table(con, current_table), current_table) #update

def trigger_update(event):
    global con
    global current_table
    global insert_args
    global header
    inp=[current_row]
    for i in insert_args:
        inp.append(i.get())
    driver.insert_table(con, current_table, inp)
    create_table(driver.output_table(con, current_table), current_table)  # update

def trigger_cleare_all(event):
    global con
    global current_table
    driver.clear_db(con)
    create_table(driver.output_table(con, current_table), current_table)  # update

def trigger_cleare(event):
    global con
    global current_table
    driver.clear_table(con, current_table)
    create_table(driver.output_table(con, current_table), current_table) #update

def trigger_insert(event):
    global con
    global current_table
    global insert_args
    inp=[]
    for i in insert_args:
        inp.append(i.get())
    driver.insert_table(con, current_table, inp)
    create_table(driver.output_table(con, current_table), current_table)  # update

def trigger_fill_table(event): #TODO
    global con
    create_table(driver.output_table(con, event.widget.cget("text")), event.widget.cget("text"))

def trigger_find_picture(event): #TODO
    global con
    create_table(driver.find(con, event.widget.get()), 'pictures')

def create_button_panel():
    global current_table
    picture_button = Button(text='pictures', font=5)
    orders_button = Button(text='orders', font=5)
    delivery_button = Button(text='delivery', font=5)
    picture_button.place(x=400, y=0)
    orders_button.place(x=500, y=0)
    delivery_button.place(x=600, y=0)
    picture_button.bind('<Button-1>', trigger_fill_table)
    orders_button.bind('<Button-1>', trigger_fill_table)
    delivery_button.bind('<Button-1>', trigger_fill_table)
    clear_db = Button(text="clear all tables")
    clear_db.bind('<Button-1>', trigger_cleare_all)
    if current_table in ['pictures','orders','delivery']:
        clear_tab = Button(text="clear current table")
        clear_tab.bind('<Button-1>', trigger_cleare)
        clear_tab.place(x=400, y=50)
        clear_tab = Button(text="clear all tables")
        clear_tab.bind('<Button-1>', trigger_cleare_all)
        clear_tab.place(x=500, y=50)
        find_label = Label(text='Search Picture by Name')
        find_entry = Entry()
        find_entry.bind('<Return>', trigger_find_picture)
        find_entry.place(x=480, y=75)
        find_label.place(x=400, y=75)


def main(db, login, password, entrypoint_root):
    global con
    global table_frame
    global little_frame
    entrypoint_root.destroy()
    table_frame=None
    little_frame = None
    try:
        con = driver.connect_database(db, login, password)
    except:
        return 1
    root = Tk()
    root.geometry("700x500+30+30")
    create_table([], 'orders')
    create_button_panel()
    root.mainloop()