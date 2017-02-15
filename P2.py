import sys
import random
import signal
import time
import copy

class player22):

	def __init__(self):
		pass

	def heuristics_player(self):
		score = 0
		for i in range(4):
			for j in range(4):
				# winning a block
				if self.local_board.block_status[i][j] == self.player:
					score += 10
					# winning any of the 4 center blocks
					if i >= 1 and i <= 2 and j >= 1 and j <= 2:
						score += 10
					# winning any of the 4 corner blocks
					elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
						score += 4

			# for 2 blocks in a row
			x = i
			for y in range(3):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x][y+1] and self.local_board.block_status[x][y] == self.player:
					score += 5
			# for 3 blocks in a row
			for y in range(2):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x][y+1] and self.local_board.block_status[x][y] == self.local_board.block_status[x][y+2] and self.local_board.block_status[x][y] == self.player:
					score += 3

			# for 2 blocks in a column
			y = i
			for x in range(3):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x+1][y] and self.local_board.block_status[x][y] == self.player:
					score += 5
			# for 3 blocks in a column
			for x in range(2):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x+1][y] and self.local_board.block_status[x][y] == self.local_board.block_status[x+2][y] and self.local_board.block_status[x][y] == self.player:
					score += 3

		for x in range(3):
			# for 2 blocks in the \ diagonal
			if self.local_board.block_status[x][x] == self.local_board.block_status[x+1][x+1] and self.local_board.block_status[x][x] == self.player:
				score += 5
			# for 2 blocks in the / diagonal
			y = 3 - x
			if self.local_board.block_status[y][x] == self.local_board.block_status[y-1][x+1] and self.local_board.block_status[y][x] == self.player:
				score += 5

		for x in range(2):
			# for 3 blocks in the \ diagonal
			if self.local_board.block_status[x][x] == self.local_board.block_status[x+1][x+1] and self.local_board.block_status[x][x] == self.local_board.block_status[x+2][x+2] and self.local_board.block_status[x][x] == self.player:
				score += 3
			# for 3 blocks in the / diagonal
			y = 3 - x
			if self.local_board.block_status[y][x] == self.local_board.block_status[y-1][x+1] and self.local_board.block_status[x][x] == self.local_board.block_status[y-2][x+2] and self.local_board.block_status[y][x] == self.player:
				score += 3

		return score

	def heuristics_opponent(self):
		score = 0
		for i in range(4):
			for j in range(4):
				if self.local_board.block_status[i][j] == self.opponent:
					score -= 10
					if i >= 1 and i <= 2 and j >= 1 and j <= 2:
						score -= 10
					elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
						score -= 4

			# for 2 blocks in a row
			x = i
			for y in range(3):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x][y+1] and self.local_board.block_status[x][y] == self.opponent:
					score -= 5
			# for 3 blocks in a row
			for y in range(2):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x][y+1] and self.local_board.block_status[x][y] == self.local_board.block_status[x][y+2] and self.local_board.block_status[x][y] == self.opponent:
					score -= 3

			# for 2 blocks in a column
			y = i
			for x in range(3):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x+1][y] and self.local_board.block_status[x][y] == self.opponent:
					score -= 5
			# for 3 blocks in a column
			for x in range(2):
				if self.local_board.block_status[x][y] == self.local_board.block_status[x+1][y] and self.local_board.block_status[x][y] == self.local_board.block_status[x+2][y] and self.local_board.block_status[x][y] == self.opponent:
					score -= 3

		for x in range(3):
			# for 2 blocks in the \ diagonal
			if self.local_board.block_status[x][x] == self.local_board.block_status[x+1][x+1] and self.local_board.block_status[x][x] == self.opponent:
				score -= 5
			# for 2 blocks in the / diagonal
			y = 3 - x
			if self.local_board.block_status[y][x] == self.local_board.block_status[y-1][x+1] and self.local_board.block_status[y][x] == self.opponent:
				score -= 5

		for x in range(2):
			# for 3 blocks in the \ diagonal
			if self.local_board.block_status[x][x] == self.local_board.block_status[x+1][x+1] and self.local_board.block_status[x][x] == self.local_board.block_status[x+2][x+2] and self.local_board.block_status[x][x] == self.opponent:
				score -= 3
			# for 3 blocks in the / diagonal
			y = 3 - x
			if self.local_board.block_status[y][x] == self.local_board.block_status[y-1][x+1] and self.local_board.block_status[x][x] == self.local_board.block_status[y-2][x+2] and self.local_board.block_status[y][x] == self.opponent:
				score -= 3

		return score

	def alphabeta (self, depth, alpha, beta, maximini, old_move):
		terminal_status = self.local_board.find_terminal_state()
		if depth == 0 or terminal_status[0] != "CONTINUE":
			if terminal_status[0] == self.player:
				return 160
			elif terminal_status[0] != self.player and terminal_status[1] == "WON":
				return -160
			elif terminal_status[1] == "DRAW":
				score = 0
				for i in range(4):
					for j in range(4):
						if self.block_status[i][j] == self.player:
							score += 7
						if self.block_status[i][j] == self.opponent:
							score -= 7
				return score
			return (self.heuristics_player() + self.heuristics_opponent())

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
				player_ply = "x" if self.player == "o" else "x"
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

	def signal_handler(self, signum, frame):
    		raise Exception("Timed out!")

	def move(self, board, old_move, flag):
		self.player = flag
		self.opponent = "x" if self.player == "o" else "o"
		saved=copy.deepcopy(board)
		self.local_board = board
		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(15)   # 15 seconds

		try:
			for i in range(5,100):
				self.alphabeta (i, -1000, 1000, 1, old_move)
				best = self.best_move
				self.local_board=saved

		except Exception, msg:
			pass

		return best
