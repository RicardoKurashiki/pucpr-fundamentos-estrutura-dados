from pyvis.network import Network


class GraphNode:
    def __init__(self, id: int, name: str, coord: tuple = (0, 0)):
        self.id = id
        self.name = name
        self.coord = coord


class GraphEdge:
    def __init__(self, id_1: int, id_2: int, weight: float):
        self.id_1 = id_1
        self.id_2 = id_2
        self.weight = weight


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        # Dicionários para acesso rápido, evitando buscas lineares
        self._nodes_map = {}

    def add_node(self, node_id: int, node_name: str, coord: tuple = (0, 0)):
        node = GraphNode(node_id, node_name, coord)
        self.nodes.append(node)
        self._nodes_map[node_id] = node

    def add_edge(self, node_id_1: int, node_id_2: int, edge_weight: float):
        self.edges.append(GraphEdge(node_id_1, node_id_2, edge_weight))

    def get_node(self, node_id: int) -> GraphNode:
        """Retorna o objeto do nó a partir de seu ID."""
        return self._nodes_map.get(node_id)

    def get_neighbors(self, node_id: int) -> list:
        """Retorna uma lista de IDs dos nós vizinhos."""
        neighbors = []
        for edge in self.edges:
            if edge.id_1 == node_id:
                neighbors.append(edge.id_2)
            elif edge.id_2 == node_id:
                neighbors.append(edge.id_1)
        return neighbors

    def get_edge_weight(self, node_id_1: int, node_id_2: int) -> float:
        """Retorna o peso da aresta entre dois nós."""
        for edge in self.edges:
            if (edge.id_1 == node_id_1 and edge.id_2 == node_id_2) or (
                edge.id_1 == node_id_2 and edge.id_2 == node_id_1
            ):
                return edge.weight
        return float("inf")  # Retorna infinito se não houver conexão direta

    def _generate_network(self, path: list = None):
        """
        Metodo auxiliar para gerar a rede Pyvis com base em um caminho opcional.
        Este metodo contém a lógica de layout geográfico (posicionamento relativo
        das coordenadas geográficas em pixels).
        """
        net = Network(height="1000px", width="100%", bgcolor="#222222", font_color="white", notebook=True,
                      cdn_resources='in_line')

        # Este bloco de opções desliga a suavização dinâmica das arestas e confirma
        # que toda a física está desativada, resultando em um grafo estático.
        options = """
        var options = {
          "edges": { "smooth": { "enabled": false } },
          "physics": { "enabled": false }
        }
        """
        net.set_options(options)

        # LÓGICA DE MAPEAMENTO GEOGRÁFICO
        # Para exibir nós com coordenadas geográficas (latitude, longitude) em uma tela 2D (pixels),
        # é necessário converter um sistema de coordenadas para outro. O metodo a seguir é uma
        # projeção linear simples, também conhecida como normalização.

        # 1. Encontrar a "caixa" (bounding box) que contém todos os nossos pontos geográficos.
        latitudes = [node.coord[0] for node in self.nodes]
        longitudes = [node.coord[1] for node in self.nodes]
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        # 2. Definir o tamanho do nosso "canvas" de destino onde o mapa será desenhado em pixels
        canvas_width = 1200
        canvas_height = 1000
        padding = 50  # Uma margem para que os nós não fiquem colados nas bordas.

        def scale_coords(lat, lon):
            """
            Converte uma coordenada geográfica (lat, lon) para uma coordenada de tela (x, y).
            """
            # 3. Normalização: Transforma a longitude em uma porcentagem (0 a 1) de sua posição
            #    dentro da largura geográfica total (max_lon - min_lon).
            #    Fórmula: (valor - mínimo) / (máximo - mínimo)
            percent_x = (lon - min_lon) / (max_lon - min_lon)

            # 4. Escalonamento: Multiplica a porcentagem pela largura do canvas para obter a posição em pixel.
            x = (percent_x * (canvas_width - 2 * padding)) + padding

            # 5. Repete o processo para a latitude (eixo Y).
            percent_y = (lat - min_lat) / (max_lat - min_lat)
            y = (percent_y * (canvas_height - 2 * padding)) + padding

            # 6. Inversão do Eixo Y: No sistema de coordenadas geográficas, a latitude cresce para o norte (para cima).
            #    Na maioria dos sistemas de tela, a coordenada Y cresce para baixo. Invertemos o Y
            #    para que o mapa tenha a orientação correta (Norte em cima, Sul embaixo).
            return x, canvas_height - y

        # --- ADIÇÃO DE NÓS E ARESTAS ---
        path_nodes = set(path) if path else set()
        path_edges = set()
        if path:
            for i in range(len(path) - 1):
                path_edges.add(tuple(sorted((path[i], path[i + 1]))))

        for node in self.nodes:
            scaled_x, scaled_y = scale_coords(node.coord[0], node.coord[1])
            color = "#FFD700" if node.id in path_nodes else "#97C2FC"
            size = 25 if node.id in path_nodes else 15
            net.add_node(node.id, node.name, x=scaled_x, y=scaled_y, physics=False, color=color, size=size)

        for edge in self.edges:
            edge_tuple = tuple(sorted((edge.id_1, edge.id_2)))
            color = "#00FF00" if edge_tuple in path_edges else "grey"
            width = 3 if edge_tuple in path_edges else 1
            net.add_edge(edge.id_1, edge.id_2, weight=edge.weight, color=color, width=width)

        return net

    def show_plain(self, filename: str = "net.html"):
        """ Função para montagem do grafo com parametrização padrão - motor de física ativado - ocorrem artefatos quando
            a densidade de arestas é muito grande (>3), pois o pyvis tenta posicionar os elementos de modo a não ter
            arestas sobrepostas, o que fica inviável em grafos mais densos
        """
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True,
                      cdn_resources='in_line')

        for node in self.nodes:
            # Transforma lat e lon em x e y
            # Coordenadas geográficas: (latitude, longitude)
            # Para o pyvis: x = longitude, y = -latitude (invertido para corrigir orientação)
            x = node.coord[1]  # longitude
            y = -node.coord[0]  # -latitude (invertido para sul ficar embaixo)
            net.add_node(node.id, node.name, x=x, y=y)
        for edge in self.edges:
            net.add_edge(
                edge.id_1,
                edge.id_2,
                weight=edge.weight,
                label=f"{edge.weight} km",
            )
        # net.show(filename) # Quebrou após incluir o parâmetro cdn_resources='in_line' na criação do objeto Network
        # Agora, em vez de net.show(), salvamos o arquivo manualmente com a codificação correta.
        with open(filename, "w", encoding="utf-8") as f:
            f.write(net.generate_html())

    def show(self, filename: str = "net.html"):
        net = self._generate_network()  # Gera a rede sem caminho destacado

        # Solução para o erro de codificação: escrita manual em UTF-8
        with open(filename, "w", encoding="utf-8") as f:
            f.write(net.generate_html())

    def show_path_plain(self, path: list, filename: str):
        """
        Gera uma visualização do grafo, destacando um caminho específico.
        :param path: Uma lista de IDs de nós representando o caminho.
        :param filename: O nome do arquivo HTML a ser salvo.
        """
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True,
                      cdn_resources='in_line')

        # Cores para o destaque
        path_node_color = "#FFD700"  # Dourado
        path_edge_color = "#00FF00"  # Verde brilhante

        # Converte o caminho em um conjunto de arestas para busca rápida
        path_edges = set()
        for i in range(len(path) - 1):
            # Adiciona a aresta de forma ordenada para facilitar a verificação
            edge_tuple = tuple(sorted((path[i], path[i + 1])))
            path_edges.add(edge_tuple)

        # Adiciona os nós, destacando os que estão no caminho
        for node in self.nodes:
            if node.id in path:
                net.add_node(node.id, node.name, color=path_node_color, size=25)
            else:
                net.add_node(node.id, node.name, color="#97C2FC")  # Cor padrão azul claro

        # Adiciona as arestas, destacando as que estão no caminho
        for edge in self.edges:
            edge_tuple = tuple(sorted((edge.id_1, edge.id_2)))
            if edge_tuple in path_edges:
                net.add_edge(
                    edge.id_1, edge.id_2, weight=edge.weight,
                    label=f"{edge.weight} km", color=path_edge_color, width=3
                )
            else:
                net.add_edge(
                    edge.id_1, edge.id_2, weight=edge.weight,
                    color="grey"
                )

        # net.show(filename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(net.generate_html())

    def show_path(self, path: list, filename: str):
        net = self._generate_network(path=path)  # Gera a rede COM caminho destacado

        # Solução definitiva para o erro de codificação
        with open(filename, "w", encoding="utf-8") as f:
            f.write(net.generate_html())