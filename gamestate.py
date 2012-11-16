import networkx as nx
import graphics
from math import sqrt

class Board(object):
    """
    A board is represented as a NetworkX graph. 
    Each node has 3 attributes: the number of grains on it, boolean telling it whether to fire, and the owner of that grid.
    Don't know how NetworkX graph runtimes work, so this might be horribly inefficient
    It supports methods involving grain adding.
    """
    def __init__(self, graph, diag = True):
        self.grid = graph
    def get_node(self, node_name):
        """Returns the node specified by the given name.
        Nodes in NetworkX are represented as dictionaries of various node attributes.
        """
        return self.grid.node[node_name]
    def add_grain(self, node_name, player):
        """Adds a grain and gives ownership of the named pile to the given player."""
        self.grid.node[node_name]['grains'] += 1
        self.grid.node[node_name]['owner'] = player
        if self.grid.node[node_name]['grains'] >= nx.degree(self.grid, node_name):
            self.grid.node[node_name]['to_fire'] = True
    def fire(self):
        """
        The fire method checks each node. If it should fire, then it does.
        After all the nodes have fired, it checks again to see if any nodes should re-fire.
        In each round, a node can fire at most once. This prevents infinite loops.
        Can probably be improved by checking from the node you add the grain to, so you don't have to check everything.
        """
        for pile in self.grid.nodes():
            if self.grid.node[pile]['to_fire'] and not self.grid.node[pile]['fired_this_turn']:
                deg = nx.degree(self.grid, pile)
                player = self.grid.node[pile]['owner']
                self.grid.node[pile]['grains'] -= deg
                for neighbor in self.grid.neighbors(pile):
                    self.grid.node[neighbor]['grains'] += 1
                    self.grid.node[neighbor]['owner'] = player
                self.grid.node[pile]['to_fire'] = False
                self.grid.node[pile]['fired_this_turn'] = True
                print(pile + ' is unstable and fires.')
            elif self.grid.node[pile]['to_fire']:
                print(pile + ' is unstable and will fire next turn.')
                
        for pile in self.grid.nodes():
            if self.grid.node[pile]['grains'] >= nx.degree(self.grid, pile):
                self.grid.node[pile]['to_fire'] = True
    def should_fire(self):
        for pile in self.grid.nodes():
            if self.grid.node[pile]['to_fire'] and not self.grid.node[pile]['fired_this_turn']:
                return True
        return False
    def next_turn(self):
        """
        Prepares board for the next turn.
        Right now it doesn't do anything to the players, should probably do something about that soon.
        """
        for pile in self.grid.nodes():
            self.grid.node[pile]['fired_this_turn'] = False
    def __str__(self):
        """For now, prints the number of grains in each square, assuming the board is a square.
        MODIFY LATER.
        """
        size = int(sqrt(len(self.grid.nodes())))
        ret_val = ''
        for y in range(size):
            for x in range(size):
                name = str(x) + '_' + str(y)
                player = self.grid.node[name]['owner']
                if player is None:
                    player_name = 'N'
                elif player.name == 'Player 1':
                    player_name = '1'
                else:
                    player_name = '2'
                ret_val += str(self.grid.node[name]['grains']) + '_' + player_name + ' '
            ret_val += '\n'
        return ret_val

