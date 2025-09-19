from geopy.distance import geodesic
from graph import Graph
from algorithms import dijkstra, greedy_search, a_star, depth_first_search, breadth_first_search


coords = {
    "Curitiba": {
        "id": 1,
        "coord": (-25.4284, -49.2733),
    },
    "Ponta Grossa": {
        "id": 2,
        "coord": (-25.095, -50.1619),
    },
    "Londrina": {
        "id": 3,
        "coord": (-23.3103, -51.1628),
    },
    "Maringa": {
        "id": 4,
        "coord": (-23.4205, -51.9331),
    },
    "Manoel Ribas": {
        "id": 5,
        "coord": (-24.5146, -51.6668),
    },
    "Cascavel": {
        "id": 6,
        "coord": (-24.9573, -53.459),
    },
    "São Mateus do Sul": {
        "id": 7,
        "coord": (-25.8687, -50.3841),
    },
    "Toledo": {
        "id": 8,
        "coord": (-24.7246, -53.7412),
    },
    "Araucária": {
        "id": 9,
        "coord": (-25.593, -49.4103),
    },
    "Foz do Iguaçú": {
        "id": 10,
        "coord": (-25.5469, -54.5882),
    },
}

roads = [
    ("Curitiba", "Araucária"),
    ("Curitiba", "Ponta Grossa"),
    ("Araucária", "Ponta Grossa"),
    ("Ponta Grossa", "São Mateus do Sul"),
    ("Ponta Grossa", "Manoel Ribas"),
    ("Manoel Ribas", "Maringa"),
    ("Maringa", "Londrina"),
    ("Maringa", "Cascavel"),
    ("Cascavel", "Toledo"),
    ("Toledo", "Foz do Iguaçú"),
]

def calculate_distance(coord1, coord2):
    return round(geodesic(coord1, coord2).km, 2)


def main():
    graph = Graph()
    # Mapeamento reverso de ID para Nome para facilitar a exibição
    id_to_name = {}
    for key, value in coords.items():
        graph.add_node(value["id"], key, value["coord"])
        id_to_name[value["id"]] = key

    for city1, city2 in roads:
        id1, id2 = coords[city1]["id"], coords[city2]["id"]
        dist = calculate_distance(coords[city1]["coord"], coords[city2]["coord"])
        graph.add_edge(id1, id2, dist)

    # Visualização do Grafo
    graph.show("parana_roads.html")
    print("Grafo de cidades do Paraná gerado em 'parana_roads.html'")

    # --- Execução e Comparação dos Algoritmos ---
    start_city = "Curitiba"
    goal_city = "Foz do Iguaçú"

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