import numpy as np
import random
import time

# -1 regina
# 0 altrove
class NQueens:
    def __init__(self, N):
        # board che mi rappresenta la configurazione della scacchiera ad ogni iterazione
        self.board = np.zeros((N, N), dtype=int)
        # parametri che mi servono solo per tenere conto del numero di iterazioni totali e della miglior configurazione raggiunta fin'ora
        self.iterations = 0
        self.bestBoard = np.zeros((N, N), dtype=int)

    # metodo per contare il numero di coppie sotto scacco nella matrice in input M
    def couplesInCheck(self, N, M):
        # mi creo la matrice che andrò a riempire cella per cella con il numero di scacchi a cui quella è sottoposta
        matrixCheckMate = np.zeros((N, N), dtype=int)
        # ciclo sulle colonne
        for col in range(N):
            # trovo l'indice di riga in cui si trova la regina
            row = list(M[:,col]).index(-1)
            # """mi salvo il valore della cella perché non deve essere incrementato, in quanto la cella in cui si trova la regina non ha senso
            # che mi venga tenuta sotto scacco da se stessa"""
            temp = matrixCheckMate[row, col]
            # aumento di uno tutte le celle che si trovano all'indice di riga row, di colonna col e le diagonali
            matrixCheckMate[row, :] += 1
            matrixCheckMate[:, col] += 1
            for i in range(N):
                for j in range(N):
                    if i-row == j-col or i+j == col+row:
                        matrixCheckMate[i, j] += 1
            # ri-setto il valore corretto alla cella in questione
            matrixCheckMate[row, col] = temp

        # sommo i valori di tutte le celle corrispondenti alla posizione delle regine
        sum = 0
        for i in range(N):
            for j in range(N):
                if M[i, j] == -1:
                    sum += matrixCheckMate[i, j]
        # se due regine si tengono sotto scacco, quello scacco viene contato due volte (uno per regina), divido per 2 per trovare il numero di coppie
        return int(sum/2)

    # metodo che mi genera una pool (lista l) di neighbors
    def neighbor(self, N):
        l = []
        # mi genero 5*N neighbors
        for j in range(5*N):
            # mi creo una copia della board per evitare di modificare la board corrente
            tempMat = self.board.copy()
            # scelgo una colonna random della board e sposto la regina di quella colonna in una nuova cella
            col = random.randint(0, N-1)
            row = list(tempMat[:,col]).index(-1)
            newRow = random.choice([i for i in range(N) if i != row])
            tempMat[row, col] = 0
            tempMat[newRow, col] = -1
            # evito doppioni
            if not any(np.array_equal(tempMat, m) for m in l):
                l.append(tempMat)
        return l

    def simulatedAnnealing(self, N, schedule):
        self.bestBoard = self.board.copy()
        # itero su ogni valore dello schedule di temperature generato
        for T in schedule:
            self.iterations+=1
            # se la configurazione corrente presenta 0 coppie sotto scacco, ho trovato la soluzione ed interrompo il ciclo
            if self.couplesInCheck(N, self.board)==0:
                self.bestBoard = self.board.copy()
                break
            # in caso contrario, scelgo randomicamente dalla pool di neighbors un canditato allo stato futuro
            next = random.choice(self.neighbor(N))
            de = self.couplesInCheck(N, next) - self.couplesInCheck(N, self.board)
            # """se il neighbor scelto ha meno coppie sotto scacco compio la transizione, in caso contrario la transizione può comunque essere
            # compiuta con una probabilità che va diminuendo nel tempo"""
            if de < 0 or random.random() < np.exp(-de / T):
                self.board = next
            # controllo ogni volta che la configurazione corrente non sia la migliore mai trovata
            if self.couplesInCheck(N, self.board) < self.couplesInCheck(N, self.bestBoard):
                self.bestBoard = self.board.copy()
        # in caso di soluzione non trovata returno sempre la configurazione migliore
        self.board = self.bestBoard.copy()

def scheduleGenerator(start_temp=100000, cooling_rate=0.998, min_temp=0.01):
    temp = start_temp
    while temp > min_temp:
        yield temp
        temp *= cooling_rate

if __name__ == '__main__':
    N = int(input("Quante regine vuoi utilizzare? "))
    b = NQueens(N)

    # """come configurazione iniziale, da una board vuota piazzo una regina in una cella random per ogni colonna
    # così da avere solo una regina per colonna (unico vincolo del codice)"""
    for i in range(N):
        b.board[random.randint(0, N-1),i] = -1
    print("Configurazione iniziale:\n", b.board)
    print(f"Coppie sotto scacco: {b.couplesInCheck(N, b.board)}")

    startTime= time.time()
    schedule = scheduleGenerator()
    b.simulatedAnnealing(N, schedule)
    endTime = time.time()

    print("\nConfigurazione finale:\n", b.board)
    print(f"Coppie ancora sotto scacco: {b.couplesInCheck(N, b.board)}")
    print(f"Numero di iterazioni: {b.iterations}")
    print("Tempo di esecuzione: ", f"{endTime-startTime:.4f}", " secondi")