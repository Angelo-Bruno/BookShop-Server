from Author import Author
from DB.main import Database


database = Database()
class Book:
    def __init__(self, isbn, title, price,author): # book constructor 
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        
    
    def get_author(self):
        return self.author



    def __str__(self): #retornar string com infos de books
        return self.title + ' by ' + self.author_name + ' @ ' + str(self.price)