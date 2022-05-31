from DB.main import Database


database = Database()
class Author:
    def __init__(self,id,first_name,middle_name,last_name) -> None:
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def getId(self):
        print(self.id)
        return self.id
    
    def __str__(self):
        return self.first_name +" "+ self.middle_name+" "+self.last_name