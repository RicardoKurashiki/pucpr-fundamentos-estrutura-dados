import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import itertools

# --- CONFIGURAÇÃO ---
OUTPUT_PATH = './outputs/'
CHARTS_PATH = os.path.join(OUTPUT_PATH, 'charts_analysis/')

# Mapeia os nomes dos arquivos para nomes amigáveis e cores consistentes
BASE_ALGORITHMS = {
    'linear_array': {'name': 'Array Linear', 'color': 'blue'},
    'regular_tree': {'name': 'Árvore Desbalanceada', 'color': 'red'},
    'avl_tree': {'name': 'Árvore Balanceada', 'color': 'green'}
}


# --- FUNÇÕES DE CARREGAMENTO E AGREGAÇÃO ---

def load_all_data(path, algorithms):
    """
    Carrega todos os arquivos CSV de resultados em um único DataFrame do Pandas.
    """
    all_dfs = []

    # Carrega as estruturas base (Array, Árvores)
    for key, props in algorithms.items():
        filename = os.path.join(path, f"{key}.csv")
        try:
            df = pd.read_csv(filename)
            df['Algorithm'] = props['name']
            all_dfs.append(df)
        except FileNotFoundError:
            print(f"Aviso: Arquivo '{filename}' não encontrado.")

    # Carrega e processa a Tabela Hash
    try:
        df_hash = pd.read_csv(os.path.join(path, 'hash_table.csv'))
        df_hash['Algorithm'] = 'Hash Table (M=' + df_hash['M parameter'].astype(str) + \
                               ', ' + df_hash['Hash Function'] + ')'
        all_dfs.append(df_hash)
    except FileNotFoundError:
        print("Aviso: Arquivo 'hash_table.csv' não encontrado.")

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)


def aggregate_data(df):
    """
    Agrupa os dados por algoritmo e tamanho, calculando a média e o desvio padrão
    APENAS para colunas numéricas, resolvendo o erro anterior.
    """
    grouping_cols = ['Algorithm', 'Size']

    # Seleciona apenas as colunas numéricas, excluindo as de agrupamento e iteração
    numeric_cols = df.select_dtypes(include=np.number).columns.drop(
        grouping_cols + ['Iteration'], errors='ignore'
    )

    aggregations = {col: ['mean', 'std'] for col in numeric_cols}

    agg_df = df.groupby(grouping_cols).agg(aggregations)

    agg_df.columns = ['_'.join(col).strip() for col in agg_df.columns.values]

    return agg_df.reset_index()


# --- FUNÇÃO DE PLOTAGEM ---

