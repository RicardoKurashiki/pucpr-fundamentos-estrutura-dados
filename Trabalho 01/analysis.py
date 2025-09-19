import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import itertools

# CONFIGURAÇÃO INICIAL
OUTPUT_PATH = './outputs/'
CHARTS_PATH = os.path.join(OUTPUT_PATH, 'charts_analysis/')

# Mapeia os nomes dos arquivos para nomes amigáveis e cores consistentes
BASE_ALGORITHMS = {
    'linear_array': {'name': 'Array Linear', 'color': 'blue'},
    'regular_tree': {'name': 'Árvore Desbalanceada', 'color': 'red'},
    'avl_tree': {'name': 'Árvore Balanceada', 'color': 'green'}
}


# FUNÇÕES DE CARREGAMENTO E AGREGAÇÃO

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

# FUNÇÕES DE PLOTAGEM

def plot_distribution_boxplots(path):
    """
    Carrega os dados de distribuição e plota um boxplot comparativo.
    """
    try:
        df_dist = pd.read_csv(os.path.join(path, 'hash_distribution.csv'))
    except FileNotFoundError:
        print("Aviso: Arquivo 'hash_distribution.csv' não encontrado. Pulando boxplots.")
        return

    # Gera um gráfico para cada combinação de N e M
    for (size, m_param), group in df_dist.groupby(['Size', 'M parameter']):
        plt.figure(figsize=(12, 8))

        # O truque é "descomprimir" os dados de frequência para o boxplot
        # Ex: Se 'Bucket Size' 2 tem 'Frequency' 10, criamos [2, 2, ..., 2] dez vezes
        data_to_plot = []
        labels = []
        # Agrupa por função de hash para criar um boxplot para cada uma
        for func_name, func_group in group.groupby('Hash Function'):
            # np.repeat repete cada 'Bucket Size' pelo número de vezes em 'Frequency'
            # Isso recria a distribuição original dos tamanhos dos buckets
            reconstructed_data = np.repeat(func_group['Bucket Size'], func_group['Frequency'].astype(int))
            data_to_plot.append(reconstructed_data)
            labels.append(func_name)

        plt.boxplot(data_to_plot, labels=labels, patch_artist=True, showmeans=True)

        plt.title(f'Distribuição do Tamanho dos Buckets (N={int(size / 1000)}k, M={m_param})', fontsize=16)
        plt.ylabel('Tamanho do Bucket (Nº de Itens)', fontsize=12)
        plt.xlabel('Função de Hash', fontsize=12)
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)

        filename = os.path.join(CHARTS_PATH, f"Boxplot_Distribution_N{size}_M{m_param}.png")
        plt.savefig(filename)
        plt.close()
        print(f"Boxplot salvo: {filename}")

def plot_distribution_histograms(path, algorithms_to_plot):
    """
    Carrega os dados de distribuição e plota um histograma comparativo.
    """
    try:
        df_dist = pd.read_csv(os.path.join(path, 'hash_distribution.csv'))
    except FileNotFoundError:
        print("Aviso: Arquivo 'hash_distribution.csv' não encontrado. Pulando histogramas.")
        return

    # Agrega os dados de frequência (tira a média das 5 iterações)
    agg_dist = df_dist.groupby(['Size', 'M parameter', 'Hash Function', 'Bucket Size']).mean().reset_index()

    # Gera um gráfico para cada combinação de N e M
    for (size, m_param), group in agg_dist.groupby(['Size', 'M parameter']):
        plt.figure(figsize=(15, 8))

        colors = plt.cm.viridis(np.linspace(0, 1, len(group['Hash Function'].unique())))

        for i, func_name in enumerate(sorted(group['Hash Function'].unique())):
            func_df = group[group['Hash Function'] == func_name]

            # Encontra o desvio padrão correspondente nos dados principais para a legenda
            std_dev_row = algorithms_to_plot[
                (algorithms_to_plot['Algorithm'].str.contains(f"M={m_param}, {func_name}")) &
                (algorithms_to_plot['Size'] == size)
                ]
            std_dev = std_dev_row['Std Dev of Bucket Lengths_mean'].iloc[0] if not std_dev_row.empty else 0

            plt.plot(func_df['Bucket Size'], func_df['Frequency'], marker='o', linestyle='-',
                     label=f'{func_name} (StdDev: {std_dev:.2f})', color=colors[i], alpha=0.7)

        plt.title(f'Distribuição do Tamanho dos Buckets (N={int(size / 1000)}k, M={m_param})', fontsize=16)
        plt.xlabel('Tamanho do Bucket (Nº de Itens)', fontsize=12)
        plt.ylabel('Frequência Média (Nº de Buckets)', fontsize=12)
        plt.legend()
        plt.grid(True, which="both", ls="--", alpha=0.4)
        plt.yscale('log')
        plt.xscale('log')  # Escala de log no X também ajuda a ver a cauda da distribuição

        filename = os.path.join(CHARTS_PATH, f"Histogram_N{size}_M{m_param}.png")
        plt.savefig(filename)
        plt.close()
        print(f"Histograma salvo: {filename}")


