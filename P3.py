import sys
import random
import signal
import time
import copy

class player3():

	def __init__(self):
		self.block = [[0 for x in range(4)] for y in range(4)]
		self.hash_block = [[0 for x in range(4)] for y in range(4)]
		self.hash_board = 0
		self.transposition_table = {}
		self.heuristic_table = {}
		self.zobrist_board = []
		for x in range(512):
			self.zobrist_board.append(random.randint(0,1<<63))
		self.zobrist_block = []
		value = 1
		for x in range(32):
			self.zobrist_block.append(value)
			value *= 2

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
					score += 5
				elif player_count == 3:
					score += 15

			# for 2 and 3 blocks in a column
			col = [x[i] for x in self.local_board.block_status]			#i'th column
			if col.count(self.opponent) == 0:
				player_count = col.count(self.player)
				if player_count == 2:
					score += 5
				elif player_count == 3:
					score += 15

		# for 2 and 3 blocks in the \ diagonal
		diagonal_1 = []
		for x in range(4):
			diagonal_1.append(self.local_board.block_status[x][x])

		if diagonal_1.count(self.opponent) == 0:
			player_count = diagonal_1.count(self.player)
			if player_count == 2:
				score += 5
			elif player_count == 3:
				score += 15

		# for 2 and 3 blocks in the ? diagonal
		diagonal_2 = []
		for x in range(4):
			diagonal_2.append(self.local_board.block_status[3-x][x])

		if diagonal_2.count(self.opponent) == 0:
			player_count = diagonal_2.count(self.player)
			if player_count == 2:
				score += 5
			elif player_count == 3:
				score += 15

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

			# for 2 and 3 blocks in a row
			if self.local_board.block_status[i].count(self.player) == 0:
				opponent_count = self.local_board.block_status[i].count(self.opponent)
				if opponent_count == 2:
					score += 5
				elif opponent_count == 3:
					score += 15

			# for 2 and 3 blocks in a column
			col = [x[i] for x in self.local_board.block_status]			#i'th column
			if col.count(self.player) == 0:
				opponent_count = col.count(self.opponent)
				if opponent_count == 2:
					score += 5
				elif opponent_count == 3:
					score += 15

		# for 2 and 3 blocks in the \ diagonal
		diagonal_1 = []
		for x in range(4):
			diagonal_1.append(self.local_board.block_status[x][x])

		if diagonal_1.count(self.player) == 0:
			opponent_count = diagonal_1.count(self.opponent)
			if opponent_count == 2:
				score += 5
			elif opponent_count == 3:
				score += 15

		# for 2 and 3 blocks in the ? diagonal
		diagonal_2 = []
		for x in range(4):
			diagonal_2.append(self.local_board.block_status[3-x][x])

		if diagonal_2.count(self.player) == 0:
			opponent_count = diagonal_2.count(self.opponent)
			if opponent_count == 2:
				score += 5
			elif opponent_count == 3:
				score += 15

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
							score += 0.5
							if center:
								score += 0.2
						elif player_count == 3:
							score += 1.5
							if center:
								score += 0.2

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.opponent) == 0:
						player_count = col.count(self.player)
						if player_count == 2:
							score += 0.5
							if center:
								score += 0.2
						elif player_count == 3:
							score += 1.5
							if center:
								score += 0.2

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.opponent) == 0:
					player_count = diagonal_1.count(self.player)
					if player_count == 2:
						score += 0.5
						if center:
							score += 0.2
					elif player_count == 3:
						score += 1.5
						if center:
							score += 0.2

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.opponent) == 0:
					player_count = diagonal_2.count(self.player)
					if player_count == 2:
						score += 0.5
						if center:
							score += 0.2
					elif player_count == 3:
						score += 1.5
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
							score += 0.5
							if center:
								score += 0.2
						elif opponent_count == 3:
							score += 1.5
							if center:
								score += 0.2

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.player) == 0:
						opponent_count = col.count(self.opponent)
						if opponent_count == 2:
							score += 0.5
							if center:
								score += 0.2
						elif opponent_count == 3:
							score += 1.5
							if center:
								score += 0.2

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.player) == 0:
					opponent_count = diagonal_1.count(self.opponent)
					if opponent_count == 2:
						score += 0.5
						if center:
							score += 0.2
					elif opponent_count == 3:
						score += 1.5
						if center:
							score += 0.2

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.player) == 0:
					opponent_count = diagonal_2.count(self.opponent)
					if opponent_count == 2:
						score += 0.5
						if center:
							score += 0.2
					elif opponent_count == 3:
						score += 1.5
						if center:
							score += 0.2

		return score

	def signal_handler(self, signum, frame):
    		raise Exception("Timed out!")

	def hash(self):
		for p in range(4):
			for q in range(4):
				x = 0
				result = 0
				for i in range(4):
					for j in range(4):
						current = self.local_board.board_status[4*p+i][4*q+j]
						if current == self.player:
							result = result ^ self.zobrist_block[x*2+1]
						elif current == self.opponent:
							result = result ^ self.zobrist_block[x*2+0]
						x += 1
				self.hash_block[p][q] = result

		x = 0
		result = 0
		for p in range(16):
			for q in range(16):
				current = self.local_board.board_status[p][q]
				if current == self.player:
					result = result ^ self.zobrist_board[x*2+1]
				elif current == self.opponent:
					result = result ^ self.zobrist_board[x*2+0]
				x += 1
		self.hash_board = result

	# 0 = minScore
	# 1 = maxScore
	# 2 = bestMove
	# 3 = depth
	def test(self, maxDepth, currentDepth, gamma, old_move, flag):

		if self.hash_board in self.transposition_table:
			entry = self.transposition_table[self.hash_board]
			if entry[3] > maxDepth - currentDepth:
				if entry[0] > gamma:
					return entry[0], entry[2]
				if entry[1] < gamma:
					return entry[1], entry[2]
		else:
			self.transposition_table[self.hash_board] = [-1000,1000,(-1,-1),maxDepth - currentDepth]

		# check if we're done recursing, gameover condition

		terminal_status = self.local_board.find_terminal_state()
		if currentDepth == maxDepth or terminal_status[0] != "CONTINUE":
			if terminal_status[0] == self.player:
				self.transposition_table[self.hash_board][0] = self.transposition_table[self.hash_board][1] = 160
			elif terminal_status[0] != self.player and terminal_status[1] == "WON":
				self.transposition_table[self.hash_board][0] = self.transposition_table[self.hash_board][1] = -160
			elif terminal_status[1] == "DRAW":
				score = 0
				for i in range(4):
					for j in range(4):
						if self.block_status[i][j] == self.player:
							score += 7
						if self.block_status[i][j] == self.opponent:
							score -= 7
				self.transposition_table[self.hash_board][0] = self.transposition_table[self.hash_board][1] = score
			else:
				self.transposition_table[self.hash_board][0] = self.transposition_table[self.hash_board][1] = self.heuristics_player() + self.heuristics_opponent() + self.heuristics_player_block() - self.heuristics_opponent_block()

			return self.transposition_table[self.hash_board][0], self.transposition_table[self.hash_board][2]

		bestMove = (-1,-1)
		bestScore = -160

		valid_moves = self.local_board.find_valid_move_cells(old_move)
		for valid_move in valid_moves:
			if flag == 1:
				self.local_board.update(old_move,valid_move,self.player)
			else:
				self.local_board.update(old_move,valid_move,self.opponent)
			self.last_move = valid_move
			self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+flag]
			self.hash_block[valid_move[0]/4][valid_move[1]/4] ^= self.zobrist_block[2*((valid_move[0]%4)*4+valid_move[1]%4)+flag]
			#recurse
			recursedScore, currentMove = self.test(maxDepth, currentDepth+1, -gamma, valid_move, (flag+1)%2)

			currentScore = -recursedScore
			self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+flag]
			self.hash_block[valid_move[0]/4][valid_move[1]/4] ^= self.zobrist_block[2*((valid_move[0]%4)*4+valid_move[1]%4)+flag]
			self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
			x = valid_move[0]/4
			y = valid_move[1]/4
			self.local_board.block_status[x][y] = '-'
			if currentScore > bestScore:
				self.transposition_table[self.hash_board][2] = bestMove = valid_move
				bestScore = currentScore
			# If we pruned, then we have a min score, otherwise we have a max score.
			if bestScore < gamma:
				self.transposition_table[self.hash_board][1] = bestScore
			else:
				self.transposition_table[self.hash_board][0] = bestScore

		return bestScore, bestMove

	def mtd(self, maxDepth, guess, old_move):
		for i in range(1):
			gamma = guess
			guess, move = self.test(maxDepth, 0, gamma-1, old_move, 1)
			#if there is no improvement, stop looking
			if gamma == guess:
				break
		return guess, move

	def mtdf(self, maxDepth, old_move):
		guess = 0
		# Iteratively deepen the search
		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(15)
		try:
			for i in range(2,maxDepth):

				guess, move = self.mtd(i,guess, old_move)
				print i
				self.local_board = self.saved
		except Exception, msg:
			return move

	def move(self, board, old_move, flag):
		self.player = flag
		self.opponent = "x" if self.player == "o" else "o"
		self.saved = copy.deepcopy(board)
		self.local_board = board
		self.hash()
		self.last_move = (0,0)

		bestMove = self.mtdf(20, old_move)
		return bestMove
