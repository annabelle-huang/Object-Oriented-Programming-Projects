from Exceptions import BadSpace
from Space import Space

class Board:
    def __init__(self, white, blue):
        self._board = [[Space(y,x) for x in range(5)] for y in range(5)]

        white['B'].place(self._board[1][3])

        white['A'].place(self._board[3][1])

        blue['Y'].place(self._board[1][1])

        blue['Z'].place(self._board[3][3])
        
        self._white = white
        self._blue = blue
    
    def __iter__(self, center):
        x = center.get_x()
        y = center.get_y()
        return AdjacentSpaceIterator(self._board, x, y)
        
    def __str__(self):
        board_string = "+--+--+--+--+--+\n"
        div =  "+--+--+--+--+--+\n"
        for row in self._board:
            board_string += '|'
            for space in row:
                board_string += str(space) + '|'
            board_string += '\n'
            board_string += div
            
        return board_string[0:-1]
    
    def get_space(self, start, dir):
        d = {'n': (-1, 0), 'e': (0, 1), 's': (1, 0), 'w': (0, -1), 'ne': (-1, 1), 'se': (1, 1), 'sw': (1, -1), 'nw': (-1, -1)} 
                
        cur_x = start.get_x()
        cur_y = start.get_y()
        add_y, add_x = d[dir]

        if not 0 <= cur_y + add_y <= 4:
            raise BadSpace
        
        if not 0 <= cur_x + add_x <= 4:
            raise BadSpace
        

        return self._board[cur_y + add_y][cur_x + add_x]
    
    def select_space(self, x, y):
        return self._board[y][x]

    def get_white(self):
        return self._white
    
    def get_blue(self):
        return self._blue
    
class AdjacentSpaceIterator:
    def __init__(self, board, x, y):
        self._move_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self._index = 0
        self._x = y
        self._y = x
        self._board = board

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self._index == 8:
                raise StopIteration
            add_y, add_x = self._move_list[self._index]
            self._index += 1
            if self._x + add_x < 0 or self._x + add_x > 4 or self._y + add_y < 0 or self._y + add_y > 4:
                continue
            else:
                return self._board[self._x + add_x][self._y + add_y]

    
