from utils import generate_data
from time import time, sleep
import psutil as p
import os
from tqdm import tqdm
import tracemalloc

from hashtable import HashTable
from avltree import AVLTree

def compute_algorithms(data, func, name, iteration, size):
    p.cpu_percent()
    sleep(0.05)
    tracemalloc.start()

    start = time()
    func(data)
    end = time()

    memory_usage = tracemalloc.get_tracemalloc_memory()
    tracemalloc.stop()

    p_cpu_usage = p.cpu_percent()

    os.makedirs("./outputs/", exist_ok=True)

    with open(f"./outputs/{name}_{size}.txt", "a") as f:
        f.writelines(
            "--------------------------------\n\n"
            f"| Size: {size}\n"
            f"| Iteration: {iteration}\n"
            f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % \n"
            f"| Time: {end - start:.4f} s \n"
            "\n"
        )

def linear_array_test(data):
    pass

def tree_test(data):
    tree = AVLTree()
    for item in data:
        tree.insert(item[0])
    tree.search(data[len(data) // 2][0])

def hash_test(data):
    hash_table = HashTable(len(data))
    for item in data:
        hash_table.insert(item[0], item[1:])
    hash_table.search(data[len(data) // 2][0])

def main():
    sizes = [50_000, 100_000, 500_000, 1_000_000]
    iterations = 5
    for size in tqdm(sizes):
        for i in range(iterations):
            data = generate_data(size)
            compute_algorithms(data, linear_array_test, "linear_array", i, size)
            compute_algorithms(data, tree_test, "avl_tree", i, size)
            compute_algorithms(data, hash_test, "hash_table", i, size)


if __name__ == "__main__":
    main()