def plot_distribution_boxplots_grid(path):
    """
    Carrega os dados de distribuição e plota uma grade de boxplots comparativos.
    """
    try:
        df_dist = pd.read_csv(os.path.join(path, 'hash_distribution.csv'))
    except FileNotFoundError:
        print("Aviso: Arquivo 'hash_distribution.csv' não encontrado. Pulando boxplots.")
        return

    # Agrega os dados de frequência (tira a média das 5 iterações)
    agg_dist = df_dist.groupby(['Size', 'M parameter', 'Hash Function', 'Bucket Size']).mean().reset_index()

    # Gera uma figura consolidada para cada tamanho de dataset (N)
    for size, size_group in agg_dist.groupby('Size'):

        # Determina as dimensões da grade
        hash_functions = sorted(size_group['Hash Function'].unique())
        m_params = sorted(size_group['M parameter'].unique())
        n_rows = len(hash_functions)
        n_cols = len(m_params)

        # Cria a figura e os eixos (subplots)
        # sharey=True faz com que todos os gráficos na mesma linha compartilhem o mesmo eixo Y, facilitando a comparação
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharey=True)

        fig.suptitle(f'Distribuição do Tamanho dos Buckets para N = {int(size)}', fontsize=18, fontweight='bold')

        for row_idx, func_name in enumerate(hash_functions):
            for col_idx, m_param in enumerate(m_params):
                ax = axes[row_idx, col_idx]

                # Filtra os dados para o subplot atual
                subset = size_group[(size_group['Hash Function'] == func_name) & (size_group['M parameter'] == m_param)]

                if not subset.empty:
                    # Reconstrói a distribuição a partir da frequência para o boxplot
                    reconstructed_data = np.repeat(subset['Bucket Size'], subset['Frequency'].astype(int))

                    ax.boxplot(reconstructed_data, vert=True, patch_artist=True, showmeans=True)

                # Configura os títulos e labels
                if row_idx == 0:
                    ax.set_title(f'M = {int(m_param)}', fontsize=14)
                if col_idx == 0:
                    ax.set_ylabel(f'{func_name}\n\nTamanho do Bucket', fontsize=12)

                ax.grid(True, axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Ajusta para o super-título caber

        filename = os.path.join(CHARTS_PATH, f"Boxplot_Grid_N{size}.png")
        plt.savefig(filename)
        plt.close()
        print(f"Gráfico em grade salvo: {filename}")


def plot_distribution_boxplot_evolution_grid(path, exclude_functions=None, suffix=""):
    """
    Carrega os dados de distribuição e plota uma grade de boxplots normalizados.
    Pode excluir funções de hash para uma visualização focada.
    """
    if exclude_functions is None:
        exclude_functions = []

    try:
        df_dist = pd.read_csv(os.path.join(path, 'hash_distribution.csv'))
    except FileNotFoundError:
        print("Aviso: Arquivo 'hash_distribution.csv' não encontrado. Pulando boxplots.")
        return

    # Filtra as funções de hash a serem excluídas
    df_dist = df_dist[~df_dist['Hash Function'].isin(exclude_functions)]

    agg_dist = df_dist.groupby(['Size', 'M parameter', 'Hash Function', 'Bucket Size']).mean().reset_index()

    hash_functions = sorted(agg_dist['Hash Function'].unique())
    m_params = sorted(agg_dist['M parameter'].unique())
    sizes = sorted(agg_dist['Size'].unique())

    if not hash_functions or not m_params:
        print("Não há dados suficientes para gerar o gráfico de boxplot.")
        return

    n_rows, n_cols = len(hash_functions), len(m_params)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows), squeeze=False)
    fig.suptitle(f'Distribuição Normalizada do Tamanho dos Buckets{suffix}', fontsize=20, fontweight='bold')

    y_limits = {}
    for m_param in m_params:
        m_subset = agg_dist[agg_dist['M parameter'] == m_param]
        all_reconstructed_data = []
        for _, row in m_subset.iterrows():
            expected_avg = row['Size'] / row['M parameter']
            if expected_avg > 0:
                normalized_size = row['Bucket Size'] / expected_avg
                all_reconstructed_data.extend([normalized_size] * int(row['Frequency']))

        if all_reconstructed_data:
            p98 = np.percentile(all_reconstructed_data, 98)
            y_limits[m_param] = p98 * 1.2
        else:
            y_limits[m_param] = 1

    for row_idx, func_name in enumerate(hash_functions):
        for col_idx, m_param in enumerate(m_params):
            ax = axes[row_idx, col_idx]

            subset_config = agg_dist[(agg_dist['Hash Function'] == func_name) & (agg_dist['M parameter'] == m_param)]

            data_to_plot_for_subplot = []
            labels_for_subplot = []

            for size in sizes:
                subset_size = subset_config[subset_config['Size'] == size]
                if not subset_size.empty:
                    expected_avg = size / m_param
                    if expected_avg == 0: continue
                    reconstructed_data = np.repeat(subset_size['Bucket Size'], subset_size['Frequency'].astype(int))
                    normalized_data = reconstructed_data / expected_avg
                    data_to_plot_for_subplot.append(normalized_data)
                    labels_for_subplot.append(f'N={int(size / 1000)}k')

            if data_to_plot_for_subplot:
                ax.boxplot(data_to_plot_for_subplot, labels=labels_for_subplot, patch_artist=True, showmeans=True,
                           showfliers=False)

            ax.axhline(1.0, color='r', linestyle='--', linewidth=1.2, label='Média Esperada')
            ax.set_ylim(0, y_limits[m_param])

            if row_idx == 0:
                ax.set_title(f'M = {int(m_param)}', fontsize=14)
            if col_idx == 0:
                ax.set_ylabel(f'{func_name}\n\nTamanho Normalizado', fontsize=12)

            ax.grid(True, axis='y', linestyle='--', alpha=0.6)
            ax.tick_params(axis='x', rotation=45)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    filename = os.path.join(CHARTS_PATH, f"Boxplot_Evolution_Grid{suffix.replace(' ', '_')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico em grade salvo: {filename}")


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

            # Plot das médias no formato de linhas
            plt.plot(sizes, means, marker='o', linestyle=linestyles[i], label=f'{algo_name}', color=color)
            # Plot do desvio padrão ao redor das médias
            plt.fill_between(sizes, means - stds, means + stds, color=color, alpha=0.1)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Tamanho do Dataset (N)', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)

    if use_log_scale: plt.yscale('log')
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend(fontsize=14, loc='best')
    plt.tight_layout()

    os.makedirs(CHARTS_PATH, exist_ok=True)
    filename = os.path.join(CHARTS_PATH, f"{title.replace(' ', '_').replace('/', '')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo: {filename}")


