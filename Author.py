from DB.main import Database


database = Database()
class Author:
    def __init__(self,id,name)-> None:
        self.id = id
        self.name = name


    def getId(self):
        print(self.id)
        return self.id
    
    def __str__(self):
        return self.name