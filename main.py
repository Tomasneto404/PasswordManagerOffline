from functions import *
from database_conn import *

clr()

first_start()

key = str(input("Secret key: "))


clr()
if key:
    while True:

        print("""

        [Developed by: Tomás Neto in 2022]\n\n
        1 - New Account\n
        2 - See Account\n
        3 - Update Account\n
        4 - Delete Account\n
        5 - Search Account\n
        0 - Quit\n

        """)

        cmd = input("> ")
        
        if cmd == '1':
            clr()
            newAccount(key)

        elif cmd == '2':
            clr()
            seeAccount(key)

        elif cmd == '3':
            clr()
            updateAccount(key)

        elif cmd == '4':
            clr()
            deleteAccount()

        elif cmd == '5':
            clr()
            search(key)

        else:
            clr()
            database_conn.conn.close()
            print("SUCCESS: Database closed!\nLeaving ...")
            time.sleep(2)
            break

else: 
    print("ERROR: Key was not inserted.")
