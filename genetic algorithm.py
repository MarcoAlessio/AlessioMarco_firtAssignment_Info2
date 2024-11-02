import numpy as np
import random
import time
import sys

class NQueens:
    def __init__(self, N):
        # la board mi serve solo per mostrare la soluzione finale sottoforma di matrice
        self.board = np.zeros((N, N), dtype=int)
        # """popolazione e mating pool selezionata ad ogni generazione, sono liste di stringhe di lunghezza N 
        # ad esempio per N=5 potrebbe essere '01234', dove ogni intero rappresenta l'indice di riga in cui si trova la regina in quella colonna
        # (in questo esempio ho tutte le regine nella diagonale principale) """
        self.population = []
        self.matingPool = []
        # variabile che mi serve solo per printare la generazione a cui è arrivato l'algoritmo per trovare la soluzione
        self.generation = 0

    # metodo identico al simulated annealing per contare il numero di coppie sotto scacco nella matrice M
    def couplesInCheck(self, N, M):
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
    
    # metodo per generare la mating pool
    def getMatingPool(self, N, lenMat):
        # """creo una copia per non modificare la popolazione iniziale e una lista per contenere il numero di coppie sotto scacco 
        # per ogni elemento della popolazione"""
        population = self.population.copy()
        checkList = []
        for j in range(len(population)):
            state = population[j]
            # mi creo una matrice che mi serve da dare in input al metodo couplesInCheck()
            matrix = np.zeros((N, N), dtype=int)
            for i in range(N):
                matrix[int(state[i]),i] = -1
            n = self.couplesInCheck(N, matrix)
            checkList.append(n)

        # """se non è presente una soluzione all'interno della popolazione mi devo creare la mating pool attraverso una roulette di probabilità:
        # meno coppie sotto scacco ha una configurazione, più probabile sarà la sua estrazione per l'inserimento nella mating pool"""       
        if 0 not in checkList:
            inverse = [1 / v for v in checkList]
            prob = [inv / sum(inverse) for inv in inverse]
            self.matingPool = random.choices(population, weights=prob, k=lenMat)
        else:
            # se è presente una soluzione all'interno della popolazione viene restituita
            self.matingPool = [population[checkList.index(0)]]
 
    def crossover(self, N, i):
        matingPool = self.matingPool.copy()
        rand = random.randint(1, N-1)

        # prendo l'elemento all'indice i e all'indice i+1 e scambio tra loro le prime rand colonne 
        temp1 = matingPool[i][:rand] + matingPool[i+1][rand:]
        temp2 = matingPool[i+1][:rand] + matingPool[i][rand:]

        self.matingPool[i+1] = temp1
        self.matingPool[i] = temp2
            
    def mutation(self, N, i):
        matingPool = self.matingPool.copy()
        randPos = random.randint(0, N-1)
        # dato lo stato i-esimo della mating pool, modico la posizione di una delle sue regine
        state = matingPool[i]
        oldValue = state[randPos]
        newValue = str(random.choice([ele for ele in range(N) if ele != oldValue]))
        state = state[:randPos] + newValue + state[randPos+1:]
        self.matingPool[i] = state

    def geneticRecursive(self, N, lenMat, gen, maxGen):
        self.getMatingPool(N, lenMat)
        
        # caso base: se la mating pool ha un solo elemento vuol dire che probabilmente è la soluzione trovata
        if len(self.matingPool)==1:
            mat = np.zeros((N, N), dtype=int)
            for col in range(N):
                row = int(self.matingPool.copy()[0][col])
                mat[row,col] = -1
            if self.couplesInCheck(N, mat)==0:
                self.generation = gen
                return True
            else:
                return False
        # se viene superato il numero massimo di ricorsioni concesse il ciclo si ferma
        elif gen>=maxGen:
            return False
        # """in caso contrario applico con una certa probabilità (in funzione della stagnazione della mating pool) gli operatori 
        # di crossover e mutazione"""
        else:
            for i in range(0, lenMat-1, 2):
                uniqueConf = len(set(self.matingPool))
                dens = uniqueConf/len(self.matingPool)
                pCross = 1-0.3*dens
                if random.random()<pCross:
                    self.crossover(N, i)
                    
            for i in range(lenMat):
                uniqueConf = len(set(self.matingPool))
                dens = uniqueConf/len(self.matingPool)
                pMut = 0.05-0.03*dens
                if random.random()<pMut:
                    self.mutation(N, i)
        
        # la popolazione per la generazione successiva sarà la mating pool della generazione precedente     
        self.population = self.matingPool.copy()
        found = self.geneticRecursive(N, lenMat, gen+1, maxGen)
        return found
        
if __name__ == '__main__':
    N = int(input("Quante regine vuoi utilizzare? "))
    b = NQueens(N)
    # lunghezza iniziale della popolazione e della mating pool da estrarre
    lenPop = N*7
    lenMat = lenPop
    # setto il limite massimo di chiamate ricorsive ammesse
    limit = 10000
    sys.setrecursionlimit(limit) 

    # creo la mia popolazione come descritto nell'__init__
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

    # """creo la matrice con il risultato ottenuto, nel caso sia la soluzione sarà l'unico elemento nella mating pool, altrimenti prendo il primo 
    # in posizione 0 nella mating pool"""
    for col in range(N):
        row = int(b.matingPool[0][col])
        b.board[row,col] = -1
    if found:
        print(f"Soluzione raggiunta alla generazione {b.generation}:\n", b.board)
    else:
        print("Soluzione non trovata:\n", b.board)
        print("Coppie ancora sotto scacco: ", b.couplesInCheck(N, b.board))
    print("Tempo di esecuzione: ", f"{endTime-startTime:.3f}", " secondi")