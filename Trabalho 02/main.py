from geopy.distance import geodesic
from graph import Graph
from algorithms import dijkstra, greedy_search, a_star, depth_first_search, breadth_first_search

# --- Cenário: Malha Logística Nacional - 100 Maiores Cidades do Brasil ---

coords = {
    "São Paulo": {"id": 1, "coord": (-23.5505, -46.6333)},
    "Rio de Janeiro": {"id": 2, "coord": (-22.9068, -43.1729)},
    "Brasília": {"id": 3, "coord": (-15.7801, -47.9292)},
    "Salvador": {"id": 4, "coord": (-12.9777, -38.5016)},
    "Fortaleza": {"id": 5, "coord": (-3.7319, -38.5267)},
    "Belo Horizonte": {"id": 6, "coord": (-19.9167, -43.9345)},
    "Manaus": {"id": 7, "coord": (-3.1190, -60.0217)},
    "Curitiba": {"id": 8, "coord": (-25.4284, -49.2733)},
    "Recife": {"id": 9, "coord": (-8.0476, -34.8770)},
    "Goiânia": {"id": 10, "coord": (-16.6869, -49.2648)},
    "Porto Alegre": {"id": 11, "coord": (-30.0346, -51.2177)},
    "Belém": {"id": 12, "coord": (-1.4558, -48.5044)},
    "Guarulhos": {"id": 13, "coord": (-23.4536, -46.5333)},
    "Campinas": {"id": 14, "coord": (-22.9099, -47.0626)},
    "São Luís": {"id": 15, "coord": (-2.5307, -44.3068)},
    "São Gonçalo": {"id": 16, "coord": (-22.8275, -43.0528)},
    "Maceió": {"id": 17, "coord": (-9.6653, -35.7351)},
    "Duque de Caxias": {"id": 18, "coord": (-22.7858, -43.3114)},
    "Campo Grande": {"id": 19, "coord": (-20.4697, -54.6201)},
    "Natal": {"id": 20, "coord": (-5.7945, -35.2110)},
    "Teresina": {"id": 21, "coord": (-5.0919, -42.8034)},
    "São Bernardo do Campo": {"id": 22, "coord": (-23.6944, -46.5653)},
    "Nova Iguaçu": {"id": 23, "coord": (-22.7594, -43.4514)},
    "João Pessoa": {"id": 24, "coord": (-7.1195, -34.8450)},
    "Santo André": {"id": 25, "coord": (-23.6608, -46.5367)},
    "São José dos Campos": {"id": 26, "coord": (-23.1791, -45.8872)},
    "Jaboatão dos Guararapes": {"id": 27, "coord": (-8.1139, -35.0153)},
    "Osasco": {"id": 28, "coord": (-23.5325, -46.7917)},
    "Ribeirão Preto": {"id": 29, "coord": (-21.1767, -47.8103)},
    "Uberlândia": {"id": 30, "coord": (-18.9186, -48.2772)},
    "Sorocaba": {"id": 31, "coord": (-23.5019, -47.4581)},
    "Contagem": {"id": 32, "coord": (-19.9181, -44.0542)},
    "Aracaju": {"id": 33, "coord": (-10.9111, -37.0717)},
    "Feira de Santana": {"id": 34, "coord": (-12.2669, -38.9669)},
    "Cuiabá": {"id": 35, "coord": (-15.6014, -56.0977)},
    "Joinville": {"id": 36, "coord": (-26.3031, -48.8456)},
    "Juiz de Fora": {"id": 37, "coord": (-21.7642, -43.3497)},
    "Londrina": {"id": 38, "coord": (-23.3103, -51.1628)},
    "Aparecida de Goiânia": {"id": 39, "coord": (-16.8225, -49.2461)},
    "Ananindeua": {"id": 40, "coord": (-1.3650, -48.3717)},
    "Porto Velho": {"id": 41, "coord": (-8.7619, -63.9039)},
    "Niterói": {"id": 42, "coord": (-22.8833, -43.1036)},
    "Campos dos Goytacazes": {"id": 43, "coord": (-21.7522, -41.3256)},
    "Belford Roxo": {"id": 44, "coord": (-22.7642, -43.3986)},
    "Serra": {"id": 45, "coord": (-20.1281, -40.3078)},
    "Caxias do Sul": {"id": 46, "coord": (-29.1678, -51.1789)},
    "Vila Velha": {"id": 47, "coord": (-20.3422, -40.2919)},
    "Florianópolis": {"id": 48, "coord": (-27.5954, -48.5480)},
    "São João de Meriti": {"id": 49, "coord": (-22.8050, -43.3717)},
    "Mauá": {"id": 50, "coord": (-23.6678, -46.4614)},
    "Macapá": {"id": 51, "coord": (0.0389, -51.0664)},
    "São José do Rio Preto": {"id": 52, "coord": (-20.8197, -49.3792)},
    "Santos": {"id": 53, "coord": (-23.9608, -46.3331)},
    "Mogi das Cruzes": {"id": 54, "coord": (-23.5236, -46.1883)},
    "Diadema": {"id": 55, "coord": (-23.6864, -46.6225)},
    "Betim": {"id": 56, "coord": (-19.9675, -44.1983)},
    "Campina Grande": {"id": 57, "coord": (-7.2306, -35.8811)},
    "Jundiaí": {"id": 58, "coord": (-23.1869, -46.8856)},
    "Olinda": {"id": 59, "coord": (-8.0089, -34.8553)},
    "Carapicuíba": {"id": 60, "coord": (-23.5239, -46.8358)},
    "Piracicaba": {"id": 61, "coord": (-22.7253, -47.6492)},
    "Montes Claros": {"id": 62, "coord": (-16.7350, -43.8644)},
    "Bauru": {"id": 63, "coord": (-22.3147, -49.0606)},
    "Rio Branco": {"id": 64, "coord": (-9.9749, -67.8100)},
    "São Vicente": {"id": 65, "coord": (-23.9631, -46.3919)},
    "Pelotas": {"id": 66, "coord": (-31.7719, -52.3425)},
    "Canoas": {"id": 67, "coord": (-29.9178, -51.1831)},
    "Maringá": {"id": 68, "coord": (-23.4253, -51.9389)},
    "Anápolis": {"id": 69, "coord": (-16.3267, -48.9528)},
    "Vitória da Conquista": {"id": 70, "coord": (-14.8661, -40.8394)},
    "Caucaia": {"id": 71, "coord": (-3.7381, -38.6575)},
    "Petrópolis": {"id": 72, "coord": (-22.5053, -43.1786)},
    "Itaquaquecetuba": {"id": 73, "coord": (-23.4864, -46.3486)},
    "Ponta Grossa": {"id": 74, "coord": (-25.0950, -50.1619)},
    "Franca": {"id": 75, "coord": (-20.5386, -47.4008)},
    "Caruaru": {"id": 76, "coord": (-8.2828, -35.9761)},
    "Foz do Iguaçu": {"id": 77, "coord": (-25.5469, -54.5882)},
    "Paulista": {"id": 78, "coord": (-7.9406, -34.8728)},
    "Uberaba": {"id": 79, "coord": (-19.7483, -47.9319)},
    "Guarujá": {"id": 80, "coord": (-23.9939, -46.2561)},
    "Blumenau": {"id": 81, "coord": (-26.9194, -49.0661)},
    "Cascavel": {"id": 82, "coord": (-24.9573, -53.4590)},
    "Petrolina": {"id": 83, "coord": (-9.3992, -40.5008)},
    "Suzano": {"id": 84, "coord": (-23.5433, -46.3106)},
    "Limeira": {"id": 85, "coord": (-22.5647, -47.4019)},
    "Boa Vista": {"id": 86, "coord": (2.8235, -60.6753)},
    "Santarém": {"id": 87, "coord": (-2.4431, -54.7083)},
    "Taubaté": {"id": 88, "coord": (-23.0264, -45.5556)},
    "Barueri": {"id": 89, "coord": (-23.5106, -46.8761)},
    "Governador Valadares": {"id": 90, "coord": (-18.8508, -41.9492)},
    "Volta Redonda": {"id": 91, "coord": (-22.5222, -44.1039)},
    "Santa Maria": {"id": 92, "coord": (-29.6842, -53.8069)},
    "Gravataí": {"id": 93, "coord": (-29.9442, -50.9931)},
    "Viamão": {"id": 94, "coord": (-30.0811, -51.0233)},
    "Imperatriz": {"id": 95, "coord": (-5.5261, -47.4756)},
    "Novo Hamburgo": {"id": 96, "coord": (-29.6875, -51.1319)},
    "Várzea Grande": {"id": 97, "coord": (-15.6469, -56.1333)},
    "Ipatinga": {"id": 98, "coord": (-19.4678, -42.5281)},
    "Juazeiro do Norte": {"id": 99, "coord": (-7.2128, -39.3158)},
    "Palmas": {"id": 100, "coord": (-10.1844, -48.3336)},
}

