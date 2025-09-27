import sys

# Usamos um valor alto para representar a ausência de conexão direta (infinito).
INFINITO = float('inf')

class RedeDeMetro:
    """
    Representa a rede de metrô como um grafo, contendo a matriz de
    distâncias para o roteamento.
    """
    def __init__(self, num_estacoes):
        self.num_estacoes = num_estacoes
        # Matriz de distâncias 'D' do pseudocódigo
        self.matriz_custos = [[INFINITO] * num_estacoes for _ in range(num_estacoes)]

        for i in range(num_estacoes):
            self.matriz_custos[i][i] = 0

    def adicionar_trecho(self, estacao_a, estacao_b, custo):
        """ Adiciona uma conexão (aresta) não-direcionada entre duas estações. """
        idx_a, idx_b = estacao_a - 1, estacao_b - 1
        self.matriz_custos[idx_a][idx_b] = custo
        self.matriz_custos[idx_b][idx_a] = custo

    @staticmethod
    def carregar_de_arquivo(caminho_arquivo):
        """
        Lê um arquivo de texto para criar e popular uma instância da RedeDeMetro.
        """
        try:
            with open(caminho_arquivo, 'r') as f:
                num_estacoes, num_trechos = map(int, f.readline().split())
                rede = RedeDeMetro(num_estacoes)
                for _ in range(num_trechos):
                    v1, v2, custo = map(int, f.readline().split())
                    rede.adicionar_trecho(v1, v2, custo)
                return rede
        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
            return None

    def calcular_todas_rotas_floyd_warshall(self):
        """
        Executa o algoritmo de Floyd-Warshall. Esta é a implementação
        direta do pseudocódigo.
        """
        for k in range(self.num_estacoes):
            for i in range(self.num_estacoes):
                for j in range(self.num_estacoes):
                    custo_via_k = self.matriz_custos[i][k] + self.matriz_custos[k][j]
                    if custo_via_k < self.matriz_custos[i][j]:
                        self.matriz_custos[i][j] = custo_via_k

    def encontrar_estacao_central(self):
        """
        Analisa a matriz de custos para determinar a estação central.
        """
        melhor_candidata_idx = -1
        menor_soma_distancias = INFINITO
        for i in range(self.num_estacoes):
            soma_atual = sum(self.matriz_custos[i])
            if soma_atual < menor_soma_distancias:
                menor_soma_distancias = soma_atual
                melhor_candidata_idx = i
        
        if melhor_candidata_idx == -1:
            return None, [], None, INFINITO

        estacao_central_id = melhor_candidata_idx + 1
        vetor_distancias_central = self.matriz_custos[melhor_candidata_idx]
        distancia_maxima_final = max(vetor_distancias_central)
        no_mais_distante_id = vetor_distancias_central.index(distancia_maxima_final) + 1
        
        return estacao_central_id, vetor_distancias_central, no_mais_distante_id, distancia_maxima_final

def formatar_impressao_matriz(matriz, titulo):
    """Função auxiliar para formatar e imprimir uma matriz."""
    print(f"\n{titulo}:")
    num_colunas = len(matriz[0])
    print(" " * 4 + " ".join(f"{i+1:>5}" for i in range(num_colunas)))
    print("----" + "-----" * num_colunas)
    for i, linha in enumerate(matriz):
        linha_formatada = [int(item) if item != INFINITO else 'inf' for item in linha]
        print(f"{i+1:<3}|" + " ".join(f"{item:>5}" for item in linha_formatada))
    print()

# --- Execução Principal ---
if __name__ == "__main__":
    # Garanta que o arquivo 'graph1.txt' está na mesma pasta que o script.
    caminho_arquivo_entrada = "graph1.txt"
    rede_metro = RedeDeMetro.carregar_de_arquivo(caminho_arquivo_entrada)

    if rede_metro:
        rede_metro.calcular_todas_rotas_floyd_warshall()
        (estacao_central, vetor_distancias, vertice_distante, dist_vert_dist) = rede_metro.encontrar_estacao_central()

        print("\n--- Resultado da Análise da Estação Central ---")
        print(f"\n1. Estação Central Escolhida: {estacao_central}")
        print(f"\n2. Vetor de Distâncias (da estação {estacao_central}):\n   {list(map(int, vetor_distancias))}")
        print(f"\n3. Vértice Mais Distante da Estação Central:\n   - Vértice: {vertice_distante}\n   - Distância: {int(dist_vert_dist)}")
        formatar_impressao_matriz(rede_metro.matriz_custos, "4. Matriz Final de Distâncias Mínimas")