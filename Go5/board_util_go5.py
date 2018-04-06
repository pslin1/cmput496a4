from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL
import numpy as np

class GoBoardUtilGo5(GoBoardUtil):

    #Calculates probability for all empty points and pass move
    @staticmethod
    def generate_moves_with_feature_based_probs_Go5(board):
        from feature import Features_weight
        from feature import Feature
        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint + 1)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.check_legal(move, color) and not board.is_eye(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(Features_weight, all_board_features[move])
                gamma_sum += probs[move]
        #Append Pass to the list of moves
        moves.append("PASS")
        #Compute gamma for Pass move
        probs[len(probs) - 1] = Feature.compute_move_gamma(Features_weight, all_board_features["PASS"])
        #Add it to gamma sum
        gamma_sum += probs[len(probs) - 1]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                if m == "PASS":
                    probs[len(probs) - 1] = probs[len(probs) - 1] / gamma_sum
                else:
                    probs[m] = probs[m] / gamma_sum

        return moves, probs