import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
SQUARE_SIZE = WINDOW_SIZE // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Initialize display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game")

class ChessGame:
    def __init__(self):
        self.board = self.init_board()
        self.selected_piece = None
        self.turn = 'white'
        self.font = pygame.font.SysFont('Arial', 64)
        
    def init_board(self):
        # Initialize standard chess board layout
        board = {}
        # Set up pawns
        for i in range(8):
            board[(i, 1)] = {'piece': 'pawn', 'color': 'black', 'symbol': 'p'}
            board[(i, 6)] = {'piece': 'pawn', 'color': 'white', 'symbol': 'P'}
            
        # Set up other pieces
        pieces = [
            ('rook', 'R'), ('knight', 'N'), ('bishop', 'B'), 
            ('queen', 'Q'), ('king', 'K'), ('bishop', 'B'), 
            ('knight', 'N'), ('rook', 'R')
        ]
        for i in range(8):
            board[(i, 0)] = {'piece': pieces[i][0], 'color': 'black', 'symbol': pieces[i][1].lower()}
            board[(i, 7)] = {'piece': pieces[i][0], 'color': 'white', 'symbol': pieces[i][1]}
            
        return board

    def get_valid_moves(self, pos):
        piece = self.board.get(pos)
        if not piece:
            return []
        
        valid_moves = []
        x, y = pos
        
        if piece['piece'] == 'pawn':
            direction = 1 if piece['color'] == 'black' else -1
            # Forward move
            next_pos = (x, y + direction)
            if next_pos not in self.board:
                valid_moves.append(next_pos)
                # Initial two-square move
                if (piece['color'] == 'black' and y == 1) or (piece['color'] == 'white' and y == 6):
                    double_pos = (x, y + 2*direction)
                    if double_pos not in self.board:
                        valid_moves.append(double_pos)
            # Capture moves
            for dx in [-1, 1]:
                capture_pos = (x + dx, y + direction)
                if capture_pos in self.board and self.board[capture_pos]['color'] != piece['color']:
                    valid_moves.append(capture_pos)
                    
        elif piece['piece'] == 'rook':
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for i in range(1, 8):
                    new_pos = (x + direction[0]*i, y + direction[1]*i)
                    if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                        break
                    if new_pos in self.board:
                        if self.board[new_pos]['color'] != piece['color']:
                            valid_moves.append(new_pos)
                        break
                    valid_moves.append(new_pos)
                    
        elif piece['piece'] == 'knight':
            moves = [
                (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
                (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)
            ]
            for move in moves:
                if (0 <= move[0] < 8 and 0 <= move[1] < 8 and 
                    (move not in self.board or self.board[move]['color'] != piece['color'])):
                    valid_moves.append(move)
                    
        elif piece['piece'] == 'bishop':
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_pos = (x + direction[0]*i, y + direction[1]*i)
                    if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                        break
                    if new_pos in self.board:
                        if self.board[new_pos]['color'] != piece['color']:
                            valid_moves.append(new_pos)
                        break
                    valid_moves.append(new_pos)
                    
        elif piece['piece'] == 'queen':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for direction in directions:
                for i in range(1, 8):
                    new_pos = (x + direction[0]*i, y + direction[1]*i)
                    if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                        break
                    if new_pos in self.board:
                        if self.board[new_pos]['color'] != piece['color']:
                            valid_moves.append(new_pos)
                        break
                    valid_moves.append(new_pos)
                    
        elif piece['piece'] == 'king':
            moves = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
            ]
            for move in moves:
                if (0 <= move[0] < 8 and 0 <= move[1] < 8 and 
                    (move not in self.board or self.board[move]['color'] != piece['color'])):
                    valid_moves.append(move)
                    
        return valid_moves

    def draw(self):
        # Draw board
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                # Highlight selected piece and valid moves
                if self.selected_piece and (col, row) == self.selected_piece:
                    color = YELLOW
                elif self.selected_piece and (col, row) in self.get_valid_moves(self.selected_piece):
                    color = YELLOW
                    
                pygame.draw.rect(screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw pieces using ASCII symbols
                pos = (col, row)
                if pos in self.board:
                    piece = self.board[pos]
                    text = self.font.render(piece['symbol'], True, BLACK if piece['color'] == 'black' else WHITE)
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2,
                                                    row * SQUARE_SIZE + SQUARE_SIZE//2))
                    screen.blit(text, text_rect)
        
        pygame.display.flip()

def main():
    game = ChessGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                
                if game.selected_piece is None:
                    if (col, row) in game.board and game.board[(col, row)]['color'] == game.turn:
                        game.selected_piece = (col, row)
                else:
                    # Handle piece movement with valid move checking
                    start = game.selected_piece
                    valid_moves = game.get_valid_moves(start)
                    
                    if (col, row) in valid_moves:
                        game.board[(col, row)] = game.board[start]
                        del game.board[start]
                        game.turn = 'black' if game.turn == 'white' else 'white'
                    game.selected_piece = None
        
        game.draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
