### TEORIA DOS GRAFOS

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
cen3.py e rodar o algoritmo.

Os comparativos com o pseudocódigo base utilizado está em comparativo.txt
