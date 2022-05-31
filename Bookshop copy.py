import flask
class Bookshop:
    def __init__(self, books: list):  # constructor
        self.books = books

    def get(self, isbn):  # get book by id(isbn)
        if int(isbn) > len(self.books):
            flask.abort(404,"book do not exist")
        return list(filter(lambda b: b.isbn == isbn, self.books))[0]

    def add_book(self, book):  # adicionar um livro a lista books
        self.books.append(book)

    def delete_book(self, isbn):  # remover um livro po isbn
        self.books = list(filter(lambda b: b.isbn != isbn, self.books))
