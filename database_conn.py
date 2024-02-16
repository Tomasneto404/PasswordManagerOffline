import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

def create_table():
    
    try:
        flag = c.execute("""

                CREATE TABLE accounts ( 
                    site TEXT,
                    email TEXT,
                    username TEXT,
                    password TEXT,
                    twofa TEXT,
                    twofa_app TEXT,
                    regist_date TEXT,
                    last_seen TEXT,
                    last_update TEXT
                )
                
            """)
        
        conn.commit()
        
        if flag:
            return 1
        else:
            return 2
        
    except:
        return 0
    
    