if __name__ == "__main__":
    full_df = load_all_data(OUTPUT_PATH, BASE_ALGORITHMS)

    if full_df.empty:
        print("Nenhum dado encontrado para análise. Execute o script 'main.py' primeiro.")
    else:
        aggregated_df = aggregate_data(full_df)

        print("--- Tabela de Médias e Desvios Padrão ---")
        pd.set_option('display.max_rows', 100)
        print(aggregated_df.to_string())
        aggregated_df.to_csv(f"{OUTPUT_PATH}/complete_experiment_df.csv")

        print("\n--- Gerando Gráficos de Análise ---")

        # LÓGICA PARA COMPARAÇÃO GERAL
        general_comparison_algos = [
            BASE_ALGORITHMS['linear_array']['name'],
            BASE_ALGORITHMS['regular_tree']['name'],
            BASE_ALGORITHMS['avl_tree']['name'],
        ]

        # Filtra os resultados da Hash Table para N=1,000,000 - vamos avaliar para o caso mais crítico
        hash_results_for_best = aggregated_df[
            (aggregated_df['Algorithm'].str.contains('Hash Table')) &
            (aggregated_df['Size'] == 1000000)
            ]

        # Se encontrou resultados, identifica a melhor e a adiciona para a comparação geral
        if not hash_results_for_best.empty: #
            #best_hash_config = hash_results_for_best.sort_values('Search CPU Time (s)_mean').iloc[0]['Algorithm']
            #Insertion CPU Time (s),Total Insertion Steps, Std Dev of Bucket Lengths
            best_hash_config = hash_results_for_best.sort_values('Std Dev of Bucket Lengths_mean').iloc[0]['Algorithm']
            general_comparison_algos.append(best_hash_config)
            print(f"\nMelhor configuração da Tabela Hash identificada para comparação: {best_hash_config}\n")
        else:
            print(
                "\nAviso: Não foram encontrados resultados para a Tabela Hash com N=1,000,000 para determinar a melhor configuração.")

        # Gera os gráficos de comparação geral incluindo a melhor Hash Table
        plot_comparison(aggregated_df, 'Insertion CPU Time (s)_mean', 'Insertion CPU Time (s)_std',
                        'Custo de Inserção (CPU Time)', 'CPU Time (s)', general_comparison_algos)
        plot_comparison(aggregated_df, 'Search CPU Time (s)_mean', 'Search CPU Time (s)_std',
                        'Custo de Busca (CPU Time)', 'CPU Time (s)', general_comparison_algos,
                        use_log_scale=True)
        plot_comparison(aggregated_df, 'Memory Usage (Peak Bytes)_mean', 'Memory Usage (Peak Bytes)_std',
                        'Uso de Memória', 'Memória (Bytes)', general_comparison_algos)

        plot_comparison(aggregated_df, 'Average Search Steps_mean', 'Average Search Steps_std',
                        'Eficiência de Busca (Passos)', 'Nº Médio de Passos', general_comparison_algos,
                        use_log_scale=True)
        plot_comparison(aggregated_df, 'Total Insertion Steps_mean', 'Total Insertion Steps_std',
                        'Eficiência de Inserção (Passos)', 'Nº Médio de Passos', general_comparison_algos,use_log_scale=True)

        # GRÁFICOS ESPECÍFICOS DAS TABELAS HASH (Comparando todas as configurações)
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
            # Comparação da Qualidade da Distribuição ---
            if 'Std Dev of Bucket Lengths_mean' in aggregated_df.columns:
                plot_comparison(aggregated_df,
                                'Std Dev of Bucket Lengths_mean', 'Std Dev of Bucket Lengths_std',
                                'Hash Tables - Qualidade da Distribuição (Desvio Padrão)',
                                'Desvio Padrão do Tamanho dos Buckets',
                                hash_configs)
        # Geração de Histograma da distribuição dos buckets
        # if os.path.exists(os.path.join(OUTPUT_PATH, 'hash_distribution.csv')):
        #     print("\n--- Gerando Histogramas de Distribuição da Tabela Hash ---")
        #     plot_distribution_histograms(OUTPUT_PATH, aggregated_df)
        if os.path.exists(os.path.join(OUTPUT_PATH, 'hash_distribution.csv')):
            print("\n--- Gerando Boxplots de Distribuição da Tabela Hash ---")
            plot_distribution_boxplots(OUTPUT_PATH)
        if os.path.exists(os.path.join(OUTPUT_PATH, 'hash_distribution.csv')):
            print("\n--- Gerando Gráficos Consolidados (Boxplot Grid) da Tabela Hash ---")
            plot_distribution_boxplots_grid(OUTPUT_PATH)
        # if os.path.exists(os.path.join(OUTPUT_PATH, 'hash_distribution.csv')):
        #     print("\n--- Gerando Gráficos Consolidados (Boxplot Evolution Grid) da Tabela Hash ---")
        #     plot_distribution_boxplot_evolution_grid(OUTPUT_PATH)
        if os.path.exists(os.path.join(OUTPUT_PATH, 'hash_distribution.csv')):
            print("\n--- Gerando Gráficos Consolidados da Tabela Hash ---")

            # 1. Gera o gráfico completo com todos os dados
            plot_distribution_boxplot_evolution_grid(OUTPUT_PATH, suffix=" (Completo)")

            # 2. Gera o gráfico "Showcase", excluindo a função 'folding'
            plot_distribution_boxplot_evolution_grid(OUTPUT_PATH, exclude_functions=['folding'], suffix=" (Showcase)")

        # Métrica de altura da árvore
        tree_configs = sorted(
            aggregated_df[aggregated_df['Algorithm'].str.contains('Árvore')]['Algorithm'].unique())
        #tree_algorithms = {k: v for k, v in ALGORITHMS.items() if 'tree' in k}
        plot_comparison(aggregated_df,
                        'Tree Height_mean', 'Tree Height_std',
                        'Arvores Binárias - Eficiência Estrutural (Altura)', 'Altura da Árvore', tree_configs)


        print("\nAnálise concluída!")
