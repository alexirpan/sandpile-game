from tkinter import *
from gamestate import *

class BoardGUI(Frame):
    """
	The graphic user interface for the sandpile game.
	Unfinished.
    """
    def __init__(self, side_length, master=None):
        Frame.__init__(self, master)
        self.side = side_length
        self.board = Board(create_square(side_length))
        self.players = [Player('Player ' + str(i+1), self.board) for i in range(2)]
        self.grid()
        self.create_widgets()
        self.grid_widgets()
        self.mainloop()
    def create_widgets(self):
        self.p1_label = Label(self, text = self.players[0].name + ": 0")
        self.p2_label = Label(self, text = self.players[1].name + ": 0")
        self.status = Label(self, text = self.players[0].name + "'s turn")
        self.squares = [[PhotoImage(file="blank.gif") for i in range(self.side)] for j in range(self.side)]
        
        
        
    