def create_grid(size, diagonal_neighbors = True):
    """Creates a square board with side length size.
    Each square on the board is neighbors with each other board that is a neighbor of it.
    
    >>> b = create_grid(4)
    >>> b.node['3_3']['grains']
    0
    >>> nx.degree(b, '0_0')
    3
    >>> nx.degree(b, '2_0')
    5
    >>> nx.degree(b, '2_2')
    8
    """
    board = nx.Graph()
    def node_name(x, y):
        """Returns the name of the node at coordinate (x, y).
        x_y."""
        if x >= 0 and x < size and y >= 0 and y < size:
            return str(x) + '_' + str(y)
    def edge_maker(x, y):
        """Returns a list of all edges that connect the node at (x,y) with its neighbors."""
        edges = []
        curr_node = node_name(x, y)
        for i in range(size):
            for j in range(size):
                neighbors = [node_name(x - 1, y), 
                                node_name(x + 1, y), 
                                node_name(x, y - 1), 
                                node_name(x, y + 1)]
                if diagonal_neighbors:
                    neighbors.append(node_name(x - 1, y - 1))
                    neighbors.append(node_name(x + 1, y - 1))
                    neighbors.append(node_name(x - 1, y + 1))
                    neighbors.append(node_name(x + 1, y + 1))
                for node in neighbors:
                    if node is not None:
                        edges.append((curr_node, node))
        return edges
    # NetworkX graphs auto add nodes if they are referred to in edges, but we have to add attributes
    for i in range(size):
        for j in range(size):
            board.add_node(node_name(i,j), grains = 0, to_fire = False, owner = None, fired_this_turn = False)
            board.add_edges_from(edge_maker(i, j))
    return board
    
class Player(object):
    """
    A class that represents a player.
    Each player has knowledge of the board.
    """
    def __init__(self, name, board):
        self.points = 0
        self.name = name
        self.board = board
    def calc_points(self):
        """
        Calculates and returns the total points for this player.
        """
        self.points = 0
        for pile in self.board.grid.nodes():
            if self.board.grid.node[pile]['owner'] is self:
                self.points += self.board.grid.node[pile]['grains']
        return self.points
    def add_grain(self, node_name):
        self.board.next_turn()
        self.board.add_grain(node_name, self)
        print(self.name + ' adds grain to ' + node_name)
        print(self.board)
        while self.board.should_fire():
            self.board.fire()
            print(self.board)
    def add_grains(self, node_name, num):
        """
        Used for debugging purposes.
        """
        for _ in range(num):
            self.add_grain(node_name)
    
class BoardGUI(object):
    """
    Controls the user interface and graphics of the game.
    """
    
    def __init__(self):
        self.initialized = False

    def initialize_board_graphics(self, board):
        """Create canvas, control panel, places, and labels."""
        self.initialized = True
        self.canvas = graphics.Canvas()
        self.point_text_one = self.canvas.draw_text('Player 1: 0', (20, 20))
        self.point_text_two = self.canvas.draw_text('Player 2: 0', (20, 40))
        self._click_rectangles = list()
        self._init_squares(board)
        
    def _init_squares(self, board):
        """Construct squares in the play window.
        ONLY WORKS FOR SQUARE BOARDS RIGHT NOW."""
        size = int(sqrt(len(board.grid.nodes())))
        SQUARE_SIZE = 50
        X_OFFSET = 100
        Y_OFFSET = 100
        
        def on_click(board, frame):
            self.canvas.draw_text("This actually does something!", (100, 100))
        
        for x in range(size):
            for y in range(size):
                self.add_click_rect((X_OFFSET + x * SQUARE_SIZE, Y_OFFSET + y * SQUARE_SIZE),
                                    SQUARE_SIZE,
                                    SQUARE_SIZE,
                                    on_click)
    
    def add_click_rect(self, pos, width, height, on_click, color='White'):
        """Construct a rectangle that can be clicked."""
        frame_points = graphics.rectangle_points(pos, width, height)
        frame = self.canvas.draw_polygon(frame_points, fill_color=color)
        self._click_rectangles.append((pos, width, height, frame, on_click))
        return frame
        
    def _interpret_click(self, pos, board):
        """Interpret a click position by finding its click rectangle."""
        x, y = pos
        for corner, width, height, frame, on_click in self._click_rectangles:
            cx, cy = corner
            if x >= cx and x <= cx + width and y >= cy and y <= cy + height:
                on_click(board, frame)
    
game_board = Board(create_grid(5))
players = [Player('Player ' + str(i+1), game_board) for i in range(2)]
game_graphics = BoardGUI()