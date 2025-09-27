from uteis import GraphAdjMatrix


class ReadFile:

    def __init__(self) -> None:
        self.nos = None

    @property
    def openfile(self):
        with open("graph2.txt", "r") as file:
            readfile = file.read()
            linhas = readfile.split("\n")
            # Retirando a primeira linha do arquivo e usando list  comprehension para mudar o tipo para int.
            self.nos = [int(num) for linha in linhas for num in linha.split() if num.strip() != ""]

        return self.nos


class BellmanFord(ReadFile, GraphAdjMatrix):
    # Iniciar o classe com a matriz de adjacência e a matriz de roteamento M
    def __init__(self) -> None:
        ReadFile.__init__(self)
        self.nosfloyd = self.openfile
        GraphAdjMatrix.__init__(self, n = self.nos[0], directed = True)
        
        # Matriz de Distância
        n = self.nos[0]
        self.dist = [[float('inf') for _ in range(n)] for _ in range(n)]

        # Diagonais igual a 0
        for i in range(n):
            self.dist[i][i] = 0


        # Construído a matriz de Recorrência
        for i in range(2, len(self.nos), 3):
            # Construí os pesos iniciais D0
            v = self.nos[i] 
            w = self.nos[i+1] 
            weight = self.nos[i+2]
            
            self.addEdge(v,w)
            self.dist[v][w] = weight

            
    def CaminhoMinimo(self):
        matriz_dist = self.dist
        
        for k in range(self.nos[0]):
            for i in range(self.nos[0]):
                for j in range(self.nos[0]):
                    if matriz_dist[i][k] + matriz_dist[k][j] < matriz_dist[i][j]:
                        matriz_dist[i][j] = matriz_dist[i][k] + matriz_dist[k][j]
                        self.M[i][j] = self.M[i][k]

        origem = 0
        destino = 6
        
        # 1. Custo mínimo
        custo_minimo = self.dist[origem][destino]
        
        # 2. Reconstruir o caminho usando a matriz de roteamento
        caminho = self.reconstruir_caminho(origem, destino)
        
        return caminho, custo_minimo

    def reconstruir_caminho(self, origem, destino):
        """Reconstrói o caminho usando a matriz de roteamento R"""
        if self.dist[origem][destino] == float('inf'):
            return None  # Não há caminho
        
        caminho = [origem]
        atual = origem
        
        while atual != destino:
            atual = self.M[atual][destino]
            caminho.append(atual)
        
        return caminho
    

objeto = BellmanFord()
caminho, custo_minimo = objeto.CaminhoMinimo()
print(f'O caminho mínimo partindo de 0 até 6: {",".join( map(str,caminho))} \n'
      f'Custo mínimo saindo de 0 até 6: {custo_minimo}')