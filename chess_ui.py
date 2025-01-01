import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from board import Board
from move_generator import MoveGenerator
import os

class ChessUI:
    def __init__(self, root, board, move_generator):
        self.root = root
        self.board = board
        self.move_generator = move_generator
        self.selected_square = None
        self.moved = True
        self.buttons = {}
        self.piece_images = {}
        self.current_turn = 'white'
        self.valid_moves = []
        self.game_mode = None
        self.player_color = None
        
        self.screen_width = 850
        self.screen_height = 850
        self.board_size = 800
        self.square_size = 100

        self.setup_window()
        self.load_images()
        self.show_game_mode_selection()

    def setup_window(self):
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.resizable(width=False, height=False)
        self.root.title("Chess")

    def load_images(self):
        image_folder = "images"
        pieces = {
            'K': 'white-king.png', 'Q': 'white-queen.png', 'R': 'white-rook.png',
            'B': 'white-bishop.png', 'N': 'white-knight.png', 'P': 'white-pawn.png',
            'k': 'black-king.png', 'q': 'black-queen.png', 'r': 'black-rook.png',
            'b': 'black-bishop.png', 'n': 'black-knight.png', 'p': 'black-pawn.png',
        }
        for piece, filename in pieces.items():
            image_path = os.path.join(image_folder, filename)
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                scaled_image = pil_image.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
                self.piece_images[piece] = ImageTk.PhotoImage(scaled_image)
            else:
                print(f"Warning: Missing image for piece '{piece}' at {image_path}")
        empty_image = Image.new("RGBA", (self.square_size, self.square_size), (255, 255, 255, 0))
        self.piece_images['empty'] = ImageTk.PhotoImage(empty_image)

    def show_game_mode_selection(self):
        frame = tk.Frame(self.root, bg="#282c34")
        frame.pack(expand=True, fill="both", pady=20)

        tk.Label(
            frame, text="Select Game Mode:", font=("Helvetica", 20, "bold"), bg="#282c34", fg="#61dafb"
        ).pack(pady=20)

        button_styles = {
            "font": ("Helvetica", 16, "bold"),
            "bg": "#61dafb",
            "fg": "#282c34",
            "activebackground": "#21a1f1",
            "activeforeground": "#ffffff",
            "relief": "raised",
            "bd": 3,
            "width": 20,
            "height": 2
        }

        tk.Button(
            frame, text="Human vs Human", command=lambda: self.start_game("human_vs_human"), **button_styles
        ).pack(pady=10)

        tk.Button(
            frame, text="Human vs AI", command=self.show_ai_color_selection, **button_styles
        ).pack(pady=10)

        tk.Button(
            frame, text="Analyze", command=lambda: self.start_game("analyze"), **button_styles
        ).pack(pady=10)

    def show_ai_color_selection(self):
        frame = tk.Frame(self.root, bg="#282c34")
        frame.pack(expand=True, fill="both", pady=20)

        tk.Label(
            frame, text="Play as:", font=("Helvetica", 20, "bold"), bg="#282c34", fg="#61dafb"
        ).pack(pady=20)

        button_styles = {
            "font": ("Helvetica", 16, "bold"),
            "bg": "#61dafb",
            "fg": "#282c34",
            "activebackground": "#21a1f1",
            "activeforeground": "#ffffff",
            "relief": "raised",
            "bd": 3,
            "width": 20,
            "height": 2
        }

        tk.Button(
            frame, text="White", command=lambda: self.start_game("human_vs_ai", "white"), **button_styles
        ).pack(pady=10)

        tk.Button(
            frame, text="Black", command=lambda: self.start_game("human_vs_ai", "black"), **button_styles
        ).pack(pady=10)


    def start_game(self, mode, player_color=None):
        self.game_mode = mode
        self.player_color = player_color
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_board()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                piece = self.board.get_piece(row, col)
                image = self.piece_images.get(piece, self.piece_images['empty'])
                button = tk.Button(
                    self.root, image=image, width=self.square_size, height=self.square_size,
                    command=lambda row=row, col=col: self.on_square_click(row, col), bg=color, relief='flat'
                )
                button.grid(row=row, column=col, padx=0, pady=0)
                self.buttons[(row, col)] = button

    def on_square_click(self, row, col):
        piece = self.board.get_piece(row, col)
        self.clear_highlight()
        if piece != '.' and self.is_piece_turn(piece):
            self.selected_square = (row, col)
            self.highlight_valid_moves(row, col)
        elif self.selected_square:
            self.move_piece(self.selected_square, (row, col))

    def highlight_valid_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        self.valid_moves = self.move_generator.generate_piece_moves(row, col, piece)
        self.valid_moves = self.move_generator.filter_moves(self.valid_moves, self.current_turn)
        for move in self.valid_moves:
            to_row, to_col = move[2], move[3]
            self.buttons[(to_row, to_col)].config(bg='green')

    def clear_highlight(self):
        for move in self.valid_moves:
            to_row, to_col = move[2], move[3]
            current_color = '#f0d9b5' if (to_row + to_col) % 2 == 0 else '#b58863'
            self.buttons[(to_row, to_col)].config(bg=current_color)

    def is_piece_turn(self, piece):
        return (self.current_turn == 'white' and piece.isupper()) or \
               (self.current_turn == 'black' and piece.islower())

    def move_piece(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        move = (from_row, from_col, to_row, to_col)

        if move in self.valid_moves:
            self.board.make_move(move, self.move_generator)
            self.update_ui()
            self.switch_turn()
        else:
            print("Invalid move!")

        self.clear_highlight()
        self.selected_square = None

    def update_ui(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                image = self.piece_images.get(piece, self.piece_images['empty'])
                self.buttons[(row, col)].config(image=image)

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.board.update_board_state()
        res = self.board.check_game_state(self.current_turn, self.move_generator)
        if res:
            self.show_game_over(res)

    def show_game_over(self, result):
        message = f"Game Over! {result}"
        messagebox.showinfo("Game Over", message)
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    board = Board()
    move_generator = MoveGenerator(board)
    chess_ui = ChessUI(root, board, move_generator)
    root.mainloop()
