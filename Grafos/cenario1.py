import sys

# Usamos um valor alto para representar a ausência de conexão direta (infinito).
INFINITO = float('inf')

class RedeDeMetro:
    """
    Representa a rede de metrô como um grafo, contendo as matrizes de
    distância e de próximos saltos para o roteamento.
    """
    def __init__(self, num_estacoes):
        self.num_estacoes = num_estacoes
        # Matriz para armazenar as distâncias mínimas (custos).
        self.matriz_custos = [[INFINITO] * num_estacoes for _ in range(num_estacoes)]
        # Matriz para reconstruir os caminhos (roteamento).
        self.proximo_no_no_caminho = [[None] * num_estacoes for _ in range(num_estacoes)]

        for i in range(num_estacoes):
            self.matriz_custos[i][i] = 0
            self.proximo_no_no_caminho[i][i] = i + 1

    def adicionar_trecho(self, estacao_a, estacao_b, custo):
        """ Adiciona uma conexão (aresta) não-direcionada entre duas estações. """
        idx_a, idx_b = estacao_a - 1, estacao_b - 1
        
        # Como o grafo é não-direcionado, a conexão vale para ambos os sentidos.
        self.matriz_custos[idx_a][idx_b] = custo
        self.proximo_no_no_caminho[idx_a][idx_b] = estacao_b

        self.matriz_custos[idx_b][idx_a] = custo
        self.proximo_no_no_caminho[idx_b][idx_a] = estacao_a

    @staticmethod
    def carregar_de_arquivo(caminho_arquivo):
        """
        Lê um arquivo de texto para criar e popular uma instância da RedeDeMetro.
        """
        try:
            with open(caminho_arquivo, 'r') as f:
                # A primeira linha contém o número de vértices e arestas.
                num_estacoes, num_trechos = map(int, f.readline().split())
                
                rede = RedeDeMetro(num_estacoes)

                for _ in range(num_trechos):
                    v1, v2, custo = map(int, f.readline().split())
                    rede.adicionar_trecho(v1, v2, custo)
            
            return rede
            
        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
            return None

    def calcular_todas_rotas(self):
        """
        Executa o algoritmo de Floyd-Warshall para encontrar os menores caminhos
        entre todos os pares de estações.
        """
        for k in range(self.num_estacoes):      # Nó pivô/intermediário
            for i in range(self.num_estacoes):  # Nó de origem
                for j in range(self.num_estacoes): # Nó de destino
                    # Verifica se o caminho passando por 'k' é mais curto.
                    custo_via_k = self.matriz_custos[i][k] + self.matriz_custos[k][j]
                    if custo_via_k < self.matriz_custos[i][j]:
                        self.matriz_custos[i][j] = custo_via_k
                        # Atualiza a rota: para ir de 'i' a 'j', o próximo passo é o mesmo que ir de 'i' a 'k'.
                        self.proximo_no_no_caminho[i][j] = self.proximo_no_no_caminho[i][k]

    def encontrar_estacao_central(self):
        """
        Analisa a matriz de custos para determinar a estação central baseada
        no somatório das distâncias e, como desempate, na menor distância máxima.
        """
        melhor_candidata = -1
        menor_soma_distancias = INFINITO
        menor_distancia_max = INFINITO

        for i in range(self.num_estacoes):
            soma_atual = sum(self.matriz_custos[i])
            dist_max_atual = max(self.matriz_custos[i])

            if soma_atual < menor_soma_distancias:
                menor_soma_distancias = soma_atual
                menor_distancia_max = dist_max_atual
                melhor_candidata = i
            elif soma_atual == menor_soma_distancias:
                # Critério de desempate: menor distância máxima.
                if dist_max_atual < menor_distancia_max:
                    menor_distancia_max = dist_max_atual
                    melhor_candidata = i
        
        if melhor_candidata == -1:
            return None, [], None, INFINITO

        estacao_central_id = melhor_candidata + 1
        vetor_distancias_central = self.matriz_custos[melhor_candidata]
        distancia_maxima_final = max(vetor_distancias_central)
        no_mais_distante = vetor_distancias_central.index(distancia_maxima_final) + 1
        
        return estacao_central_id, vetor_distancias_central, no_mais_distante, distancia_maxima_final

def formatar_impressao_matriz(matriz, titulo):
    """Função auxiliar para formatar e imprimir uma matriz de forma legível."""
    if not matriz:
        return f"\n{titulo}:\n<Matriz Vazia>\n"
    
    num_colunas = len(matriz[0])
    cabecalho = " " * 4 + " ".join(f"{i+1:>5}" for i in range(num_colunas))
    linhas_formatadas = [f"\n{titulo}:", cabecalho]

    for i, linha in enumerate(matriz):
        itens_linha = []
        for item in linha:
            if item == INFINITO:
                itens_linha.append("inf")
            elif isinstance(item, float):
                itens_linha.append(str(int(item)))
            else:
                itens_linha.append(str(item))
        
        linhas_formatadas.append(f"{i+1:<3}" + " ".join(f"{item:>5}" for item in itens_linha))
    
    return "\n".join(linhas_formatadas) + "\n"


if __name__ == "__main__":
    # Corrigindo a linha problemática do arquivo de entrada (8 10 com peso 13)
    # e unindo as duas partes do anexo.
    # O conteúdo do 'graph1.txt' deve ser:
    # 12 22
    # 1 2 17
    # 1 3 25
    # 1 5 21
    # 2 4 10
    # 2 6 15
    # 3 7 20
    # 4 6 9
    # 4 8 23
    # 5 6 12
    # 5 7 19
    # 6 8 8
    # 6 9 7
    # 7 9 17
    # 7 11 12
    # 7 12 22
    # 8 9 10
    # 8 10 13
    # 9 10 12
    # 9 11 15
    # 10 11 14
    # 10 12 21
    # 11 12 10
    
    caminho_arquivo_entrada = "graph1.txt"
    rede_metro = RedeDeMetro.carregar_de_arquivo(caminho_arquivo_entrada)

    if rede_metro:
        rede_metro.calcular_todas_rotas()
        
        (estacao_central, 
         vetor_distancias, 
         vertice_distante, 
         distancia_vertice_distante) = rede_metro.encontrar_estacao_central()

        # --- Apresentação dos Resultados ---
        print("\n--- Análise da Rede de Metrô ---")
        
        print(f"\n1. Estação Central Escolhida: {estacao_central}")
        print("   (Critério: Menor somatorio das distâncias a todos os outros vertices)")

        print(f"\n2. Vetor de Distâncias (da estação {estacao_central} para as demais):")
        # Formatando o vetor para melhor leitura
        vetor_formatado = [int(d) for d in vetor_distancias]
        print(f"   {vetor_formatado}")

        print("\n3. Vértice Mais Distante da Estação Central:")
        print(f"   - Vértice: {vertice_distante}")
        print(f"   - Distância: {int(distancia_vertice_distante)}")

        print(formatar_impressao_matriz(
            rede_metro.matriz_custos, 
            "4. Matriz de Distâncias Mínimas Entre Todos os Pares"
        ))