def calculate_distance(coord1, coord2):
    return round(geodesic(coord1, coord2).km, 2)


def build_road_network(graph, coords_dict, neighbors_count=4):
    """
    Constrói a malha rodoviária conectando cada cidade às suas N vizinhas mais próximas.
    """
    city_names = list(coords_dict.keys())

    # Usamos um set para evitar adicionar arestas duplicadas (A->B e B->A com o mesmo peso)
    existing_edges = set()

    for city1_name in city_names:
        distances = []
        for city2_name in city_names:
            if city1_name != city2_name:
                coord1 = coords_dict[city1_name]["coord"]
                coord2 = coords_dict[city2_name]["coord"]
                dist = calculate_distance(coord1, coord2)
                distances.append((dist, city2_name))

        distances.sort()

        for i in range(min(neighbors_count, len(distances))):
            dist, neighbor_name = distances[i]
            id1 = coords_dict[city1_name]["id"]
            id2 = coords_dict[neighbor_name]["id"]

            # Garante que a aresta seja armazenada de forma consistente (menor_id, maior_id)
            edge_tuple = tuple(sorted((id1, id2)))

            if edge_tuple not in existing_edges:
                graph.add_edge(id1, id2, round(dist, 2))
                existing_edges.add(edge_tuple)

def main():
    graph = Graph()
    # Mapeamento reverso de ID para Nome para facilitar a exibição
    id_to_name = {}
    for city, data in coords.items():
        graph.add_node(data["id"], city, data["coord"])
        id_to_name[data["id"]] = city

    build_road_network(graph, coords, neighbors_count=3)

    # Visualização do Grafo
    graph.show("logistica_brasil.html")
    print("Grafo da malha logística nacional gerado em 'logistica_brasil.html'")

    # Primeiro Desafio Logístico
    start_city = "Manaus"
    goal_city = "Curitiba"

    start_id = coords[start_city]["id"]
    goal_id = coords[goal_city]["id"]

    print(f"\nBuscando a melhor rota de '{start_city}' para '{goal_city}'...")

    algorithms_to_run = [
        dijkstra,
        a_star,
        greedy_search,
        breadth_first_search,
        depth_first_search
    ]

    results = []
    iterations = 40 # Necessário para conseguir medir o tempo de execução da CPU, através da média dessas execuções. Uma única execução retorno 0.000 para a maioria dos algoritmos
    for algorithm_func in algorithms_to_run:
        cpu_total_time = 0
        for i in range(iterations):
            result = algorithm_func(graph, start_id, goal_id)
            if result:
                cpu_total_time += result['cpu_time']
        if result:
            result['cpu_time'] = cpu_total_time/iterations
            results.append(result)

    # --- Apresentação dos Resultados ---
    print("\n--- Tabela Comparativa de Resultados ---\n")
    header = (
        f"{'Algoritmo':<15} | {'Custo (km)':<12} | {'Nós Expandidos':<16} | {'Arestas Avaliadas':<20} | "
        f"{'Pico Memória (KiB)':<20} | {'Tempo CPU (s)':<15} | {'Caminho Encontrado'}"
    )
    print(header)
    print("-" * len(header))
    # Ordena os resultados pelo custo para facilitar a comparação
    for res in sorted(results, key=lambda x: x['cost']):
        path_names = " -> ".join([id_to_name[i] for i in res['path']])

        # Formatação da linha de resultado
        result_line = (
            f"{res['name']:<15} | {res['cost']:<12.2f} | {res['nodes_expanded']:<16} | {res['edges_evaluated']:<20} | "
            f"{res['memory_peak_kb']:<20.2f} | {res['cpu_time']:<15.9f} | {path_names}"
        )
        print(result_line)

if __name__ == "__main__":
    main()