# -*- coding: utf-8 -*-
import numpy as np
import time
import random
import tracemalloc
import psutil as p

# INSERT ALGORITHMS

#def insert_value(value):


# SEARCH ALGORITHMS

def sequential_search(arr, target):
    steps = 0
    for i, value in enumerate(arr):
        steps += 1
        if value == target:
            return i, steps
    return -1, steps

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps


# SORTING ALGORITHMS

def bubble_sort(arr):
    n = len(arr)
    swap_count = 0
    shift_count = 0
    step_count = 0
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):  # A cada rodada do Bubblue sort os maiores elementos vão sendo movidos para o final da lista e não precisam mais ser verificados.
            step_count += 1         # Número de operações
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1     # Número de troca de elementos
                swapped = True
        if not swapped:
            break
    return arr, swap_count, shift_count, step_count

def selection_sort(arr):
  n = len(arr)
  swap_count = 0
  shift_count = 0
  step_count = 0
  for i in range(n):
    min_idx = i
    for j in range(i + 1, n):     # Loop para descobrir o índice do menor elemento da lista
        step_count += 1
        if arr[j] < arr[min_idx]:
            min_idx = j
    if min_idx != i:
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        swap_count += 1
  return arr, swap_count, shift_count, step_count

def insertion_sort(arr):
  n = len(arr)
  swap_count = 0
  shift_count = 0
  step_count = 0
  for i in range(1, n):
      key = arr[i]
      j = i - 1
      while j >= 0:
          step_count += 1
          if arr[j] > key:
              arr[j + 1] = arr[j]  # Desloca uma posição
              shift_count += 1
              j -= 1
          else:
              break
      arr[j + 1] = key
  return arr, swap_count, shift_count, step_count


def compute_sorting_algorithms(arr, size, func):

        p.cpu_percent()                         # Esta chamada funciona como um reset para a próxima medição de consumo de CPU, já que cada chamada de cpu_percent traz o consumo desde a última chamada
        time.sleep(0.05)                        # Delay necessário para que não ocorram medições muito rápidas do consumo de CPU

        tracemalloc.start()                     # Inicia a coleta de memória alocada
        
        start = time.time()
        ordered_arr, swap_count, shift_count, step_count = func(arr.copy())
        end = time.time()
            
        memory_usage = tracemalloc.get_tracemalloc_memory() # Coleta de memória
        tracemalloc.stop()                      # Para a coleta de memória alocada
            
        p_cpu_usage = p.cpu_percent()           # Coleta o consumo de CPU desde a última chamada

        print(
            f"Size {size:6d} | Swaps: {swap_count:6d} | Shifts: {shift_count:6d} "
            f"| Steps: {step_count:6d} | MemMoves: {swap_count * 2 + shift_count:3d} "
            f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
            f"| Time: {end - start:.4f} s "
            f"| {arr[:5]} -> {ordered_arr[:5]}"
        )

def main():
    sizes = [100, 200, 300, 400, 500]
    algorithms = [
        ('Bubble Sort', bubble_sort),
        ('Insertion Sort', insertion_sort),
        ('Selection Sort', selection_sort)
    ]

    results = {
        "times": {name: [] for name, _ in algorithms},
        "steps": {name: [] for name, _ in algorithms},
        "swaps": {name: [] for name, _ in algorithms},
        "shifts": {name: [] for name, _ in algorithms},
        "mem_moves": {name: [] for name, _ in algorithms},
        "memory_usage": {name: [] for name, _ in algorithms},
        "cpu_usage": {name: [] for name, _ in algorithms}
    }

    base_arrays = {size: np.random.randint(0, 10000, size) for size in sizes}

    for name, func in algorithms:
        print(f"\n{name}:")
        for size in sizes:
            compute_sorting_algorithms(base_arrays[size], size, func)
            #compute_sequential_search()
            #compute_binary_search()

if __name__ == "__main__":
    main()