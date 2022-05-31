from bookshopService import create_bookshop_service


if __name__ == '__main__':
    app = create_bookshop_service()
    app.run(debug=True)