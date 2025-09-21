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

    def show(self, filename: str = "net.html"):
        net = Network(
            height="95vh", width="100%", bgcolor="#222222", font_color="white"
        )
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
        net.save_graph(filename)
