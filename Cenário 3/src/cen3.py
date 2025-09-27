import math
import os
# Importando as classes base fornecidas
from uteis import GraphBase, GraphAdjMatrix 
from typing import List, Tuple, Dict, Set, Optional, Generator

# --- 1. CONFIGURAÇÃO DE CUSTOS E LEITURA ---

CUSTOS = {
    '.': 1,      # Célula livre (custo 1)
    '~': 3,      # Piso difícil (custo 3)
    'S': 0,      # Ponto de Início (custo inicial d[S] é 0)
    'G': 1,      # Ponto de Objetivo (custo de movimento para 'G' é como piso livre)
    '#': math.inf # Obstáculo (Intransponível)
}

def ler_grid_do_arquivo(nome_arquivo: str) -> Tuple[int, int, List[List[str]]]:
    """Lê o grid do arquivo de texto."""
    try:
        with open(nome_arquivo, 'r') as f:
            linhas = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        # Conteúdo do grid_example.txt como fallback
        print(f"Aviso: O arquivo '{nome_arquivo}' não foi encontrado. Usando o conteúdo do arquivo anexado para demonstração.")
        linhas = [
            "10 15",
            "~~~~~~~~.......",
            "~~####~~~~~~...",
            "~~#..#.~~~~....",
            "S.#..#..G......",
            "..#..####~~....",
            "..#.........~~.",
            "..######..~~...",
            "......#.~~##...",
            "..##..#..###...",
            "..............."
        ]

    dimensao_linha = linhas[0].split()
    num_linhas, num_colunas = map(int, dimensao_linha)
    grid = [list(row) for row in linhas[1:]]

    return num_linhas, num_colunas, grid

# --- 2. EXTENSÃO DA CLASSE DE GRAFO PARA SUPORTE A PESOS ---

class WeightedGridGraph(GraphAdjMatrix):
    """
    Extende GraphAdjMatrix para suportar pesos (custos) de aresta,
    necessários para o Algoritmo de Dijkstra.
    """

    def __init__(self, n: int, directed: bool = False):
        super().__init__(n, directed)
        # self.M é a matriz de adjacência (usaremos para armazenar o peso da aresta)

    def addEdge(self, v: int, w: int, weight: float):
        """Adiciona aresta vw com o peso (custo)."""
        # Armazena o peso na matriz M
        self.M[v][w] = weight
        if not self.directed:
            self.M[w][v] = weight
        self.m += 1

    def getNeighbors(self, v: int) -> Generator[Tuple[int, float], None, None]:
        """Retorna vizinhos de v e o custo do movimento (peso)."""
        w = 1
        while w <= self.n:
            weight = self.M[v][w]
            # Uma aresta existe se o peso for > 0 (e não infinito, que é o caso do '#')
            if weight > 0 and weight != math.inf: 
                yield (w, weight)
            w += 1

# --- 3. CONVERSOR DO GRID PARA GRAFO E MAPEAMENTO DE ÍNDICES ---

