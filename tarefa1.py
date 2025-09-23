from uteis import GraphAdjMatrix


class ReadFile:

    def __init__(self) -> None:
        self.nos = None

    @property
    def openfile(self):
        with open("Pratica_1_-_Grafos/graph1.txt", "r") as file:
            readfile = file.read()
            linhas = readfile.split("\n")
            # Retirando a primeira linha do arquivo e usando list  comprehension para mudar o tipo para int.
            self.nos = [int(num) for linha in linhas for num in linha.split(" ") if num.strip() != ""]

        return self.nos


class Floyd(ReadFile, GraphAdjMatrix):
    # Iniciar o classe com a matriz de adjacência
    def __init__(self) -> None:
        ReadFile.__init__(self)
        self.nosfloyd = self.openfile
        GraphAdjMatrix.__init__(self, n = self.nos[0], directed = False)
        
        # Matriz de Distância
        n = self.nos[0]
        self.dist = [[float('inf') for _ in range(n+1)] for _ in range(n+1)]
        
        for i in range(n + 1):
            self.dist[i][i] = 0

        # Construído a matriz de Recorrência
        for i in range(2, len(self.nos), 3):
            # Construí os pesos iniciais D0
            v = self.nos[i] 
            w = self.nos[i+1] 
            weight = self.nos[i+2]
            
            self.addEdge(self.nos[i], self.nos[i+1])
            self.dist[v][w] = weight
            
            if not self.directed:
                self.dist[w][v] = weight

        
    def _centralstation(self):
        n = self.nos[0]
        
        # Algoritmo de Floyd-Warshall
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.M[i][j] = self.M[i][k]
        return self.dist

    def shortestpath(self):
        dist = self._centralstation()
        n = self.nos[0] + 1
        soma = [None] * n
        c = 0
