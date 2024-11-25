class GameState:
    def remove_piece(self, piece):
        if piece in self.pieces:  # Assuming you have a pieces list
            self.pieces.remove(piece)
            print(f"Piece removed from game")
            return True
        return False

    def is_empty(self, position):
        return self.get_piece_at(position) is None 