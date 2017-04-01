#Alexander Tran 46182166 ICS32 Project 5

import tkinter
import project5gl

DEFAULT_FONT = ('Helvetica', 20)

class BoardApplication:
    def __init__(self):
        
        settings = Gamesettings()
        settings.show()
     
        self.gamelogic = project5gl.gamestate(int(settings.get_rows()),
                                         int(settings.get_columns()),
                                         settings.get_topleft(),
                                         settings.get_firstplayer(),
                                         settings.get_wincondition())

        self._root_window = tkinter.Tk()
        self._root_window.title('OTHELLO')
        
        #header
        self._header = tkinter.Frame(master = self._root_window, width = 600, height = 50)
        self._header.grid(row = 0, column = 0, columnspan = 3)
        
        #canvas
        self._canvas = tkinter.Canvas(master = self._root_window, width = 600, height = 400, background = 'grey')
        self._canvas.grid(row = 1, column = 0, columnspan = 3,
                          sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        self._canvas.bind('<Configure>', self._canvas_resized)
        self._canvas.bind('<Button-1>', self._canvas_clicked)

        #footer                                    
        self._footer = tkinter.Frame(self._root_window, width = 600, height = 20)
        self._footer.grid(row = 2, column = 0, columnspan = 3)
        
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 3)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)
        self._root_window.columnconfigure(2, weight = 1)

        self._score = tkinter.StringVar()
        self._turn = tkinter.StringVar()
        self._winner = tkinter.StringVar()

        self._canvas_width = 0
        self._canvas_height = 0
        self._pixel_width = 0
        self._pixel_height = 0

    def _create_board(self) -> list:
        self._root_window.update()
        self.rules()
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()
        self._pixel_width = (self._canvas_width/self.gamelogic.columns)
        self._pixel_height = (self._canvas_height/self.gamelogic.rows)
        board = []
        for i in range(self.gamelogic.rows + 1):
            for j in range(self.gamelogic.columns + 1):
                x0 = self._pixel_width * j
                x1 = x0 + self._pixel_width
                y0 = self._pixel_height * i
                y1 = y0 + self._pixel_height
                board.append((x0,y0,x1,y1))
                self._canvas.create_rectangle(x0,y0,x1,y1, outline = 'black', fill='grey')

        row_mid = int(self._pixel_height * (self.gamelogic.rows/2 - 1))
        col_mid = int(self._pixel_width * (self.gamelogic.columns/2 - 1))

        if self.gamelogic.topleft == 'B':
            self._canvas.create_oval(col_mid, row_mid, col_mid + self._pixel_width, row_mid + self._pixel_height, fill = 'black')
            self._canvas.create_oval(col_mid + self._pixel_width, row_mid + self._pixel_height, col_mid + self._pixel_width * 2, row_mid + self._pixel_height * 2, fill = 'black')
            self._canvas.create_oval(col_mid + self._pixel_width, row_mid, col_mid + self._pixel_width * 2, row_mid + self._pixel_height, fill = 'white')
            self._canvas.create_oval(col_mid, row_mid + self._pixel_height, col_mid + self._pixel_width, row_mid + self._pixel_height * 2, fill = 'white')
        if self.gamelogic.topleft == 'W':
            self._canvas.create_oval(col_mid, row_mid, col_mid + self._pixel_width, row_mid + self._pixel_height, fill = 'white')
            self._canvas.create_oval(col_mid + self._pixel_width, row_mid + self._pixel_height, col_mid + self._pixel_width * 2, row_mid + self._pixel_height * 2, fill = 'white')
            self._canvas.create_oval(col_mid + self._pixel_width, row_mid, col_mid + self._pixel_width * 2, row_mid + self._pixel_height, fill = 'black')
            self._canvas.create_oval(col_mid, row_mid + self._pixel_height, col_mid + self._pixel_width, row_mid + self._pixel_height * 2, fill = 'black')

        return board
        
    def _canvas_resized(self, event: tkinter.Event) -> None:
        self._canvas.delete(tkinter.ALL)
        self._create_board()
        self._redraw_board()

    def rules(self):
        rules = tkinter.Label(master = self._header,
                              text = 'FULL', font = DEFAULT_FONT, background = 'white')
        rules.grid(row = 0, column = 0, padx = 10, pady = 10)
    
    def score(self):
        self._score.set('Black: ' + str(self.gamelogic.black_score()) + '  White: ' + str(self.gamelogic.white_score()))
        score_text = tkinter.Label(master = self._header,
                                    textvariable = self._score, font = DEFAULT_FONT, background = 'white')
        score_text.grid(row = 0, column = 2, padx = 10, pady = 10)

    def turn_info(self):
        self._turn.set('Current Turn: ' + self.gamelogic.current_turn())
        turn_text = tkinter.Label(master = self._footer,
                                    textvariable = self._turn, font = DEFAULT_FONT, background = 'white')
        turn_text.grid(row = 0, column = 1, padx = 10, pady = 10)

    def winner(self):
        winner = self.gamelogic.checkgameover()
        if winner == 'BLACK' or 'WHITE' or 'NONE':
            self._winner.set('WINNER: ' + str(winner))
            winner_text = tkinter.Label(master = self._footer,
                            textvariable = self._winner, font = DEFAULT_FONT, background = 'white')
            winner_text.grid(row = 0, column = 2, padx = 10, pady = 10)

    def convertclicked(self, mousex: float, mousey: float):
        colnum = 0
        rownum = 0
        for col in range(1, self.gamelogic.columns + 1):
            if (col - 1) * self._pixel_width <= mousex <= col * self._pixel_width:
                colnum = col
        for row in range(1, self.gamelogic.rows + 1):
            if (row - 1) * self._pixel_height <= mousey <= row * self._pixel_height:
                rownum = row
        return (rownum, colnum)

    def _canvas_clicked(self, event: tkinter.Event) -> None:
        clicked = (event.x, event.y)
        move = self.convertclicked(clicked[0],clicked[1])
        try:
            self.gamelogic.make_move(move[0], move[1])
            self._create_board()
            self._redraw_board()
        except:
            pass

    def _redraw_board(self) -> None:
        self._canvas.delete(tkinter.ALL)
        self.rules()
        self.score()
        self.turn_info()
        self.winner()
        currentboard = self.gamelogic.get_board()
        for row in range(self.gamelogic.rows):
            for col in range(len(currentboard)):
                x0 = self._pixel_width * col
                x1 = x0 + self._pixel_width
                y0 = self._pixel_height * row
                y1 = y0 + self._pixel_height
                self._canvas.create_rectangle(x0,y0,x1,y1, outline = 'black', fill='grey')
                if currentboard[row][col] == 'B':
                    self._canvas.create_oval(self._pixel_width * (col),
                                             self._pixel_height * (row),
                                             self._pixel_width * (col + 1),
                                             self._pixel_height * (row + 1),
                                             fill = 'black')
                    
                elif currentboard[row][col] == 'W':
                    self._canvas.create_oval(self._pixel_width * (col),
                                             self._pixel_height * (row),
                                             self._pixel_width * (col + 1),
                                             self._pixel_height * (row + 1),
                                             fill = 'white')
                else:
                    pass
    def run(self):
        self._root_window.mainloop()
                
