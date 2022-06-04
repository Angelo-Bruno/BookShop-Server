


class Artist:
        def __init__(self,name,isAuthor)-> None:
            self.name = name
            self.isAuthor = isAuthor


        def getIsAuthor(self):
            return self.isAuthor
        
        def __str__(self):
            return self.name