class Board:
    def __init__(self):
        # 8x8 chessboard initialized with starting positions for pieces
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Black pieces
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Black pawns
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # White pawns
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # White pieces
        ]
        
        # Dictionary to access pieces by their symbol
        self.pieces = {}
        self.en_passant = None  # Initialize en passant as None
        self.castling_rights = {
            'K': True,  # White king-side castling
            'Q': True,  # White queen-side castling
            'k': True,  # Black king-side castling
            'q': True   # Black queen-side castling
        }
        self._populate_pieces()

    def _populate_pieces(self):
        """Populate the pieces dictionary based on the current board"""
        self.pieces = {}  # Clear the current dictionary before repopulating
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.':
                    if piece not in self.pieces:
                        self.pieces[piece] = []
                    self.pieces[piece].append((row, col))

    def make_move(self, move):
        """Make a move on the board"""
        from_row, from_col, to_row, to_col = move
        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'

        # Update castling rights
        if piece.lower() == 'k':  # King moved
            if piece == 'K':  # White king
                self.castling_rights['K'] = self.castling_rights['Q'] = False
            else:  # Black king
                self.castling_rights['k'] = self.castling_rights['q'] = False
        elif piece.lower() == 'r':  # Rook moved
            if piece == 'R':  # White rook
                if from_col == 0:  # A-file rook
                    self.castling_rights['Q'] = False
                elif from_col == 7:  # H-file rook
                    self.castling_rights['K'] = False
            else:  # Black rook
                if from_col == 0:  # A-file rook
                    self.castling_rights['q'] = False
                elif from_col == 7:  # H-file rook
                    self.castling_rights['k'] = False

        # Check for en passant conditions
        if piece.lower() == 'p':  # Only pawns can trigger en passant
            if abs(from_row - to_row) == 2:  # Pawn moves two squares
                self.set_en_passant((to_row, to_col), piece)

        # Update pieces dictionary
        self._populate_pieces()

    def print_board(self):
        """Print the board for debugging purposes"""
        for row in self.board:
            print(' '.join(row))

    def get_piece(self, row, col):
        """Return the piece at a specific board position"""
        return self.board[row][col]
    
    def set_piece(self, row, col, piece):
        """Set a piece at a specific board position"""
        self.board[row][col] = piece

    def set_en_passant(self, square, color):
        """
        Set the en passant square and color that can capture the pawn.
        `square` is the square where en passant can happen (row, col).
        `color` is the color of the pawn that moved two squares.
        """
        self.en_passant = (square, color)

    def clear_en_passant(self):
        """Clear the en passant status."""
        self.en_passant = None

    def check_en_passant(self, row, col, color):
        """Check if en passant is possible at the given square for the specified color."""
        if self.en_passant:
            en_passant_square, en_passant_color = self.en_passant
            if en_passant_color != color:
                if color == 'w' and (row == en_passant_square[0] - 1) and (col == en_passant_square[1]):
                    return en_passant_square
                elif color == 'b' and (row == en_passant_square[0] + 1) and (col == en_passant_square[1]):
                    return en_passant_square
        return None
