import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONFIGURAÇÃO ---
# Mapeia os nomes dos arquivos CSV para nomes mais amigáveis e cores para os gráficos
ALGORITHMS = {
    'linear_array': {'name': 'Array Linear', 'color': 'blue'},
    'regular_tree': {'name': 'Árvore Desbalanceada', 'color': 'red'},
    'avl_tree': {'name': 'Árvore Balanceada', 'color': 'green'}
}
OUTPUT_PATH = './outputs/'
CHARTS_PATH = os.path.join(OUTPUT_PATH, 'charts_analysis/')


# --- FUNÇÕES DE ANÁLISE E PLOTAGEM ---

def load_all_data(path, algorithms):
    """
    Carrega todos os arquivos CSV de resultados em um único DataFrame do Pandas.
    """
    all_dfs = []
    for key, props in algorithms.items():
        filename = os.path.join(path, f"{key}.csv")
        try:
            df = pd.read_csv(filename)
            df['Algorithm'] = props['name']  # Adiciona uma coluna para identificar o algoritmo
            all_dfs.append(df)
        except FileNotFoundError:
            print(f"Aviso: Arquivo '{filename}' não encontrado. Pulando este algoritmo.")

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)


def aggregate_data(df):
    """
    Agrupa os dados por algoritmo e tamanho, calculando a média e o desvio padrão.
    """
    # Lista de colunas para agregar (todas exceto as de identificação)
    metric_columns = df.columns.drop(['Size', 'Iteration', 'Algorithm'])

    # Cria um dicionário de agregações para passar ao pandas
    aggregations = {col: ['mean', 'std'] for col in metric_columns}

    # Agrupa e agrega
    agg_df = df.groupby(['Algorithm', 'Size']).agg(aggregations)

    # Simplifica os nomes das colunas (ex: ('Memory Usage', 'mean') -> 'Memory Usage_mean')
    agg_df.columns = ['_'.join(col).strip() for col in agg_df.columns.values]

    return agg_df.reset_index()


def plot_comparison(df_agg, metric_mean, metric_std, title, ylabel, algorithms, use_log_scale=False):
    """
    Gera um gráfico comparativo com a média (linha) e o desvio padrão (área sombreada).
    """
    plt.figure(figsize=(12, 7))

    for key, props in algorithms.items():
        algo_name = props['name']
        color = props['color']

        # Filtra os dados para o algoritmo atual
        algo_df = df_agg[df_agg['Algorithm'] == algo_name]

        if not algo_df.empty:
            # Extrai os dados para o plot
            sizes = algo_df['Size']
            means = algo_df[metric_mean]
            stds = algo_df[metric_std]

            # Plota a linha da média
            plt.plot(sizes, means, marker='o', linestyle='-', label=f'{algo_name} (Média)', color=color)

            # Adiciona a área sombreada para o desvio padrão (média ± std)
            plt.fill_between(sizes, means - stds, means + stds, color=color, alpha=0.15,
                             label=f'{algo_name} (Desvio Padrão)')

    # Configurações do gráfico
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Tamanho do Dataset (N)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    # Configura a escala do eixo Y (linear ou logarítmica)
    if use_log_scale:
        plt.yscale('log')
        plt.grid(True, which="both", ls="--", alpha=0.4)
    else:
        plt.grid(True, alpha=0.4)

    plt.legend(fontsize=10)
    plt.tight_layout()

    # Salva o gráfico em um arquivo
    os.makedirs(CHARTS_PATH, exist_ok=True)
    filename = os.path.join(CHARTS_PATH, f"{title.replace(' ', '_')}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo: {filename}")


# --- BLOCO PRINCIPAL DE EXECUÇÃO ---

if __name__ == "__main__":
    # 1. Carrega todos os dados
    full_df = load_all_data(OUTPUT_PATH, ALGORITHMS)

    if full_df.empty:
        print("Nenhum dado encontrado para análise. Execute o script 'main.py' primeiro.")
    else:
        # 2. Agrega os dados para calcular média e desvio padrão
        aggregated_df = aggregate_data(full_df)

        print("--- Tabela de Médias e Desvios Padrão ---")
        print(aggregated_df)

        # 3. Gera os gráficos de comparação
        print("\n--- Gerando Gráficos de Análise ---")

        # Gráfico: Custo de Inserção
        plot_comparison(aggregated_df,
                        'Insertion CPU Time (s)_mean', 'Insertion CPU Time (s)_std',
                        'Custo de Construção (CPU Time)', 'CPU Time (s)', ALGORITHMS)

        # Gráfico: Custo de Busca
        plot_comparison(aggregated_df,
                        'Search CPU Time (s)_mean', 'Search CPU Time (s)_std',
                        'Custo de Busca (CPU Time)', 'CPU Time (s)', ALGORITHMS, use_log_scale=True)

        # Gráfico: Eficiência de Memória
        plot_comparison(aggregated_df,
                        'Memory Usage (Peak Bytes)_mean', 'Memory Usage (Peak Bytes)_std',
                        'Uso de Memória', 'Memória (Bytes)', ALGORITHMS)

        # Gráfico: Eficiência Estrutural (Passos de Busca)
        plot_comparison(aggregated_df,
                        'Average Search Steps_mean', 'Average Search Steps_std',
                        'Eficiência de Busca (Passos)', 'Nº Médio de Passos', ALGORITHMS, use_log_scale=True)

        # Gráfico: Altura da Árvore (apenas para as árvores)
        tree_algorithms = {k: v for k, v in ALGORITHMS.items() if 'tree' in k}
        plot_comparison(aggregated_df,
                        'Tree Height_mean', 'Tree Height_std',
                        'Eficiência Estrutural (Altura)', 'Altura da Árvore', tree_algorithms)

        print("\nAnálise concluída!")