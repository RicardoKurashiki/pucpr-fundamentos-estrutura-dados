import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import itertools  # Para gerar combinações de cores

# --- CONFIGURAÇÃO ---
OUTPUT_PATH = './outputs/'
CHARTS_PATH = os.path.join(OUTPUT_PATH, 'charts_analysis/')

# Mapeia os nomes dos arquivos para nomes amigáveis e cores
BASE_ALGORITHMS = {
    'linear_array': {'name': 'Array Linear', 'color': 'blue'},
    'regular_tree': {'name': 'Árvore Desbalanceada', 'color': 'red'},
    'avl_tree': {'name': 'Árvore Balanceada', 'color': 'green'}
}


# --- FUNÇÕES DE ANÁLISE E PLOTAGEM ---

def load_all_data(path, algorithms):
    """
    Carrega todos os arquivos CSV de resultados, tratando a Tabela Hash de forma especial.
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
        # Cria uma coluna de "Algoritmo" descritiva para cada configuração
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
    Agrupa os dados por algoritmo e tamanho, calculando a média e o desvio padrão.
    """
    metric_columns = df.columns.drop(['Size', 'Iteration', 'Algorithm', 'M parameter', 'Hash Function'],
                                     errors='ignore')
    aggregations = {col: ['mean', 'std'] for col in metric_columns}
    agg_df = df.groupby(['Algorithm', 'Size']).agg(aggregations)
    agg_df.columns = ['_'.join(col).strip() for col in agg_df.columns.values]
    return agg_df.reset_index()


def plot_comparison(df_agg, metric_mean, metric_std, title, ylabel, algorithms_to_plot, use_log_scale=False):
    """
    Gera um gráfico comparativo com a média (linha) e o desvio padrão (área sombreada).
    """
    plt.figure(figsize=(12, 7))

    # Gerador de cores para garantir que cada algoritmo tenha uma cor única
    colors = plt.cm.viridis(np.linspace(0, 1, len(algorithms_to_plot)))
    color_map = {name: color for name, color in zip(algorithms_to_plot, colors)}

    for algo_name in algorithms_to_plot:
        algo_df = df_agg[df_agg['Algorithm'] == algo_name]
        if not algo_df.empty:
            sizes = algo_df['Size']
            means = algo_df[metric_mean]
            stds = algo_df[metric_std].fillna(0)  # Preenche std nulo com 0 para evitar erros

            plt.plot(sizes, means, marker='o', linestyle='-', label=f'{algo_name} (Média)', color=color_map[algo_name])
            plt.fill_between(sizes, means - stds, means + stds, color=color_map[algo_name], alpha=0.15)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Tamanho do Dataset (N)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    if use_log_scale:
        plt.yscale('log')
        plt.grid(True, which="both", ls="--", alpha=0.4)
    else:
        plt.grid(True, alpha=0.4)

    plt.legend(fontsize=10)
    plt.tight_layout()

    os.makedirs(CHARTS_PATH, exist_ok=True)
    filename = os.path.join(CHARTS_PATH, f"{title.replace(' ', '_')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo: {filename}")


# --- BLOCO PRINCIPAL DE EXECUÇÃO ---

if __name__ == "__main__":
    full_df = load_all_data(OUTPUT_PATH, BASE_ALGORITHMS)

    if full_df.empty:
        print("Nenhum dado encontrado para análise.")
    else:
        aggregated_df = aggregate_data(full_df)

        print("--- Tabela de Médias e Desvios Padrão ---")
        pd.set_option('display.max_rows', None)
        print(aggregated_df)

        print("\n--- Gerando Gráficos de Análise ---")

        # Identifica a melhor configuração da Hash Table (menor tempo de busca para N=1M)
        best_hash_config = aggregated_df[
            (aggregated_df['Algorithm'].str.contains('Hash Table')) &
            (aggregated_df['Size'] == 1000000)
            ].sort_values('Search CPU Time (s)_mean').iloc[0]['Algorithm']
        print(f"Melhor configuração da Tabela Hash identificada: {best_hash_config}")

        # Lista de algoritmos para a comparação geral
        general_comparison_algos = [
            BASE_ALGORITHMS['linear_array']['name'],
            BASE_ALGORITHMS['regular_tree']['name'],
            BASE_ALGORITHMS['avl_tree']['name'],
            best_hash_config
        ]

        # Gráficos de Comparação Geral
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

        # Gráficos de Comparação Específica das Tabelas Hash
        hash_configs = aggregated_df[aggregated_df['Algorithm'].str.contains('Hash Table')]['Algorithm'].unique()
        plot_comparison(aggregated_df, 'Insertion CPU Time (s)_mean', 'Insertion CPU Time (s)_std',
                        'Hash Tables - Custo de Construção', 'CPU Time (s)', hash_configs)
        plot_comparison(aggregated_df, 'Search CPU Time (s)_mean', 'Search CPU Time (s)_std',
                        'Hash Tables - Custo de Busca', 'CPU Time (s)', hash_configs, use_log_scale=True)
        plot_comparison(aggregated_df, 'Average Search Steps_mean', 'Average Search Steps_std',
                        'Hash Tables - Eficiência de Busca (Passos)', 'Nº Médio de Passos', hash_configs,
                        use_log_scale=True)

        print("\nAnálise concluída!")