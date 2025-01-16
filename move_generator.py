class MoveGenerator:
    def __init__(self, board):
        self.board = board

        self.en_pass_to_square = ()
        self.en_pass_from_squares = []
        self.en_pass_possible = False

    def moves_present(self, ct):
        temp_is_lower = ct == 'black'  # Check color once instead of repeatedly.
        for i in range(8):
            for j in range(8):
                piece = self.board.get_piece(i, j)
                if piece!='.' and piece.islower() == temp_is_lower:  # Match piece with current turn.
                    piece_moves = self.generate_piece_moves(i, j, piece)
                    if any(self.filter_moves(piece_moves, ct)):  # Stop if valid move exists.
                        return True
        return False



    def generate_piece_moves(self, row, col, piece):
        """Generate moves for a specific piece."""
        moves = []
        if piece.lower() == 'p':
            moves =  self.generate_pawn_moves(row, col, piece)
        elif piece.lower() == 'r':
            moves =  self.generate_rook_moves(row, col, piece)
        elif piece.lower() == 'n':
            moves =  self.generate_knight_moves(row, col, piece)
        elif piece.lower() == 'b':
            moves =  self.generate_bishop_moves(row, col, piece)
        elif piece.lower() == 'q':
            moves =  self.generate_queen_moves(row, col, piece)
        elif piece.lower() == 'k':
            moves =  self.generate_king_moves(row, col, piece)
        return moves
    
    def generate_pawn_moves(self, row, col, piece):
        """Generate moves for a pawn."""
        moves = []
        direction = -1 if piece.isupper() else 1  # White moves up, black moves down

        # Normal move (one square forward)
        if self.board.get_piece(row + direction, col) == '.':
            if (piece == 'P' and row+direction == 0) or (piece == 'p' and row+direction == 7):
                moves.append((row, col, row + direction, col, 'Q' if piece.isupper() else 'q'))
                moves.append((row, col, row + direction, col, 'R' if piece.isupper() else 'r'))
                moves.append((row, col, row + direction, col, 'B' if piece.isupper() else 'b'))
                moves.append((row, col, row + direction, col, 'N' if piece.isupper() else 'n'))
            else:
                moves.append((row, col, row + direction, col))


        # Double square move from the starting position
        if (piece.isupper() and row == 6) or (piece.islower() and row == 1):
            if self.board.get_piece(row + direction * 2, col) == '.' and self.board.get_piece(row + direction, col) == '.':
                moves.append((row, col, row + direction * 2, col))

        # Pawn captures
        for dc in [-1, 1]:
            if 0 <= col + dc < 8:
                target = self.board.get_piece(row + direction, col + dc)
                if target != '.' and target.islower() != piece.islower():
                    if (piece == 'P' and row+direction == 0) or (piece == 'p' and row+direction == 7):
                        moves.append((row, col, row + direction, col+dc, 'Q' if piece.isupper() else 'q'))
                        moves.append((row, col, row + direction, col+dc, 'R' if piece.isupper() else 'r'))
                        moves.append((row, col, row + direction, col+dc, 'B' if piece.isupper() else 'b'))
                        moves.append((row, col, row + direction, col+dc, 'N' if piece.isupper() else 'n'))
                    else:
                        moves.append((row, col, row + direction, col + dc))
        
        # En pass moves if eligible
        if self.en_pass_possible:
            if((row, col) in self.en_pass_from_squares):
                moves.append((row, col, self.en_pass_to_square[0], self.en_pass_to_square[1]))

        return moves

    def generate_en_pass_moves(self, row, col, piece):
        self.en_pass_to_square = (row+1, col) if(piece=='P') else (row-1, col)
        for dc in [-1, 1]:
            if 0<= col + dc < 8:
                self.en_pass_from_squares.append((row, col+dc))
        self.en_pass_possible = True
    
    def clear_en_pass(self):
        self.en_pass_from_squares = ()
        self.en_pass_from_squares = []
        self.en_pass_possible = False


    def generate_rook_moves(self, row, col, piece):
        """Generate moves for a rook."""
        return self.generate_linear_moves(row, col, piece, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def generate_knight_moves(self, row, col, piece):
        """Generate moves for a knight."""
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
        """Generate moves for a bishop."""
        return self.generate_linear_moves(row, col, piece, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

    def generate_queen_moves(self, row, col, piece):
        """Generate moves for a queen."""
        return self.generate_linear_moves(row, col, piece, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)])

    def generate_king_moves(self, row, col, piece):
        """Generate moves for a king."""
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        moves = []
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.board.get_piece(r, c) == '.' or self.board.get_piece(r, c).islower() != piece.islower()):
                moves.append((row, col, r, c))
        
        # Generate casteling Moves
        if piece.islower() != True:
            king_moved = self.board.white_king_has_moved
            rook1_moved = self.board.white_rook1_has_moved
            rook2_moved = self.board.white_rook2_has_moved
        else: 
            king_moved = self.board.black_king_has_moved
            rook1_moved = self.board.black_rook1_has_moved
            rook2_moved = self.board.black_rook2_has_moved
        
        ct = 'white' if piece.lower() != True else 'black'
        if not king_moved and (not self.is_check(ct)):
            # long casteling move:
            if (not rook1_moved) and ((row, col, row, 3) in moves) and  self.board.get_piece(row, 2)=='.':
                moves.append((row, col, row, 2))
            
            # short casteling move
            if (not rook2_moved) and ((row, col, row, 5) in moves) and  self.board.get_piece(row, 6)=='.':
                moves.append((row, col, row, 6))
        return moves

    def generate_linear_moves(self, row, col, piece, directions):
        """Generate linear moves for rooks, bishops, and queens."""
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board.get_piece(r, c)
                if target == '.':
                    moves.append((row, col, r, c))
                elif target.islower() != piece.islower():
                    moves.append((row, col, r, c))
                    break  # Stop after capturing
                elif piece.lower() == 'k':
                    moves.append((row, col, r, c))
                else:
                    break  # Blocked by same-color piece
                r += dr
                c += dc  # Move in the same direction
        return moves
    
    def generate_king_radar(self, ct):
        """Generates radar of the king"""
        king_all_moves = []
        row, col, king = self.board.black_king if ct == 'black' else self.board.white_king
        rowx, colx, kingx = self.board.white_king if ct == 'black' else self.board.black_king

        king_all_moves += self.generate_queen_moves(row, col, king)
        king_all_moves += self.generate_knight_moves(row, col, king)
        if (row, col, rowx, colx) in king_all_moves:
            king_all_moves.remove((row, col, rowx, colx))
        return king_all_moves

    def filter_moves(self, moves, ct):
        """Check for Possible Checks"""
        i = 0
        while(i<len(moves)):
            move = moves[i]
            # Store en pass state and king state and rook state
            en_pass_to_square = self.en_pass_to_square
            en_pass_from_squares = self.en_pass_from_squares
            en_pass_possible = self.en_pass_possible
            white_king_has_moved = self.board.white_king_has_moved 
            black_king_has_moved = self.board.black_king_has_moved
            white_rook1_has_moved = self.board.white_rook1_has_moved 
            black_rook1_has_moved = self.board.black_rook1_has_moved
            white_rook2_has_moved = self.board.white_rook2_has_moved
            black_rook2_has_moved = self.board.black_rook2_has_moved
            ply_count = self.board.ply_count

            # simulate move
            captured_piece = self.board.make_move(move, self)

            # check for the validity
            if(self.is_check(ct)):
                if self.board.get_piece(move[2], move[3]).lower() == 'k' and move in [(0, 4, 0, 5), (0, 4, 0, 3), (7, 4, 7, 5), (7, 4, 7, 3)]:
                    temp = (move[0], move[1], move[0], move[3] + (move[3] - move[1]))
                    if temp in moves:
                        moves.remove(temp)
                moves.pop(i)
            else:
                i+=1
            
            self.board.undo_move(move, captured_piece)

            #restore en pass state and king state and rook state
            self.en_pass_to_square = en_pass_to_square
            self.en_pass_from_squares = en_pass_from_squares
            self.en_pass_possible = en_pass_possible
            self.board.white_king_has_moved = white_king_has_moved 
            self.board.black_king_has_moved = black_king_has_moved
            self.board.white_rook1_has_moved = white_rook1_has_moved
            self.board.black_rook1_has_moved = black_rook1_has_moved
            self.board.white_rook2_has_moved = white_rook2_has_moved
            self.board.black_rook2_has_moved = black_rook2_has_moved
            self.board.ply_count = ply_count
            
        return moves

    def is_check(self, ct):
        king_all_moves = self.generate_king_radar(ct)
        for from_row, from_col, to_row, to_col in king_all_moves:
            test_piece = self.board.get_piece(to_row, to_col)
            king = self.board.get_piece(from_row, from_col)
            if test_piece !='.' and test_piece.islower() != king.islower():
                test_piece_moves = self.generate_piece_moves(to_row, to_col, test_piece)
                for i in test_piece_moves:
                    if (i[2], i[3]) == (from_row, from_col):
                        """King is in direct check"""
                        return True

        return False
