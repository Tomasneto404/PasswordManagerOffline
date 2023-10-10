import sqlite3
import database
from datetime import date, datetime
import os
from tabulate import tabulate
from cryptography.fernet import Fernet
import time


def clr():
    os.system('cls')

def write_key():
    key = Fernet.generate_key() # Generates the key
    with open("key.key", "wb") as key_file: # Opens the file the key is to be written to
        key_file.write(key) # Writes the key

def load_key():
    return open("key.key", "rb").read() #Opens the file, reads and returns the key stored in the file


def novaPassword(key):
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
    data_registo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    last_seen = data_registo
    last_update = data_registo
    

    #Comando
    database.c.execute("INSERT INTO contas (site, email, username, password, twofa, twofa_app, data_registo, last_seen, last_update) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (site, email, username, password, twofa, twofa_app, data_registo, last_seen, last_update))
    #Enviar comando
    database.conn.commit()
    clr()
    print("Dados registados com sucesso!\n")


def listarPasswords():
    i = 1
    database.c.execute("SELECT rowid, * FROM contas")

    #key = load_key()
    #f = Fernet(key)

    registos = database.c.fetchall()

    if registos:
        print("{:<5} | {:<15} | {:<30} | {:<30} | {:<30} \n".format("ID", "SITE", "Data Registo", "Última vez visto", "Último Update"))
        #print (tabulate(registos, headers=["Id", "Site", "Email", "Password","Username", "2FA", "2FA App", "Data Registo", "Ultima Vez Aberto"]))
        for registo in registos:
            #password = f.decrypt(registo[4])
            #print(password)
            print("{:<5} | {:<15} | {:<30} | {:<30} | {:<30} \n".format(registo[0], registo[1], registo[7], registo[8], registo[9]))

    else:
        print("Não existem registos.\n")
        i = 0

    return i



def verificaConta(id):
    database.c.execute("SELECT rowid, * FROM contas")
    registos = database.c.fetchall()
    database.conn.commit()

    verifica = 0

    for registo in registos:
        if id == registo[0]:
            verifica = 1

    return verifica



def eliminarPassword(key):

    if key:

        if listarPasswords():
            
            print("Selecione o id para eliminar password\n")
            while True:
                id = int(input("ID: "))
                
                if (verificaConta(id) == 0):
                    print("Esta conta não existe.")
                else:
                    
                    verifica = str(input("Tem a certeza que quer eliminar esta conta? (y/n) "))

                    if verifica == "y" or verifica == "Y":
                        database.c.execute("DELETE FROM contas WHERE rowid = ?",(id,))
                        database.conn.commit()
                        clr()
                        print("Conta eliminada com sucesso!\n")
                        break
                    else:
                        break
    
    else:
        print("Impossível eliminar conta sem 'Secret key' ")

                    
def verConta(key):

    if listarPasswords():

        print("Selecione o id para ver password\n")
        while True:
            id = int(input("ID: "))
            
            if (verificaConta(id) == 0):
                print("Esta conta não existe.")
            else:
                
                verifica = str(input("Tem a certeza que quer ver esta conta? (y/n) "))

                if verifica == "y" or verifica == "Y":
                    database.c.execute("SELECT * FROM contas WHERE rowid = ?",(id,))
                    database.conn.commit()
                    registos = database.c.fetchall()

                    f = Fernet(key)


                    print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format("Site", "Email", "Username", "Password", "2FA", "2FA APP", "Data Registo", "Última vez visto", "Último Update"))
                    print("{:185} \n".format("-"*205))
                    for registo in registos:
                        print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format(registo[0], f.decrypt(registo[1]).decode(), f.decrypt(registo[2]).decode(), f.decrypt(registo[3]).decode(), f.decrypt(registo[4]).decode(), f.decrypt(registo[5]).decode(), registo[6], registo[7], registo[8]))
                        database.c.execute("UPDATE contas SET last_seen = ? WHERE rowid = ?",(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),id,))
                        database.conn.commit()
                        time.sleep(5)
                        clr()

                    break
                else:
                    break
    

