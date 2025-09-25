import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def generate_analysis_charts(csv_path):
    """
    Lê o arquivo CSV com os resultados dos algoritmos e gera gráficos
    comparativos para cada desafio logístico.
    """
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # --- CORREÇÃO APLICADA AQUI ---
        # Removemos a tentativa de "adivinhar" e usamos o formato exato
        # que o main.py gera: separador ponto e vírgula (;) e decimal vírgula (,).
        df = pd.read_csv(csv_path, sep=';', decimal=',')
    except Exception as e:
        print(
            f"Erro ao ler o arquivo CSV. Verifique se o arquivo '{csv_path}' existe e está no formato correto. Erro: {e}")
        return

    # Garante que as colunas numéricas sejam do tipo correto
    numeric_cols = [
        'custo_km', 'nos_expandidos', 'arestas_avaliadas',
        'cpu_media', 'cpu_desvio_padrao',
        'memoria_media_kib', 'memoria_desvio_padrao'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    challenges = df['desafio'].unique()

    # Loop para Gerar Gráficos para Cada Desafio
    for challenge in challenges:
        print(f"Gerando gráficos para o desafio: {challenge}...")
        df_challenge = df[df['desafio'] == challenge].sort_values(by='custo_km').set_index('algoritmo')

        # Gráfico 1: Custo (km)
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df_challenge.index, df_challenge['custo_km'], color='skyblue', zorder=2)
        ax.set_ylabel('Custo Total (km)')
        ax.set_title(f'Custo do Caminho Encontrado\nDesafio: {challenge}')
        plt.xticks(rotation=45, ha='right')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:,.0f} km', va='bottom', ha='center', fontsize=9)
        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, f'grafico_custo_{challenge}.png'))
        plt.close(fig)

        # Gráfico 2: Eficiência da Busca (Nós e Arestas)
        fig, ax = plt.subplots(figsize=(10, 6))
        width = 0.4
        x = np.arange(len(df_challenge.index))

        rects1 = ax.bar(x - width / 2, df_challenge['nos_expandidos'], width, label='Nós Expandidos', color='coral',
                        zorder=2)
        rects2 = ax.bar(x + width / 2, df_challenge['arestas_avaliadas'], width, label='Arestas Avaliadas',
                        color='lightgreen', zorder=2)

        ax.set_ylabel('Contagem (Escala Logarítmica)')
        ax.set_title(f'Eficiência da Busca (Nós e Arestas)\nDesafio: {challenge}')
        ax.set_xticks(x)
        ax.set_xticklabels(df_challenge.index, rotation=45, ha='right')
        ax.legend()
        ax.set_yscale('log')

        for rects in [rects1, rects2]:
            for rect in rects:
                height = rect.get_height()
                if height > 0:
                    ax.annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, f'grafico_eficiencia_{challenge}.png'))
        plt.close(fig)

        # Gráfico 3: Tempo de CPU
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df_challenge.index, df_challenge['cpu_media'],
               yerr=df_challenge['cpu_desvio_padrao'], capsize=5, color='gold', zorder=2)
        ax.set_ylabel('Tempo Médio de CPU (s)')
        ax.set_title(f'Tempo de Execução da CPU (Média e Desvio Padrão)\nDesafio: {challenge}')
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, f'grafico_cpu_{challenge}.png'))
        plt.close(fig)

        # Gráfico 4: Pico de Memória
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df_challenge.index, df_challenge['memoria_media_kib'],
               yerr=df_challenge['memoria_desvio_padrao'], capsize=5, color='mediumpurple', zorder=2)
        ax.set_ylabel('Pico Médio de Memória (KiB)')
        ax.set_title(f'Pico de Memória Alocada (Média e Desvio Padrão)\nDesafio: {challenge}')
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, f'grafico_memoria_{challenge}.png'))
        plt.close(fig)

    print(f"\nGráficos de análise salvos na pasta '{output_dir}'.")


def create_summary_table(csv_path):
    """
    Lê o arquivo CSV e cria uma tabela de resumo agregada com a performance
    média dos algoritmos em todos os desafios.
    """
    print("\n\n--- Gerando Tabela de Resumo Agregada ---\n")
    try:
        # Ajustado para ler o CSV gerado pelo main.py (sep=';', decimal=',')
        df = pd.read_csv(csv_path, sep=';', decimal=',')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    numeric_cols = ['custo_km', 'nos_expandidos', 'arestas_avaliadas', 'cpu_media', 'memoria_media_kib']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    optimal_costs = df.groupby('desafio')['custo_km'].transform('min')
    df['is_optimal'] = df['custo_km'].round(2) == optimal_costs.round(2)

    summary = df.groupby('algoritmo').agg(
        optimalidade_perc=('is_optimal', lambda x: x.mean() * 100),
        nos_expandidos_media=('nos_expandidos', 'mean'),
        arestas_avaliadas_media=('arestas_avaliadas', 'mean'),
        cpu_media_s=('cpu_media', 'mean'),
        memoria_media_kib=('memoria_media_kib', 'mean')
    ).reset_index()

    summary['cpu_media_us'] = summary['cpu_media_s'] * 1_000_000

    summary = summary.sort_values(by=['optimalidade_perc', 'nos_expandidos_media'], ascending=[False, True])

    summary_table = summary[
        ['algoritmo', 'optimalidade_perc', 'nos_expandidos_media', 'arestas_avaliadas_media', 'cpu_media_us',
         'memoria_media_kib']]
    summary_table.columns = ['Algoritmo', '% Optimalidade', 'Nós Exp. (Média)', 'Arestas Aval. (Média)', 'CPU (μs)',
                             'Memória (KiB)']

    # --- Imprime a Tabela em formato de texto simples ---
    print("--- Tabela de Performance Média (Texto Simples) ---")
    print(summary_table.to_string(index=False, float_format="%.2f"))

    # --- Imprime a Tabela em formato Markdown (para Copiar e Colar no Word) ---
    print("\n--- Tabela de Performance Média (Formato Markdown) ---")
    print(summary_table.to_markdown(index=False, floatfmt=".2f"))


if __name__ == '__main__':
    csv_file_path = os.path.join('outputs', 'analise_comparativa_algoritmos.csv')

    if os.path.exists(csv_file_path):
        create_summary_table(csv_file_path)
        generate_analysis_charts(csv_file_path)
    else:
        print(f"Arquivo de análise não encontrado em: '{csv_file_path}'")
        print("Por favor, execute o 'main.py' primeiro para gerar o arquivo de resultados.")