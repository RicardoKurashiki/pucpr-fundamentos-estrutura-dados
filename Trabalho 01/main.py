from utils import generate_data
from time import time, sleep
import psutil as p
import tracemalloc

from hashmap import HashTable
from avltree import AVLTree

def compute_algorithms(data, func):
    p.cpu_percent()
    sleep(0.05)
    tracemalloc.start()

    start = time()
    func(data)
    end = time()

    memory_usage = tracemalloc.get_tracemalloc_memory()
    tracemalloc.stop()

    p_cpu_usage = p.cpu_percent()

    print(
        f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
        f"| Time: {end - start:.4f} s "
    )

def linear_array_test(data):
    print("\nLinear Array Test")

def tree_test(data):
    print("\nTree Test")
    tree = AVLTree()
    for item in data:
        tree.insert(item[0])
    print(tree.search(data[0][0]))

def hash_test(data):
    print("\nHash Test")
    hash_table = HashTable(len(data))
    for item in data:
        hash_table.insert(item[0], item[1:])
    hash_table.search(data[0][0])

def main():
    sizes = [50_000, 100_000, 500_000, 1_000_000]
    iterations = 5
    for size in sizes:
        print(f"\nSize: {size}")
        for i in range(iterations):
            print(f"\nIteration: {i+1}\n")
            data = generate_data(size)
            compute_algorithms(data, linear_array_test)
            compute_algorithms(data, tree_test)
            compute_algorithms(data, hash_test)


if __name__ == "__main__":
    main()