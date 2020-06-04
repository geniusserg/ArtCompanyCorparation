from tkinter import *
import driver

con = None
table_frame  =0
current_table =0
current_row=0
little_frame=0
args=[]

def trigger_little_panel(event):
    global little_frame
    global current_row
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

def create_table(data, table):
    global current_table
    current_table = table
    global table_frame
    global little_frame
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

def trigger_delete(event):
    global con
    global current_table
    global current_row
    driver.delete_row(con, current_table, current_row)
    create_table(driver.output_table(con, current_table), current_table) #update

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
    driver.insert_table(con, current_table, insert_args)
    create_table(driver.output_table(con, current_table), current_table)  # update

def trigger_fill_table(event): #TODO
    global con
    create_table(driver.output_table(con, event.widget.cget("text")), event.widget.cget("text"))

def trigger_find_picture(event): #TODO
    global con
    create_table(driver.find(con, event.widget.get()), 'pictures')

def create_button_panel():
    picture_button = Button(text='pictures', font=5)
    orders_button = Button(text='orders', font=5)
    delivery_button = Button(text='delivery', font=5)
    picture_button.place(x=400, y=0)
    orders_button.place(x=500, y=0)
    delivery_button.place(x=600, y=0)
    picture_button.bind('<Button-1>', trigger_fill_table)
    orders_button.bind('<Button-1>', trigger_fill_table)
    delivery_button.bind('<Button-1>', trigger_fill_table)

    find_label = Label(text='Search Picture by Name')
    find_entry = Entry()
    find_entry.bind('<Return>', trigger_find_picture)
    find_entry.place(x=550, y=100)
    find_label.place(x=400, y=100)

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
    create_button_panel()
    root.mainloop()