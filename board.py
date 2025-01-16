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

        self.white_king = (7, 4, 'K')
        self.black_king = (0, 4, 'k')
        self.white_king_has_moved = False
        self.black_king_has_moved = False
        self.white_rook1_has_moved = False
        self.black_rook1_has_moved = False
        self.white_rook2_has_moved = False
        self.black_rook2_has_moved = False
        self.ply_count = 0
        self.board_states = {}
    
    def print_board(self):
        """Print the board for debugging purposes."""
        for row in self.board:
            print(' '.join(row))

    def get_piece(self, row, col):
        """Return the piece at a specific board position."""
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        """Set a piece at a specific board position."""
        self.board[row][col] = piece

    def is_valid_move(self, move):
        """Check if the move is within board bounds."""
        from_row, from_col, to_row, to_col, *e = move
        return 0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8
    
    def make_move(self, move, move_generator):
        """Make a move on the board."""
        if not self.is_valid_move(move):
            raise ValueError("Invalid move")
        
        move_generator.clear_en_pass()

        from_row, from_col, to_row, to_col, *e = move
        piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'

        # Handle pawn promotion and en passant
        if piece.lower() == 'p':
            if len(move) == 5:
                self.board[to_row][to_col] = move[4]
            
            # en passant has hapened
            if (abs(from_col - to_col) == 1 and captured_piece=='.'):
                self.board[from_row][to_col] = '.'
            
            # Eligible for en passant
            if(abs(from_row-to_row)==2):
                move_generator.generate_en_pass_moves(to_row, to_col, piece)
            
            if(captured_piece!='.'):
                self.ply_count = 0
            else:
                self.ply_count+=1
        
        # Handle casteling
        if piece.lower() == 'k' and abs(to_col - from_col)==2:    
            if(to_col==6):
                self.board[from_row][5] = self.board[from_row][7]
                self.board[from_row][7]  = '.'
                if from_row == 0:
                    self.black_rook2_has_moved = True
                else:
                    self.white_rook2_has_moved = True
            else:
                self.board[from_row][3] = self.board[from_row][0]
                self.board[from_row][0] = '.'
                if from_row == 0:
                    self.black_rook1_has_moved = True
                else:
                    self.white_rook1_has_moved = True
            
        # Update king positions
        if(piece == 'k'):
            self.black_king = (to_row, to_col, 'k')
            self.black_king_has_moved = True
        elif(piece=='K'):
            self.white_king = (to_row, to_col, 'K')
            self.white_king_has_moved = True

        
        if piece.lower() == 'r' and not(self.black_rook1_has_moved and self.black_rook2_has_moved and self.white_rook1_has_moved and self.white_rook2_has_moved):
            if from_row==7 and from_col==0:
                self.white_rook1_has_moved = True
            
            if from_row==7 and from_col==7:
                self.white_rook2_has_moved = True
            
            if from_row == 0 and from_col == 0:
                self.black_rook1_has_moved = True
            
            if from_row == 0 and from_col == 7:
                self.black_rook2_has_moved = True
    
        return captured_piece  # Return captured piece for undo handling

    def undo_move(self, move, captured_piece):
        """move: old move"""
        from_row, from_col, to_row, to_col, *e = move
        piece = self.board[to_row][to_col]
        if len(move)==5:
            piece = 'p' if(piece.islower()) else 'P'
            
    
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured_piece

        # Update king positions
        if(piece == 'k'):
            self.black_king = (from_row, from_col, 'k')
        elif(piece=='K'):
            self.white_king = (from_row, from_col, 'K')
        
        if piece.lower() == 'k' and abs(to_col - from_col)==2:    
            if(to_col==6):
                self.board[from_row][7] = self.board[from_row][5]
                self.board[from_row][5] = '.'
            else:
                self.board[from_row][0] = self.board[from_row][3]
                self.board[from_row][3] = '.'
    
    def check_game_state(self, ct, move_generator):
        if(not move_generator.moves_present(ct)):
            if(move_generator.is_check(ct)):
                winner = 'White' if ct=='black' else 'Black'
                return f"{winner} won by Checkmate!"
            else:
                return "Draw by Stalemate"
        
        if(self.has_insufficient_material()):
            return "Draw by Insufficient Material!"

        if(self.is_50_move_rule()):
            return "Draw by 50 move rule!"
        
        if(self.is_threefold_repetition()):
            return "Draw by threefold repetition!"
        
    def has_insufficient_material(self):
        pieces = [piece.lower() for row in self.board for piece in row if piece != '.']
        if pieces == ['k', 'k']:
            return True
        if len(pieces) == 3 and ('b' in pieces or 'n' in pieces):
            return True
        return False
    
    def is_50_move_rule(self):
        return self.ply_count>=100
    
    def get_board_state(self):
        # Convert the board and state into a unique string
        board_string = ''.join([''.join(row) for row in self.board])
        castling_info = f"{self.white_king_has_moved}{self.black_king_has_moved}" \
                        f"{self.white_rook1_has_moved}{self.white_rook2_has_moved}" \
                        f"{self.black_rook1_has_moved}{self.black_rook2_has_moved}"
        return board_string + castling_info

    def update_board_state(self):
        state = self.get_board_state()
        if state in self.board_states:
            self.board_states[state] += 1
        else:
            self.board_states[state] = 1

    def is_threefold_repetition(self):
        for state, count in self.board_states.items():
            if count >= 3:
                return True
        return False
        