def plot_comparison(df_agg, metric_mean, metric_std, title, ylabel, algorithms_to_plot, use_log_scale=False):
    """
    Gera um gráfico comparativo com a média (linha) e o desvio padrão (área sombreada).
    """
    plt.figure(figsize=(14, 8))

    # Dicionário de cores para manter consistência
    color_map = {props['name']: props.get('color', None) for key, props in BASE_ALGORITHMS.items()}
    hash_colors = plt.cm.plasma(np.linspace(0.2, 0.8, len([a for a in algorithms_to_plot if 'Hash' in a])))
    hash_counter = 0

    linestyles = ['-', '--', ':', '-.'] * (len(algorithms_to_plot) // 4 + 1)

    for i, algo_name in enumerate(algorithms_to_plot):
        algo_df = df_agg[df_agg['Algorithm'] == algo_name]

        # Define a cor para o algoritmo atual
        color = color_map.get(algo_name)
        if color is None:
            color = hash_colors[hash_counter]
            hash_counter += 1

        if not algo_df.empty and metric_mean in algo_df.columns:
            sizes = algo_df['Size']
            means = algo_df[metric_mean]
            stds = algo_df[metric_std].fillna(0)

            plt.plot(sizes, means, marker='o', linestyle=linestyles[i], label=f'{algo_name}', color=color)
            plt.fill_between(sizes, means - stds, means + stds, color=color, alpha=0.1)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Tamanho do Dataset (N)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    if use_log_scale: plt.yscale('log')
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()

    os.makedirs(CHARTS_PATH, exist_ok=True)
    filename = os.path.join(CHARTS_PATH, f"{title.replace(' ', '_').replace('/', '')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo: {filename}")


# --- BLOCO PRINCIPAL DE EXECUÇÃO ---

if __name__ == "__main__":
    full_df = load_all_data(OUTPUT_PATH, BASE_ALGORITHMS)

    if full_df.empty:
        print("Nenhum dado encontrado para análise. Execute o script 'main.py' primeiro.")
    else:
        aggregated_df = aggregate_data(full_df)

        print("--- Tabela de Médias e Desvios Padrão ---")
        pd.set_option('display.max_rows', 100)
        print(aggregated_df.to_string())
        aggregated_df.to_csv(f"{OUTPUT_PATH}/experiment_df.csv")

        print("\n--- Gerando Gráficos de Análise ---")

        # --- LÓGICA PARA COMPARAÇÃO GERAL ---
        general_comparison_algos = [
            BASE_ALGORITHMS['linear_array']['name'],
            BASE_ALGORITHMS['regular_tree']['name'],
            BASE_ALGORITHMS['avl_tree']['name'],
        ]

        # Filtra os resultados da Hash Table para N=1,000,000
        hash_results_for_best = aggregated_df[
            (aggregated_df['Algorithm'].str.contains('Hash Table')) &
            (aggregated_df['Size'] == 500000)
            ]

        # Se encontrou resultados, identifica a melhor e a adiciona para a comparação geral
        if not hash_results_for_best.empty:
            best_hash_config = hash_results_for_best.sort_values('Search CPU Time (s)_mean').iloc[0]['Algorithm']
            general_comparison_algos.append(best_hash_config)
            print(f"\nMelhor configuração da Tabela Hash identificada para comparação: {best_hash_config}\n")
        else:
            print(
                "\nAviso: Não foram encontrados resultados para a Tabela Hash com N=1,000,000 para determinar a melhor configuração.")

        # Gera os gráficos de comparação geral incluindo a melhor Hash Table
        plot_comparison(aggregated_df, 'Insertion CPU Time (s)_mean', 'Insertion CPU Time (s)_std',
                        'Geral - Custo de Construção (CPU Time)', 'CPU Time (s)', general_comparison_algos)
        plot_comparison(aggregated_df, 'Search CPU Time (s)_mean', 'Search CPU Time (s)_std',
                        'Geral - Custo de Busca (CPU Time)', 'CPU Time (s)', general_comparison_algos,
                        use_log_scale=True)
        plot_comparison(aggregated_df, 'Memory Usage (Peak Bytes)_mean', 'Memory Usage (Peak Bytes)_std',
                        'Geral - Uso de Memória', 'Memória (Bytes)', general_comparison_algos)

        plot_comparison(aggregated_df, 'Average Search Steps_mean', 'Average Search Steps_std',
                        'Geral - Eficiência de Busca (Passos)', 'Nº Médio de Passos', general_comparison_algos,
                        use_log_scale=True)
        plot_comparison(aggregated_df, 'Total Insertion Steps_mean', 'Total Insertion Steps_std',
                        'Geral - Eficiência de Inserção (Passos)', 'Nº Médio de Passos', general_comparison_algos,
                        use_log_scale=True)

        # --- GRÁFICOS ESPECÍFICOS DAS TABELAS HASH (Comparando todas as configurações) ---
        hash_configs = sorted(
            aggregated_df[aggregated_df['Algorithm'].str.contains('Hash Table')]['Algorithm'].unique())

        if hash_configs:
            # Garante que as colunas existem antes de tentar plotar
            if 'Total Collisions_mean' in aggregated_df.columns:
                plot_comparison(aggregated_df, 'Total Collisions_mean', 'Total Collisions_std',
                                'Hash Tables - Análise de Colisões', 'Nº Total de Colisões (log)', hash_configs,
                                use_log_scale=True)
            if 'Max Bucket Size_mean' in aggregated_df.columns:
                plot_comparison(aggregated_df, 'Max Bucket Size_mean', 'Max Bucket Size_std',
                                'Hash Tables - Pior Caso (Tamanho Máx. do Bucket)', 'Tamanho Máximo', hash_configs,
                                use_log_scale=True)
            if 'Load Factor_mean' in aggregated_df.columns:
                plot_comparison(aggregated_df, 'Load Factor_mean', 'Load Factor_std',
                                'Hash Tables - Análise do Fator de Carga', 'Fator de Carga (N/M)', hash_configs)


        print("\nAnálise concluída!")