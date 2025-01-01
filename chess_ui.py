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
        self.selected_piece = None
        self.valid_moves = []
        self.current_turn = 'white'
        self.screen_width = 800
        self.screen_height = 800
        self.square_size = self.screen_width // 8
        self.animation_speed = 20
        self.root.withdraw()  # Hide the main window initially
        self.show_game_mode_selection()

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.piece_items = {}

    def load_images(self):
        image_folder = "images"
        pieces = {
            'K': 'white-king.png', 'Q': 'white-queen.png', 'R': 'white-rook.png',
            'B': 'white-bishop.png', 'N': 'white-knight.png', 'P': 'white-pawn.png',
            'k': 'black-king.png', 'q': 'black-queen.png', 'r': 'black-rook.png',
            'b': 'black-bishop.png', 'n': 'black-knight.png', 'p': 'black-pawn.png',
        }
        self.piece_images = {}
        for piece, filename in pieces.items():
            image_path = os.path.join(image_folder, filename)
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                scaled_image = pil_image.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
                self.piece_images[piece] = ImageTk.PhotoImage(scaled_image)
            else:
                print(f"Warning: Missing image for piece '{piece}' at {image_path}")

    def draw_board(self):
        colors = ['#f0d9b5', '#b58863']
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece != '.':
                    image = self.piece_images[piece]
                    x, y = self.get_square_coords(row, col)
                    item = self.canvas.create_image(x, y, image=image, tags=piece)
                    self.piece_items[(row, col)] = item

    def get_square_coords(self, row, col):
        x = col * self.square_size + self.square_size / 2
        y = row * self.square_size + self.square_size / 2
        return (x, y)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        col, row = self.get_square_at_position(x, y)
        if row is None or col is None:
            return
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece:
            from_row, from_col = self.selected_piece
            if piece != '.' and self.is_piece_turn(piece):
                # Deselect previous piece and select new piece
                self.remove_highlights()
                self.selected_piece = (row, col)
                self.valid_moves = self.move_generator.generate_piece_moves(row, col, piece)
                self.valid_moves = self.move_generator.filter_moves(self.valid_moves, self.current_turn)
                self.highlight_moves(self.valid_moves)
            else:
                move = (from_row, from_col, row, col)
                if move in self.valid_moves:
                    self.make_move(move)
                self.selected_piece = None
                self.remove_highlights()
        else:
            if piece != '.' and self.is_piece_turn(piece):
                self.selected_piece = (row, col)
                self.valid_moves = self.move_generator.generate_piece_moves(row, col, piece)
                self.valid_moves = self.move_generator.filter_moves(self.valid_moves, self.current_turn)
                self.highlight_moves(self.valid_moves)
            else:
                self.selected_piece = None
                self.remove_highlights()

    def highlight_moves(self, moves):
        for move in moves:
            to_row, to_col = move[2], move[3]
            x1 = to_col * self.square_size
            y1 = to_row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='green', width=3, tags='highlight')

    def remove_highlights(self):
        self.canvas.delete('highlight')

    def make_move(self, move):
        from_row, from_col, to_row, to_col = move
        piece = self.board.get_piece(from_row, from_col)
        captured_piece = self.board.get_piece(to_row, to_col)

        def finalize_move():
            # Update the board state and switch turns after animation
            self.board.make_move(move, self.move_generator)
            self.update_canvas()
            self.switch_turn()
            result = self.board.check_game_state(self.current_turn, self.move_generator)
            if result:
                self.show_game_over(result)

        if piece.lower() == 'k' and abs(to_col - from_col) == 2:
            # Castling animation
            self.animate_castling(from_row, from_col, to_row, to_col, piece)
            self.root.after(100, finalize_move)  # Adjust the delay to match castling animation time
        else:
            # Regular move animation
            self.animate_move(from_row, from_col, to_row, to_col, piece)
            self.root.after(100, finalize_move)  # Adjust the delay to match move animation time


    def animate_move(self, from_row, from_col, to_row, to_col, piece):
        from_x, from_y = self.get_square_coords(from_row, from_col)
        to_x, to_y = self.get_square_coords(to_row, to_col)
        piece_item = self.piece_items.pop((from_row, from_col))
        total_steps = 5  # Adjust for smoother or faster animation
        dx = (to_x - from_x) / total_steps
        dy = (to_y - from_y) / total_steps
        current_step = 0

        def move_piece():
            nonlocal current_step
            if current_step < total_steps:
                current_x = from_x + current_step * dx
                current_y = from_y + current_step * dy
                self.canvas.coords(piece_item, current_x, current_y)
                current_step += 1
                self.root.after(self.animation_speed, move_piece)
            else:
                # Finalize position
                self.canvas.coords(piece_item, to_x, to_y)
                self.piece_items[(to_row, to_col)] = piece_item
                self.board.set_piece(to_row, to_col, piece)
                self.board.set_piece(from_row, from_col, '.')
                captured_item = self.piece_items.pop((to_row, to_col), None)
                if captured_item:
                    self.canvas.delete(captured_item)

        move_piece()


    def animate_castling(self, from_row, from_col, to_row, to_col, king_piece):
        if to_col == 6:
            rook_from_col, rook_to_col = 7, 5
        elif to_col == 2:
            rook_from_col, rook_to_col = 0, 3
        else:
            return
        rook_piece = self.board.get_piece(from_row, rook_from_col)
        king_item = self.piece_items.pop((from_row, from_col))
        rook_item = self.piece_items.pop((from_row, rook_from_col))
        king_start_x, king_start_y = self.get_square_coords(from_row, from_col)
        king_target_x, king_target_y = self.get_square_coords(to_row, to_col)
        rook_start_x, rook_start_y = self.get_square_coords(from_row, rook_from_col)
        rook_target_x, rook_target_y = self.get_square_coords(to_row, rook_to_col)
        king_dx = (king_target_x - king_start_x) / 10
        king_dy = (king_target_y - king_start_y) / 10
        rook_dx = (rook_target_x - rook_start_x) / 10
        rook_dy = (rook_target_y - rook_start_y) / 10

        def move_king(current_kx, current_ky):
            if current_kx != king_target_x or current_ky != king_target_y:
                current_kx += king_dx
                current_ky += king_dy
                self.canvas.coords(king_item, current_kx, current_ky)
                self.root.after(50, move_king, current_kx, current_ky)
            else:
                self.canvas.coords(king_item, king_target_x, king_target_y)
                self.piece_items[(to_row, to_col)] = king_item
                self.board.set_piece(to_row, to_col, king_piece)
                self.board.set_piece(from_row, from_col, '.')

        def move_rook(current_rx, current_ry):
            if current_rx != rook_target_x or current_ry != rook_target_y:
                current_rx += rook_dx
                current_ry += rook_dy
                self.canvas.coords(rook_item, current_rx, current_ry)
                self.root.after(50, move_rook, current_rx, current_ry)
            else:
                self.canvas.coords(rook_item, rook_target_x, rook_target_y)
                self.piece_items[(to_row, rook_to_col)] = rook_item
                self.board.set_piece(to_row, rook_to_col, rook_piece)
                self.board.set_piece(from_row, rook_from_col, '.')
        move_king(king_start_x, king_start_y)
        move_rook(rook_start_x, rook_start_y)

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.board.update_board_state()

    def show_game_over(self, result):
        messagebox.showinfo("Game Over", result)
        self.root.quit()

    def get_square_at_position(self, x, y):
        col = x // self.square_size
        row = y // self.square_size
        if 0 <= row < 8 and 0 <= col < 8:
            return (col, row)
        else:
            return (None, None)

    def is_piece_turn(self, piece):
        return (self.current_turn == 'white' and piece.isupper()) or \
               (self.current_turn == 'black' and piece.islower())

    def show_game_mode_selection(self):
        # Create a Toplevel window for game mode selection
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Game Mode")
        selection_window.grab_set()  # Make it modal
        self.center_window(selection_window, 300, 200)

        # Function to start Human vs Human game
        def start_human_vs_human():
            selection_window.destroy()  # Close the selection window
            self.setup_canvas()  # Initialize the chess UI
            self.load_images()
            self.draw_board()
            self.draw_pieces()
            # Position the main window at top-left corner
            self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
            self.root.deiconify()  # Show the main window

        # Function to handle Human vs AI selection
        def start_human_vs_ai():
            selection_window.withdraw()  # Hide the selection window

            # Create a new window for choosing color
            color_window = tk.Toplevel(self.root)
            color_window.title("Choose Color")
            color_window.grab_set()
            self.center_window(color_window, 300, 200)

            def show_coming_soon():
                messagebox.showinfo("Coming Soon", "AI functionality is coming soon!")
                color_window.destroy()
                selection_window.deiconify()

            # Button for playing as white
            white_button = tk.Button(color_window, text="Play as White", command=show_coming_soon, width=15)
            white_button.pack(pady=10)

            # Button for playing as black
            black_button = tk.Button(color_window, text="Play as Black", command=show_coming_soon, width=15)
            black_button.pack(pady=10)

        # Function to handle Analyse selection
        def start_analyse():
            messagebox.showinfo("Coming Soon", "Analyse functionality is coming soon!")
            selection_window.deiconify()

        # Create buttons for each game mode
        human_vs_human_button = tk.Button(selection_window, text="Human vs Human", command=start_human_vs_human, width=20)
        human_vs_human_button.pack(pady=10)

        human_vs_ai_button = tk.Button(selection_window, text="Human vs AI", command=start_human_vs_ai, width=20)
        human_vs_ai_button.pack(pady=10)

        analyse_button = tk.Button(selection_window, text="Analyse", command=start_analyse, width=20)
        analyse_button.pack(pady=10)

    def center_window(self, window, width, height):
        # Function to center a window on the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == '__main__':
    root = tk.Tk()
    board = Board()
    move_generator = MoveGenerator(board)
    chess_ui = ChessUI(root, board, move_generator)
    root.mainloop()