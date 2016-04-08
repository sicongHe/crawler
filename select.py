import sqlite3


def select():
    print('Your target:')
    target = input()
    try:
        if(target == 'no'):
            exit()
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("select * from user where name='%s'" % target)
        values = cursor.fetchall()
        cursor.close()
        conn.close()
        print(values)
    except BaseException:
        print('Can not find your target,please try again...')
        select()
    finally:
        select()

if __name__ == '__main__':
    select()
