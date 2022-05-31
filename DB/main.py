import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bookshop.sqlite3")

class Database:
    def __init__(self):
        self.db = os.path.join(BASE_DIR, "bookshop.sqlite3")
        self.connection = None
        self.getConnection()

    def getConnection(self):
        try:
            self.connection = sqlite3.connect(self.db,check_same_thread=False)
            print("Connection created")
        except sqlite3.Error as e:
            print(f"Error {e}")
            exit()

    def query(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def fetch(self,sql):
        rows=[]
        self.sql = sql
        cursor = self.query(self.sql)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetchOne(self, sql,id):
        cursor = self.connection.cursor()
        self.sql = sql
        cursor.execute(self.sql, (str(id),))
        row = cursor.fetchone()
        cursor.close()
        return row

    def insertmany(self, sql, data):
        cursor = self.connection.cursor()
        cursor.executemany(sql, data)
        self.connection.commit()
        cursor.close()


    def insert(self,sql,data):
        cursor = self.connection.cursor()
        self.sql = sql
        cursor.execute(self.sql, data)
        self.connection.commit()
        cursor.close()
        return cursor

    def execute(self,sql,data):
        cursor = self.connection.cursor()
        self.sql = sql
        cursor.execute(self.sql, data)
        self.connection.commit()
        cursor.close()

    def delete(self,sql, data):
        self.execute(sql,data)
        
    

    def updateOne(self,sql,data):
        self.execute(sql,data)


    def fetchAuthor(self,isbn):
        cursor = self.connection.cursor()
        self.sql = "select * from author where id = ?"
        cursor.execute(self.sql, (str(isbn),))
        row = cursor.fetchone()
        cursor.close()
        return row



#db.insert("INSERT INTO `books` (id,title, author, price) VALUES (? ,?, ?, ?)", ("2","The Lord of the Rings", "J.R.R. Tolkien", "19"))


