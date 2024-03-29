import sys
import random
import signal
import time
import copy

class player4():

	def __init__(self):
		self.block = [[0 for x in range(4)] for y in range(4)]
		self.hash_block = [[0 for x in range(4)] for y in range(4)]
		self.heuristic_table = {}
		self.heuristic_table[0] = [0,0,0,0,0,0]
		self.zobrist_block = []
		value = 1
		for x in range(32):
			self.zobrist_block.append(value)
			value *= 2

		self.transposition_table = {}
		self.zobrist_board = []
		self.hash_board = 0
		for x in range(512):
			self.zobrist_board.append(random.randint(0,1<<127))

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

	def heuristics_player(self):
		score = 0
		for i in range(4):
			for j in range(4):
				# winning a block
				if self.local_board.block_status[i][j] == self.player:
					score += 10
					# winning any of the 4 center blocks
					if i >= 1 and i <= 2 and j >= 1 and j <= 2:
						score += 6
					# winning any of the 4 corner blocks
					elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
						score += 2

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
						score += 6
					elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
						score += 2

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
		totalBonus = 0
		center = -1
		openMove = 0
		lastscore=0
		consCount = 0
		consBonus = 0

		if self.local_board.block_status[self.last_move[0]/4][self.last_move[1]/4] != '-':
			if self.local_board.board_status[self.last_move[0]][self.last_move[1]] == self.player:
				score += 20
				openMove = 20
			else:
				score -= 20
				openMove = -20

		for p in range(4):
			for q in range(4):
				center = 0
				centerBonus = 0
				lastscore = score

				if self.local_board.block_status[p][q] != '-':
					continue

				if p >= 1 and p <= 2 and q >= 1 and q <= 2:
					center = 1

				if self.block[p].count(self.opponent) == 0:
					consCount += 1

				col = [x[q] for x in self.block]
				if col.count(self.opponent) == 0:
					consCount += 1

				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.opponent) == 0 and p == q:
					consCount += 1

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.opponent) == 0 and p+q == 3:
					consCount += 1

				if self.hash_block[p][q] in self.heuristic_table:
					score += self.heuristic_table[self.hash_block[p][q]][1]
					if center:
						totalBonus += self.heuristic_table[self.hash_block[p][q]][3]
					totalBonus += self.heuristic_table[self.hash_block[p][q]][5] * consCount
					continue

				for i in range(4):
					for j in range(4):
						self.block[i][j] = self.local_board.board_status[4*p+i][4*q+j]

				for i in range(4):
					# for j in range(4):
					# 	# winning any of the 4 center self.blocks
					# 	if self.block[i][j] == self.player:
					# 		if i >= 1 and i <= 2 and j >= 1 and j <= 2:
					# 			score += 0.5
					# 			centerBonus += 0.2
					# 		# winning any of the 4 corner self.blocks
					# 		elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
					# 			score += 0.2
					# 			centerBonus += 0.2
					# 		else:
					# 			score += 0.0
					# 			centerBonus += 0.2

					# for 2 and 3 self.blocks in a row
					if self.block[i].count(self.opponent) == 0:
						player_count = self.block[i].count(self.player)
						if player_count == 2:
							score += 1.2
							centerBonus += 0.2
							consBonus += 0.2							

						elif player_count == 3:
							score += 3.0
							centerBonus += 0.2
							consBonus += 0.5

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.opponent) == 0:
						player_count = col.count(self.player)
						if player_count == 2:
							score += 1.2
							centerBonus += 0.2
							consBonus += 0.2

						elif player_count == 3:
							score += 3.0
							centerBonus += 0.2
							consBonus += 0.5

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.opponent) == 0:
					player_count = diagonal_1.count(self.player)
					if player_count == 2:
						score += 1.2
						centerBonus += 0.2
						consBonus += 0.2

					elif player_count == 3:
						score += 3.0
						centerBonus += 0.2
						consBonus += 0.5

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.opponent) == 0:
					player_count = diagonal_2.count(self.player)
					if player_count == 2:
						score += 1.2
						centerBonus += 0.2
						consBonus += 0.2

					elif player_count == 3:
						score += 3.0
						centerBonus += 0.2
						consBonus += 0.5

				if center:
					totalBonus += centerBonus
				totalBonus += consBonus * consCount

				self.heuristic_table[self.hash_block[p][q]] = [-1000, score - openMove - lastscore, 0, centerBonus, 0, consBonus]
		return score + totalBonus

	def heuristics_opponent_block(self):
		score = 0
		center = -1
		totalBonus = 0
		consBonus = 0
		consCount = 0

		for p in range(4):
			for q in range(4):

				center = 0
				centerBonus = 0
				lastscore=score

				if self.local_board.block_status[p][q] != '-':
					continue

				if p >= 1 and p <= 2 and q >= 1 and q <= 2:
					center = 1

				if self.block[p].count(self.player) == 0:
					consCount += 1

				col = [x[q] for x in self.block]
				if col.count(self.player) == 0:
					consCount += 1

				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.player) == 0 and p == q:
					consCount += 1

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.player) == 0 and p+q == 3:
					consCount += 1

				if self.heuristic_table[self.hash_block[p][q]][0] != -1000:
					score += self.heuristic_table[self.hash_block[p][q]][0]
					if center:
						totalBonus += self.heuristic_table[self.hash_block[p][q]][2]
					totalBonus += consCount * self.heuristic_table[self.hash_block[p][q]][4]
					continue

				for i in range(4):
					for j in range(4):
						self.block[i][j] = self.local_board.board_status[4*p+i][4*q+j]

				for i in range(4):
					# for j in range(4):
					# 	# winning any of the 4 center self.blocks
					# 	if self.block[i][j] == self.opponent:
					# 		if i >= 1 and i <= 2 and j >= 1 and j <= 2:
					# 			score += 0.5
					# 			centerBonus += 0.2

					# 		# winning any of the 4 corner self.blocks
					# 		elif ((i == 0 and (j == 0 or j == 3 )) or (i == 3 and (j == 0 or j == 3 ))):
					# 			score += 0.2
					# 			centerBonus += 0.2
					# 		else:
					# 			score += 0.0
					# 			centerBonus += 0.2

					# for 2 and 3 self.blocks in a row
					if self.block[i].count(self.player) == 0:
						opponent_count = self.block[i].count(self.opponent)
						if opponent_count == 2:
							score += 1.2
							centerBonus += 0.2
							consBonus += 0.2

						elif opponent_count == 3:
							score += 3.0
							centerBonus += 0.2
							consBonus += 0.5

					# for 2 and 3 self.blocks in a column
					col = [x[i] for x in self.block]
					if col.count(self.player) == 0:
						opponent_count = col.count(self.opponent)
						if opponent_count == 2:
							score += 1.2
							centerBonus += 0.2
							consBonus += 0.2

						elif opponent_count == 3:
							score += 3.0
							centerBonus += 0.2
							consBonus += 0.5

				# for 2 and 3 self.blocks in the \ diagonal
				diagonal_1 = []
				for x in range(4):
					diagonal_1.append(self.block[x][x])

				if diagonal_1.count(self.player) == 0:
					opponent_count = diagonal_1.count(self.opponent)
					if opponent_count == 2:
						score += 1.2
						centerBonus += 0.2
						consBonus += 0.2

					elif opponent_count == 3:
						score += 3.0
						centerBonus += 0.2
						consBonus += 0.5

				# for 2 and 3 self.blocks in the / diagonal
				diagonal_2 = []
				for x in range(4):
					diagonal_2.append(self.block[3-x][x])

				if diagonal_2.count(self.player) == 0:
					opponent_count = diagonal_2.count(self.opponent)
					if opponent_count == 2:
						score += 1.2
						centerBonus += 0.2
						consBonus += 0.2

					elif opponent_count == 3:
						score += 3.0
						centerBonus += 0.2
						consBonus += 0.5

				if center:
					totalBonus += centerBonus
				totalBonus += consBonus * consCount

				self.heuristic_table[self.hash_block[p][q]][0] = score-lastscore
				self.heuristic_table[self.hash_block[p][q]][2] = centerBonus
				self.heuristic_table[self.hash_block[p][q]][4] = consBonus

		return score + totalBonus

	def alphabeta (self, depth, alpha, beta, maximini, old_move):
		terminal_status = self.local_board.find_terminal_state()
		if depth == 0 or terminal_status[0] != "CONTINUE":
			if terminal_status[0] == self.player:
				return 260
			elif terminal_status[0] != self.player and terminal_status[1] == "WON":
				return -260
			elif terminal_status[1] == "DRAW":
				score = 0
				for i in range(4):
					for j in range(4):
						if self.local_board.block_status[i][j] == self.player:
							score += 10
						if self.local_board.block_status[i][j] == self.opponent:
							score -= 10
				return score

			return (self.heuristics_player() - self.heuristics_opponent() + self.heuristics_player_block() - self.heuristics_opponent_block())

		if maximini:
			v = -1000
			valid_moves = self.local_board.find_valid_move_cells (old_move)
			for valid_move in valid_moves:
				self.local_board.update(old_move,valid_move,self.player)
				self.hash_block[valid_move[0]/4][valid_move[1]/4] ^= self.zobrist_block[2*((valid_move[0]%4)*4+valid_move[1]%4)+1]
				self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+1]
				self.last_move = valid_move
				new_v = self.alphabeta (depth - 1, alpha, beta, 0, valid_move)
				self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
				x = valid_move[0]/4
				y = valid_move[1]/4
				self.local_board.block_status[x][y] = '-'
				self.hash_block[x][y] ^= self.zobrist_block[2*((valid_move[0]%4)*4 + valid_move[1]%4) + 1]
				self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+1]
				if new_v > v:
					if self.level == depth:
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
				self.hash_block[valid_move[0]/4][valid_move[1]/4] ^= self.zobrist_block[2*((valid_move[0]%4)*4+valid_move[1]%4)+0]
				self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+0]
				self.last_move = valid_move
				v = min(v, self.alphabeta (depth - 1, alpha, beta, 1, valid_move))
				self.local_board.board_status[valid_move[0]][valid_move[1]]='-'
				x = valid_move[0]/4
				y = valid_move[1]/4
				self.local_board.block_status[x][y] = '-'
				self.hash_block[x][y] ^= self.zobrist_block[2*((valid_move[0]%4)*4 + valid_move[1]%4) + 0]
				self.hash_board ^= self.zobrist_board[2*(valid_move[0]*16+valid_move[1])+0]
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v

	def signal_handler(self, signum, frame):
    		raise Exception("Timed out!")

	def move(self, board, old_move, flag):

		self.player = flag
		self.opponent = "x" if self.player == "o" else "o"
		self.local_board = copy.deepcopy(board)
		if old_move != (-1,-1):
			self.hash_block[old_move[0]/4][old_move[1]/4] ^= self.zobrist_block[2*((old_move[0]%4)*4+old_move[1]%4)+0]
		signal.signal(signal.SIGALRM, self.signal_handler)
		self.last_move=(0,0)
		signal.alarm(15)
		self.hash()
		try:
			for i in range(3,100):
				self.level = i
				try:
					self.alphabeta(i,-1000,1000,1,old_move)
				except Exception as e:
					print 'Exception occurred ', e
					print 'Traceback printing ', sys.exc_info()[2].format_exc()
				best = self.best_move
				print i

		except Exception, msg:
			pass
		self.hash_block[best[0]/4][best[1]/4] ^= self.zobrist_block[2*((best[0]%4)*4+best[1]%4)+1]
		return best
