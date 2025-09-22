from geopy.distance import geodesic
import os
import pandas as pd
import numpy as np
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
    "Vitória": {"id": 101, "coord": (-20.3194, -40.3378)},
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
    # Parâmetros
    ITERATIONS = 40  # Necessário para conseguir medir o tempo de execução da CPU, através da média dessas execuções. Uma única execução retorno 0.000 para a maioria dos algoritmos
    output_dir = "outputs"

    # Lista de desafios logísticos
    challenges = [
        {"name": "Norte_Sul", "origin": "Manaus", "destination": "Porto Alegre"},
        {"name": "Litoral", "origin": "Fortaleza", "destination": "Rio de Janeiro"},
        {"name": "Leste_Oeste", "origin": "Rio Branco", "destination": "João Pessoa"},
        {"name": "Centro_Sudeste", "origin": "Campo Grande", "destination": "Vitória"},
        {"name": "Vale_do_Paraiba", "origin": "São José dos Campos", "destination": "Niterói"},
    ]

    graph = Graph()
    # Mapeamento reverso de ID para Nome para facilitar a exibição
    id_to_name = {}
    for city, data in coords.items():
        graph.add_node(data["id"], city, data["coord"])
        id_to_name[data["id"]] = city

    build_road_network(graph, coords, neighbors_count=4)

    # Garante que existe a pasta de saída, caso ela não exista
    os.makedirs(output_dir, exist_ok=True)

    # Visualização do Grafo geral, apenas uma vez
    geral_map_filename = os.path.join(output_dir, "logistica_brasil_malha_completa.html")
    graph.show(geral_map_filename)
    print(f"Grafo da malha logística nacional gerado em '{geral_map_filename}'")

    all_challenges_summary = []  # Lista para acumular todos os resultados

    # Loop Principal sobre os Desafios
    for challenge in challenges:
        challenge_name = challenge["name"]
        start_city = challenge["origin"]
        goal_city = challenge["destination"]

        start_id = coords[start_city]["id"]
        goal_id = coords[goal_city]["id"]

        #print(f"\nBuscando a melhor rota de '{start_city}' para '{goal_city}'...")
        print(f"\n\n=======================================================================================")
        print(f"--- EXECUTANDO DESAFIO: {challenge_name} ({start_city} -> {goal_city}) ---")
        print(f"=======================================================================================")
        print(f"Cada algoritmo será executado {ITERATIONS} vezes para análise estatística.\n")

        algorithms_to_run = [
            dijkstra,
            a_star,
            greedy_search,
            breadth_first_search,
            depth_first_search
        ]

        # Estrutura para acumular os resultados
        aggregated_results = {func.__name__: {"cpu_times": [], "memory_peaks": []} for func in algorithms_to_run}
        # Armazena os resultados determinísticos da primeira execução
        deterministic_results = {}

        for i in range(ITERATIONS):
            print(f"   Executando rodada {i + 1}/{ITERATIONS}...")
            for algorithm_func in algorithms_to_run:
                result = algorithm_func(graph, start_id, goal_id)
                if result:
                    # Acumula as métricas de performance
                    aggregated_results[algorithm_func.__name__]["cpu_times"].append(result["cpu_time"])
                    aggregated_results[algorithm_func.__name__]["memory_peaks"].append(result["memory_peak_kb"])

                    # Na primeira rodada, salva os resultados que não mudam
                    if i == 0:
                        deterministic_results[algorithm_func.__name__] = result

        # Pós-processamento e Cálculo das Estatísticas
        summary_results = []
        for func in algorithms_to_run:
            algo_name = func.__name__
            if algo_name in deterministic_results:
                det_res = deterministic_results[algo_name]
                agg_res = aggregated_results[algo_name]

                # Calcula média e desvio padrão (stdev)
                mean_cpu = np.mean(agg_res["cpu_times"])
                stdev_cpu = np.std(agg_res["cpu_times"])

                mean_mem = np.mean(agg_res["memory_peaks"])
                stdev_mem = np.std(agg_res["memory_peaks"])

                # Adiciona o desafio atual ao dicionário de resultado
                summary = {
                    "algoritmo": det_res["name"],
                    "custo_km": det_res["cost"],
                    "nos_expandidos": det_res["nodes_expanded"],
                    "arestas_avaliadas": det_res["edges_evaluated"],
                    "caminho": det_res["path"],
                    "cpu_media": mean_cpu, "cpu_desvio_padrao": stdev_cpu,
                    "memoria_media_kib": mean_mem, "memoria_desvio_padrao": stdev_mem,
                }
                summary_results.append(summary)

                # Prepara os dados para o CSV final
                summary_for_csv = summary.copy()
                summary_for_csv["desafio"] = challenge_name
                summary_for_csv["origem"] = start_city
                summary_for_csv["destino"] = goal_city
                summary_for_csv["caminho_str"] = " -> ".join([id_to_name[i] for i in det_res['path']])
                del summary_for_csv["caminho"]  # Remove a lista de IDs do dicionário do CSV
                # Acumula os resultados na lista geral
                all_challenges_summary.append(summary_for_csv)

        # --- Apresentação dos Resultados ---
        print("\n--- Tabela Comparativa de Resultados ---\n")
        header = (
            f"{'Algoritmo':<15} | {'Custo (km)':<12} | {'Nós Expandidos':<16} | {'Arestas Avaliadas':<20} | "
            f"{'Pico Memória (μ ± σ KiB)':<28} | {'Tempo CPU (μ ± σ s)':<25} | {'Caminho Encontrado'}"
        )
        print(header)
        print("-" * (len(header)+10))
        # Ordena os resultados pelo custo para facilitar a comparação
        for res in sorted(summary_results, key=lambda x: x['custo_km']):
            path_names = " -> ".join([id_to_name[i] for i in res['caminho']])

            mem_stats_str = f"{res['memoria_media_kib']:.2f} ± {res['memoria_desvio_padrao']:.2f}"
            cpu_stats_str = f"{res['cpu_media']:.6f} ± {res['cpu_desvio_padrao']:.6f}"
            # Formatação da linha de resultado
            result_line = (
                f"{res['algoritmo']:<15} | {res['custo_km']:<12.2f} | {res['nos_expandidos']:<16} | {res['arestas_avaliadas']:<20} | "
                f"{mem_stats_str:<28} | {cpu_stats_str:<25} | {path_names}"
            )
            print(result_line)

            # Ajusta o nome do algoritmo para criar um nome de arquivo válido
            algo_filename = res['algoritmo'].replace(' ', '_').replace('*', 'Star')
            output_filename = os.path.join(output_dir, f"caminho_{challenge_name}_{algo_filename}.html")
            # Chama o metodo para gerar o arquivo HTML com o caminho destacado
            graph.show_path(res['caminho'], filename=output_filename)

        # --- Exportação Final para CSV ---
        if all_challenges_summary:
            print("\n\nExportando resultados consolidados para CSV...")
            df = pd.DataFrame(all_challenges_summary)

            # Reordena as colunas para melhor legibilidade
            column_order = [
                'desafio', 'origem', 'destino', 'algoritmo', 'custo_km', 'nos_expandidos',
                'arestas_avaliadas', 'cpu_media', 'cpu_desvio_padrao', 'memoria_media_kib',
                'memoria_desvio_padrao', 'caminho_str'
            ]
            df = df[column_order]

            csv_filename = os.path.join(output_dir, "analise_comparativa_algoritmos.csv")
            df.to_csv(csv_filename, index=False, decimal=',', sep=';')
            print(f"Resultados salvos com sucesso em '{csv_filename}'")


if __name__ == "__main__":
    main()