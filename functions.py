import database_conn
from datetime import datetime
import os
from cryptography.fernet import Fernet
import time


def first_start():
    if database_conn.create_table() == 1:
        print("""
              This function is designed to be executed only once in the lifetime of the program.
              This functions creates the 'accounts' table in the database and shows your new secret key. After getting your new secret key open the main.py
              file and delete the first_start() function. Otherwise erros will occur.\n
              WARNING: Save carefully your secret key. Once lost is impossible to recover the encrypted data.
              """)
        
        print("Secret Key (copy only what is between quotes): {}".format(generate_key()))
    else:
        print("ERROR: Something went wrong. Try delete the database.db file and restart the process. \nDont forget to delete the first_start() function.\n")

def clr():
    os.system('cls')

def generate_key():
    return Fernet.generate_key()


def newAccount(key):
    f = Fernet(key)

    site = ""
    while site == "":
        site = str(input("SITE: "))

    clr()
    email = ""
    while email == "":
        email = str(input("EMAIL: "))

        if email:
            email = f.encrypt(email.encode())

    clr()
    username = str(input("USERNAME: "))
    if username:
        username = f.encrypt(username.encode())
    else:
        username = f.encrypt('NaN'.encode())
        
    clr()
    password = str(input("PASSWORD: "))
    if password:
        password = f.encrypt(password.encode())
    else:
        password = f.encrypt('NaN'.encode())
    

    clr()
    twofa = str(input("2FA: "))
    if twofa:
        twofa = f.encrypt(twofa.encode())
    else:
        twofa = f.encrypt('NaN'.encode())
    

    clr()
    twofa_app = str(input("2FA APP: "))
    if twofa_app:
        twofa_app = f.encrypt(twofa_app.encode())
    else:
        twofa_app = f.encrypt('NaN'.encode())

    clr()
    regist_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    last_seen = regist_date
    last_update = regist_date

    database_conn.c.execute("INSERT INTO accounts (site, email, username, password, twofa, twofa_app, regist_date, last_seen, last_update) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (site, email, username, password, twofa, twofa_app, regist_date, last_seen, last_update))
    database_conn.conn.commit()
    clr()
    print("SUCCESS: New data was registed!\n")


def listAccounts():
    i = 1
    database_conn.c.execute("SELECT rowid, * FROM accounts")

    registers = database_conn.c.fetchall()

    if registers:
        print("{:<5} | {:<15} | {:<30} | {:<30} | {:<30} \n".format("ID", "SITE", "Registration Date", "Last Time Opened", "Last Update"))
       
        for regist in registers:
            print("{:<5} | {:<15} | {:<30} | {:<30} | {:<30} \n".format(regist[0], regist[1], regist[7], regist[8], regist[9]))

    else:
        print("ERROR: Registers not found.\n")
        i = 0

    return i



def verifyAccount(id):
    database_conn.c.execute("SELECT rowid, * FROM accounts")
    registers = database_conn.c.fetchall()
    database_conn.conn.commit()

    flag = 0

    for regist in registers:
        if id == regist[0]:
            flag = 1

    return flag



def deleteAccount():

    if listAccounts():
            
        print("Select ID to delete account\n")
        while True:
            id = int(input("ID: "))
                
            if (verifyAccount(id) == 0):
                print("ERROR: Account not found.")
            else:
                    
                flag = str(input("Are you sure you want to delete this account? (y/n) "))

                if flag == "y" or flag == "Y":
                    database_conn.c.execute("DELETE FROM accounts WHERE rowid = ?",(id,))
                    database_conn.conn.commit()
                    clr()
                    print("SUCCESS: Account deleted!\n")
                    break
                else:
                    break
    
   

                    
def seeAccount(key):

    if listAccounts():

        print("Select ID to see account\n")
        while True:
            id = int(input("ID: "))
            
            if (verifyAccount(id) == 0):
                print("ERROR: Account not found.")
            else:
                
                flag = str(input("Are you sure you want to see this account? (y/n) "))

                if flag == "y" or flag == "Y":
                    database_conn.c.execute("SELECT * FROM accounts WHERE rowid = ?",(id,))
                    database_conn.conn.commit()
                    registers = database_conn.c.fetchall()

                    f = Fernet(key)


                    print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format("Site", "Email", "Username", "Password", "2FA", "2FA APP", "Registration Date", "Last Time Opened", "Last Update"))
                    print("{:185} \n".format("-"*205))
                    for regist in registers:
                        print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format(regist[0], f.decrypt(regist[1]).decode(), f.decrypt(regist[2]).decode(), f.decrypt(regist[3]).decode(), f.decrypt(regist[4]).decode(), f.decrypt(regist[5]).decode(), regist[6], regist[7], regist[8]))
                        database_conn.c.execute("UPDATE accounts SET last_seen = ? WHERE rowid = ?",(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),id,))
                        database_conn.conn.commit()
                        time.sleep(5)
                        clr()

                    break
                else:
                    break
    

