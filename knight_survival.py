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
DARK_GRAY = (64, 64, 64)
SPAWN_RATE = 1
MAX_ENEMIES = 5
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Knight Survival")

class KnightSurvivalGame:
    def __init__(self):
        self.board = {}
        self.player_pos = (4, 4)
        self.board[self.player_pos] = {'piece': 'knight', 'color': 'white', 'symbol': 'N'}
        self.game_over = False
        self.pieces_sprites = self.load_sprites()
        self.turn_count = 0
        self.score = 0
        self.valid_moves = []
        self.update_valid_moves()
        print("Game initialized")  # Debug print
        
    def update_valid_moves(self):
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
        print(f"Valid moves updated: {self.valid_moves}")  # Debug print

    def spawn_enemy(self):
        if len([p for p in self.board.values() if p['color'] == 'black']) >= MAX_ENEMIES:
            return
            
        side = random.randint(0, 3)
        if side == 0:
            pos = (random.randint(0, 7), 0)
        elif side == 1:
            pos = (7, random.randint(0, 7))
        elif side == 2:
            pos = (random.randint(0, 7), 7)
        else:
            pos = (0, random.randint(0, 7))
            
        if pos in self.board:
            return
            
        piece_type = random.choice(['bishop', 'knight'])
        self.board[pos] = {
            'piece': piece_type,
            'color': 'black',
            'symbol': 'B' if piece_type == 'bishop' else 'N'
        }
        print(f"Enemy spawned at {pos}")  # Debug print

    def move_enemies(self):
        enemies = [(pos, piece) for pos, piece in self.board.items() 
                  if piece['color'] == 'black']
        print(f"Moving enemies: {len(enemies)} found")  # Debug print
        
        for pos, piece in enemies:
            if pos not in self.board:
                continue
                
            valid_moves = self.get_valid_moves(pos)
            if valid_moves:
                best_move = min(valid_moves, 
                    key=lambda m: abs(m[0] - self.player_pos[0]) + abs(m[1] - self.player_pos[1]))
                
                del self.board[pos]
                self.board[best_move] = piece
                print(f"Enemy moved from {pos} to {best_move}")  # Debug print
                
                if best_move == self.player_pos:
                    self.game_over = True
                    print("Game Over - Player captured!")  # Debug print
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
                
                black_image = pygame.image.load(black_path)
                white_image = pygame.image.load(white_path)
                
                black_scaled = pygame.transform.scale(black_image, (SQUARE_SIZE, SQUARE_SIZE))
                white_scaled = pygame.transform.scale(white_image, (SQUARE_SIZE, SQUARE_SIZE))
                
                sprites[f'black_{piece}'] = black_scaled
                sprites[f'white_{piece}'] = white_scaled
                
        except FileNotFoundError as e:
            print(f"Error loading sprites: {e}")
            raise
        
        return sprites
        
    def draw(self):
        # Draw board squares
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                
                if (col, row) == self.player_pos:
                    color = BLUE
                elif (col, row) in self.valid_moves:
                    color = RED
                
                pygame.draw.rect(screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw pieces first
                pos = (col, row)
                if pos in self.board:
                    piece = self.board[pos]
                    sprite_key = f"{piece['color']}_{piece['piece']}"
                    sprite = self.pieces_sprites[sprite_key]
                    screen.blit(sprite, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Draw move numbers on top of everything
                if (col, row) in self.valid_moves:
                    move_index = self.valid_moves.index((col, row)) + 1
                    font = pygame.font.SysFont('Arial', 32)
                    
                    # Create a small background circle for better visibility
                    circle_center = (
                        col * SQUARE_SIZE + SQUARE_SIZE//2,
                        row * SQUARE_SIZE + SQUARE_SIZE//2
                    )
                    pygame.draw.circle(screen, WHITE, circle_center, 20)
                    pygame.draw.circle(screen, BLACK, circle_center, 20, 2)
                    
                    # Render number in black for better contrast
                    number_text = font.render(str(move_index), True, BLACK)
                    text_rect = number_text.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE//2,
                        row * SQUARE_SIZE + SQUARE_SIZE//2
                    ))
                    screen.blit(number_text, text_rect)
        
        # Draw UI elements
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        
        # Change help text based on game state
        if not self.game_over:
            help_text = font.render("Press SPACE to start! Use number keys (1-8) to move", True, BLACK)
        else:
            help_text = font.render("Game Over! Press SPACE to restart", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(help_text, (10, 40))
        
        if self.game_over:
            game_over_text = font.render(f"Game Over! Final Score: {self.score}", True, BLACK)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
            screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()

    def reset(self):
        """Reset the game to initial state"""
        self.board = {}
        self.player_pos = (4, 4)
        self.board[self.player_pos] = {'piece': 'knight', 'color': 'white', 'symbol': 'N'}
        self.game_over = False
        self.turn_count = 0
        self.score = 0
        self.valid_moves = []
        self.update_valid_moves()
        print("Game reset")  # Debug print

def main():
    game = KnightSurvivalGame()
    clock = pygame.time.Clock()
    running = True
    game_started = False
    
    KEY_MAPPING = {
        pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
        pygame.K_5: 4, pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7,
        pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2, pygame.K_KP4: 3,
        pygame.K_KP5: 4, pygame.K_KP6: 5, pygame.K_KP7: 6, pygame.K_KP8: 7,
        49: 0, 50: 1, 51: 2, 52: 3, 53: 4, 54: 5, 55: 6, 56: 7
    }
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")  # Debug print
                
                if event.key == pygame.K_SPACE:
                    if game.game_over:  # If game is over, reset everything
                        game.reset()
                        game_started = False
                    if not game_started:  # Start new game
                        game_started = True
                        print("Game started!")  # Debug print
                        for _ in range(3):
                            game.spawn_enemy()
                elif game_started and not game.game_over:
                    if event.key in KEY_MAPPING:
                        move_index = KEY_MAPPING[event.key]
                        print(f"Move index: {move_index}")  # Debug print
                        
                        if move_index < len(game.valid_moves):
                            new_pos = game.valid_moves[move_index]
                            print(f"Moving to: {new_pos}")  # Debug print
                            
                            if new_pos in game.board:
                                del game.board[new_pos]
                                game.score += 1
                            del game.board[game.player_pos]
                            game.player_pos = new_pos
                            game.board[new_pos] = {'piece': 'knight', 'color': 'white', 'symbol': 'N'}
                            
                            game.spawn_enemy()
                            game.move_enemies()
                            game.update_valid_moves()
        
        game.draw()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()