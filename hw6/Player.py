from Piece import Piece
from Strategies import ConcreteStrategyHuman, RandomComputer, HeuristicComputer

HUMAN = 'human'
RANDOM = 'random'
HEURISTIC = 'heuristic'

class Player:
    def __init__(self, piece1, piece2, strategy):
        if strategy == HUMAN:
            self._strategy = ConcreteStrategyHuman(self)
        elif strategy == RANDOM:
            self._strategy = RandomComputer(self)
        elif strategy == HEURISTIC:
            self._strategy = HeuristicComputer(self)

        self._pieces = {piece1: Piece(piece1), piece2: Piece(piece2)}


    def __str__(self):
        if 'A' in self._pieces:
            return 'white (AB)'
        else:
            return 'blue (YZ)'

    def __getitem__(self, k):
        if k in self._pieces:
            return self._pieces[k]
        else:
            return None
    
    def turn(self, board, score):
        choice = self._strategy.choose(self, board, score)
        return choice
    
    def get_pieces(self):
        pieces = []
        for piece in self._pieces:
            pieces.append(self._pieces[piece])
        return pieces
    
    def move_score(self, board, space1, space2):
        return (self._height_score(space1, space2), self._center_score(space1, space2), self._distance_score(board, space1, space2))

    def _height_score(self, space1, space2):
        return space1.get_height() + space2.get_height()
    
    def _center_score(self, space1, space2):
        x1 = space1.get_x()
        y1 = space1.get_y()

        x2 = space2.get_x()
        y2 = space2.get_y()
        
        score1 = 0
        score2 = 0

        if x1 == 0 or x1 == 4 or y1 == 0 or y1 == 4:
            score1 = 0
        elif x1 == 2 and y1 == 2:
            score1 = 2
        else:
            score1 = 1
        
        if x2 == 0 or x2 == 4 or y2 == 0 or y2 == 4:
            score2 = 0
        elif x2 == 2 and y2 == 2:
            score2 = 2
        else:
            score2 = 1
        
        return score1 + score2

    def _distance_score(self, board, space1, space2):
        other_pieces = []
        for y in range(5):
            for x in range(5):
                other = board.select_space(x, y).get_piece() 
                
                if other and other.where() is not space1 and other.where() is not space2:
                    other_pieces.append(board.select_space(x, y))

        return 8 - (min(self._find_distance(space1, other_pieces[0]), self._find_distance(space2, other_pieces[0])) + min(self._find_distance(space1, other_pieces[1]), self._find_distance(space2, other_pieces[1])))
    
    def _find_distance(self, space1, space2):
        x1 = space1.get_x()
        y1 = space1.get_y()

        x2 = space2.get_x()
        y2 = space2.get_y()

        return max(abs(x1 - x2), abs(y1 - y2))
    

    
        