def updateAccount(key):
    if listAccounts():

        print("Select ID to update account\n")
        while True:
            id = int(input("ID: "))
            
            if (verifyAccount(id) == 0):
                print("ERROR: Account not found.")
            else:
                
                flag = str(input("Are you sure you want to update this account? (y/n) "))

                if flag == "y" or flag == "Y":
                    database_conn.c.execute("SELECT * FROM accounts WHERE rowid = ?",(id,))
                    database_conn.conn.commit()
                    registers = database_conn.c.fetchall()

                    f = Fernet(key)

                    for regist in registers:
                        clr()
                        print("\nActual site: {}\n".format(regist[0]))
                        at_site = str(input("Update site? (y/n) "))
                        
                        if at_site == "y" or at_site == "Y":
                            site = str(input("New site: "))
                        else:
                            site = regist[0]

                        
                        clr()
                        print("\nActual email: {}\n".format(f.decrypt(regist[1]).decode()))
                        at_email = str(input("Update email? (y/n) "))
                        
                        if at_email == "y" or at_email == "Y":
                            email = str(input("New email: "))
                            email = f.encrypt(email.encode())
                        else:
                            email = regist[1]

                        
                        clr()
                        print("\nActual username: {}\n".format(f.decrypt(regist[2]).decode()))
                        at_username = str(input("Update username? (y/n) "))
                        
                        if at_username == "y" or at_username == "Y":
                            username = str(input("New username: "))
                            username = f.encrypt(username.encode())
                        else:
                            if regist[2]:
                                username = regist[2]
                            else:
                                username = f.encrypt('NaN'.encode())

                        
                        clr()
                        print("\nActual password: {}\n".format(f.decrypt(regist[3]).decode()))
                        at_password = str(input("Update password? (y/n) "))
                        
                        if at_password == "y" or at_password == "Y":
                            i = 0
                            while i == 0:
                                password = str(input("New password: "))
                                confirm_password = str(input("Confirm password: "))

                                if password == confirm_password:
                                    password  = f.encrypt(password.encode())
                                    i = 1
                                else:
                                    print("ERROR: Passwords dont match.\n")

                        else:
                            password = regist[3]


                        
                        clr()
                        print("\nActual Two Factor Authenticator code: {}\n".format(f.decrypt(regist[4]).decode()))
                        at_twofa = str(input("Update 2FA? (y/n) "))
                        
                        if at_twofa == "y" or at_twofa == "Y":
                            twofa = str(input("New 2FA: "))
                            twofa = f.encrypt(twofa.encode())
                        else:
                            if regist[4]:
                                twofa = regist[4]
                            else:
                                twofa = f.encrypt('NaN'.encode())

                       
                        clr()
                        print("\nActual Two Factor Authenticator application: {}\n".format(f.decrypt(regist[5]).decode()))
                        at_twofaaap = str(input("Update 2FA App? (y/n) "))
                        
                        if at_twofaaap == "y" or at_twofaaap == "Y":
                            twofaaap = str(input("New 2FA App: "))
                            twofaaap = f.encrypt(twofaaap.encode())
                        else:
                            if regist[5]:
                                twofaaap = regist[5]
                            else:
                                twofaaap = f.encrypt('NaN'.encode())

                        database_conn.c.execute("UPDATE accounts SET site = ?, email = ?, username = ?, password = ?, twofa = ?, twofa_app = ?, last_update = ? WHERE rowid = ?",(site, email, username, password, twofa, twofaaap, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id,))
                        database_conn.conn.commit()
                        clr()
                        print("SUCCESS: Data was updated!\n")
                    break
                else:
                    break
                

def search(key):

    _input = 'a'    

    while _input == 'a':

        _input = input("Site > ")

        database_conn.c.execute("SELECT * FROM accounts WHERE site LIKE ?",(_input,))
        database_conn.conn.commit()
        registers = database_conn.c.fetchall()

        if registers:

            f = Fernet(key)


            print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format("Site", "Email", "Username", "Password", "2FA", "2FA APP", "Registration Date", "Last Time Opened", "Last Update"))
            print("{:185} \n".format("-"*205))
            for regist in registers:
                print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format(regist[0], f.decrypt(regist[1]).decode(), f.decrypt(regist[2]).decode(), f.decrypt(regist[3]).decode(), f.decrypt(regist[4]).decode(), f.decrypt(regist[5]).decode(), regist[6], regist[7], regist[8]))
                database_conn.c.execute("UPDATE accounts SET last_seen = ? WHERE Site LIKE ?",(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),_input,))
                database_conn.conn.commit()
                time.sleep(5)
                clr()

        else:
            print("ERROR: Registers not found for this search.\nLeaving...")
            time.sleep(3)
            clr()