class GridToGraphConverter:
    """Converte o grid de caracteres em um objeto WeightedGridGraph."""

    def __init__(self, num_linhas: int, num_colunas: int, grid: List[List[str]]):
        self.num_linhas = num_linhas
        self.num_colunas = num_colunas
        self.grid = grid
        self.tamanho_V = num_linhas * num_colunas
        self.start_coord: Optional[Tuple[int, int]] = None
        self.goal_coord: Optional[Tuple[int, int]] = None
        
        # O grafo WeightedGridGraph usará indexação 1-based (1 a N)
        self.graph = WeightedGridGraph(self.tamanho_V, directed=True) # Usamos direcionado para maior flexibilidade
        
        self._encontrar_pontos()
        self._construir_arestas()

    def _encontrar_pontos(self):
        """Encontra as coordenadas de S e G."""
        for r in range(self.num_linhas):
            for c in range(self.num_colunas):
                if self.grid[r][c] == 'S':
                    self.start_coord = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal_coord = (r, c)
        
        if self.start_coord is None or self.goal_coord is None:
            raise ValueError("O grid deve conter um ponto de Início ('S') e um Objetivo ('G').")
    
    def get_start_node(self) -> int:
        """Retorna o índice 1-based do nó inicial."""
        # Mapeia 0-based para 1-based
        return self.coord_to_index(self.start_coord) + 1 
    
    def get_goal_node(self) -> int:
        """Retorna o índice 1-based do nó objetivo."""
        # Mapeia 0-based para 1-based
        return self.coord_to_index(self.goal_coord) + 1

    def coord_to_index(self, coord: Tuple[int, int]) -> int:
        """Converte uma coordenada (r, c) em um índice 0-based 1D."""
        r, c = coord
        return r * self.num_colunas + c

    def index_to_coord(self, index_0_based: int) -> Tuple[int, int]:
        """Converte um índice 0-based 1D em uma coordenada (r, c)."""
        r = index_0_based // self.num_colunas
        c = index_0_based % self.num_colunas
        return (r, c)

    def get_custo_movimento(self, coord: Tuple[int, int]) -> float:
        """Retorna o custo de *entrar* em uma célula."""
        r, c = coord
        if 0 <= r < self.num_linhas and 0 <= c < self.num_colunas:
            caractere = self.grid[r][c]
            
            # O custo de movimento para 'S' ou 'G' é o do piso livre ('.'), que é 1.
            if caractere in ('S', 'G'):
                return CUSTOS['.']
            
            return CUSTOS.get(caractere, math.inf)
        return math.inf

    def _construir_arestas(self):
        """Popula a matriz de adjacência do grafo com as arestas e pesos."""
        
        direcoes = [(-1, 0), (1, 0), (0, 1), (0, -1)] # N, S, L, O (4-direções)
        
        for r_origem in range(self.num_linhas):
            for c_origem in range(self.num_colunas):
                coord_origem = (r_origem, c_origem)
                
                # Vértice de origem (1-based)
                v = self.coord_to_index(coord_origem) + 1 
                
                # Se a origem for um obstáculo, não há arestas de saída.
                if self.grid[r_origem][c_origem] == '#':
                    continue

                for dr, dc in direcoes:
                    r_destino, c_destino = r_origem + dr, c_origem + dc
                    coord_destino = (r_destino, c_destino)
                    
                    if 0 <= r_destino < self.num_linhas and 0 <= c_destino < self.num_colunas:
                        custo_movimento = self.get_custo_movimento(coord_destino)
                        
                        if custo_movimento != math.inf:
                            # Vértice de destino (1-based)
                            w = self.coord_to_index(coord_destino) + 1
                            
                            # Adiciona a aresta v -> w com o custo
                            self.graph.addEdge(v, w, custo_movimento)
                            
# --- 4. IMPLEMENTAÇÃO DO DIJKSTRA (1-based) ---

