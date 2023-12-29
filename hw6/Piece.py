from Exceptions import BadSpace

class Piece:
    def __init__(self, name, space=None):
        self._name = name
        self._space = space
    
    def __str__(self):
        return self._name
    
    def place(self, space):
        if not self._space:
            self._space = space
            space.set_piece(self)

        elif space.get_height() - 1 <= self.where().get_height(): 
            space.set_piece(self)
            self._space.set_piece(None)
            self._space = space
        else:
            raise BadSpace

    def where(self):
        return self._space
    

