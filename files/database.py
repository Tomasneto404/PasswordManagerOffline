import bcrypt
import sqlite3

#ligação à base de dados
conn = sqlite3.connect("passdb.db")

#Criar cursor
c = conn.cursor()


#criar tabelas

# c.execute("""

#     CREATE TABLE contas ( 
#         site TEXT,
#         email TEXT,
#         username TEXT,
#         password TEXT,
#         twofa TEXT,
#         twofa_app TEXT,
#         data_registo TEXT,
#         last_seen TEXT,
#         last_update TEXT
#     )

# """)
# conn.commit()


#Inserir dados
#c.execute("INSERT INTO contas (site,email,username,password) VALUES ('www.test.pt', 'tomas@email.com', 'tomasneto36', '123wasd123')")

#Pesquisar na base de dados
# c.execute("SELECT * FROM contas")

# registos = c.fetchall()

# for registo in registos:
#     print(registo[0])

