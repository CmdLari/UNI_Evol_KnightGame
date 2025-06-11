import pygame

from board import Board
from knight import Knight
from utils import load_image

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
        self.knight_image = load_image("knight_image.png", (50, 50))
        if not self.knight_image:
            print("Failed to load knight image. Please ensure 'knight_image.png' exists.")
            self.running = False
        self.knight_image = pygame.transform.scale(self.knight_image, (50, 50))

    def run(self):
        while self.running:
            self._check_events()

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
        for row in range(self.board.height):
            for col in range(self.board.width):
                # Draw the visited positions
                if (col, row) in self.knight.visited_positions:
                    pygame.draw.circle(self.screen, (255, 0, 0), (col * 50 + 25, row * 50 + 25), 10)

        #draw knight
        kx, ky = self.knight.position
        pixel_x = kx * 50
        pixel_y = ky * 50
        self.screen.blit(self.knight_image, (pixel_x, pixel_y))


    def _check_events(self):
        '''Check for events and handle them'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                #TODO: more intuitive controls
                if event.key == pygame.K_q:   # Move 2 up, 1 left
                    self.knight.move(-1, -2)
                elif event.key == pygame.K_w: # Move 2 up, 1 right
                    self.knight.move(1, -2)
                elif event.key == pygame.K_a: # Move 2 left, 1 up
                    self.knight.move(-2, -1)
                elif event.key == pygame.K_s: # Move 2 left, 1 down
                    self.knight.move(-2, 1)
                elif event.key == pygame.K_e: # Move 2 up, 1 right
                    self.knight.move(2, -1)
                elif event.key == pygame.K_d: # Move 2 right, 1 up
                    self.knight.move(2, 1)
                elif event.key == pygame.K_z: # Move 1 down, 2 left
                    self.knight.move(-1, 2)
                elif event.key == pygame.K_x: # Move 1 down, 2 right
                    self.knight.move(1, 2)
                if event.key == pygame.K_ESCAPE:
                    self.running = False

if __name__ == "__main__":
    game = Main()
    game.run()
    pygame.quit()
