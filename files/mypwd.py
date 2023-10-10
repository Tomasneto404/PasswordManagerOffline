import functions
import database

functions.clr()
key = str(input("Secret key: "))
# key = functions.load_key()
functions.clr()
while True:

    print("""

    [Gestor de Contas - PEN]\n
    [Feito por: Tomás Neto em 2022]\n\n
    1 - Nova Conta\n
    2 - Ver Conta\n
    3 - Atualizar Conta\n
    4 - Eliminar conta\n
    5 - Procurar por Site\n
    0 - Sair\n

    """)

    cmd = input("> ")

    #try:
    if cmd == '1':
        functions.clr()
        functions.novaPassword(key)

    elif cmd == '2':
        functions.clr()
        functions.verConta(key)

    elif cmd == '3':
        functions.clr()
        functions.atualizarConta(key)

    elif cmd == '4':
        functions.clr()
        functions.eliminarPassword(key)

    elif cmd == '5':
        functions.clr()
        functions.procurar(key)

    else:
        functions.clr()
        database.conn.close()
        print("Base de dados fechada com sucesso!\nA sair...")
        functions.time.sleep(2)
        break

    #except:
        #functions.clr()
        #print("Ocorreu um erro.")
