from Exceptions import BadSpace

class Space:
    def __init__(self, y, x):
        self._height = 0
        self._piece = None
        self._x = x
        self._y = y

    def __str__(self):
        if self._piece:
            return str(self._height) + str(self._piece)
        else:
            return str(self._height) + " "
    
    def set_piece(self, piece):
        if self._piece and piece:
            raise BadSpace
        self._piece = piece

    def build(self):
        if self._piece or self._height == 4:
            raise BadSpace
        self._height += 1
    
    def get_height(self):
        return self._height
    
    def get_piece(self):
        return self._piece

    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
