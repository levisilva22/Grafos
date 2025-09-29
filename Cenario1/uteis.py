import sys
from typing import Generator
from abc import ABC, abstractmethod

# Usamos um valor alto para representar a ausência de conexão (infinito).
INFINITO = float('inf')

class GraphBase(ABC):
    # ... (O código da classe GraphBase permanece inalterado)
    def __init__(self, n: int, directed: bool = False) -> None:
      self.n, self.m, self.directed = n, 0, directed

    @abstractmethod
    def addEdge(self, v : int, w : int, weight: int = 1): # Adicionando 'weight' para ser mais geral
      pass
      
    @abstractmethod
    def removeEdge(self, v: int, w: int):
      pass
      
    def V(self) -> Generator[int, None, None]:
      for i in range(1, self.n+1):
        yield i

# ----------------------------------------------------------------------
# CLASSE GraphAdjMatrix COM FLOYD-WARSHALL
# ----------------------------------------------------------------------

class GraphAdjMatrix(GraphBase):
    """
    Implementação de grafo usando matriz de adjacências.
    A matriz M agora armazenará os custos/pesos.
    """
    def __init__(self, n, directed = False):
      super().__init__(n, directed)
      # Inicializa M com INFINITO, e 0 na diagonal
      self.M = [[INFINITO] * (self.n + 1) for _ in range(self.n + 1)]
      for i in range(1, self.n + 1):
        self.M[i][i] = 0

    def addEdge(self, v: int, w: int, weight: int = 1):
      """ Adiciona aresta com peso. Se for a primeira vez, incrementa m. """
      if self.M[v][w] == INFINITO and v != w:
          self.m += 1
          
      self.M[v][w] = weight
      if not self.directed:
        self.M[w][v] = weight
        
    def removeEdge(self, v: int, w: int):
      """ Remove a aresta, restaurando para INFINITO. """
      if self.M[v][w] != INFINITO:
          self.m -= 1
          
      self.M[v][w] = INFINITO
      if not self.directed:
        self.M[w][v] = INFINITO

    # --- IMPLEMENTAÇÃO FLOYD-WARSHALL ---
    def floyd_warshall(self):
      """
      Executa o algoritmo de Floyd-Warshall para encontrar os caminhos
      mínimos entre todos os pares de vértices na matriz M.
      O resultado é armazenado na própria matriz M.
      """
      N = self.n
      
      # Os laços vão de 1 a N, pois os vértices são indexados de 1 a N
      for k in self.V():
        for i in self.V():
          for j in self.V():
            
            # Evita a soma de INFINITO + INFINITO, mas permite qualquer soma
            # desde que não envolva um caminho impossível. 
            # Uma verificação mais simples é suficiente:
            if self.M[i][k] != INFINITO and self.M[k][j] != INFINITO:
                custo_via_k = self.M[i][k] + self.M[k][j]
            else:
                custo_via_k = INFINITO
            
            if custo_via_k < self.M[i][j]:
              self.M[i][j] = custo_via_k

      # A matriz self.M agora contém todas as distâncias mínimas.
      # Você pode retornar ou simplesmente deixá-la como um estado da classe.
      return self.M

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Grafo não-direcionado com 4 vértices
    grafo = GraphAdjMatrix(n=4, directed=False)
    
    # Adicionando arestas (v, w, peso)
    grafo.addEdge(1, 2, 3)
    grafo.addEdge(1, 4, 7)
    grafo.addEdge(2, 3, 2)
    grafo.addEdge(3, 4, 1)

    # Imprimir a matriz inicial (com zeros e INFINITO nos índices 0)
    print("Matriz de Custos Diretos (Inicial):")
    for row in grafo.M[1:]:
        print([int(x) if x != INFINITO else 'inf' for x in row[1:]])

    print("-" * 30)

    # Executar o Floyd-Warshall
    distancias_minimas = grafo.floyd_warshall()

    # Imprimir a matriz final
    print("Matriz de Distâncias Mínimas (Final):")
    for row in distancias_minimas[1:]:
        print([int(x) if x != INFINITO else 'inf' for x in row[1:]])