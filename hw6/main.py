import sys
import copy
from Player import Player
from Board import Board

ON = 'on'
OFF = 'off'

class Game:
    def __init__(self, white_strat, blue_strat, history, score):
        self._white_strat = white_strat
        self._blue_strat = blue_strat
        self._white = Player('A', 'B', white_strat)
        self._blue = Player('Y', 'Z', blue_strat)    
        self._board = Board(self._white, self._blue)
        if score == OFF:
            self._score = False
        else:
            self._score = True
        if history == OFF:
            self._history = False
        else:
            self._history = True
        self._turn = 1
        self._mover = self._white
        self._caretaker = CareTaker()
        self._caretaker.add_memento(Memento(copy.deepcopy(self._board), copy.deepcopy(self._turn), True))
    
    def do_turn(self):
        print(self._board)
        pieces = self._mover.get_pieces()
        if self._score:
            print('Turn: {}, {}, {}'.format(self._turn, self._mover, self._mover.move_score(self._board, pieces[0].where(), pieces[1].where())))
        else:
            print('Turn: {}, {}'.format(self._turn, self._mover))
        w = self._check_winner()
        if w:
            print(str(w)[0:-5] + ' has won')
            again = input('Play again?\n')
            if again == 'yes':
                self._reset()
                return False
            else:
                return True
        if self._history:
            time = input('undo, redo, or next\n')
            if time == 'undo':
                undone = self._caretaker.undo()
                if undone:
                    self._board = copy.deepcopy(undone.get_state())
                    self._turn = undone.get_date()
                    self._white = self._board.get_white()
                    self._blue = self._board.get_blue()
                    if undone.get_mover():
                        self._mover = self._white
                    else:
                        self._mover = self._blue
                return False
            elif time == 'redo':
                redone = self._caretaker.redo()
                if redone:
                    self._board = copy.deepcopy(redone.get_state())
                    self._turn = redone.get_date()
                    self._white = self._board.get_white()
                    self._blue = self._board.get_blue()
                    if redone.get_mover():
                        self._mover = self._white
                    else:
                        self._mover = self._blue
                return False
            else:
                self._caretaker.reset()
                
        
        
        if self._score:
            ((worker, move, build), score) = self._mover.turn(self._board, self._score)
            print('{},{},{} {}'.format(worker, move, build, score))
        else:
            (worker, move, build) = self._mover.turn(self._board, self._score)
            print('{},{},{}'.format(worker, move, build))


        self._turn += 1

        if self._mover is self._white:
            self._mover = self._blue
        else:
            self._mover = self._white
        
       
        self._caretaker.add_memento(Memento(copy.deepcopy(self._board), copy.deepcopy(self._turn), self._mover is self._white))
        

        return False


    def _check_winner(self):
        #check for a win
        if self._white['A'].where().get_height() == 3:
            return self._white
        if self._white['B'].where().get_height() == 3:
            return self._white
        if self._blue['Y'].where().get_height() == 3:
            return self._blue
        if self._blue['Z'].where().get_height() == 3:
            return self._blue
        
        #check for no moves
        valid_move = False
        for piece in self._mover.get_pieces():
            space = piece.where()
            h = space.get_height()
            for adj in self._board.__iter__(space):
                if adj.get_height() <= h + 1 and not adj.get_piece():
                    valid_move = True
        
        if valid_move == False:
            if self._mover is self._white:
                return self._blue
            else:
                return self._white
        
        return None
    
    def _reset(self): 
        self._white = Player('A', 'B', self._white_strat)
        self._blue = Player('Y', 'Z', self._blue_strat)  
        self._board = Board(self._white, self._blue)
        self._turn = 1
        self._mover = self._white
        self._caretaker = CareTaker()
        self._caretaker.add_memento(Memento(copy.deepcopy(self._board), self._turn, True))

class Memento:
    def __init__(self, state, date, mover):
        self._state = state
        self._date = date
        self._mover = mover

    def __str__(self):
        return str(self._state)

    def get_state(self):
        return self._state
    
    def get_date(self):
        return self._date
    
    def get_mover(self):
        return self._mover
    

    
class CareTaker:
    def __init__(self):
        self._mementos = []
        self._size = 0
        self._index = -1
    
    def add_memento(self, memento):

        self._mementos = self._mementos[0:self._index + 1]
        self._mementos.append(memento)
        self._size += 1
        self._index = self._size - 1

    
    def undo(self):
        if self._index == 0:
            return None
        else:
            self._index -= 1
            return self._mementos[self._index]
    
    def redo(self):
        if self._index == self._size - 1:
            return None
        else:
            self._index += 1
            return self._mementos[self._index]
    
    def reset(self):
        self._mementos = self._mementos[0:self._index + 1]
        self._size = len(self._mementos)
        self._index = self._size - 1


            
if __name__ == '__main__':
    white = 'human'
    blue = 'human'
    history = 'off'
    score = 'off'
    n = len(sys.argv)
    if n > 1:
        white = sys.argv[1]
    if n > 2:
        blue = sys.argv[2]
    if n > 3:
        history = sys.argv[3]
    if n > 4:
        score = sys.argv[4]
    game = Game(white, blue, history, score)
    end = False
    while not end:
        end = game.do_turn()

