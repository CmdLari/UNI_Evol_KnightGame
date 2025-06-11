class Board:

    def __init__(self, width: int, height: int):
        '''Initialize the board with given width and height'''
        self.width = width
        self.height = height
        '''set up matrix for the board'''
        self.matrix = [[0 for _ in range(width)] for _ in range(height)]

    def _is_valid_position(self, position: list) -> bool:
        '''Check if the given position is within the board boundaries'''
        if 0 <= position[0] < self.width and 0 <= position[1] < self.height:
            if self.width > position[0] >= 0 and self.height > position[1] >= 0:
                return True
        return False
    
    def place_knight(self, position: list) -> bool:
        '''Place a knight on the board at the given position if valid'''
        if self.is_valid_position(position):
            self.matrix[position[1]][position[0]] = 1