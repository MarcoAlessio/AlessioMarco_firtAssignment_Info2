import numpy as np
import time

# -1 regina
# 0 senza scacchi
# 1 - 8 in scacco da N regine
class NQueens:
    def __init__(self, N):
        # """in ogni cella della board sono segnati gli scacchi a cui quella cella è sottoposta, ad eccezione di quelle occupate dalle regine
        # che sono sempre poste a -1""" 
        self.board = np.zeros((N, N), dtype=int)

	# metodo per piazzare una regina nell'indice della matrice [row,col]
    def placeQueen(self, row, col, N):
        # aumento di 1 tutte le celle che si trovano allo stesso indice di riga e di colonna
        self.board[row, :] += 1
        self.board[:, col] += 1

		# aumento di 1 tutte le celle che si trovano sulle due diagonali
        rows, columns = self.board.shape
        for i in range(rows):
            for j in range(columns):
                if i - row == j - col or i + j == col + row:
                    self.board[i, j] += 1

		# setto il valore della cella interessata a -1
        self.board[row, col] = -1

	# metodo analogo al placeQueen ma per togliere la regina durante il backtracking
    def removeQueen(self, row, col, N):
        self.board[row, :] -= 1
        self.board[:, col] -= 1

        rows, columns = self.board.shape
        for i in range(rows):
            for j in range(columns):
                if i - row == j - col or i + j == col + row:
                    self.board[i, j] -= 1

		# """setto a 0 la cella in cui precedentemente avevo messo la regina perché per averla messa lì
  		# per forza di cose la cella non doveva essere sotto scacco"""
        self.board[row, col] = 0

    def backtrackingRecursive(self, N, col):
        # """caso base: una volta che sono arrivato alla fine delle colonne della board riuscendo a piazzare tutte le regine esco dal ciclo
        # perché vuol dire che si ha raggiunto una soluzione"""
        if col == N:
            return True
        row = 0
        found = False
        while not found and row < N:
            # se la cella non è tenuta sotto scacco piazzo la regina
            if self.board[row, col] == 0:
                self.placeQueen(row, col, N)
                # chiamata ricorsiva: vedo se alla colonna successiva c'è una cella libera per piazzare la prossima regina
                found = self.backtrackingRecursive(N, col + 1)

				# se non c'è, rimuovo la regina appena piazzata perché vuol dire che non era la strada giusta per la soluzione
                if not found:
                    self.removeQueen(row, col, N)
                    row += 1
            else:
                row += 1
        return found

if __name__ == '__main__':
    N = int(input("Quante regine vuoi utilizzare? "))
    b = NQueens(N)

    startTime = time.time()
    b.backtrackingRecursive(N, 0)
    endTime = time.time()

	# mi modifico la board finale per printarla in modo corretto
    for i in range(N):
        for j in range(N):
            if b.board[i, j] != -1:
                b.board[i, j] = 0
    print("Soluzione:\n", b.board)
    print("Tempo di esecuzione: ", f"{endTime-startTime:.3f}", " secondi\n")