from flask.json import JSONEncoder
from flask import Flask, abort, jsonify, make_response, request
from Author import Author

from Book import Book
from Bookshop import Bookshop
from CD import CD
from DB.main import Database


class BookJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return {
                'isbn': obj.isbn,
                'title': obj.title,
                'author': obj.author,
                'price': obj.price
            }
        elif isinstance(obj, CD):
            return {
                'title':obj.title,
                'genre':obj.genre,
                'artist':obj.artist,
                'release_year':obj.releaseYear,
                'disc_number':obj.discNumber,
                'duration':obj.duration,
                'price':obj.price

            }
        else:
            return super(BookJSONEncoder, self).default(obj)



bookshop = Bookshop()
db = Database()

def create_bookshop_service():
    app = Flask(__name__)
    app.json_encoder = BookJSONEncoder

    @app.route('/book/list', methods=['GET'])  # get list of books route
    def get_books():
        
        result = db.fetch("SELECT * FROM book")
        return jsonify({'books': result})

    @app.route('/book/<int:isbn>', methods=['GET'])  # get single book route
    def get_book(isbn):
        book = bookshop.get(isbn)
        return jsonify({'book': book})

    # remove book
    @app.route('/book/<int:isbn>', methods=['DELETE'])
    def delete_book(isbn):
        bookshop.delete_book(isbn)
        return jsonify({'result': True})

    @app.route('/book', methods=['POST'])  # add book
    def create_book():
        print('creating book...')
        if not request.json or not 'isbn' in request.json:
            abort(400)

        author = request.json["author"]

        book = Book(
            request.json['isbn'],
            request.json['title'],
            int(request.json['price']),
            author
        )
        
        bookshop.add_book(book)
        return jsonify({'book': book}), 201

    @app.route('/book', methods=['PUT'])  # rota para atualizar um livro
    def update_book():
        isbn = request.json['isbn']
        print(isbn)
        book = bookshop.update_book(isbn)
        return jsonify({'book': book}), 201

    @app.route('/book/author/<int:isbn>', methods=['GET'])  # rota para atualizar um livro
    def getAuthor(isbn):
        author = bookshop.getBookAuthor(isbn)
        return jsonify({'author': author}), 201

    @app.route('/book/author/<int:id>', methods=['DELETE'])  # rota para atualizar um livro
    def  deleteAuthorBook(id):
        author = bookshop.removeAuthorBooks(id)
        return jsonify({'author': "author deleted"}), 201

    @app.route('/book/total', methods=['GET'])  # rota para atualizar um livro
    def  countBooks():
        row = bookshop.countBooks()
        return jsonify({'Total books': row}), 201

    @app.route('/book/maxcost', methods=['GET'])  # rota para atualizar um livro
    def  getMaxPrice():
        row = bookshop.expensiveBook()
        return jsonify({'book': row}), 201

    @app.route('/book/mincost', methods=['GET'])  # rota para atualizar um livro
    def  getMinPrice():
        row = bookshop.lessCostBook()
        return jsonify({'book': row}), 201

    
    ############################## CD-DVD ##############################

    @app.route('/cd', methods=['POST'])  # add book
    def create_cd():
        print('creating cd-dvd...')
        if not request.json:
            abort(400)

        artist = request.json["artist"]

        cd = CD(
            request.json['title'],
            request.json['genre'],
            request.json['release_year'],
            request.json['disc_number'],
            request.json['duration'],
            int(request.json['price']),
            artist
        )
        
        bookshop.add_cd(cd)
        return jsonify({'cd': cd}), 201

    @app.errorhandler(400)
    def not_found(error):
        return make_response(jsonify({'book': 'Not found'}), 400)

    return app
