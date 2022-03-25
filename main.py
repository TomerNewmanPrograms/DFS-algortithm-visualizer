import pygame
import math
import random

ROWS = 24
WIDTH = 1200
WIN = pygame.display.set_mode((WIDTH - 100, WIDTH - 200))
pygame.display.set_caption("DFS Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# spot on the board/grid class
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_row(self):
        return self.row

    def get_id(self):
        return self.id

    def get_col(self):
        return self.col

    def get_pos(self):
        return self.row, self.col

    def ger_color(self):
        return self.color

    def is_Closed(self):
        return self.color == RED

    def is_Open(self):
        return self.color == GREEN

    def is_Barrier(self):
        return self.color == BLACK

    def is_Start(self):
        return self.color == ORANGE

    def is_End(self):
        return self.color == TURQUOISE

    def Reset(self):
        self.color = WHITE

    def Make_Closed(self):
        self.color = RED

    def Make_Open(self):
        self.color = GREEN

    def Make_Barrier(self):
        self.color = BLACK

    def Make_Start(self):
        self.color = ORANGE

    def Make_End(self):
        self.color = TURQUOISE

    def Make_Path(self):
        self.color = PURPLE

    def is_Path(self):
        return self.color == PURPLE

    def Draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def Update_Neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_Barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_Barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_Barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_Barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def reconstruct_path(current, draw):
    while current.father != -1:
        current.Make_Path()
        draw()
        current = current.father


# path finding algorithm
def dfs(draw, grid, start, end, found=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    start.Make_Open()
    draw()
    pygame.time.delay(20)
    start.Update_Neighbors(grid)
    random.shuffle(start.neighbors)
    for neighbor in start.neighbors:
        if neighbor.color == TURQUOISE:
            neighbor.Make_Path()
            start.Make_Path()
            found = True
            draw()
            return
        if neighbor.color == WHITE:
            dfs(draw, grid, neighbor, end, found)
            if neighbor.is_Path():
                start.Make_Path()
                draw()
                return
    start.Make_Closed()
    draw()


def Make_Grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def Draw_Grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Main Drawing Function
def Draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.Draw(win)
    Draw_Grid(win, rows, width)
    pygame.display.update()


# returning the position the User chose
def Get_Clicked_Position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


# Main Function
def main(win, width):
    grid = Make_Grid(ROWS, width)
    start = None
    end = None

    run = True
    while run:
        Draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # if left mouse was clicked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = Get_Clicked_Position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.Make_Start()
                elif not end and spot != start:
                    end = spot
                    end.Make_End()
                elif spot != start and spot != end:
                    spot.Make_Barrier()
            # if right mouse was clicked
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = Get_Clicked_Position(pos, ROWS, width)
                spot = grid[row][col]
                spot.Reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            # If the User chose to find the path
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for aRow in grid:
                        for aSpot in aRow:
                            aSpot.Update_Neighbors(grid)
                    dfs(lambda: Draw(win, grid, ROWS, width), grid, start, end)
                # If the User chose to clear the grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = Make_Grid(ROWS, width)
    pygame.quit()


main(WIN, WIDTH)