class Gamesettings:
    def __init__(self):
        self._settings_menu = tkinter.Tk()

        #game settings header
        header = tkinter.Label(
            master = self._settings_menu, text = 'Input the settings for the game!', font = DEFAULT_FONT)

        header.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

        #rows
        rows = tkinter.Label(
            master = self._settings_menu, text = 'How many rows are on the board (Even int bewteen 4 and 16)?', font = DEFAULT_FONT)

        rows.grid(
            row = 1, column = 0, padx = 10, pady = 10)

        self._rows_entry = tkinter.Entry(
            master = self._settings_menu, width = 20, font = DEFAULT_FONT)

        self._rows_entry.grid(
            row = 1, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        #columns
        columns = tkinter.Label(
            master = self._settings_menu, text = 'How many columns are on the board? (Even int between 4 and 16)?', font = DEFAULT_FONT)
        
        columns.grid(
            row = 2, column = 0, padx = 10, pady = 10)

        self._columns_entry = tkinter.Entry(
            master = self._settings_menu, width = 20, font = DEFAULT_FONT)        

        self._columns_entry.grid(
            row = 2, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        #firstplayer
        firstplayer = tkinter.Label(
            master = self._settings_menu, text = 'Which player — black or white — will move first (Input B or W)?', font = DEFAULT_FONT)
        
        firstplayer.grid(
            row = 3, column = 0, padx = 10, pady = 10)

        self._firstplayer_entry = tkinter.Entry(
            master = self._settings_menu, width = 20, font = DEFAULT_FONT)

        self._firstplayer_entry.grid(
            row = 3, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        #topleft
        topleft = tkinter.Label(
            master = self._settings_menu, text = 'Which player — black or white — will be in the top left of the center cells (Input B or W)?', font = DEFAULT_FONT)
        
        topleft.grid(
            row = 4, column = 0, padx = 10, pady = 10)

        self._topleft_entry = tkinter.Entry(
            master = self._settings_menu, width = 20, font = DEFAULT_FONT)

        self._topleft_entry.grid(
            row = 4, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        #wincondition
        wincondition = tkinter.Label(
            master = self._settings_menu, text = 'Will the player with the greatest or least discs win (Input > or <)?', font = DEFAULT_FONT)
        
        wincondition.grid(
            row = 5, column = 0, padx = 10, pady = 10)

        self._wincondition_entry = tkinter.Entry(
            master = self._settings_menu, width = 20, font = DEFAULT_FONT)

        self._wincondition_entry.grid(
            row = 5, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)
                
        #Exit buttons
        Exit = tkinter.Frame(master = self._settings_menu)
        
        Exit.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10)

        ok = tkinter.Button(
            master = Exit, text = 'OK', font = DEFAULT_FONT,
            command = self._ok_button)

        ok.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel = tkinter.Button(
            master = Exit, text = 'Cancel', font = DEFAULT_FONT,
            command = self._cancel_button)

        cancel.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        #outcomes
        self._gamesettingsdone = False
        self._rows = 0
        self._columns = 0
        self._firstplayer = ""
        self._topleft = ""
        self._wincondition = ""

    def show(self) -> None:
        self._settings_menu.grab_set()
        self._settings_menu.wait_window()

    def get_gamesettingsdone(self) -> bool:
        return self._gamesettingsdone

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_firstplayer(self) -> str:
        return self._firstplayer

    def get_topleft(self) -> str:
        return self._topleft

    def get_wincondition(self) -> str:
        return self._wincondition
        
    def _ok_button(self) -> None:
        self._gamesettingsdone = True
        self._rows = self._rows_entry.get()
        self._columns = self._columns_entry.get()
        self._firstplayer = self._firstplayer_entry.get()
        self._topleft = self._topleft_entry.get()
        self._wincondition = self._wincondition_entry.get()

        self._settings_menu.destroy()

    def _cancel_button(self) -> None:
        self._settings_menu.destroy()

if __name__ == '__main__':
    Othello = BoardApplication().run()
