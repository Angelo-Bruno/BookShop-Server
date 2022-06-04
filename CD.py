from Artist import Artist
from DB.main import Database


database = Database()
class CD:
    def __init__(self, title, genre,releaseYear,discNumber,duration,price,artist): # book constructor 
        self.title = title
        self.artist = artist
        self.price = price
        self.genre = genre
        self.releaseYear = releaseYear
        self.discNumber = discNumber
        self.duration = duration #in minutes
        
    
    def get_artist(self):
        return self.artist



    def __str__(self): #retornar string com infos de books
        return self.title + ' by ' + self.artist_name + ' @ ' + str(self.price)