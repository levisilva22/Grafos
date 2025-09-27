### TEORIA DOS GRAFOS
## Cenário 1 
Para executar o cenário 1, basta alterar o grafo no arquivo graph1.txt, respeitando a formatação que o script cenario1.py espera:

i j

v1 v2 custo

v1 v2 custo

.

.

.

A primeira linha deve conter o número de vértices i (estações) e o número de arestas j (conexões), separados por um espaço.

As j linhas seguintes devem definir cada aresta no formato v1 v2 custo, onde:

v1 é o número da estação de origem.

v2 é o número da estação de destino.

custo é o peso numérico (distância) da conexão entre v1 e v2.

Os três valores (v1, v2, custo) em cada linha de aresta devem ser separados por espaços.

Após definir o grafo com a formatação correta em graph1.txt, basta abrir o arquivo Python que é o cenario1.py e rodar o algoritmo.



## Cenário 3
Para executar o cenário 3 basta alterar a matriz em grid_example.txt
respeitando a formatação:

i j

a11a12a13...a1j

a21a22a23...a2j

.

.

.

ai1ai2ai3...aij

Um espaço entre o número de linhas i e de colunas j.

Sem espaços entre elementos da matriz.

Só é possível escrever os caracteres de custo pré-definidos:

"." - piso livre peso 1

"~" - piso custoso peso 3

"#" - caminho bloqueado peso infinito

"S" - ponto de partida

"G" - ponto de chegada

Após definida a matriz em grid_example.txt, basta abrir o arquivo 
cenario3.py e rodar o algoritmo.

Os comparativos com o pseudocódigo base utilizado está em comparativo.txt
