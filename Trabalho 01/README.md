# Trabalho 01: Análise Comparativa de Estruturas de Dados

[Link Documentação](https://drive.google.com/file/d/1iNAsY1hraWFMaJjWwBbhne1AnEuk6lHr/view?usp=drive_link)

## Utilização

O aplicativo permite a execução do experimento de forma individualizada, escolhendo a estrutura de dados 
a ser avaliada, permitindo a execução "paralela" dos experimentos em cada estrutura, bem como permite a
execução de todos os experimentos de maneira sequencial.

Para executar todos os experimentos, execute o comando a seguir:
```
python main.py --all
```

Para executar os experimentos individualmente, basta executar o comando com o parâmetro da respetiva 
estrutura:
```
python main.py [--array|--tree|--hash]
```

A execução dos experimentos resultará na geração de arquivos com as métricas coletadas, dentro da pasta outputs:
``` 
outputs/
├── avl_tree.csv
├── experiment_df.csv
├── hash_distribution.csv
├── hash_table.csv
├── linear_array.csv
└── regular_tree.csv
```

## Análise e plotagem de gráficos

Existindo os arquivos CSV com as métricas coletadas, é possível proceder à análise dos mesmos e geração 
dos gráficos, através do script Python analysis.py. Para tanto, execute:

``` 
python analysis.py
```

A execução produzirá os arquivo de imagem dentro da pasta charts_analysis.