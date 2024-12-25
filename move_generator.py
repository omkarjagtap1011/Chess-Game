class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def generate_moves(self, is_white):
        """Generate all possible moves for the current player"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece == '.' or (piece.isupper() != is_white):
                    continue
                moves.extend(self.generate_piece_moves(row, col, piece))
        return moves

    def generate_piece_moves(self, row, col, piece):
        """Generate moves for a specific piece"""
        if piece.lower() == 'p':
            return self.generate_pawn_moves(row, col, piece)
        elif piece.lower() == 'r':
            return self.generate_rook_moves(row, col, piece)
        elif piece.lower() == 'n':
            return self.generate_knight_moves(row, col, piece)
        elif piece.lower() == 'b':
            return self.generate_bishop_moves(row, col, piece)
        elif piece.lower() == 'q':
            return self.generate_queen_moves(row, col, piece)
        elif piece.lower() == 'k':
            return self.generate_king_moves(row, col, piece)
        return []

    def generate_pawn_moves(self, row, col, piece):
        """Generate moves for a pawn"""
        moves = []
        direction = -1 if piece.isupper() else 1
        if self.board.get_piece(row + direction, col) == '.':
            moves.append((row, col, row + direction, col))  # Normal move
            if (piece.isupper() and row == 6) or (piece.islower() and row == 1):
                if self.board.get_piece(row + direction * 2, col) == '.':
                    moves.append((row, col, row + direction * 2, col))  # Double square move
        # Pawn captures
        for dc in [-1, 1]:
            if 0 <= col + dc < 8:
                target = self.board.get_piece(row + direction, col + dc)
                if target != '.' and target.islower() != piece.islower():
                    moves.append((row, col, row + direction, col + dc))
        # En passant
        en_passant_square = self.board.check_en_passant(row, col, 'w' if piece.isupper() else 'b')
        if en_passant_square:
            moves.append((row, col, en_passant_square[0], en_passant_square[1]))
        return moves

    def generate_rook_moves(self, row, col, piece):
        """Generate moves for a rook"""
        return self.generate_linear_moves(row, col, piece, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def generate_knight_moves(self, row, col, piece):
        """Generate moves for a knight"""
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        moves = []
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.board.get_piece(r, c) == '.' or self.board.get_piece(r, c).islower() != piece.islower()):
                moves.append((row, col, r, c))
        return moves

    def generate_bishop_moves(self, row, col, piece):
        """Generate moves for a bishop"""
        return self.generate_linear_moves(row, col, piece, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

    def generate_queen_moves(self, row, col, piece):
        """Generate moves for a queen"""
        return self.generate_linear_moves(row, col, piece, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)])

    def generate_king_moves(self, row, col, piece):
        """Generate moves for a king"""
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        moves = []
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.board.get_piece(r, c) == '.' or self.board.get_piece(r, c).islower() != piece.islower()):
                moves.append((row, col, r, c))
        return moves

    def generate_linear_moves(self, row, col, piece, directions):
        """Generate linear moves (rook, bishop, queen)"""
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board.get_piece(r, c)
                if target == '.':
                    moves.append((row, col, r, c))
                elif target.islower() != piece.islower():
                    moves.append((row, col, r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
