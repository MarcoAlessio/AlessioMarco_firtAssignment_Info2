import numpy as np
import time

#-1 regina
#0 vuota
# 1 - 8 in scacco da n regine '
class NQueens:
	def __init__(self, N):
		self.board = np.zeros((N, N), dtype=int)
	
	def placeQueen(self, row, col, N):
		self.board[row, :] +=1
		self.board[:, col] +=1
		
		rows, columns = self.board.shape
		for i in range(rows):
			for j in range(columns):
				if i-row == j-col or i+j == col+row:
					self.board[i, j] +=1

		self.board[row, col] = -1
		
	def removeQueen(self, row, col, N):
		self.board[row, :] -=1
		self.board[:, col] -=1
		
		rows, columns = self.board.shape
		for i in range(rows):
			for j in range(columns):
				if i-row == j-col or i+j == col+row:
					self.board[i, j] -=1
					
		self.board[row, col] = 0
			
	def backtracking(self, N, col):		
		if col==N:
			return True	
		row = 0
		found =False	
		while not found and row<N:
			if self.board[row, col] == 0:
				self.placeQueen(row, col, N)
				found = self.backtracking(N, col+1)
				
				if not found:
					self.removeQueen(row, col, N)
					row+=1
			else:
				row+=1				
		return found
				
if __name__ == '__main__':
	N = int(input("Quante regine vuoi utilizzare? "))
	b = NQueens(N)

	startTime = time.time()
	b.backtracking(N, 0)
	endTime = time.time()

	for i in range(N):
		for j in range(N):
			if b.board[i,j] != -1:
				b.board[i,j] = 0
	print("Soluzione:\n", b.board)
	print("Tempo di esecuzione: ", f"{endTime-startTime:.3f}", " secondi\n")