class Dijkstra:
    """Implementação do Algoritmo de Dijkstra, utilizando o WeightedGridGraph e indexação 1-based."""

    def __init__(self, converter: GridToGraphConverter):
        self.graph = converter.graph
        # Vértices (1 a N)
        self.V = range(1, self.graph.n + 1)
        self.r_origem = converter.get_start_node()
        self.destino = converter.get_goal_node()
        self.INF = math.inf
        
        # Variáveis do pseudocódigo, ajustadas para indexação 1-based (tamanho N+1)
        self.d = [self.INF] * (self.graph.n + 1) # d_1i (distância da origem)
        self.anterior = [None] * (self.graph.n + 1) # anterior(i)
        
        # A (Conjunto de vértices abertos)
        self.A: Set[int] = set(self.V)
        # F (Conjunto de vértices fechados)
        self.F: Set[int] = set()

    def inicializacao(self):
        """Passos de inicialização."""
        
        # d_11 <- 0; d_1i <- inf para todo i em V - {1};
        self.d[self.r_origem] = 0
        
        # anterior(i) <- Ø para todo i em V;
        pass

    def executa(self):
        """Laço principal do algoritmo 'enquanto A != Ø fazer'."""
        
        self.inicializacao()

        while self.A: # enquanto A != Ø fazer
            
            # r <- v em V | d_1r = min{d_1j}, j em A [acha o vértice mais próximo da origem]
            r_escolhido: Optional[int] = None
            min_dist = self.INF
            
            # Busca linear para encontrar o mínimo em A (fiel ao pseudocódigo)
            for j in self.A:
                if self.d[j] < min_dist:
                    min_dist = self.d[j]
                    r_escolhido = j
            
            if r_escolhido is None:
                break 

            r = r_escolhido

            # F <- F U {r}; A <- A - {r}; [o vértice r sai de Aberto para Fechado]
            self.F.add(r)
            self.A.remove(r)
            
            # Otimização: Parar se o objetivo for alcançado
            if r == self.destino:
                break

            # S <- A ∩ N'(r) [S são os sucessores de r ainda abertos]
            
            # Itera sobre os vizinhos e o custo (peso) da aresta
            for l_vizinho_index, custo_movimento_v_rl in self.graph.getNeighbors(r):
                
                # Verifica se o vizinho 'l' ainda está em A
                if l_vizinho_index in self.A:
                    
                    # Nova soma: (d_1r + v_rl)
                    nova_soma = self.d[r] + custo_movimento_v_rl
                    
                    # se nova_soma < d_1l então [Compara o valor anterior com a nova soma, que é a lógica do 'min']
                    if nova_soma < self.d[l_vizinho_index]:
                        
                        # Início
                        
                        # d_1l <- p; anterior(l) <- r; [ganhou uma nova distância!]
                        self.d[l_vizinho_index] = nova_soma
                        self.anterior[l_vizinho_index] = r
                        
                        # fim;

        return self.d, self.anterior

    def reconstruir_caminho(self, converter: GridToGraphConverter) -> List[Tuple[int, int]]:
        """Reconstrói o caminho do destino à origem."""
        caminho_1_based = []
        vertice_atual = self.destino
        
        if self.d[self.destino] == self.INF:
            return []
            
        while vertice_atual is not None:
            caminho_1_based.append(vertice_atual)
            if vertice_atual == self.r_origem:
                break
            vertice_atual = self.anterior[vertice_atual]

        # Converte os índices 1-based para coordenadas (r, c) 0-based
        caminho_coords = []
        for index_1_based in caminho_1_based[::-1]:
            # Mapeia 1-based para 0-based
            index_0_based = index_1_based - 1
            caminho_coords.append(converter.index_to_coord(index_0_based))
            
        return caminho_coords

# --- 5. EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    nome_arquivo = "grid_example.txt"
    print(f"--- Cenário 3: Robô de armazém com obstáculos (Usando {nome_arquivo}) ---")

    try:
        # 1. Leitura e Conversão do mapa
        num_linhas, num_colunas, grid = ler_grid_do_arquivo(nome_arquivo)
        converter = GridToGraphConverter(num_linhas, num_colunas, grid)

        # 2. Execução do Dijkstra (usando os índices 1-based do grafo)
        dijkstra_solver = Dijkstra(converter)
        distancias, predecessores = dijkstra_solver.executa()

        # 3. Reconstrução do caminho (convertendo de volta para coordenadas)
        caminho = dijkstra_solver.reconstruir_caminho(converter)
        custo_total = distancias[dijkstra_solver.destino]

        # 4. Exibição dos resultados

        print(f"\nMapa do Armazém ({num_linhas}x{num_colunas}):")
        for row in grid:
            print("".join(row))

        if caminho and custo_total != math.inf:
            print("\nCaminho de Menor Custo Encontrado:")
            
            # Cria uma cópia do grid para marcar o caminho
            grid_caminho = [list(row) for row in grid]
            
            # Marca o caminho com '@'
            for r, c in caminho:
                if grid_caminho[r][c] not in ('S', 'G'):
                    grid_caminho[r][c] = '@'
            
            # Exibe o grid com o caminho marcado
            for row in grid_caminho:
                print("".join(row))
                
            print(f"\nCusto Total (Distância de S para G): {custo_total}")
            print(f"Caminho (coordenadas r, c): {caminho}")

        else:
            print("\nO destino ('G') é inalcançável a partir da origem ('S').")

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")