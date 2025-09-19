from pyvis.network import Network


class GraphNode:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class GraphEdge:
    def __init__(self, id_1: int, id_2: int, weight: float):
        self.id_1 = id_1
        self.id_2 = id_2
        self.weight = weight


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node_id: int, node_name: str):
        self.nodes.append(GraphNode(node_id, node_name))

    def add_edge(self, node_id_1: int, node_id_2: int, edge_weight: float):
        self.edges.append(GraphEdge(node_id_1, node_id_2, edge_weight))

    def show(self, filename: str = "net.html"):
        net = Network()
        for node in self.nodes:
            net.add_node(node.id, node.name)
        for edge in self.edges:
            net.add_edge(
                edge.id_1,
                edge.id_2,
                weight=edge.weight,
                label=f"{edge.weight} km",
            )
        net.save_graph(filename)
