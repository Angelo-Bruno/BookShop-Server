import flask
from flask import Flask, abort, jsonify, make_response, request
from Artist import Artist
from Author import Author
from Book import Book
from CD import CD


from DB.main import Database


class Bookshop:
    def __init__(self):  # constructor

        self.db = Database()

    def get(self, isbn):  # get book by id(isbn)
        return self.db.fetchOne("SELECT * FROM book WHERE isbn = ?", isbn)

    def add_book(self, book):  # adicionar um livro a lista books
        self.book = book
        self.author = self.book.get_author()

        query2 = "insert into author (name) values (?)"
        cursor = self.db.insert(query2, (self.author['name'],))
        self.author = Author(cursor.lastrowid, self.author['name'])

        self.book = Book(book.isbn, book.title, book.price, cursor.lastrowid)
        query = "insert into book (isbn,title,price,author_id) values (?,?,?,?)"
        data = (self.book.isbn, self.book.title,
                self.book.price, self.author.id)
        self.db.insert(query, data)

    def delete_book(self, isbn):  # remover um livro po isbn
        query = "delete from book where isbn = ?"
        self.db.delete(query, isbn)
        #self.books = list(filter(lambda b: b.isbn != isbn, self.books))

    def update_book(self, isbn):
        self.isbn = isbn
        book = self.get(self.isbn)

        if book is None:
            abort(404)
        title = request.json['title']
        author = request.json['author_id']
        price = request.json['price']
        author_id = request.json['author_id']

        bookValues = (title, price, author_id, self.isbn)
        query = "update book set title = ?, price = ?, author_id=? where isbn = ?"
        self.db.updateOne(query, bookValues)
        book = self.get(self.isbn)

        return book

    def getBookAuthor(self, author_id):
        row = list()
        #query = f"select * from book where author_id = (select id from author where id = {isbn})"
        query_name = self.db.fetchOne(
            f"SELECT `name` FROM author WHERE id = ? ", author_id)
        if not query_name:
            abort(404, {"error": "author not found"})
        row.append({"author_name": query_name})
        query = f"SELECT title from book inner join author on book.author_id = author.id where author.id = {author_id}"
        row.append(self.db.fetch(query))
        return row

    def removeAuthorBooks(self, author_id):
        row = self.db.delete(
            "DELETE FROM book WHERE author_id = ?", (author_id,))
        return row if row else abort(404, "Author not found")

    def countBooks(self):
        query = "SELECT COUNT(isbn) FROM book"
        row = self.db.fetch(query)
        return row

    def expensiveBook(self):
        query = "SELECT isbn,title, 'price' || ':'|| MAX(price) FROM book"
        row = self.db.fetch(query)
        return row

    def lessCostBook(self):
        query = "SELECT isbn,title, 'price' || ':'|| MIN(price) FROM book"
        row = self.db.fetch(query)
        return row

    ############################## CD-DVD ##############################
    def add_cd(self, cd):  # adicionar um livro a lista books
        self.cd = cd
        self.artist = cd.get_artist()
        artist_name = self.artist['name']
        self.artist = Artist(artist_name, self.artist['isAuthor'])

        isAuthor = True if self.artist.getIsAuthor() == 'True' else False
        author_id = self.artist['author_id'] if isAuthor else 0

        query2 = "insert into artist (name,isAuthor,author_id) values (?,?,?)"
        cursor = self.db.insert(query2, (artist_name, isAuthor, author_id))

        query = "insert into `cd-dvd` (title,genre,release_year,disc_number,duration,price,artist_id) values (?,?,?,?,?,?,?)"
        data = (self.cd.title, self.cd.genre, self.cd.releaseYear,
                self.cd.discNumber, self.cd.duration, self.cd.price, cursor.lastrowid)
        self.db.insert(query, data)

    def getCdBooks(self, artist_id):
        row = list()
        query_name = self.db.fetchOne(
            f"SELECT `name` FROM artist WHERE id = ? ", artist_id)
        if not query_name:
            abort(404, {"error": "artist not found"})
        row.append({"artist_name": query_name})
        # query = f"""SELECT 'cd' ||' = '|| `cd-dvd`.title , 'book' ||' = '|| book.title from `cd-dvd` 
        #         inner join artist on (`cd-dvd`.artist_id = artist.id)  
        #         INNER JOIN book on book.author_id = artist.author_id
        #         where artist.id = {artist_id}
        #          """
        query_cd = f"""SELECT `cd-dvd`.title from `cd-dvd` 
                inner join artist on (`cd-dvd`.artist_id = artist.id)
                WHERE artist.id = {artist_id}"""
        query_book = f"""SELECT book.title from `book` 
                inner join artist on (book.author_id = artist.author_id)
                WHERE artist.id = {artist_id}"""

        row.append({"Cd":self.db.fetch(query_cd)})
        row.append({"Book":self.db.fetch(query_book)})

        
        return row
