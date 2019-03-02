import sqlite3


class DB:
    def __init__(self, database):
        conn = sqlite3.connect(database, check_same_thread=False)
        self.conn = conn
        
        UsersModel(self.conn).init_table()
        NewsModel(self.conn).init_table()
        FriendsModel(self.conn).init_table()
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()
    pass


class NewsModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
    
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()    
    
    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (title, content, str(user_id)))
        cursor.close()
        self.connection.commit()
    
    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row
     
    def get_all(self, user_id = None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?", (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows
    
    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()    
    pass


class UsersModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()
    
    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.execute("SELECT id FROM users WHERE user_name = ?", (str(user_name),))
        row = cursor.fetchone()
        cursor.close()
        self.connection.commit()
        return row[0]
        
    def get(self, user_id=None, user_name=None):
        if not (user_id or user_name): return False
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        elif user_name:
            cursor.execute("SELECT * FROM users WHERE user_name = ?", (str(user_name),))
        row = cursor.fetchone()
        return row
     
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    
    def get_all_ids(self):
        all_users = self.get_all()
        all_ids = map(lambda x: x[0], all_users)
        return list(all_ids)
    
    def get_name(self, user_id):
        return self.get(user_id)[1]
    
    def get_id(self, user_name):
        return self.get(user_name=user_name)[0]
    pass


class FriendsModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS friends 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             sub_id INTEGER,
                             author_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()
    
    def add_friend(self, sub_id, author_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO friends
                          (sub_id, author_id) 
                          VALUES (?,?)''', (sub_id, author_id))
        cursor.close()
        self.connection.commit()    
        
    def remove_friend(self, sub_id, author_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM friends WHERE sub_id = ? AND
        author_id = ?''', (str(sub_id), str(author_id)))
        cursor.close()
        self.connection.commit()
    
    def check_friendship(self, sub_id, author_id):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM friends WHERE sub_id = ? AND
        author_id = ?""", (str(sub_id), str(author_id)))
        row = cursor.fetchone()
        if row:
            return True
        return False
    
    def get_friends(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM friends WHERE sub_id = ?", (str(user_id),))
        row = cursor.fetchall()
        if row:
            return row
        return False        
    pass 


if __name__ == '__main__':
    base = DB("FLASK.db")
    n = NewsModel(base.get_connection())
    u = UsersModel(base.get_connection())
    f = FriendsModel(base.get_connection())