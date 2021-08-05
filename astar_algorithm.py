import pygame
import math
from queue import PriorityQueue

# Define width of window - square, so no height variable needed
WIDTH = 800

# Setting up the display (win for window)
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# Caption for the display
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors to use
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Defining a class, creating a visualization tool
# It needs to be able to keep track of all of these nodes
# Where it is (row, col position), width of itself (to draw itself), its neighbors, color (to differentiate itself)
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        # To keep track of position
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = width
        self.total_rows = total_rows

    # To get its position
    def get_position(self):
        return self.row, self.col

    # To check if node was already checked
    def is_closed(self):
        # If the color of the node is red, it was checked
        return self.color == RED

    # To check if node can be analyzed by algorithm
    def is_open(self):
        # If the color of the node is green, it can be checked
        return self.color == GREEN

    # To check if the node is a barrier
    def is_barrier(self):
        # If the color of the node is black, it is a barrier
        return self.color == BLACK

    # Start node
    def is_start(self):
        return self.color == ORANGE

    # End node
    def is_end(self):
        return self.color == TURQUOISE

    # Method to reset the color back to white
    def reset(self):
        self.color = WHITE

    # The next series of methods essentially makes the node to the desired color

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    # Method to actually draw the node
    def draw(self, win):
        # Parameters is the window, the color, and the rectangle. Pretty self explanatory
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Check if neighbors are barriers, and if not keep them
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    # How to handle comparing two nodes together, lt for less than
    def __lt__(self, other):
        return False


# Defining the H score heuristic function, p1 and p2 are points (row, col)
def h(p1, p2):
    # Using manhattan distance, quickest L to the shape, because no diagonals on this
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# To display the actual path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    # Priority Queue is just an efficient way to get the smallest element out of it, already has sorting algorithm in it
    open_set = PriorityQueue()
    # First step to put the start node into the open set
    open_set.put((0, count, start))
    # Dictionary to check which node we came from
    came_from = {}
    # Keep track of the g score - current shortest distance fromm current node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # Keep track of the f score - with the heuristic
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_position(), end.get_position())

    # Keep track of all items in and out of the priority queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            # Way to exit the loop in case the user wants to
            if event.type == pygame.QUIT:
                pygame.quit()

        # 2 so that can get node
        current = open_set.get()[2]
        # Take whatever from the priority queue and sync with the hash
        open_set_hash.remove(current)

        # Construct path if reached the end
        if current == end:
            reconstruct_path(came_from, end, draw)
            # Prevent purple over end node
            end.make_end()
            # Prevent purple over start
            start.make_start()
            return True

        for neighbor in current.neighbors:
            # Assume all edges are 1, temp g score, and add 1 (because assuming the edge is 1 and not weighted)
            temp_g_score = g_score[current] + 1

            # If found a better way, then update the g score
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # f(n) = g(n) + h(n)
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    # Put in this neighbor into the open set
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    # Now this neighbor is open
                    neighbor.make_open()

        draw()

        # If the node just considered, is not the start node, close it
        if current != start:
            current.make_closed()

    return None


# Data structure to hold all of the nodes so you can actually do things
def make_grid(rows, width):
    grid = []
    # Gap between each of the rows
    gap = width // rows

    # In grid row i, append the node into it. Bunch of lists inside of lists that each have nodes
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


# Need a way to draw the grid
def draw_grid(win, rows, width):
    gap = width // rows

    # Drawing horizontal lines through the window
    for i in range(rows):
        # Parameters to draw line are the window, color, the position for start of the line, and end of the line
        # Multiplying the index by the gap, so we get accurate places
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    # Exact same thing but with vertical lines
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Main draw function to draw everything
def draw(win, grid, rows, width):
    # Fills the window with one color, every frame do this and then repaint with what we want
    win.fill(WHITE)

    # Loop through the window and draw the spots
    for row in grid:
        for node in row:
            node.draw(win)

    # Drawing the gridlines
    draw_grid(win, rows, width)

    # Updating the display every frame
    pygame.display.update()


# Translating the mouse position into a row column position
def clicked_position(pos, rows, width):
    # Go through the math to understand, remember // is floor division!!

    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# Main loop to check everything
def main(win, width):
    # Can change this to whatever
    rows = 50
    # Make the actual grid
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False

    # While running, check events that are happening
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            # If the player exits, stop running
            if event.type == pygame.QUIT:
                run = False

            # If the algorithm started, user should not be able to do anything but quit - it will mess the algo up
            if started:
                continue

            # If the mouse was pressed, left side
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = clicked_position(pos, rows, width)
                node = grid[row][col]

                # If the starting position hasn't been established yet...
                if not start and node != end:
                    start = node
                    start.make_start()
                # If the ending position hasn't been established yet...
                elif not end and node != start:
                    end = node
                    end.make_end()

                # If neither above, has to be made a barrier (obviously if clicked)
                elif node != end and node != start:
                    node.make_barrier()

            # If the mouse was pressed, right side
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = clicked_position(pos, rows, width)
                node = grid[row][col]
                # If right click, then will reset to white
                node.reset()
                # In case you reset the start or end nodes
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # Start running the algorithm by pressing space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    # Update neighbors
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Calling the algorithm
                    '''
                    Lambda is an anonymous function
                    x = Lambda: print("hello")
                    x() --> will print hello
                    '''
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                # If press 'c' clear the board
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    # Self explanatory, exits the game window
    pygame.quit()


main(WIN, WIDTH)
