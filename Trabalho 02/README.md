# Trabalho 02

## Utilização

O aplicativo permite a execução dos experimentos em lote e de maneira sequencial.

Para executar, execute o comando a seguir:
```
python main.py 
```

A execução dos experimentos resultará na geração de arquivos com as métricas coletadas e os mapas com as soluções encontradas, 
dentro da pasta outputs:
``` 
outputs/
├── analise_comparativa_algoritmos.csv
├── caminho_Centro_Sudeste_AStar_Search.html
├── caminho_Centro_Sudeste_BFS.html
├── caminho_Centro_Sudeste_DFS.html
├── caminho_Centro_Sudeste_Dijkstra.html
└── ...
```

## Análise e plotagem de gráficos

Uma vez gerado o arquivo CSV com as métricas coletadas, é possível proceder à análise das mesmas e geração 
dos gráficos, através do script Python analysis.py. Para tanto, execute:

``` 
python analysis.py
```

A execução produzirá os arquivo de imagem dentro da pasta outputs.