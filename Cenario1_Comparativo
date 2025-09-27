# Cenário 1 x Pseudocódigo de Floyd-Warshall

## O Problema: Vértice Central
O objetivo é identificar o vértice (estação) que possui o menor custo total para alcançar todos os outros vértices da rede. O critério principal para essa escolha é o menor somatório das distâncias do vértice em questão para todos os demais.

## Algoritmo Utilizado: Floyd-Warshall
Para resolver este problema, foi escolhido o algoritmo de Floyd-Warshall.

## Justificativa da Escolha
O algoritmo de Floyd-Warshall é ideal para este cenário porque ele calcula a distância mínima entre todos os pares de vértices do grafo em uma única execução. Como precisamos analisar o somatório das distâncias de cada vértice para todos os outros, ter a matriz completa de distâncias mínimas torna o cálculo da estação central simples e direto.

## A alternativa seria executar o algoritmo de Dijkstra a partir de cada um dos vértices do grafo, o que seria computacionalmente mais complexo para este problema específico.

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
