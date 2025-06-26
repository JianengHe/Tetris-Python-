import pygame, random, sys

pygame.init()

# Constants
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60
DROP_SPEED = 500  # milliseconds

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Tetromino shapes
SHAPES = {
    'I': [[(0, -1), (0, 0), (0, 1), (0, 2)], CYAN],
    'O': [[(0, 0), (1, 0), (0, 1), (1, 1)], YELLOW],
    'T': [[(0, 0), (-1, 0), (1, 0), (0, 1)], MAGENTA]
}

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Board setup (2D list)
board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

# Tetromino class
class Tetromino:
    def __init__(self, shape):
        self.blocks, self.color = SHAPES[shape]
        self.pos = [COLS // 2, 0]

    def get_coords(self, rotated=False):
        coords = []
        for x, y in self.blocks:
            if rotated:
                x, y = -y, x  # 90° rotation
            coords.append((self.pos[0] + x, self.pos[1] + y))
        return coords

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy
        if not is_valid(self.get_coords()):
            self.pos[0] -= dx
            self.pos[1] -= dy

    def rotate(self):
        new_coords = self.get_coords(rotated=True)
        if is_valid(new_coords):
            self.blocks = [(-y, x) for x, y in self.blocks]

def is_valid(coords):
    for x, y in coords:
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return False
        if board[y][x] != BLACK:
            return False
    return True

def lock_piece(piece):
    for x, y in piece.get_coords():
        board[y][x] = piece.color

def clear_lines():
    global board
    board = [row for row in board if any(cell == BLACK for cell in row)]
    while len(board) < ROWS:
        board.insert(0, [BLACK] * COLS)

def draw_board():
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, board[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_piece(piece):
    for x, y in piece.get_coords():
        pygame.draw.rect(screen, piece.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def game_over():
    for cell in board[0]:
        if cell != BLACK:
            return True
    return False

# Main loop
piece = Tetromino(random.choice(list(SHAPES.keys())))
drop_time = pygame.time.get_ticks()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                piece.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                piece.move(1, 0)
            elif event.key == pygame.K_DOWN:
                piece.move(0, 1)
            elif event.key == pygame.K_UP:
                piece.rotate()

    # Handle gravity
    if pygame.time.get_ticks() - drop_time > DROP_SPEED:
        piece.move(0, 1)
        if not is_valid(piece.get_coords()):
            piece.move(0, -1)
            lock_piece(piece)
            clear_lines()
            piece = Tetromino(random.choice(list(SHAPES.keys())))
            if not is_valid(piece.get_coords()):
                print("Game Over!")
                running = False
        drop_time = pygame.time.get_ticks()

    draw_board()
    draw_piece(piece)
    pygame.display.flip()

pygame.quit()
sys.exit()