def atualizarConta(key):
    if listarPasswords():

        print("Selecione o id para atualizar dados\n")
        while True:
            id = int(input("ID: "))
            
            if (verificaConta(id) == 0):
                print("Esta conta não existe.")
            else:
                
                verifica = str(input("Tem a certeza que quer atualizar esta conta? (y/n) "))

                if verifica == "y" or verifica == "Y":
                    database.c.execute("SELECT * FROM contas WHERE rowid = ?",(id,))
                    database.conn.commit()
                    registos = database.c.fetchall()

                    f = Fernet(key)

                    for registo in registos:
                        #Atualizar Site
                        clr()
                        print("\nSite atual: {}\n".format(registo[0]))
                        at_site = str(input("Deseja atualizar o Site? (y/n) "))
                        
                        if at_site == "y" or at_site == "Y":
                            site = str(input("Novo Site: "))
                        else:
                            site = registo[0]

                        #Atualizar Email
                        clr()
                        print("\nEmail atual: {}\n".format(f.decrypt(registo[1]).decode()))
                        at_email = str(input("Deseja atualizar o Email? (y/n) "))
                        
                        if at_email == "y" or at_email == "Y":
                            email = str(input("Novo Email: "))
                            email = f.encrypt(email.encode())
                        else:
                            email = registo[1]

                        #Atualizar Username
                        clr()
                        print("\nUsername atual: {}\n".format(f.decrypt(registo[2]).decode()))
                        at_username = str(input("Deseja atualizar o Username? (y/n) "))
                        
                        if at_username == "y" or at_username == "Y":
                            username = str(input("Novo Username: "))
                            username = f.encrypt(username.encode())
                        else:
                            if registo[2]:
                                username = registo[2]
                            else:
                                username = f.encrypt('NaN'.encode())

                        #Atualizar Password
                        clr()
                        print("\nPassword atual: {}\n".format(f.decrypt(registo[3]).decode()))
                        at_password = str(input("Deseja atualizar a Password? (y/n) "))
                        
                        if at_password == "y" or at_password == "Y":
                            i = 0
                            while i == 0:
                                password = str(input("Nova Password: "))
                                confirm_password = str(input("Confirmar Password: "))

                                if password == confirm_password:
                                    password  = f.encrypt(password.encode())
                                    i = 1
                                else:
                                    print("Passwords não são iguais.\n")

                        else:
                            password = registo[3]


                        #Atualizar 2fa
                        clr()
                        print("\n2FA atual: {}\n".format(f.decrypt(registo[4]).decode()))
                        at_twofa = str(input("Deseja atualizar o 2FA? (y/n) "))
                        
                        if at_twofa == "y" or at_twofa == "Y":
                            twofa = str(input("Novo 2FA: "))
                            twofa = f.encrypt(twofa.encode())
                        else:
                            if registo[4]:
                                twofa = registo[4]
                            else:
                                twofa = f.encrypt('NaN'.encode())

                        #Atualizar 2fa
                        clr()
                        print("\n2FA App atual: {}\n".format(f.decrypt(registo[5]).decode()))
                        at_twofaaap = str(input("Deseja atualizar o 2FA App? (y/n) "))
                        
                        if at_twofaaap == "y" or at_twofaaap == "Y":
                            twofaaap = str(input("Novo 2FA App: "))
                            twofaaap = f.encrypt(twofaaap.encode())
                        else:
                            if registo[5]:
                                twofaaap = registo[5]
                            else:
                                twofaaap = f.encrypt('NaN'.encode())

                        database.c.execute("UPDATE contas SET site = ?, email = ?, username = ?, password = ?, twofa = ?, twofa_app = ?, last_update = ? WHERE rowid = ?",(site, email, username, password, twofa, twofaaap, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id,))
                        database.conn.commit()
                        clr()
                        print("Dados atualizados com sucesso!\n")
                    break
                else:
                    break
                

def procurar(key):

    _input = 'a'    

    while _input == 'a':

        _input = input("Site > ")

        database.c.execute("SELECT * FROM contas WHERE site LIKE ?",(_input,))
        database.conn.commit()
        registos = database.c.fetchall()

        if registos:

            f = Fernet(key)


            print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format("Site", "Email", "Username", "Password", "2FA", "2FA APP", "Data Registo", "Última vez visto", "Último Update"))
            print("{:185} \n".format("-"*205))
            for registo in registos:
                print("{:<15} | {:<25} | {:<15} | {:<20} | {:<10} | {:<10} | {:<30} | {:<30} | {:<30} \n".format(registo[0], f.decrypt(registo[1]).decode(), f.decrypt(registo[2]).decode(), f.decrypt(registo[3]).decode(), f.decrypt(registo[4]).decode(), f.decrypt(registo[5]).decode(), registo[6], registo[7], registo[8]))
                database.c.execute("UPDATE contas SET last_seen = ? WHERE Site LIKE ?",(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),_input,))
                database.conn.commit()
                time.sleep(5)
                clr()

        else:
            print("Não foram encontrados registos para esta pesquisa.\nA sair...")
            time.sleep(3)
            clr()