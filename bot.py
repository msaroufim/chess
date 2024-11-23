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
DARK_GRAY = (64, 64, 64)  # Darker color for white pieces on light squares

# Initialize display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game")

class ChessGame:
    def __init__(self):
        self.board = self.init_board()
        self.selected_piece = None
        self.turn = 'white'
        self.font = pygame.font.SysFont('Arial', 64)
        self.game_over = False
        
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
        # Set up back rows
        for i in range(8):
            board[(i, 0)] = {'piece': pieces[i][0], 'color': 'black', 'symbol': pieces[i][1].lower()}
            board[(i, 7)] = {'piece': pieces[i][0], 'color': 'white', 'symbol': pieces[i][1]}
            
        return board

    def is_in_check(self, color):
        # Find king position
        king_pos = None
        for pos, piece in self.board.items():
            if piece['piece'] == 'king' and piece['color'] == color:
                king_pos = pos
                break
        
        # Check if any opponent piece can capture the king
        for pos, piece in self.board.items():
            if piece['color'] != color:
                valid_moves = self.get_valid_moves(pos, check_check=False)
                if king_pos in valid_moves:
                    return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
            
        # Try all possible moves for all pieces
        for pos, piece in self.board.items():
            if piece['color'] == color:
                valid_moves = self.get_valid_moves(pos)
                for move in valid_moves:
                    # Try move and see if still in check
                    original_board = self.board.copy()
                    self.board[move] = self.board[pos]
                    del self.board[pos]
                    
                    still_in_check = self.is_in_check(color)
                    self.board = original_board
                    
                    if not still_in_check:
                        return False
        return True

    def get_valid_moves(self, pos, check_check=True):
        piece = self.board.get(pos)
        if not piece:
            return []
        
        valid_moves = []
        x, y = pos
        
        if piece['piece'] == 'pawn':
            direction = 1 if piece['color'] == 'black' else -1
            # Forward move
            next_pos = (x, y + direction)
            if 0 <= next_pos[1] < 8 and next_pos not in self.board:
                valid_moves.append(next_pos)
                # Initial two-square move
                if (piece['color'] == 'black' and y == 1) or (piece['color'] == 'white' and y == 6):
                    double_pos = (x, y + 2*direction)
                    if double_pos not in self.board:
                        valid_moves.append(double_pos)
            # Capture moves diagonally
            for dx in [-1, 1]:
                capture_pos = (x + dx, y + direction)
                if (0 <= capture_pos[0] < 8 and 0 <= capture_pos[1] < 8 and
                    capture_pos in self.board and self.board[capture_pos]['color'] != piece['color']):
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

        # Filter moves that would leave king in check
        if check_check:
            filtered_moves = []
            for move in valid_moves:
                original_board = self.board.copy()
                self.board[move] = self.board[pos]
                del self.board[pos]
                
                if not self.is_in_check(piece['color']):
                    filtered_moves.append(move)
                    
                self.board = original_board
            return filtered_moves
                    
        return valid_moves

    def promote_pawn(self, pos):
        piece = self.board[pos]
        if piece['piece'] == 'pawn':
            if (piece['color'] == 'white' and pos[1] == 0) or (piece['color'] == 'black' and pos[1] == 7):
                # Automatically promote to queen for simplicity
                symbol = 'Q' if piece['color'] == 'white' else 'q'
                self.board[pos] = {'piece': 'queen', 'color': piece['color'], 'symbol': symbol}

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
                    # Use dark gray for white pieces on light squares
                    piece_color = BLACK if piece['color'] == 'black' else (DARK_GRAY if (row + col) % 2 == 0 else WHITE)
                    text = self.font.render(piece['symbol'], True, piece_color)
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2,
                                                    row * SQUARE_SIZE + SQUARE_SIZE//2))
                    screen.blit(text, text_rect)
        
        if self.game_over:
            # Display checkmate message
            winner = "Black" if self.turn == "white" else "White"
            font = pygame.font.SysFont('Arial', 32)
            text = font.render(f"{winner} wins by checkmate!", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
            screen.blit(text, text_rect)
            
        pygame.display.flip()

def main():
    game = ChessGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
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
                        # Handle capturing by replacing the piece
                        game.board[(col, row)] = game.board[start]
                        del game.board[start]
                        
                        # Check for pawn promotion
                        game.promote_pawn((col, row))
                        
                        # Switch turns
                        game.turn = 'black' if game.turn == 'white' else 'white'
                        
                        # Check for checkmate
                        if game.is_checkmate(game.turn):
                            game.game_over = True
                            
                    game.selected_piece = None
        
        game.draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
