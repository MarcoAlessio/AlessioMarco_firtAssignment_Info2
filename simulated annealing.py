import numpy as np
import random
import time

class NQueens:
    def __init__(self, N):
        self.board = np.zeros((N, N), dtype=int)
        self.iterations = 0
        self.bestBoard = np.zeros((N, N), dtype=int)

    def countCheckMate(self, N, M):
        matrixCheckMate = np.zeros((N, N), dtype=int)
        for col in range(N):
            row = list(M[:,col]).index(-1)
            temp = matrixCheckMate[row, col]
            matrixCheckMate[row, :] += 1
            matrixCheckMate[:, col] += 1
            for i in range(N):
                for j in range(N):
                    if i-row == j-col or i+j == col+row:
                        matrixCheckMate[i, j] += 1
            matrixCheckMate[row, col] = temp

        sum = 0
        for i in range(N):
            for j in range(N):
                if M[i, j] == -1:
                    sum += matrixCheckMate[i, j]
        return int(sum/2)

    def neighbor(self, N):
        l = []
        for j in range(5*N):
            tempMat = self.board.copy()
            col = random.randint(0, N-1)
            row = list(tempMat[:,col]).index(-1)
            newRow = random.choice([i for i in range(N) if i != row])
            tempMat[row, col] = 0
            tempMat[newRow, col] = -1
            if not any(np.array_equal(tempMat, m) for m in l):
                l.append(tempMat)
        return l

    def simulatedAnnealing(self, N, schedule):
        self.bestBoard = self.board.copy()
        for T in schedule:
            self.iterations+=1
            if self.countCheckMate(N, self.board)==0:
                self.bestBoard = self.board.copy()
                break
            next = random.choice(self.neighbor(N))
            de = self.countCheckMate(N, next) - self.countCheckMate(N, self.board)
            if de < 0 or random.random() < np.exp(-de / T):
                self.board = next
            if self.countCheckMate(N, self.board) < self.countCheckMate(N, self.bestBoard):
                self.bestBoard = self.board.copy()
        self.board = self.bestBoard.copy()

def scheduleGenerator(start_temp=100000, cooling_rate=0.995, min_temp=0.01):
    temp = start_temp
    while temp > min_temp:
        yield temp
        temp *= cooling_rate

if __name__ == '__main__':
    N = int(input("Quante regine vuoi utilizzare? "))
    b = NQueens(N)

    for i in range(N):
        b.board[random.randint(0, N-1),i] = -1
    print("Configurazione iniziale:\n", b.board)
    print(f"Coppie sotto scacco: {b.countCheckMate(N, b.board)}")

    startTime= time.time()
    schedule = scheduleGenerator()
    b.simulatedAnnealing(N, schedule)
    endTime = time.time()

    print("\nConfigurazione finale:\n", b.board)
    print(f"Coppie ancora sotto scacco: {b.countCheckMate(N, b.board)}")
    print(f"Numero di iterazioni: {b.iterations}")
    print("Tempo di esecuzione: ", f"{endTime-startTime:.3f}", " secondi")