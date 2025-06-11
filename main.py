import pygame

from board import Board
from knight import Knight

class Main:
    def __init__(self):
        '''Initialize the main game with a board and a knight'''
        pygame.init()

        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Knight's Tour")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board(8, 8)
        self.knight = Knight([0, 0])

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self._draw_board()

            pygame.display.flip()
            self.clock.tick(60)

    def _draw_board(self):
        '''Draw the board on the screen'''
        for row in range(self.board.height):
            for col in range(self.board.width):
                color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
                pygame.draw.rect(self.screen, color, (col * 50, row * 50, 50, 50))

if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()
