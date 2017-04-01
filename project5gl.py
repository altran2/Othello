#Alexander Tran 46182166 ICS32 Project 4

from pprint import pprint

class gamestate:
    def __init__(self, rows, columns, topleft, firstplayer, wc):
        self.rows = rows
        self.columns = columns
        self.topleft = topleft
        self.turn = firstplayer
        self.wc = wc
        self.board = self.create_board()

    def get_board(self):
        return self.board
        
    def create_board(self):
        '''creates a new board'''
        board = [['.' for i in range(self.rows)]for j in range(self.columns)]
        if self.topleft == 'B':
            board[int(self.rows/2-1)][int(self.columns/2-1)] = 'B'
            board[int(self.rows/2)-1][int((self.columns/2))] = 'W'
            board[int((self.rows/2))][int((self.columns/2)-1)] = 'W'
            board[int((self.rows/2))][int((self.columns/2))] = 'B'
        elif self.topleft == 'W':
            board[int(self.rows/2-1)][int(self.columns/2-1)] = 'W'
            board[int(self.rows/2)-1][int((self.columns/2))] = 'B'
            board[int((self.rows/2))][int((self.columns/2)-1)] = 'B'
            board[int((self.rows/2))][int((self.columns/2))] = 'W'
        return board

    def black_score(self):
        '''gets the score of the black pieces'''
        score = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'B':
                    score += 1
        return score
    
    def white_score(self):
        '''gets the score of the white pieces'''
        score = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'W':
                    score += 1
        return score

    def current_turn(self):
        '''gets the player whose turn it currently is'''
        return self.turn
        
    def change_turn(self):
        '''changes turns'''
        if self.turn == 'B':
            self.turn = 'W'
            return self.turn
        elif self.turn == 'W':
            self.turn = 'B'
            return self.turn
        
    def turn_info(self):
        '''starts playing the game'''
        print('B: ', self.black_score(), 'W: ', self.white_score())
        pprint(self.board)
        print('TURN: ', self.current_turn())
    
    def make_move(self, x, y):
        '''makes the move and flips the board pieces'''
        try:
            move = (x, y)
            origx = move[0]-1
            origy = move[1]-1
            flippedpieces = []
            if self.check_valid(origx, origy) == True:
                if self.turn == 'B':
                    otherpiece = 'W'
                elif self.turn == 'W':
                    otherpiece = 'B'                
                for x, y in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                    row = origx + x
                    column = origy + y
                    if self.on_board(row, column) == True and self.board[row][column] == otherpiece:
                        row += x
                        column += y
                        if self.on_board(row,column) != True:
                            continue
                        while self.board[row][column] == otherpiece:
                            row += x
                            column += y
                            if self.on_board(row,column) == False:
                                break
                        if self.on_board(row,column) != True:
                            continue
                        if self.board[row][column] == self.turn:
                            while True:
                                row -= x
                                column -= y
                                if row == origx and column == origy:
                                    break
                                flippedpieces.append([row,column])
                
            if len(flippedpieces) == 0:
                raise ValueError
            
        except ValueError:
            print('INVALID')
            self.make_move()
        else:
            print('VALID')
            flippedpieces.append([origx, origy])
            for row, column in flippedpieces:
                self.board[row][column] = self.turn
            self.change_turn()
          
    def check_valid(self, row: 'input', column: 'input'):
        '''checks to see if the move is valid'''
        try:
            if self.on_board(row, column) != True:
                print('INVALID')
                return False
            if self.board[row][column] != '.':
                print('INVALID')
                return False
        except IndexError:
            print('INVALID')
            self.make_move()
        else:
            return True

    def on_board(self, row: 'input', column: 'input'):
        '''checks to see if move is on board'''
        return row >= 0 and row <= self.rows-1 and column >= 0 and column <= self.columns -1
        
    def checkgameover(self):
        '''checks to see if there are no more legal moves on the board and displays who won'''
        counter = 0
        winner = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '.':
                    counter += 1
        if counter == 0:
            print('B: ', self.black_score(), 'W: ', self.white_score())
            pprint(self.board)
            
            if self.wc == '>':
                #most discs wins the game
                if self.black_score() > self.white_score():
                    winner = 'BLACK'
                elif self.black_score() < self.white_score():
                    winner = 'WHITE'
                elif self.black_score() == self.white_score():
                    winner = 'NONE'
            elif self.wc == '<':
                #least discs wins the game
                if self.black_score() > self.white_score():
                    winner = 'WHITE'
                elif self.black_score() < self.white_score():
                    winner = 'BLACK'
                elif self.black_score() == self.white_score():
                    winner = 'NONE'
        return winner
