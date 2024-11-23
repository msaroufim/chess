import pygame
import sys
import os
import random

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
SPAWN_RATE = 2  # Spawn enemy every 2 turns
MAX_ENEMIES = 5  # Maximum enemies on board
RED = (255, 0, 0)  # For highlighting valid moves
BLUE = (0, 0, 255)  # For highlighting current position

# Initialize display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game")

class KnightSurvivalGame:
    def __init__(self):
        self.board = {}  # Empty board to start
        self.player_pos = (4, 4)  # Start knight in middle
        self.board[self.player_pos] = {'piece': 'knight', 'color': 'white', 'symbol': 'N'}
        self.game_over = False
        self.pieces_sprites = self.load_sprites()
        self.turn_count = 0
        self.score = 0
        self.valid_moves = []  # Store current valid moves
        self.update_valid_moves()
        
    def update_valid_moves(self):
        """Update the list of valid knight moves"""
        x, y = self.player_pos
        possible_moves = [
            (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
            (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)
        ]
        self.valid_moves = [
            move for move in possible_moves 
            if 0 <= move[0] < 8 and 0 <= move[1] < 8 and 
            (move not in self.board or self.board[move]['color'] == 'black')
        ]

    def spawn_enemy(self):
        if len(self.board) - 1 >= MAX_ENEMIES:  # -1 because of player
            return
            
        # Choose spawn location on edge of board
        side = random.randint(0, 3)
        if side == 0:  # Top
            pos = (random.randint(0, 7), 0)
        elif side == 1:  # Right
            pos = (7, random.randint(0, 7))
        elif side == 2:  # Bottom
            pos = (random.randint(0, 7), 7)
        else:  # Left
            pos = (0, random.randint(0, 7))
            
        # Don't spawn if position is occupied
        if pos in self.board:
            return
            
        # Randomly choose between bishop and knight
        piece_type = random.choice(['bishop', 'knight'])
        self.board[pos] = {
            'piece': piece_type,
            'color': 'black',
            'symbol': 'B' if piece_type == 'bishop' else 'N'
        }

    def move_enemies(self):
        # Create a list of enemy positions and pieces before moving
        enemies = [(pos, piece) for pos, piece in self.board.items() 
                  if piece['color'] == 'black']
        
        # Process each enemy's movement
        for pos, piece in enemies:
            if pos not in self.board:  # Skip if enemy was already captured
                continue
                
            # Get valid moves towards player
            valid_moves = self.get_valid_moves(pos)
            if valid_moves:
                # Find move closest to player
                best_move = min(valid_moves, 
                    key=lambda m: abs(m[0] - self.player_pos[0]) + abs(m[1] - self.player_pos[1]))
                
                # Move enemy
                del self.board[pos]
                self.board[best_move] = piece
                
                # Check if enemy caught player
                if best_move == self.player_pos:
                    self.game_over = True
                    return

    def get_valid_moves(self, pos):
        piece = self.board.get(pos)
        if not piece:
            return []
            
        valid_moves = []
        x, y = pos
        
        if piece['piece'] == 'knight':
            moves = [
                (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
                (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)
            ]
            for move in moves:
                if (0 <= move[0] < 8 and 0 <= move[1] < 8 and 
                    (move not in self.board or 
                     (self.board[move]['color'] != piece['color']))):
                    valid_moves.append(move)
                    
        elif piece['piece'] == 'bishop':
            # Simplified bishop movement - one square diagonally
            moves = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
            for move in moves:
                if (0 <= move[0] < 8 and 0 <= move[1] < 8 and 
                    (move not in self.board or 
                     (self.board[move]['color'] != piece['color']))):
                    valid_moves.append(move)
                    
        return valid_moves

    def load_sprites(self):
        sprites = {}
        pieces = ['king', 'queen', 'rook', 'knight', 'bishop', 'pawn']
        
        try:
            for piece in pieces:
                sprite_root_folder = "./sprites"
                black_path = f'{sprite_root_folder}/b_{piece}_png_shadow_1024px.png'
                white_path = f'{sprite_root_folder}/w_{piece}_png_shadow_1024px.png'
                
                # Load and scale images
                black_image = pygame.image.load(black_path)
                white_image = pygame.image.load(white_path)
                
                # Scale images to fit squares
                black_scaled = pygame.transform.scale(black_image, (SQUARE_SIZE, SQUARE_SIZE))
                white_scaled = pygame.transform.scale(white_image, (SQUARE_SIZE, SQUARE_SIZE))
                
                sprites[f'black_{piece}'] = black_scaled
                sprites[f'white_{piece}'] = white_scaled
                
        except FileNotFoundError as e:
            print(f"Error loading sprites: {e}")
            raise
        
        return sprites

    def draw(self):
        # Draw board
        for row in range(8):
            for col in range(8):
                # Draw board squares
                color = WHITE if (row + col) % 2 == 0 else GRAY
                
                # Highlight current position
                if (col, row) == self.player_pos:
                    color = BLUE
                # Highlight valid moves with numbers
                elif (col, row) in self.valid_moves:
                    color = RED
                
                pygame.draw.rect(screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw move numbers
                if (col, row) in self.valid_moves:
                    move_index = self.valid_moves.index((col, row)) + 1
                    font = pygame.font.SysFont('Arial', 32)
                    number_text = font.render(str(move_index), True, WHITE)
                    text_rect = number_text.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE//2,
                        row * SQUARE_SIZE + SQUARE_SIZE//2
                    ))
                    screen.blit(number_text, text_rect)
                
                # Draw pieces
                pos = (col, row)
                if pos in self.board:
                    piece = self.board[pos]
                    sprite_key = f"{piece['color']}_{piece['piece']}"
                    sprite = self.pieces_sprites[sprite_key]
                    screen.blit(sprite, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Draw score and controls help
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        help_text = font.render("Use number keys (1-8) to move", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(help_text, (10, 40))
        
        if self.game_over:
            text = font.render(f"Game Over! Final Score: {self.score}", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
            screen.blit(text, text_rect)
            
        pygame.display.flip()

def main():
    game = KnightSurvivalGame()
    clock = pygame.time.Clock()
    running = True
    player_turn = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game.game_over and player_turn:
                moved = False
                
                # Number keys 1-8 for quick moves
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                               pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                    move_index = event.key - pygame.K_1  # Convert key to 0-7 index
                    if move_index < len(game.valid_moves):
                        new_pos = game.valid_moves[move_index]
                        
                        # Make the move
                        if new_pos in game.board:
                            del game.board[new_pos]  # Capture enemy piece
                        del game.board[game.player_pos]
                        game.player_pos = new_pos
                        game.board[new_pos] = {'piece': 'knight', 'color': 'white', 'symbol': 'N'}
                        moved = True
                        player_turn = False
                        game.turn_count += 1
                        game.score += 1
                        game.update_valid_moves()  # Update valid moves for new position
                
                if moved and game.turn_count % SPAWN_RATE == 0:
                    game.spawn_enemy()
        
        # Enemy turn
        if not player_turn and not game.game_over:
            game.move_enemies()
            player_turn = True
            game.update_valid_moves()  # Update valid moves after enemies move
        
        game.draw()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
