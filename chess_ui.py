import tkinter as tk
from PIL import Image, ImageTk
import os


class ChessUI:
    def __init__(self, root, board, move_generator):
        self.root = root
        self.board = board
        self.move_generator = move_generator
        self.selected_square = None
        self.buttons = {}
        self.piece_images = {}

        # Screen and board dimensions
        self.screen_width = 850
        self.screen_height = 850
        self.board_size = 800  # Board is square (800x800)
        self.square_size = 100  # Calculated size of each square (800 / 8)

        self.setup_window()
        self.load_images()
        self.create_board()

    def setup_window(self):
        """Configure the main window dimensions and title."""
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.title("Chess")

    def load_images(self):
        """Load and scale piece images from the images folder."""
        image_folder = "images"
        pieces = {
            'K': 'white-king.png',
            'Q': 'white-queen.png',
            'R': 'white-rook.png',
            'B': 'white-bishop.png',
            'N': 'white-knight.png',
            'P': 'white-pawn.png',
            'k': 'black-king.png',
            'q': 'black-queen.png',
            'r': 'black-rook.png',
            'b': 'black-bishop.png',
            'n': 'black-knight.png',
            'p': 'black-pawn.png',
        }

        for piece, filename in pieces.items():
            image_path = os.path.join(image_folder, filename)
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                scaled_image = pil_image.resize((self.square_size, self.square_size), Image.ANTIALIAS)
                self.piece_images[piece] = ImageTk.PhotoImage(scaled_image)
            else:
                print(f"Warning: Missing image for piece '{piece}' at {image_path}")

        # Create a transparent placeholder image for empty squares
        empty_image = Image.new("RGBA", (self.square_size, self.square_size), (255, 255, 255, 0))
        self.piece_images['empty'] = ImageTk.PhotoImage(empty_image)

    def create_board(self):
        """Create the chessboard UI with images."""
        for row in range(8):
            for col in range(8):
                color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'  # Light/dark squares
                piece = self.board.get_piece(row, col)
                image = self.piece_images.get(piece, self.piece_images['empty'])
                button = tk.Button(
                    self.root,
                    image=image,
                    width=self.square_size,
                    height=self.square_size,
                    command=lambda row=row, col=col: self.on_square_click(row, col),
                    bg=color,
                    relief='flat',
                )
                button.grid(row=row, column=col, padx=0, pady=0)
                self.buttons[(row, col)] = button

    def on_square_click(self, row, col):
        """Handle square click event."""
        if self.selected_square:
            self.move_piece(self.selected_square, (row, col))
        else:
            self.selected_square = (row, col)
            self.highlight_valid_moves(row, col)

    def move_piece(self, from_square, to_square):
        """Move piece from selected square to target square."""
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.board.get_piece(from_row, from_col)
        if (from_row, from_col, to_row, to_col) in self.move_generator.generate_moves(piece.isupper()):
            self.board.make_move((from_row, from_col, to_row, to_col))
            self.update_ui()
        self.clear_highlight()
        self.selected_square = None

    def highlight_valid_moves(self, row, col):
        """Highlight valid moves for the selected piece."""
        piece = self.board.get_piece(row, col)
        is_white = piece.isupper()
        valid_moves = self.move_generator.generate_moves(is_white)
        for move in valid_moves:
            if move[0] == row and move[1] == col:
                to_row, to_col = move[2], move[3]
                self.buttons[(to_row, to_col)].config(bg='green')

    def clear_highlight(self):
        """Clear all highlighted squares."""
        for (row, col), button in self.buttons.items():
            current_color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
            button.config(bg=current_color)  # Reset the color to default

    def update_ui(self):
        """Update the UI with the current board state."""
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                image = self.piece_images.get(piece, self.piece_images['empty'])
                self.buttons[(row, col)].config(image=image)


if __name__ == '__main__':
    from board import Board
    from move_generator import MoveGenerator

    root = tk.Tk()
    board = Board()
    move_generator = MoveGenerator(board)
    chess_ui = ChessUI(root, board, move_generator)
    root.mainloop()