import flask
from flask import Flask, abort, jsonify, make_response, request
from Author import Author
from Book import Book


from DB.main import Database
class Bookshop:
    def __init__(self):  # constructor
        
        self.db = Database()

    def get(self, isbn):  # get book by id(isbn)
        return self.db.fetchOne("SELECT * FROM book WHERE isbn = ?",isbn)
        

    def add_book(self, book):  # adicionar um livro a lista books
        self.book = book
        self.author = self.book.get_author()
        

        query2 = "insert into author (first_name,middle_name,last_name) values (?,?,?)"
        cursor = self.db.insert(query2,(self.author['first_name'],self.author['middle_name'],self.author['last_name']))
        self.author = Author(cursor.lastrowid,self.author['first_name'],self.author['middle_name'],self.author['last_name'])
        self.author.id = cursor.lastrowid

        self.book = Book(book.isbn,book.title,book.price,cursor.lastrowid)
        query ="insert into book (isbn,title,price,author_id) values (?,?,?,?)"
        data = (self.book.isbn,self.book.title,self.book.price,self.author.id)
        self.db.insert(query,data)
        

        

    def delete_book(self, isbn):  # remover um livro po isbn
        query ="delete from book where isbn = ?"
        self.db.delete(query,isbn)
        #self.books = list(filter(lambda b: b.isbn != isbn, self.books))

    def update_book(self,isbn):
        self.isbn = isbn
        book = self.get(self.isbn)
        
        if book is None:
            abort(404)
        title = request.json['title']
        author = request.json['author_id']
        price = request.json['price']
        author_id = request.json['author_id']

        bookValues = ( title, price,author_id,self.isbn)
        query = "update book set title = ?, price = ?, author_id=? where isbn = ?"
        self.db.updateOne(query,bookValues)
        book = self.get(self.isbn)

        return book

    def getBookAuthor(self,author_id):
        row = list()
        #query = f"select * from book where author_id = (select id from author where id = {isbn})"
        query_name = self.db.fetchOne(f"SELECT first_name || ' '|| middle_name || ' '|| last_name FROM author WHERE id = ? ",author_id)
        if not query_name:
            abort(404,{"error":"author not found"})
        row.append({"author_name":query_name})
        query = f"SELECT title from book inner join author on book.author_id = author.id where author.id = {author_id}"
        row.append(self.db.fetch(query))
        return row

    def removeAuthorBooks(self, author_id):
        row = self.db.delete("DELETE FROM book WHERE author_id = ?",(author_id,))
        return row if row else abort(404,"Author not found")



    def countBooks(self):
        query = "SELECT COUNT(isbn) FROM book"
        row = self.db.fetch(query)
        return row

    def expensiveBook(self):
        query = "SELECT isbn,title, 'price' || ':'|| MAX(price) FROM book"
        row = self.db.fetch(query)
        return row 
