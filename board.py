import random
import pygame
import time

from config import *


class Tile:
    def __init__(self, x, y, image_path, type_of_tile):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.loc = (x * TILE_SIZE, y * TILE_SIZE)
        self.rect = self.image.get_rect()
        self.type_of_tile = type_of_tile
        self.hidden = True
        self.flagged = False

    def draw(self, display):
        display.blit(self.image, self.loc)

    def __repr__(self):
        return f"{self.type_of_tile} Tile at {self.loc}"


class Board:
    def __init__(self, board_data, amt_bombs=20):
        self.tiles = []
        self.board_data = board_data
        self.flags = 0
        self.bombs = amt_bombs
        self.first_move = True

    def setup(self):
        y = 0
        for row in self.board_data:
            x = 0
            for tile in row:
                if tile == 0:
                    self.tiles.append(
                        Tile(x, y, "assets/empty.png", "0"))
                if tile == 9:
                    self.tiles.append(
                        Tile(x, y, "assets/bomb.png", "bomb"))
                if tile > 0 and tile < 9:
                    self.tiles.append(
                        Tile(x, y, f"assets/{tile}.png", f"{tile}"))
                x += 1
            y += 1

    def tile_click(self, mx, my):
        # convert mouse x and y positions to indices on board_data matrix
        mx = int(mx // TILE_SIZE)
        my = int(my // TILE_SIZE)

        print(mx, my, self.first_move)
        self.tiles[my * AMT_COLS + mx].hidden = False

        # check if the tile is a bomb
        if self.board_data[my][mx] == 9:
            for tile in self.tiles:
                print(tile)
                # reveal all the bombs one by one
                if tile.type_of_tile == "bomb":
                    tile.hidden = False
            return
        else:
            # check if the tile is empty
            if self.board_data[my][mx] == 0:
                self.get_touching_tiles(mx, my)
        self.first_move = False

    def get_touching_tiles(self, x, y):
        # recursive function that iterates over neighboring tiles and checks if they are empty for clear
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < AMT_COLS and 0 <= ny < AMT_ROWS:
                    if self.board_data[ny][nx] == 0 and self.tiles[ny * AMT_COLS + nx].hidden:
                        self.tiles[ny * AMT_COLS + nx].hidden = False
                        self.get_touching_tiles(nx, ny)
                    elif self.board_data[ny][nx] != 9 and self.tiles[ny * AMT_COLS + nx].hidden:
                        self.tiles[ny * AMT_COLS + nx].hidden = False

    def flag_tile(self, mx, my):
        # convert mouse x and y positions to indices on board_data matrix
        mx = int(mx // TILE_SIZE)
        my = int(my // TILE_SIZE)

        if self.tiles[my * AMT_COLS + mx].flagged:
            self.tiles[my * AMT_COLS + mx].flagged = False
            self.flags -= 1
            return

        self.tiles[my * AMT_COLS + mx].flagged = True
        self.flags += 1

        if self.flags == self.bombs:
            print("You Win!")

    def draw(self, display):
        for tile in self.tiles:
            if not tile.hidden:
                tile.draw(display)
            elif tile.flagged:
                display.blit(pygame.image.load("assets/flag.png"),
                             (tile.loc[0], tile.loc[1]))
            else:
                display.blit(pygame.image.load("assets/unknown.png"),
                             (tile.loc[0], tile.loc[1]))


def setup_board(amt_bombs, amt_rows, amt_cols):
    # setup board using flood fill method
    # create an empty board list with length amt_rows * amt_cols and with amt_bombs bombs
    board = [0] * (amt_rows * amt_cols - amt_bombs) + \
        [9] * amt_bombs

    # shuffle the board
    random.shuffle(board)

    # reshape the board to a 2d list
    board = [board[i:i + amt_cols] for i in range(0, len(board), amt_cols)]

    # calculate the numbers for non-bomb tiles
    for i in range(amt_rows):
        for j in range(amt_cols):
            if board[i][j] == 9:
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx = i + dx
                    ny = j + dy
                    if 0 <= nx < amt_rows and 0 <= ny < amt_cols and board[nx][ny] == 9:
                        count += 1
            board[i][j] = count

    return board


def draw_board(board):
    # draw the board
    for i in board:
        for j in i:
            print(j, end=" ")
        print()
