import sqlite3

connect_flag = False
__connection = None


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('db.db') as conn:
            res = func(conn, *args, **kwargs)
        return res

    return inner


@ensure_connection
def add_sms(conn, sms: str):
    c = conn.cursor()
    c.execute('INSERT INTO test (text) VALUES(?)', [sms])
    conn.commit()


@ensure_connection
def create_user(conn, id: int):
    c = conn.cursor()
    c.execute('INSERT INTO main (id, sms_1, secret, sms_2, aut_decryption) VALUES(?, ?, ? ,?, ?)',
              [id, 'sms', 'sms', 'sms', 0])

    c.execute('INSERT INTO passwords (id, password, flag) VALUES(?, ?, ?)', [id, '444', 1])
    conn.commit()


@ensure_connection
def change_sms_1(conn, id: int, sms: str):
    c = conn.cursor()
    c.execute('''UPDATE main SET sms_1 = (?) WHERE id = (?)''', [sms, id])
    conn.commit()


@ensure_connection
def change_sms_2(conn, id: int, sms: str):
    c = conn.cursor()
    c.execute('''UPDATE main SET sms_2 = (?) WHERE id = (?)''', [sms, id])
    conn.commit()


@ensure_connection
def change_secret(conn, id: int, sms: str):
    c = conn.cursor()
    c.execute('''UPDATE main SET secret = (?) WHERE id = (?)''', [sms, id])
    conn.commit()


@ensure_connection
def change_aut_decryption(conn, id: int):
    c = conn.cursor()
    c.execute('''SELECT aut_decryption FROM main WHERE id = (?)''', [id])
    flag = int(c.fetchall()[0][0])

    c.execute('''UPDATE main SET aut_decryption = (?) WHERE id = (?)''', [(flag + 1) % 2, id])
    conn.commit()
    if flag == 0:
        return True
    return False


@ensure_connection
def add_new_password(conn, id: int, password: str):
    c = conn.cursor()
    c.execute('''SELECT password FROM passwords WHERE id = (?)''', [id])
    arr = c.fetchall()[0]
    if password not in arr:
        c.execute('INSERT INTO passwords (id, password, flag) VALUES(?, ?, ?)', [id, password, 0])
        conn.commit()
        return True
    return False


@ensure_connection
def return_passwords(conn, id: int, flag: int):
    c = conn.cursor()
    c.execute('''SELECT password FROM passwords WHERE id = (?) and flag >= (?)''', [id, flag])
    arr = []
    for i in c.fetchall():
        arr.append(i[0])
    # print(arr)
    return arr



@ensure_connection
def delete_password(conn, id: int, password: str):
    c = conn.cursor()
    c.execute('''SELECT password FROM passwords WHERE id = (?)''', [id])
    arr = list(c.fetchall())
    print('!!!')
    print(arr)
    if len(arr) > 1:
        c.execute('''DELETE FROM passwords WHERE id = (?) and password = (?)''', [id, password])
        conn.commit()
        return True
    return False


@ensure_connection
def change_password_flag(conn, id: int, password: str):
    c = conn.cursor()
    c.execute('''SELECT flag FROM passwords WHERE id = (?) and password = (?)''', [id, password])
    flag = int(c.fetchall()[0][0])
    print(flag)

    c.execute('''UPDATE passwords SET flag = (?) WHERE id = (?) and password = (?)''', [(flag + 1) % 2, id, password])
    conn.commit()


@ensure_connection
def return_sms(conn, id:int):
    c = conn.cursor()
    c.execute('''SELECT sms_1, secret, sms_2, aut_decryption FROM main WHERE id = (?)''', [ id])
    arr = c.fetchall()
    return list(arr[0])
