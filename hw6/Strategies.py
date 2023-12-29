import random

class Strategy:
    def __init__(self, player):
        self._player = player

    def choose(self, player, board, score):
        raise NotImplementedError


class ConcreteStrategyHuman(Strategy):
    def choose(self, player, board, score):
        while True:
                worker = input('Select a worker to move\n')
                if worker in ['A', 'B', 'Y', 'Z']:
                    if player[worker]:
                        valid_move = False
                        space = player[worker].where()
                        for adj in board.__iter__(space):
                            if adj.get_height() <= space.get_height() + 1 and not adj.get_piece():
                                valid_move = True
                        if valid_move:
                            break
                        else:
                            print('That worker cannot move')
                    else:
                        print('That is not your worker')
                else:
                    print('Not a valid worker')

        while True:
            move = input('Select a direction to move (n, ne, e, se, s, sw, w, nw)\n')
            if move in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                try:
                    target = board.get_space(player[worker].where(), move)
                    player[worker].place(target)
                    break
                except:
                    print('Cannot move ' + move)
            else:
                print('Not a valid direction')

        while True:
            build = input('Select a direction to build (n, ne, e, se, s, sw, w, nw)\n')
            if build in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] :
                try:
                    target = board.get_space(player[worker].where(), build)
                    target.build()
                    break
                except:
                    print('Cannot build ' + build)
            else:
                print('Not a valid direction')
        if score:
            spaces = []
            for check_worker in ['A', 'B', 'Y', 'Z']:
                if player[check_worker]:
                    spaces.append(player[check_worker].where())
            return ((worker, move, build), player.move_score(board, spaces[0], spaces[1]))
        else:
            return (worker, move, build)

class ConcreteStrategyComputerTemplate(Strategy):
    def choose(self, player, board, score):
        
        move_list = self._enumerate_moves(player, board)
        worker, move, build = self._pick_one(move_list, player, board)
        summary = self._get_summary(player, worker, move, build)

        worker.place(move)
        build.build()
        space_list = []
        for piece in player.get_pieces():
            space_list.append(piece.where())
        if score:
            score = player.move_score(board, space_list[0], space_list[1])
            return summary, score
        else:
            return summary


    def _enumerate_moves(self, player, board):
        move_list = []

        for piece in player.get_pieces():
            space = piece.where()
            h = space.get_height()
            for adj in board.__iter__(space):
                if adj.get_height() <= h + 1 and not adj.get_piece():
                    for adj_build in board.__iter__(adj):
                        if adj_build is space or adj_build.get_height() < 4 and not adj_build.get_piece():
                            move_list.append((piece, adj, adj_build))
        return move_list
    
    def _get_summary(self, player, worker, move, build):
        start = worker.where()
        start_x = start.get_x()
        start_y = start.get_y()

        move_x = move.get_x()
        move_y = move.get_y()

        build_x = build.get_x()
        build_y = build.get_y()

        d = {(-1, 0): 'n', (0, 1): 'e', (1, 0): 's', (0, -1): 'w', (-1, 1): 'ne', (1, 1): 'se', (1, -1): 'sw', (-1, -1): 'nw'} 
        
        return (worker, d[(move_y - start_y, move_x - start_x)], d[(build_y - move_y, build_x - move_x)])


    
    def _pick_one(self, player, move_list, board):
        raise NotImplementedError



class RandomComputer(ConcreteStrategyComputerTemplate):
    def _pick_one(self, move_list, player, board):
        return random.choice(move_list)

        
        

class HeuristicComputer(ConcreteStrategyComputerTemplate):
    def _pick_one(self, move_list, player, board):
        best_move = -1
        candidates = []
        for worker, move, build in move_list:
            other_worker = None
            for piece in player.get_pieces():
                if not (worker is piece):
                    other_worker = piece
            
            height, center, distance = player.move_score(board, move, other_worker.where())
            if move.get_height() == 3:
                score = 99999
            score = height * 3 + center * 2 + distance 
            if score == best_move:
                candidates.append((worker, move, build))
            elif score > best_move:
                candidates = [(worker, move, build)]
                best_move = score
        return random.choice(candidates)
