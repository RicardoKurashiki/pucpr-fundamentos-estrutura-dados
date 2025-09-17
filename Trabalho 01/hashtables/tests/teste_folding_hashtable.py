# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 22:35:54 2025

@author: uende
"""


#%% Hash

record = {
    'matricula': '',
    'nome': '',
    'salario': 0.00,
    'cod_setor': ''
    }


#%%
import copy

#%%
from modulo_hashtable import ModuloHashTable
from folding_hashtable import FoldingHashTable
from multiplication_hashtable import EulerHashTable, GoldenRatioHashTable, PiHashTable

hashtables = [ModuloHashTable, FoldingHashTable, EulerHashTable, GoldenRatioHashTable, PiHashTable]

config = {
    'use_prime_capacity': True,
    'key_hashing_strategy': 'positional',
    'bucket_strategy': 'sorted',
    'auto_shrinking': False,
    'folding_block_strategy': 'dynamic',
    }


for Class in hashtables:
    
    ht = Class(100, **config)
    ht.insert(0, 'insert')
    ht.insert(-1, 'insert')
    ht.insert(0.00001, 'insert')
    ht.insert(2182, 'insert')
    ht.insert(6102, 'insert')
    ht.insert(2328, 'insert')
    ht.insert(1111, 'insert')
    ht.insert(1111, 'update')
    
    # Search
    ht.search(2328) # existe
    ht.search(9999) # não existe
    
    # Remove
    ht.remove(0) # inválido
    ht.remove(-1) # inválido
    ht.remove(0.00001) #inválido
    ht.remove(1234) # não existe
    ht.remove(1111) # existe
    
    # Resize
    ht.resize(50)
    
    for x in range(1000):
        try:
            ht.insert(x, f'insert {x}')
        except:
            print(x)
            break
    
    ht.resize(10000)
    ht.resize(999)
    del ht


#%%
import pandas as pd
from multiplication_hashtable import GoldenRatioHashTable

ht = GoldenRatioHashTable(100, optimized=True)
ht.insert(2182, '2182')
ht.insert(6102, '6102')
ht.insert(2328, '2328')

info = ht.info()
df_info = pd.DataFrame(info['metrics'])
df_info

#%%
from multiplication_hashtable import GoldenRatioHashTable

ht = GoldenRatioHashTable(100, True)
ht.insert(2182, '2182')
ht.insert(6102, '6102')
ht.insert(2328, '2328')



#%%
value = copy.deepcopy(record)
value['matricula'] = 'S037529'
value['nome'] = 'Uendel A Rocha'
value['salario'] = 50000
value['cod_sector'] = 'aia'

ht.insert('S037529', value)
ht.search('S037529')

ht.insert(15, 'Teste 15')


# ht.insert(10, 'Uendel')
# ht.insert(10, 'Maria')
# ht.insert(19, 'Débora')
# ht.insert(29, 'Pedro')
# ht.insert(9, 'Uendel')
# ht.insert(109, 'Evanilza')
# ht.insert(49, 'André')
# ht.insert(39, 'Tiago')
# ht.insert(59, 'João')
# ht.insert(119, 'Bartolomeu')
# ht.insert(1119, 'Bartolomeu')
# ht.insert(11119, 'Bartolomeu')
#%%
import random

def hashtable_test(Class, size, num_elements, 
                   p_hat_dense = 0.50, seed = 42, optimized = True):
    '''
    Parameters
    ----------
    Class : TYPE
        Classe ModuloHashTable usada para criar a tabela.
    size : TYPE
        Tamanho máximo da tabela. Se optimized = True, o tamanho será um número
        primo (o próprio número ou um primo posterior)
    num_elements : TYPE
        É o volume máximo de dados que será utilizado para o teste.
    p_hat_dense : TYPE, optional
        É a proporção do volume de dados que formará uma lista densa.
        Uma lista densa é aquela contendo elementos bem próximos
        uns dos outros. Quanto menor p_hat_dense, maior a densidade da lista.
        Por exemplo, seja p_hat_dense igual a 0.20 de um volume de 1000 chaves.
        Então, 20% do volume será reservado para formar um intervalo de 
        200 chaves em sequência (de 1 a 200) das quais 160 (80%) serão 
        selecionadas aleatoriamente. O restante (80%) formará uma lista
        espassa com 800 chaves aleatórias selecionadas de um intervalo 
        entre 201 e o quadrado do volume restante (800 * 800), isto é, 
        entre 201 e 640.000.
        
        Outro caso, seja p_hat_dense igual a 0.50 de um volume de 1000 chaves.
        Neste cenário, haverá 250 chaves aleatórias (50% das chaves) extraídas 
        de um intervalo de 500 chaves em sequência (50% do volume) de 1 a 500.
        O restante (50%) formará uma lista espassa com 500 chaves aleatórias 
        selecionadas de um intervalo entre 501 e o quadrado do volume restante 
        (500 * 500), isto é, entre 501 e 550.000.
        
        Observe que o primeiro caso é mais denso que o segundo.
        
        Considerando o mesmo volume do caso anterior, se p_hat_dense for igual 
        a 0.00, haverá 0 chaves densas e toda a lista será espassa contendo
        1000 chaves aleatórias entre 1 e 1.000.000 (1000 * 1000).
        
        O default é 0.50.
    seed : int, optional
        É a semente para reproduzir os testes. O default é 42.
    optimized : boolean, optional
        Se True, busca otimizar a lista com números primos e mecanismos de
        menor colisão. Isso é útil para volumes acima de 1000.
        
        Para volumes com até 1000 elementos, utilize optimized = False.
        
        O valor default é True.

    Returns
    -------
    buckets : dict
        DESCRIPTION.

    '''
    
    random.seed(seed)
    
    # Define o intervalo para lista densa (com mais elementos próximos por intervalo)
    # Indica limite máximo da lista densa
    # Desse intervalo será selecionada uma amostra
    # As chaves serão geradas de 1 até dense_range_size
    p_dense = p_hat_dense # Proporção de elementos densos da lista: quanto menor, mais denso
    dense_range_size = int(num_elements * p_dense)
    
    # Define o intervalo para lista esparsa (com menos elementos por intervalo)
    sparse_range_start = dense_range_size + 1
    sparse_range_end = int((num_elements - dense_range_size) ** 2)
    
    # Calcula o número de chaves para cada intervalo
    num_dense_keys = int(dense_range_size * (1 - p_dense))
    num_sparse_keys = num_elements - num_dense_keys
    
    # Gera as chaves aleatórias
    dense_keys = random.sample(range(1, dense_range_size + 1), num_dense_keys)
    sparse_keys = random.sample(range(sparse_range_start, sparse_range_end + 1), num_sparse_keys)
    
    all_keys = dense_keys + sparse_keys
    random.shuffle(all_keys)
    
    # Instancia a tabela hash com um tamanho de 100
    # O construtor ajustará para o próximo primo, 101
    hash_table = Class(size, True)
    
    # Insere os elementos na tabela hash
    for key in all_keys:
        hash_table.insert(str(key), f"value_{key}")
    
    # Obtém a distribuição de elementos nos buckets
    bucket_lengths = hash_table.lengths
    print(f"Número de elementos inseridos: {num_elements}")
    print(f"Tamanho da tabela hash: {hash_table.size}")
    # print("Tamanho dos buckets (listas de colisões):")
    # for i, size in enumerate(bucket_sizes):
    # if size > 0:
    #     print(f"  Bucket {i}: {size} elementos")
    
    # Estatísticas de resumo para análise
    print("\nEstatísticas de distribuição:")
    print(f"  Número de buckets não vazios: {sum(1 for size in bucket_lengths if size > 0)}")
    print(f"  Tamanho máximo de bucket: {max(bucket_lengths)}")
    print(f"  Tamanho mínimo de bucket (não-zero): {min(size for size in bucket_lengths if size > 0) if any(bucket_lengths) else 0}")
    print(f"  Tamanho médio de bucket: {sum(bucket_lengths) / len(bucket_lengths):.2f}")
    

    buckets = {"class":[], "index":[], "size":[], 
               "max_size": [], "max_elements": [], "optimized": [],
               "p_dense": [], "seed": []}
    for i, length in enumerate(bucket_lengths):
        if size > 0:
            buckets["class"].append(type(hash_table).__name__)
            buckets["index"].append(i)
            buckets["length"].append(length)
            # buckets["size"].append(size)
            buckets["max_key"].append(max(hash_table.table))
            buckets["min_key"].append(min())
            
            
    return buckets    
#%%
import pandas as pd
from folding_hashtable import FoldingHashTable
from modulo_hashtable import ModuloHashTable

# Semente fixa
seed = 42

# Proporção de densidade da lista 
p_dense = 0.5

# Se otimiza com números primos para grandes volumes de dados
optimized = True

# Tamanho
M = bucket_size = [100, 1000, 5000]

# Define o número de elementos para inserir
# Os elementos serão distribuídos entre os buckets por desdobramento
N = num_elements = [10000, 50000, 100000]

C = classes = [FoldingHashTable, ModuloHashTable]
df_buckets = pd.DataFrame({"class":[], "index":[], "size":[], "max_size": [], "max_elements": [], "optimized": []})
for m in M:
    for n in N:
        for c in C:
            df_buckets = pd.concat([df_buckets, pd.DataFrame(hashtable_test(
                c, m, n, p_dense, seed))], ignore_index = True) 
            
# Estatísticas de resumo para análise
# print("\nEstatísticas de distribuição:")
# print(f"  Número de buckets não vazios: {sum(1 for size in bucket_sizes if size > 0)}")
# print(f"  Tamanho máximo de bucket: {max(bucket_sizes)}")
# print(f"  Tamanho mínimo de bucket (não-zero): {min(size for size in bucket_sizes if size > 0) if any(bucket_sizes) else 0}")
# print(f"  Tamanho médio de bucket: {sum(bucket_sizes) / len(bucket_sizes):.2f}")


# for m in M:
#     for n in N:

    


#%% Gráfico
import matplotlib.pyplot as plt

# Using Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(df_buckets['index'], df_buckets['sizes'])
#plt.plot(df_buckets['index'], df_buckets['sizes'])
plt.xlabel(f'Index :: Max: {bucket_length - 1}')
plt.ylabel('Frequência')
plt.title('Distribuição de Frequência')
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels if needed
plt.tight_layout()
plt.show()


#%%

def plot(self):

    # Using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(df_buckets['index'], df_buckets['sizes'])
    #plt.plot(df_buckets['index'], df_buckets['sizes'])
    plt.xlabel(f'Index :: Max: {bucket_length - 1}')
    plt.ylabel('Frequência')
    plt.title('Distribuição de Frequência')
    plt.xticks(rotation=45, ha='right') # Rotate x-axis labels if needed
    plt.tight_layout()
    plt.show()


#%%
import seaborn as sns

# Alternatively, using Seaborn for a more aesthetically pleasing plot
plt.figure(figsize=(10, 6))
sns.barplot(x='index', y='sizes', data=df_buckets)
plt.xlabel('Index')
plt.ylabel('Frequência')
plt.title('Distribuição de Frequência')
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.tight_layout()
plt.show()

#%%

import matplotlib.pyplot as plt
import numpy as np

# Data for plot 1
x1 = np.array([0, 1, 2, 3])
y1 = np.array([3, 8, 1, 10])

# Data for plot 2
x2 = np.array([0, 1, 2, 3])
y2 = np.array([10, 20, 30, 40])

# Create a 1x2 grid and select the first subplot
plt.subplot(1, 2, 1)
plt.plot(x1, y1)
plt.title("Plot 1")

# Select the second subplot
plt.subplot(1, 2, 2)
plt.plot(x2, y2)
plt.title("Plot 2")

plt.tight_layout() # Adjust subplot parameters for a tight layout
plt.show()


#%%

import matplotlib.pyplot as plt
import numpy as np

# Data for plot 1
x1 = np.array([0, 1, 2, 3])
y1 = np.array([3, 8, 1, 10])

# Data for plot 2
x2 = np.array([0, 1, 2, 3])
y2 = np.array([10, 20, 30, 40])

# Create a figure and a 1x2 grid of subplots
fig, axs = plt.subplots(1, 2)

# Plot on the first Axes object
axs[0].plot(x1, y1)
axs[0].set_title("Plot A")

# Plot on the second Axes object
axs[1].plot(x2, y2)
axs[1].set_title("Plot B")

plt.tight_layout()
plt.show()

#%%

import matplotlib.pyplot as plt
import numpy as np

# Data for the first line
x1 = np.array([0, 1, 2, 3, 4])
y1 = np.array([0, 2, 4, 6, 8])

# Data for the second line
x2 = np.array([0, 1, 2, 3, 4])
y2 = np.array([8, 6, 4, 2, 0])

# Data for a third line (e.g., a sine wave)
x3 = np.linspace(0, 4, 100)
y3 = np.sin(x3 * np.pi) * 4 + 4

# Plotting the lines
plt.plot(x1, y1, label='Line 1')
plt.plot(x2, y2, label='Line 2', linestyle='--') # Example with a different linestyle
plt.plot(x3, y3, label='Sine Wave', color='green') # Example with a specific color

# Adding labels, title, and legend for clarity
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Multiple Lines on One Plot")
plt.legend() # Displays the labels for each line

# Display the plot
plt.show()

#%%

import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.random.rand(50) * 10
y = np.random.rand(50) * 10
z = np.random.rand(50) * 100  # Values to determine color

# Create the scatter plot, coloring by 'z' values
plt.scatter(x, y, c=z, cmap='viridis', s=100) # s controls marker size

# Add a colorbar
plt.colorbar(label='Value of Z')

# Set plot labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot Colored by Z Value')

plt.show()

#%%

import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 3, 4, 5]
y = [10, 5, 8, 12, 6]
category = ['A', 'B', 'A', 'C', 'B']

# Define a mapping from category to color
color_map = {'A': 'red', 'B': 'blue', 'C': 'green'}
colors = [color_map[cat] for cat in category]

plt.scatter(x, y, c=colors, s=100)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot with Custom Colors')
plt.show()