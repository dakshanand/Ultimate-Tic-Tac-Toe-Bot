import sys
import random
import signal
import time
import copy

class player1():
	def __init__(self):
		pass

	def t(self):
		return 0
	def alphabeta (self,depth, alpha, beta, maximini, old_move):
		terminal_status = self.local_board.find_terminal_state()
		if depth == 0 or terminal_status[0] != "CONTINUE":
			if terminal_status[0] == self.player_char:
				return 160
			return random.randint(-160,160)

		if maximini:
			v = -1000
			valid_moves = self.local_board.find_valid_move_cells (old_move)
			for valid_move in valid_moves:

				new_v = self.alphabeta (depth - 1, alpha, beta, 0, valid_move)
				self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
				x = valid_move[0]/4
				y = valid_move[1]/4
				self.local_board.block_status[x][y] = '-'
				if new_v >= v:
					self.best_move = valid_move
					v = new_v
				alpha = max(alpha, v)
				self.best_move = valid_move
				if beta <= alpha:
					break
			return v
		else:
			v = 1000
			valid_moves = self.local_board.find_valid_move_cells (old_move)
			for valid_move in valid_moves:

				player_ply = "x" if self.player_char == "o" else "x"
				self.local_board.update(old_move, valid_move, player_ply)
				v = min(v, self.alphabeta (depth - 1, alpha, beta, 1, valid_move))
				self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
				x = valid_move[0]/4
				y = valid_move[1]/4
				self.local_board.block_status[x][y] = '-'
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v


	def signal_handler(self,signum, frame):
    		raise Exception("Timed out!")
	def move(self, board, old_move, flag):

		self.player_char = flag
		self.local_board=board
		saved=copy.deepcopy(board)
		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(15)   # Ten seconds


		try:
			for i in range(5,100):
				self.alphabeta (i, -1000, 1000, 1, old_move)
				best=self.best_move
				self.local_board=saved

		except Exception, msg:
			pass

		return best
