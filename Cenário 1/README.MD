Cenário 1: Encontrando a Estação Central
Este projeto implementa uma solução em Python para o "Cenário 1", que consiste em determinar a estação de metrô mais central em uma rede não-direcionada e ponderada.

O Problema: Vértice Central
O objetivo é identificar o vértice (estação) que possui o menor custo total para alcançar todos os outros vértices da rede. O critério principal para essa escolha é o menor somatório das distâncias do vértice em questão para todos os demais.

Algoritmo Utilizado: Floyd-Warshall
Para resolver este problema, foi escolhido o algoritmo de Floyd-Warshall.

Justificativa da Escolha
O algoritmo de Floyd-Warshall é ideal para este cenário porque ele calcula a distância mínima entre todos os pares de vértices do grafo em uma única execução. Como precisamos analisar o somatório das distâncias de cada vértice para todos os outros, ter a matriz completa de distâncias mínimas torna o cálculo da estação central simples e direto.

A alternativa seria executar o algoritmo de Dijkstra a partir de cada um dos vértices do grafo, o que seria computacionalmente mais complexo para este problema específico.

Comparativo: Pseudocódigo vs. Implementação em Python
A implementação em Python é uma tradução fiel da lógica do pseudocódigo clássico, adaptada para uma estrutura orientada a objetos.

Lógica Principal
A essência do algoritmo é um conjunto de três laços aninhados que verificam sistematicamente se um caminho através de um vértice intermediário k é mais curto do que o caminho conhecido até o momento.

Pseudocódigo Clássico:

para k de 1 até n:
  para i de 1 até n:
    para j de 1 até n:
      se d[i][k] + d[k][j] < d[i][j] então:
        d[i][j] ← d[i][k] + d[k][j]
Implementação em Python (Método Principal):

Python

def calcular_todas_rotas_floyd_warshall(self):
    for k in range(self.num_estacoes):
        for i in range(self.num_estacoes):
            for j in range(self.num_estacoes):
                custo_via_k = self.matriz_custos[i][k] + self.matriz_custos[k][j]
                if custo_via_k < self.matriz_custos[i][j]:
                    self.matriz_custos[i][j] = custo_via_k
Mapeamento de Conceitos
Conceito (Pseudocódigo)	Implementação (Python)	Descrição
n (Nº de Vértices)	self.num_estacoes	Quantidade total de estações.
D (Matriz de Distâncias)	self.matriz_custos	Armazena as distâncias mínimas.
infinito	INFINITO = float('inf')	Representa a ausência de conexão.

Exportar para as Planilhas
Estrutura do Código
O código é organizado de forma modular e orientada a objetos:

RedeDeMetro (classe): Encapsula todos os dados (matriz de custos) e operações relacionadas ao grafo.

carregar_de_arquivo(): Método estático que lê e interpreta o arquivo de entrada (.txt) para construir a estrutura do grafo.

calcular_todas_rotas_floyd_warshall(): Implementa o algoritmo principal para preencher a matriz de distâncias mínimas.

encontrar_estacao_central(): Analisa a matriz de distâncias resultante para identificar o vértice central com base no critério do menor somatório.

Formato do Arquivo de Entrada
O programa espera um arquivo .txt (ex: graph1.txt) com o seguinte formato:

<num_vertices> <num_arestas>
<vertice1> <vertice2> <custo_da_conexao>
<vertice1> <vertice2> <custo_da_conexao>
...
Como Executar
Certifique-se de que o arquivo de dados (ex: graph1.txt) está na mesma pasta que o script Python.

Execute o script através do terminal:

Bash

python seu_script.py
Dependências
Python 3.x (não requer bibliotecas externas).

Exemplo de Saída
Ao executar o script com o graph1.txt fornecido, a saída esperada é:

--- Resultado da Análise da Estação Central ---

1. Estação Central Escolhida: 9
   (Critério: Menor somatório das distâncias a todos os outros vértices)

2. Vetor de Distâncias (da estação 9 para as demais):
   [39, 22, 37, 16, 19, 7, 17, 10, 0, 12, 15, 25]

3. Vértice Mais Distante da Estação Central:
   - Vértice: 1
   - Distância: 39

4. Matriz de Distâncias Mínimas Entre Todos os Pares (Resultado de Floyd-Warshall):

        1     2     3     4     5     6     7     8     9    10    11    12
    ----------------------------------------------------------------
    1  |    0    17    25    27    21    32    40    40    39    51    52    62
    2  |   17     0    42    10    27    15    39    23    22    34    37    47
    ... (restante da matriz)
