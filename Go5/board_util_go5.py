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

    #Takes moves and probs arrays from generate_moves_with_feature_based_probs_Go5 and returns array
    #of the form [move(as a point), winrate, sims(rounded), wins(rounded)]
    @staticmethod
    def find_sim_win_list(moves, probs):
        max_p = max(probs)
        sims_wins_list = []
        for m in moves:
            if m == "PASS":
                sims = 10 * probs[len(probs) - 1] / max_p
                #No formula explicitly given for winrate, this formula is based off example on assignment page
                winrate = sims * 0.05
                winrate = winrate + 0.5
                wins = sims * winrate
                sims = int(round(sims))
                wins = int(round(wins))
                sims_wins_list.append([m, winrate, wins, sims])
            else:
                sims = 10 * probs[m] / max_p
                #No formula explicitly given for winrate, this formula is based off example on assignment page
                winrate = sims * 0.05
                winrate = winrate + 0.5
                wins = sims * winrate
                sims = int(round(sims))
                wins = int(round(wins))
                sims_wins_list.append([m, winrate, wins, sims])
        return sims_wins_list

    @staticmethod
    def format_list(board, sims_wins_list):
        for item in sims_wins_list:
            if item[0] == "PASS":
                item[0] = "Pass"
            else:
                row, col = board._point_to_coord(item[0])
                move = GoBoardUtil.format_point((row, col))
                item[0] = move
        sorted_list = sorted(sims_wins_list, key=lambda element: (-element[1], element[0]))
        return sorted_list

