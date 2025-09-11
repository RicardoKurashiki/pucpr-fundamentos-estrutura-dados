from utils import generate_data
from time import time, sleep
import psutil as p
import os
from tqdm import tqdm
import tracemalloc

from hashtable import HashTable
from avltree import AVLTree
from unbaltree import UnBalTree

def compute_algorithms(data, func, name, iteration, size):

    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())
    # Mede o tempo de CPU inicial
    cpu_before = process.cpu_times()

    p.cpu_percent()
    tracemalloc.start()

    # A função de teste pode retornar um dicionário de métricas específicas
    specific_metrics = func(data)

    # Mede o tempo de CPU final
    cpu_after = process.cpu_times()

    #memory_usage = tracemalloc.get_tracemalloc_memory()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calcula a diferença de tempo de CPU
    cpu_time_user = cpu_after.user - cpu_before.user
    cpu_time_system = cpu_after.system - cpu_before.system
    total_cpu_time = cpu_time_user + cpu_time_system
    # Usaremos o valor de PICO (peak_mem) para o nosso relatório.
    memory_usage = peak_mem

    p_cpu_usage = p.cpu_percent()

    os.makedirs("./outputs/", exist_ok=True)

    with open(f"./outputs/{name}_{size}.txt", "a") as f:
        f.writelines(
            "--------------------------------\n\n"
            f"| Size: {size}\n"
            f"| Iteration: {iteration}\n"
            f"| Memory Usage: {memory_usage:9d} bytes | CPU Usage: {p_cpu_usage} % \n"
            f"| CPU Time (user+system): {total_cpu_time:.4f} s\n"
        )
        # Loop genérico para salvar as eventuais métricas retornadas
        if specific_metrics is not None:
            for metric_name, metric_value in specific_metrics.items():
                f.writelines(f"| {metric_name}: {metric_value}\n")
        f.writelines("\n")

def linear_array_test(data):
    pass

def tree_test(data):
    tree = AVLTree(key=lambda registro: registro[0])
    for item in data:
        tree.insert(item)
    # Capturamos os dados (ignoramos) e o dicionário de métricas
    _, metrics = tree.search(data[len(data) // 2][0])
    return metrics # Retornamos o dicionário

def unbaltree_test(data):
    tree = UnBalTree(key=lambda registro: registro[0])
    for item in data:
        tree.insert(item)
    _, metrics = tree.search(data[len(data) // 2][0])
    return metrics

def hash_test(data):
    hash_table = HashTable(len(data))
    for item in data:
        hash_table.insert(item[0], item[1:])

    # EXEMPLO DE EXTENSIBILIDADE:
    # Suponha que o search da HashTable retorne o número de colisões encontradas
    # _, metrics = hash_table.search(data[len(data) // 2][0])
    # return metrics # -> retornaria algo como {'Collisions': 1}

    # Por enquanto, não faremos isso
    hash_table.search(data[len(data) // 2][0])

def main():
    sizes = [50_000, 100_000, 500_000, 1_000_000]
    iterations = 5
    for size in tqdm(sizes):
        for i in range(iterations):
            data = generate_data(size)
            compute_algorithms(data, linear_array_test, "linear_array", i, size)
            compute_algorithms(data, unbaltree_test, "regular_tree", i, size)
            compute_algorithms(data, tree_test, "avl_tree", i, size)
            compute_algorithms(data, hash_test, "hash_table", i, size)


if __name__ == "__main__":
    main()