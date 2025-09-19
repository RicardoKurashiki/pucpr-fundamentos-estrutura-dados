from geopy.distance import geodesic
from graph import Graph
from algorithms import dijkstra, greedy_search, a_star, depth_first_search, breadth_first_search

# --- Cenário: Malha Logística Sul-Sudeste do Brasil ---
# Um grafo com 15 cidades importantes para a logística de transportes.

coords = {
    # Sudeste
    "São Paulo":      {"id": 1, "coord": (-23.5505, -46.6333)},
    "Rio de Janeiro": {"id": 2, "coord": (-22.9068, -43.1729)},
    "Belo Horizonte": {"id": 3, "coord": (-19.9167, -43.9345)},
    "Vitória":        {"id": 4, "coord": (-20.3194, -40.3378)},
    "Campinas":       {"id": 5, "coord": (-22.9099, -47.0626)},
    "Santos":         {"id": 6, "coord": (-23.9608, -46.3331)},
    "Ribeirão Preto": {"id": 7, "coord": (-21.1767, -47.8103)},
    "Uberlândia":     {"id": 8, "coord": (-18.9186, -48.2772)},
    # Sul
    "Curitiba":       {"id": 9, "coord": (-25.4284, -49.2733)},
    "Florianópolis":  {"id": 10, "coord": (-27.5954, -48.5480)},
    "Porto Alegre":   {"id": 11, "coord": (-30.0346, -51.2177)},
    "Joinville":      {"id": 12, "coord": (-26.3031, -48.8456)},
    "Londrina":       {"id": 13, "coord": (-23.3103, -51.1628)},
    "Cascavel":       {"id": 14, "coord": (-24.9573, -53.4590)},
    "Caxias do Sul":  {"id": 15, "coord": (-29.1678, -51.1789)},
}

# Principais conexões rodoviárias (arestas do grafo)
roads = [
    # Conexões em SP e arredores
    ("São Paulo", "Santos"),
    ("São Paulo", "Campinas"),
    ("São Paulo", "Curitiba"),
    ("São Paulo", "Rio de Janeiro"),
    ("Campinas", "Ribeirão Preto"),
    ("Ribeirão Preto", "Uberlândia"),
    # Conexões Eixo Sudeste
    ("São Paulo", "Belo Horizonte"),
    ("Rio de Janeiro", "Belo Horizonte"),
    ("Rio de Janeiro", "Vitória"),
    ("Belo Horizonte", "Vitória"),
    ("Belo Horizonte", "Uberlândia"),
    # Conexões para o Sul
    ("Curitiba", "Joinville"),
    ("Curitiba", "Londrina"),
    ("Londrina", "Cascavel"),
    ("Joinville", "Florianópolis"),
    ("Florianópolis", "Porto Alegre"),
    ("Porto Alegre", "Caxias do Sul"),
]
def calculate_distance(coord1, coord2):
    return round(geodesic(coord1, coord2).km, 2)


def main():
    graph = Graph()
    # Mapeamento reverso de ID para Nome para facilitar a exibição
    id_to_name = {}
    for city, data in coords.items():
        graph.add_node(data["id"], city, data["coord"])
        id_to_name[data["id"]] = city

    for city1, city2 in roads:
        id1, id2 = coords[city1]["id"], coords[city2]["id"]
        dist = calculate_distance(coords[city1]["coord"], coords[city2]["coord"])
        graph.add_edge(id1, id2, dist)

    # Visualização do Grafo
    graph.show("logistica_sul_sudeste.html")
    print("Grafo da malha logística gerado em 'logistica_sul_sudeste.html'")

    # Primeiro Desafio Logístico
    start_city = "Santos"
    goal_city = "Caxias do Sul"

    start_id = coords[start_city]["id"]
    goal_id = coords[goal_city]["id"]

    print(f"\nBuscando o caminho de '{start_city}' para '{goal_city}'...")

    algorithms_to_run = [
        dijkstra,
        a_star,
        greedy_search,
        breadth_first_search,
        depth_first_search
    ]

    results = []
    for algorithm_func in algorithms_to_run:
        result = algorithm_func(graph, start_id, goal_id)
        if result:
            results.append(result)

    # --- Apresentação dos Resultados ---
    print("\n--- Tabela Comparativa de Resultados ---\n")
    header = (
        f"{'Algoritmo':<15} | {'Custo (km)':<12} | {'Nós Expandidos':<16} | "
        f"{'Pico Memória (KiB)':<20} | {'Tempo CPU (s)':<15} | {'Caminho Encontrado'}"
    )
    print(header)
    print("-" * len(header))
    # Ordena os resultados pelo custo para facilitar a comparação
    for res in sorted(results, key=lambda x: x['cost']):
        path_names = " -> ".join([id_to_name[i] for i in res['path']])

        # Formatação da linha de resultado
        result_line = (
            f"{res['name']:<15} | {res['cost']:<12.2f} | {res['nodes_expanded']:<16} | "
            f"{res['memory_peak_kb']:<20.2f} | {res['cpu_time']:<15.6f} | {path_names}"
        )
        print(result_line)

if __name__ == "__main__":
    main()