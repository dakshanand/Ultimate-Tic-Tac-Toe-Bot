import sys
import random
import signal
import time
import copy

class player2():

	def __init__(self):
		self.block = [[0 for x in range(4)] for y in range(4)]

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

			# for 2 and 3 blocks in a row
			if self.local_board.block_status[i].count(self.opponent) == 0:
				player_count = self.local_board.block_status[i].count(self.player)
				if player_count == 2:
					score += 15
				elif player_count == 3:
					score += 35

			# for 2 and 3 blocks in a column
			col = [x[i] for x in self.local_board.block_status]			#i'th column
			if col.count(self.opponent) == 0:
				player_count = col.count(self.player)
				if player_count == 2:
					score += 15
				elif player_count == 3:
					score += 35

		# for 2 and 3 blocks in the \ diagonal
		diagonal_1 = []
		for x in range(4):
			diagonal_1.append(self.local_board.block_status[x][x])

		if diagonal_1.count(self.opponent) == 0:
			player_count = diagonal_1.count(self.player)
			if player_count == 2:
				score += 15
			elif player_count == 3:
				score += 35

		# for 2 and 3 blocks in the ? diagonal
		diagonal_2 = []
		for x in range(4):
			diagonal_2.append(self.local_board.block_status[3-x][x])

		if diagonal_2.count(self.opponent) == 0:
			player_count = diagonal_2.count(self.player)
			if player_count == 2:
				score += 15
			elif player_count == 3:
				score += 35

		return score

	def heuristics_opponent(self):
		score = 0
		for i in range(4):
			for j in range(4):
				if self.local_board.block_status[i][j] == self.opponent:
					score += 10
					if i >= 1 and i <= 2 and j >= 1 and j <= 2:
						score += 10
					elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
						score += 4

			# for 2 and 3 blocks in a row
			if self.local_board.block_status[i].count(self.player) == 0:
				opponent_count = self.local_board.block_status[i].count(self.opponent)
				if opponent_count == 2:
					score += 15
				elif opponent_count == 3:
					score += 35

			# for 2 and 3 blocks in a column
			col = [x[i] for x in self.local_board.block_status]			#i'th column
			if col.count(self.player) == 0:
				opponent_count = col.count(self.opponent)
				if opponent_count == 2:
					score += 15
				elif opponent_count == 3:
					score += 35

		# for 2 and 3 blocks in the \ diagonal
		diagonal_1 = []
		for x in range(4):
			diagonal_1.append(self.local_board.block_status[x][x])

		if diagonal_1.count(self.player) == 0:
			opponent_count = diagonal_1.count(self.opponent)
			if opponent_count == 2:
				score += 15
			elif opponent_count == 3:
				score += 35

		# for 2 and 3 blocks in the ? diagonal
		diagonal_2 = []
		for x in range(4):
			diagonal_2.append(self.local_board.block_status[3-x][x])

		if diagonal_2.count(self.player) == 0:
			opponent_count = diagonal_2.count(self.opponent)
			if opponent_count == 2:
				score += 15
			elif opponent_count == 3:
				score += 35

		return score

	def heuristics_player_block(self):
		score = 0
		center = -1

		if self.local_board.block_status[self.last_move[0]/4][self.last_move[1]/4] != '-':
			if self.local_board.board_status[self.last_move[0]][self.last_move[1]] == self.player:
				score += 20
			else:
				score -= 20

		for p in range(4):
			for q in range(4):
				if self.local_board.block_status[p][q] != '-':
					continue
				center = 0
				if p >= 1 and p <= 2 and q >= 1 and q <= 2:
					center = 1

				for i in range(4):
					for j in range(4):
						self.block[i][j] = self.local_board.board_status[4*p+i][4*q+j]

				for i in range(4):
					for j in range(4):
						# winning any of the 4 center self.blocks
						if self.block[i][j] == self.player:
							if i >= 1 and i <= 2 and j >= 1 and j <= 2:
								score += 0.5
								if center:
									score += 0.2

							# winning any of the 4 corner self.blocks
							elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
								score += 0.2
								if center:
									score += 0.2

					# for 2 and 3 self.blocks in a row
					if self.block[i].count(self.opponent) == 0:
						player_count = self.block[i].count(self.player)
						if player_count == 2:
							score += 1.5
							if center:
								score += 0.2
						elif player_count == 3:
							score += 3.5
							if center:
								score += 0.2

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.opponent) == 0:
						player_count = col.count(self.player)
						if player_count == 2:
							score += 1.5
							if center:
								score += 0.2
						elif player_count == 3:
							score += 3.5
							if center:
								score += 0.2

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.opponent) == 0:
					player_count = diagonal_1.count(self.player)
					if player_count == 2:
						score += 1.5
						if center:
							score += 0.2
					elif player_count == 3:
						score += 3.5
						if center:
							score += 0.2

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.opponent) == 0:
					player_count = diagonal_2.count(self.player)
					if player_count == 2:
						score += 1.5
						if center:
							score += 0.2
					elif player_count == 3:
						score += 3.5
						if center:
							score += 0.2

		return score

	def heuristics_opponent_block(self):
		score = 0
		center = -1

		for p in range(4):
			for q in range(4):
				if self.local_board.block_status[p][q] != '-':
					continue
				center = 0
				if p >= 1 and p <= 2 and q >= 1 and q <= 2:
					center = 1

				for i in range(4):
					for j in range(4):
						self.block[i][j] = self.local_board.board_status[4*p+i][4*q+j]

				for i in range(4):
					for j in range(4):
						# winning any of the 4 center self.blocks
						if self.block[i][j] == (self.opponent):
							if i >= 1 and i <= 2 and j >= 1 and j <= 2:
								score += 0.5
								if center:
									score += 0.2

							# winning any of the 4 corner self.blocks
							elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
								score += 0.2
								if center:
									score += 0.2

					# for 2 and 3 self.blocks in a row
					if self.block[i].count(self.player) == 0:
						opponent_count = self.block[i].count(self.opponent)
						if opponent_count == 2:
							score += 1.5
							if center:
								score += 0.2
						elif opponent_count == 3:
							score += 3.5
							if center:
								score += 0.2

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.player) == 0:
						opponent_count = col.count(self.opponent)
						if opponent_count == 2:
							score += 1.5
							if center:
								score += 0.2
						elif opponent_count == 3:
							score += 3.5
							if center:
								score += 0.2

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.player) == 0:
					opponent_count = diagonal_1.count(self.opponent)
					if opponent_count == 2:
						score += 1.5
						if center:
							score += 0.2
					elif opponent_count == 3:
						score += 3.5
						if center:
							score += 0.2

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.player) == 0:
					opponent_count = diagonal_2.count(self.opponent)
					if opponent_count == 2:
						score += 1.5
						if center:
							score += 0.2
					elif opponent_count == 3:
						score += 3.5
						if center:
							score += 0.2

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

			return (self.heuristics_player() - self.heuristics_opponent() + self.heuristics_player_block() - self.heuristics_opponent_block())

		if maximini:
			v = -1000
			valid_moves = self.local_board.find_valid_move_cells (old_move)
			for valid_move in valid_moves:
				self.local_board.update(old_move,valid_move,self.player)
				self.last_move = valid_move
				new_v = self.alphabeta (depth - 1, alpha, beta, 0, valid_move)
				self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
				x = valid_move[0]/4
				y = valid_move[1]/4
				self.local_board.block_status[x][y] = '-'
				if new_v > v:
					if self.level==depth:
						self.best_move = valid_move
					v = new_v
				alpha = max(alpha, v)
				if beta <= alpha:
					break
			return v
		else:
			v = 1000
			valid_moves = self.local_board.find_valid_move_cells (old_move)
			for valid_move in valid_moves:
				player_ply = "x" if self.player == "o" else "x"
				self.local_board.update(old_move, valid_move, self.opponent)
				self.last_move=valid_move
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
		self.last_move=(0,0)
		signal.alarm(15)

		try:
			for i in range(3,5):
				self.level = i
				self.alphabeta (i, -1000, 1000, 1, old_move)
				print i
				best = self.best_move
				self.local_board = saved



		except Exception, msg:
			pass
		return best
