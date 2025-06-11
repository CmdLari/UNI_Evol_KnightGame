class Knight:
    '''Knight object to be moved across the board'''

    def __init__(self, position=[0,0], board_size=8):
        '''Initialize the knight with a position on the board'''
        self.position = position
        self.board_size = board_size
        self.visited_positions = set()  

    def move(self, steps_x, steps_y):
        '''Move the knight by the specified steps in x and y direction'''
        # Validate the move
        if self._move_is_valid(steps_x, steps_y):
            self.position[0]+=steps_x
            self.position[1]+=steps_y
            self.visited_positions.add(tuple(self.position))

    def _move_is_valid(self, steps_x, steps_y):        
        '''Check if the move is valid for a knight'''
        if (abs(steps_x) == 2 and abs(steps_y) == 1) or (abs(steps_x) == 1 and abs(steps_y) == 2):
            if self.position[0] + steps_x >= 0 and self.position[1] + steps_y >= 0:
                # Assuming the board is 8x8, adjust as necessary
                if self.position[0] + steps_x < self.board_size and self.position[1] + steps_y < self.board_size:
                 return True
        return False 



