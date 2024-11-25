from enum import Enum
import pygame

class AbilityType(Enum):
    TELEPORT = "teleport"
    SWAP = "swap"
    SHIELD = "shield"
    DESTROY = "destroy"

class Ability:
    def __init__(self, name, key, cooldown):
        self.name = name
        self.key = key
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def is_available(self):
        return self.current_cooldown == 0

    def use(self):
        if self.is_available():
            print(f"Using {self.name} ability")  # Debug print
            self.current_cooldown = self.cooldown
            return True
        print(f"{self.name} is on cooldown: {self.current_cooldown} turns remaining")  # Debug print
        return False

    def update(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def draw(self, screen, position):
        # Draw ability box background
        pygame.draw.rect(screen, (50, 50, 50), (position[0], position[1], 50, 60))
        
        # Draw main text (either cooldown or key) - raised by 5 pixels
        if self.is_available():
            main_text = self.key
            color = (0, 255, 0)  # Green for available
        else:
            main_text = str(self.current_cooldown)
            color = (255, 255, 255)  # White for cooldown
        
        # Raised the text position by adjusting y coordinate
        text = self.font.render(main_text, True, color)
        text_rect = text.get_rect(center=(position[0] + 25, position[1] + 15))  # Changed from +20 to +15
        screen.blit(text, text_rect)
        
        # Draw ability name below - raised by 5 pixels
        name_text = self.small_font.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(position[0] + 25, position[1] + 40))  # Changed from +45 to +40
        screen.blit(name_text, name_rect)

class TeleportAbility(Ability):
    def __init__(self):
        super().__init__("Teleport", "Q", 3)
    
    def execute(self, game_state, selected_piece, target_pos):
        if not selected_piece:
            print("No piece selected for teleport")
            return False
        if not game_state.is_empty(target_pos):
            print("Target position is not empty")
            return False
        if self.use():
            print(f"Teleporting piece from {selected_piece.position} to {target_pos}")
            selected_piece.position = target_pos
            return True
        return False

class SwapAbility(Ability):
    def __init__(self):
        super().__init__("Swap", "W", 4)
    
    def execute(self, game_state, piece1, piece2):
        if not piece1 or not piece2:
            print("Need two pieces to swap")
            return False
        if self.use():
            print(f"Swapping pieces at {piece1.position} and {piece2.position}")
            pos1 = piece1.position
            piece1.position = piece2.position
            piece2.position = pos1
            return True
        return False

class ShieldAbility(Ability):
    def __init__(self):
        super().__init__("Shield", "E", 5)
    
    def execute(self, game_state, piece):
        if not piece:
            print("No piece selected for shield")
            return False
        if self.use():
            print(f"Shielding piece at {piece.position}")
            piece.shielded = True
            return True
        return False

class DestroyAbility(Ability):
    def __init__(self):
        super().__init__("Destroy", "R", 8)
    
    def execute(self, game_state, target_piece):
        if not target_piece:
            print("No piece selected for destroy")
            return False
        if self.use():
            print(f"Destroying piece at {target_piece.position}")
            game_state.remove_piece(target_piece)
            return True
        return False

class AbilityManager:
    def __init__(self):
        self.abilities = {
            'Q': TeleportAbility(),
            'W': SwapAbility(),
            'E': ShieldAbility(),
            'R': DestroyAbility()
        }
        self.selected_ability = None

    def draw(self, screen):
        # Draw abilities in a row at the bottom of the screen
        start_x = 10
        start_y = screen.get_height() - 80  # Moved up to make room for ability names
        for ability in self.abilities.values():
            ability.draw(screen, (start_x, start_y))
            start_x += 60  # Increased spacing between abilities

    def update(self):
        for ability in self.abilities.values():
            ability.update()

    def handle_key(self, key):
        key = key.upper()
        if key in self.abilities:
            ability = self.abilities[key]
            if ability.is_available():
                print(f"Selected ability: {key}")  # Debug print
                self.selected_ability = ability
                return True
            else:
                print(f"Ability {key} on cooldown: {ability.current_cooldown} turns remaining")
        return False

    def get_selected_ability(self):
        return self.selected_ability

    def clear_selected_ability(self):
        self.selected_ability = None 