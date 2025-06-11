class Board:

    def __init__(self, width: int, height: int):
        '''Initialize the board with given width and height'''
        self.width = width
        self.height = height
        '''set up matrix for the board'''
        self.matrix = [[0 for _ in range(width)] for _ in range(height)]