from evaluation import Evaluation
from move_generator import MoveGenerator
class Search:
    def __init__(self, board, depth):
        """
        Initializes the search with a given board and depth.

        :param board: The current board state (an instance of the Board class)
        :param depth: The search depth (how many plies to search ahead)
        """
        self.board = board
        self.depth = depth
        self.evaluator = Evaluation(board)  # Assuming you have an Evaluation class
        self.move_generator = MoveGenerator(board)  # Assuming you have a MoveGenerator class

    def minimax(self, is_white, depth, alpha, beta):
        """
        The Minimax algorithm with Alpha-Beta pruning.

        :param is_white: True if it's White's turn, False if Black's turn
        :param depth: The current search depth
        :param alpha: The best score found so far for the maximizer
        :param beta: The best score found so far for the minimizer
        :return: The evaluated score of the current position
        """
        if depth == 0:
            return self.evaluator.evaluate(is_white)

        moves = self.move_generator.generate_moves(is_white)
        if is_white:
            max_eval = -float('inf')
            for move in moves:
                self.board.make_move(move)
                eval = self.minimax(False, depth-1, alpha, beta)
                self.board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                self.board.make_move(move)
                eval = self.minimax(True, depth-1, alpha, beta)
                self.board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def find_best_move(self, is_white):
        """
        Finds the best move using the Minimax algorithm with Alpha-Beta pruning.

        :param is_white: True if it's White's turn, False if Black's turn
        :return: The best move (an instance of the Move class)
        """
        best_move = None
        best_value = -float('inf') if is_white else float('inf')
        moves = self.move_generator.generate_moves(is_white)

        for move in moves:
            self.board.make_move(move)
            move_value = self.minimax(not is_white, self.depth-1, -float('inf'), float('inf'))
            self.board.undo_move()

            if (is_white and move_value > best_value) or (not is_white and move_value < best_value):
                best_value = move_value
                best_move = move

        return best_move
