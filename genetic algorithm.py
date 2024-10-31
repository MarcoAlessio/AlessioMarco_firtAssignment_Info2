import numpy as np
import random
import time
import sys

class NQueens:
    def __init__(self, N):
        self.board = np.zeros((N, N), dtype=int)
        self.population = []
        self.matingPool = []
        self.generation = 0

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
    
    def getMatingPool(self, N, lenMat):
        population = self.population.copy()
        checkList = []
        for j in range(len(population)):
            state = population[j]
            matrix = np.zeros((N, N), dtype=int)
            for i in range(N):
                matrix[int(state[i]),i] = -1
            
            n = self.countCheckMate(N, matrix)
            checkList.append(n)
        
        if 0 not in checkList:
            inverseProb = [1 / v for v in checkList]
            prob = [inv / sum(inverseProb) for inv in inverseProb]
            self.matingPool = random.choices(population, weights=prob, k=lenMat)
            # z = [x for _, x in sorted(zip(prob, matingPool), reverse=True)]
        else:
            self.matingPool = [population[checkList.index(0)]]
 
    def crossover(self, N, i):
        matingPool = self.matingPool.copy()
        rand = random.randint(1, N-2)

        temp1 = matingPool[i][:rand] + matingPool[i+1][rand:]
        temp2 = matingPool[i+1][:rand] + matingPool[i][rand:]

        self.matingPool[i+1] = temp1
        self.matingPool[i] = temp2
            
    def mutation(self, N, i):
        matingPool = self.matingPool.copy()
        randPos = random.randint(0, N-1)
        state = matingPool[i]
        oldValue = state[randPos]
        newValue = str(random.choice([ele for ele in range(N) if ele != oldValue]))
        state = state[:randPos] + newValue + state[randPos+1:]
        self.matingPool[i] = state

    def geneticRecursive(self, N, lenMat, gen, maxGen):
        self.getMatingPool(N, lenMat)

        mat = np.zeros((N, N), dtype=int)
        for col in range(N):
            row = int(self.matingPool.copy()[0][col])
            mat[row,col] = -1

        if len(self.matingPool)==1 and self.countCheckMate(N, mat)==0:
            self.generation = gen
            return True
        elif gen>=maxGen:
            return False
        else:
            for i in range(0, lenMat-1, 2):
                uniqueConf = len(set(self.matingPool))
                dens = uniqueConf/len(self.matingPool)
                pCross = 0.7+0.3*dens
                if random.random()<pCross:
                    self.crossover(N, i)
                    
            for i in range(lenMat):
                uniqueConf = len(set(self.matingPool))
                dens = uniqueConf/len(self.matingPool)
                pMut = 0.01+0.04*dens
                if random.random()<pMut:
                    self.mutation(N, i)
            
        self.population = self.matingPool.copy()
        found = self.geneticRecursive(N, lenMat, gen+1, maxGen)
        return found
        
if __name__ == '__main__':
    N = int(input("Quante regine vuoi utilizzare? "))
    b = NQueens(N)
    lenPop = N*8
    lenMat = int(lenPop*(2/3))   
    limit = 10000
    sys.setrecursionlimit(limit) 

    for j in range(lenPop):
        l=[]
        for i in range(N):
            rand = random.randint(0, N-1)
            l.append(rand)

        s = "".join(str(x) for x in l)
        b.population.append(s)

    startTime = time.time()
    found = b.geneticRecursive(N, lenMat, 0, limit-(limit/100))
    endTime = time.time()

    for col in range(N):
        row = int(b.matingPool[0][col])
        b.board[row,col] = -1
    if found:
        print(f"Soluzione raggiunta alla generazione {b.generation}:\n", b.board)
    else:
        print("Soluzione non trovata:\n", b.board)
        print("Coppie ancora sotto scacco: ", b.countCheckMate(N, b.board))
    print("Tempo di esecuzione: ", f"{endTime-startTime:.3f}", " secondi")