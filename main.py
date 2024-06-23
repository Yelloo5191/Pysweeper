import pygame
import sys
import random
from pygame.locals import *

from board import setup_board, Board
from config import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(SCALED_WINDOW_SIZE)
pygame.display.set_caption("Minesweeper by @Yelloo5191")


def main():

    # main menu loop
    def menu():
        while True:
            # fill the display with blue
            display.fill((55, 118, 171))

            # get mouse position
            mx, my = pygame.mouse.get_pos()
            # normalze the mouse position
            mx /= WINDOW_SIZE[0] / SCALED_WINDOW_SIZE[0]
            my /= WINDOW_SIZE[1] / SCALED_WINDOW_SIZE[1]

            # render the menu
            font = pygame.font.SysFont("Tahoma", 24)
            title = font.render("Minesweeper", True, (255, 211, 67))
            display.blit(title, (SCALED_WINDOW_SIZE[0] // 2 - title.get_width() // 2,
                                 SCALED_WINDOW_SIZE[1] // 2 - title.get_height() // 2))
            start = font.render("Start", True, (255, 211, 67))
            display.blit(start, (SCALED_WINDOW_SIZE[0] // 2 - start.get_width() // 2,
                                 SCALED_WINDOW_SIZE[1] // 2 - start.get_height() // 2 + 50))

            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mx > SCALED_WINDOW_SIZE[0] // 2 - start.get_width() // 2 and mx < SCALED_WINDOW_SIZE[0] // 2 + start.get_width() // 2:
                            if my > SCALED_WINDOW_SIZE[1] // 2 - start.get_height() // 2 + 50 and my < SCALED_WINDOW_SIZE[1] // 2 + start.get_height() // 2 + 50:
                                game()

            # render the display
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(FPS)

    # game loop
    def game():
        # setup board
        board_data = setup_board(
            amt_bombs=AMT_BOMBS, amt_rows=AMT_ROWS, amt_cols=AMT_COLS)
        board = Board(board_data=board_data, amt_bombs=AMT_BOMBS)
        board.setup()

        # game loop runs till event QUIT is called
        while True:
            # fill the display with blue
            display.fill((55, 118, 171))

            # get mouse position
            mx, my = pygame.mouse.get_pos()
            # normalze the mouse position
            mx /= WINDOW_SIZE[0] / SCALED_WINDOW_SIZE[0]
            my /= WINDOW_SIZE[1] / SCALED_WINDOW_SIZE[1]

            # render the menu
            font = pygame.font.SysFont("Impact", 14)
            bombs = font.render(f"Bombs: {board.bombs}", True, (255, 211, 67))
            display.blit(
                bombs, (0, SCALED_WINDOW_SIZE[1] - bombs.get_height()))

            restart = font.render("Restart", True, (255, 211, 67))
            display.blit(restart, (SCALED_WINDOW_SIZE[0] - restart.get_width(),
                                   SCALED_WINDOW_SIZE[1] - restart.get_height()))

            # render the board
            board.draw(display=display)

            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mx > SCALED_WINDOW_SIZE[0] - restart.get_width() and mx < SCALED_WINDOW_SIZE[0]:
                            if my > SCALED_WINDOW_SIZE[1] - restart.get_height() and my < SCALED_WINDOW_SIZE[1]:
                                game()
                        # check if within bounds of board
                        if mx > 0 and mx < SCALED_WINDOW_SIZE[0] and my > 0 and my < AMT_COLS * TILE_SIZE * 2 // 2:
                            board.tile_click(mx, my)
                    if event.button == 3:
                        board.flag_tile(mx, my)

            # render the display
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(FPS)

    menu()


if __name__ == "__main__":
    main()
