# Cenário 1 x Pseudocódigo de Floyd-Warshall

## O Problema: Vértice Central
O objetivo é identificar o vértice (estação) que possui o menor custo total para alcançar todos os outros vértices da rede. O critério principal para essa escolha é o menor somatório das distâncias do vértice em questão para todos os demais.

## Algoritmo Utilizado: Floyd-Warshall
Para resolver este problema, foi escolhido o algoritmo de Floyd-Warshall.

## Justificativa da Escolha
O algoritmo de Floyd-Warshall é ideal para este cenário porque ele calcula a distância mínima entre todos os pares de vértices do grafo em uma única execução. Como precisamos analisar o somatório das distâncias de cada vértice para todos os outros, ter a matriz completa de distâncias mínimas torna o cálculo da estação central simples e direto.

## Comparativo: Pseudocódigo vs. Implementação em Python
A implementação em Python é uma tradução fiel da lógica do pseudocódigo clássico, adaptada para uma estrutura orientada a objetos.
```
    ALGORITMO FloydWarshall(Grafo G)
  // Entrada: Grafo G com n vértices, representado por uma matriz de adjacências
  // Saída: Matriz D com as distâncias mais curtas entre todos os pares de vértices

  // 1. Inicializar a matriz de distâncias
  D = matriz de adjacências do Grafo G (com ∞ para arestas não existentes e 0 para a distância de um vértice a ele mesmo)

  // 2. Iterar através de todos os vértices como intermediários
  PARA k DE 1 ATÉ n
    // 3. Iterar através de todos os vértices de origem
    PARA i DE 1 ATÉ n
      // 4. Iterar através de todos os vértices de destino
      PARA j DE 1 ATÉ n
        // 5. Atualizar a distância se um caminho mais curto for encontrado através de k
        SE (D[i][k] + D[k][j] < D[i][j]) ENTÃO
          D[i][j] = D[i][k] + D[k][j]
        FIM SE
      FIM PARA
    FIM PARA
  FIM PARA

  RETORNAR D
FIM ALGORITMO
```
## A implementação em Python : 
```
  def calcular_todas_rotas_floyd_warshall(self):
      for k in range(self.num_estacoes):
          for i in range(self.num_estacoes):
              for j in range(self.num_estacoes):
                  custo_via_k = self.matriz_custos[i][k] + self.matriz_custos[k][j]
                  if custo_via_k < self.matriz_custos[i][j]:
                      self.matriz_custos[i][j] = custo_via_k
```

| **Pseudocódigo** | **Código Python** | **Explicação** |
|------------------|-------------------|----------------|
| `dados G = (V,E); matriz de valores V(G)` | `GraphAdjMatrix.__init__(self, n = self.nos[0], directed = True)` | Inicialização do grafo com vértices e arestas |
| `D⁰ = [dᵢⱼ] ← V(G)` | `self.dist = [[float('inf') for _ in range(n)] for _ in range(n)]` | Criação da matriz de distâncias inicial |
| `rᵢⱼ ← j ∀i` | `self.M[v][w] = w (arquivo uteis - class GraphAdjMatrix - método addEdge)` | Inicialização da matriz de roteamento |
| `para k = 1, ..., n fazer` | `for k in range(self.nos[0]):` | Loop externo do vértice intermediário k |
| `para todo i, j = 1, ..., n fazer` | `for i in range(self.nos[0]):`<br>`for j in range(self.nos[0]):` | Loops aninhados para todos os pares (i,j) |
| `se dᵢₖ + dₖⱼ < dᵢⱼ então` | `if matriz_dist[i][k] + matriz_dist[k][j] < matriz_dist[i][j]:` | Condição de relaxamento da distância |
| `dᵢⱼ ← dᵢₖ + dₖⱼ` | `matriz_dist[i][j] = matriz_dist[i][k] + matriz_dist[k][j]` | Atualização da distância mínima |
| `rᵢⱼ ← rᵢₖ` | `self.M[i][j] = self.M[i][k]` | Atualização da matriz de roteamento |



| **Pseudocódigo** | **Código Python** | **Correspondência** |
|------------------|-------------------|---------------------|
|`PARA k DE 1 ATÉ n` |	for k in range(self.num_estacoes):|	Laço do vértice intermediário (pivot).`|
|`PARA i DE 1 ATÉ n` |for i in range(self.num_estacoes):|	Laço do vértice de origem.`|
|`PARA j DE 1 ATÉ n` |	for j in range(self.num_estacoes):`|` Laço do vértice de destino.`|
|`D[i][k] + D[k][j]|`	self.matriz_custos[i][k] + self.matriz_custos[k][j]`|`	O custo de ir de i a j via k.`|
|`SE (...) ENTÃO D[i][j] = (...)`|	`if custo_via_k < self.matriz_custos[i][j]:`|`	A condição de relaxamento (atualização).`|




