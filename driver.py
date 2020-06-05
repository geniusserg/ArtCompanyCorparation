import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

global commands


def load_functions():
    global commands
    commands = {}
    for i in os.listdir(path=os.getcwd()+"\\sql"):
        command = ""
        file = open(os.getcwd()+"\\sql\\" + i, "r")
        func = i.split(".")[0]
        for j in file:
            command = command + j + '\n'
        commands[func] = command


def create_database(name, login, password):
    result = False
    global commands
    load_functions()
    database_name = name
    login = login
    password = password
    con = psycopg2.connect(
        database="postgres",
        user=login,
        password=password,
        host="127.0.0.1",
        port="5432"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("select * from current_database()")
    except():
        print("Error connect db postgres")
        return
    try:
        cur.execute("call create_database('" + database_name + "','" + password + "');")
    except:
        print("already exists!!!")
        return
    cur.close()
    con = psycopg2.connect(
        database=database_name,
        user=login,
        password=password,
        host="127.0.0.1",
        port="5432"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("select * from current_database()")
    except():
        print("Error creation db")
        return 1
    cur.execute(commands["create_tables"])
    cur.execute("call create_tables()")
    for i in commands:
        cur.execute(commands[i])
    cur.close()
    return 0


def install_functions_create_delete_db(login, password):
    con = psycopg2.connect(
        database="postgres",
        user=login,
        password=password,
        host="127.0.0.1",
        port="5432"
    )
    load_functions()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("select * from current_database()")
    except():
        print("Error connect to postgres db")
        return None
    try:
        cur.execute(commands["create_db"])
        cur.execute(commands["delete_db"])
        cur.execute("call install_dblink()")
    except:
        print("Already installed")
        return None
    return 0


def connect_database(name, login, password):
    con = psycopg2.connect(
        database=name,
        user=login,
        password=password,
        host="127.0.0.1",
        port="5432"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("select * from current_database()")
    except():
        print("Error connect db" + name)
        return None
    return con


def output_table(con, name):
    cs = con.cursor()
    try:
        cs.execute("select output_" + name + "()")
    except:
        return None
    result = cs.fetchall()
    ret = []
    for i in result:
        ret.append(list(i[0].replace('(', '').replace(')', '').split(",")))
    return ret


def insert_table(con, name, args):
    cs = con.cursor()
    command = "call insert_" + name + "("
    for i in args:
        if type(i) == str:
            command = command + "'" + str(i) + "',"
        else:
            command = command + str(i) + ","
    command = command[:-1] + ");"
    try:
        cs.execute(command)
    except:
        return 1
    return 0


def delete_row(con, name, id):
    cs = con.cursor()
    try:
        cs.execute("call delete_record(\'" + name + "\'," + id + ");")
    except:
        return 1
    return 0


def find(con, picture_name):
    cs = con.cursor()
    try:
        cs.execute("select find(\'" + picture_name + "\');")
    except:
        print('cant perform search')
    try:
        result = cs.fetchall()
    except:
        return []
    ret = []
    for i in result:
        ret.append(list(i[0].replace('(', '').replace(')', '').split(",")))
    return ret


def clear_table(con, name):
    cs = con.cursor()
    try:
        cs.execute("call clear(\'" + name + "\');")
    except:
        print("cant clear table" + name)
        return 1
    return 0


def clear_db(con):
    cs = con.cursor()
    try:
        cs.execute("call clear_all_tables();")
    except:
        print("cant clear tables")
        return 1
    return 0


def delete_database(name, login, password):
    con_del = connect_database("postgres", login, password)
    cs = con_del.cursor()
    cs.execute("call delete_database(\'" + name + "\',\'" + password + "\');")
    try:
        con_del = connect_database(name, login, password)
    except:
        return 0
    print("cant delete db, sorry")
    return 1


def output_databases(con):
    cs = con.cursor()
    try:
        cs.execute("select output_databases()")
    except:
        return None
    result = cs.fetchall()
    ret = []
    for i in result:
        ret.append(list(i[0].replace('(', '').replace(')', '').split(",")))
    return ret





if __name__ == '__main__':
    # create_database('gr', 'vasya', 'vasya')
    con = connect_database('gr', 'vasya', 'vasya')
    insert_table(con, "pictures", [2, 'art1', 'Arts', 250])
    for i in output_table(con, 'pictures'):
        print(i)