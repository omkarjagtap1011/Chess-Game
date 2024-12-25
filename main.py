from board import Board
from move_generator import MoveGenerator
from evaluation import Evaluator
from search import Search

def main():
    # Initialize components
    board = Board()
    move_generator = MoveGenerator(board)
    evaluator = Evaluator()
    search = Search(evaluator, move_generator)

    # Display the board
    board.display()

    # Generate and display moves for white pawns
    print("\nGenerating moves for white:")
    moves = move_generator.generate_moves(is_white=True)
    print(f"Moves: {moves}")

if __name__ == "__main__":
    main()
