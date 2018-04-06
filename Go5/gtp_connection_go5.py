import traceback
import sys
import os
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL
from board_util_go5 import GoBoardUtilGo5
import gtp_connection
import numpy as np
import re

class GtpConnectionGo5(gtp_connection.GtpConnection):

    def __init__(self, go_engine, board, outfile = 'gtp_log', debug_mode = False):
        """
        GTP connection of Go1

        Parameters
        ----------
        go_engine : GoPlayer
            a program that is capable of playing go by reading GTP commands
        komi : float
            komi used for the current game
        board: GoBoard
            SIZExSIZE array representing the current board state
        """
        gtp_connection.GtpConnection.__init__(self, go_engine, board, outfile, debug_mode)
        self.go_engine.con = self
        self.commands["prior_knowledge"] = self.prior_knowledge_cmd

    def prior_knowledge_cmd(self, args):
    	moves, probs = GoBoardUtilGo5.generate_moves_with_feature_based_probs_Go5(self.board)