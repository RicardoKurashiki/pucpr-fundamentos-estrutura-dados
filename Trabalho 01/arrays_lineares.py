# -*- coding: utf-8 -*-
import numpy as np
import time
import random
import tracemalloc
import psutil as p

# INSERT ALGORITHMS

def insert_value(arr, value):
    arr = np.array(arr)
    new_arr = np.append(arr, value)

    return new_arr


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

def partition(arr, lo, hi):
    swap_count = 0
    step_count = 0


    mid = (lo + hi) // 2
    pivot = arr[mid]
    # Move o pivot para o final temporariamente
    arr[mid], arr[hi] = arr[hi], arr[mid]
    swap_count += 1


    i = lo
    for j in range(lo, hi):
        step_count += 1
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            swap_count += 1


    arr[i], arr[hi] = arr[hi], arr[i]
    swap_count += 1
    return i, swap_count, step_count

def quick_sort(arr, lo = None, hi = None):
    swap_count = 0
    step_count = 0
    shift_count = 0

    if lo is None:
        lo = 0
    if hi is None:
        hi = len(arr) - 1


    if lo < hi:
        pivot_index, part_swaps, part_steps = partition(arr, lo, hi)
        swap_count += part_swaps
        step_count += part_steps


        _, left_swaps, _, left_steps = quick_sort(arr, lo, pivot_index - 1)
        swap_count += left_swaps
        step_count += left_steps


        _, right_swaps, _, right_steps = quick_sort(arr, pivot_index + 1, hi)
        swap_count += right_swaps
        step_count += right_steps


    return arr, swap_count, shift_count, step_count

# COMPUTING METRICS

def compute_sorting_algorithms(arr, func):
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
        f"Swaps: {swap_count:6d} | Shifts: {shift_count:6d} "
        f"| Steps: {step_count:6d} | MemMoves: {swap_count * 2 + shift_count:3d} "
        f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
        f"| Time: {end - start:.4f} s "
        f"| {arr[:5]} -> {ordered_arr[:5]}"
    )

    return ordered_arr

def compute_binary_search(arr, target):
    p.cpu_percent()                        
    time.sleep(0.05)                        

    tracemalloc.start()                     
    start = time.time()
    _, step_count = binary_search(arr, target)
    end = time.time()

    memory_usage = tracemalloc.get_tracemalloc_memory() 
    tracemalloc.stop()                     
            
    p_cpu_usage = p.cpu_percent()     

    print(
        f"Binary Search: "
        f"Target: {target} | Steps: {step_count} "
        f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
        f"| Time: {end - start:.4f} s"
    )      

def compute_sequential_search(arr, target):
    p.cpu_percent()                        
    time.sleep(0.05)                        

    tracemalloc.start()                     
    start = time.time()
    _, step_count = sequential_search(arr, target)
    end = time.time()

    memory_usage = tracemalloc.get_tracemalloc_memory() 
    tracemalloc.stop()                     
            
    p_cpu_usage = p.cpu_percent()     

    print(
        f"Sequential Search: "
        f"Target: {target} | Steps: {step_count} "
        f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
        f"| Time: {end - start:.4f} s"
    ) 

def compute_insert_value(arr, value):
    p.cpu_percent()                        
    time.sleep(0.05)                        

    tracemalloc.start()                     
    start = time.time()
    new_arr = insert_value(arr, value)
    end = time.time()

    memory_usage = tracemalloc.get_tracemalloc_memory() 
    tracemalloc.stop()                     
            
    p_cpu_usage = p.cpu_percent()     

    print(
        f"Insert Value: {value} "
        f"| Memory Usage: {memory_usage:6d} bytes | CPU Usage: {p_cpu_usage} % "
        f"| Time: {end - start:.4f} s"
    )
    return new_arr

def main():
    sizes = [100, 200, 300, 400, 500]
    algorithms = [
        ('Bubble Sort', bubble_sort),
        ('Insertion Sort', insertion_sort),
        ('Selection Sort', selection_sort),
        ('Quick Sort', quick_sort)
    ]
    value_to_insert_and_search = 88

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
        print(f"\n----------------------------------------------------------------------------------------------------------------------")
        for size in sizes:
            print(f"\nArray of size: {size + 1}")

            print(f"Inserting {value_to_insert_and_search} in array...")
            arr = compute_insert_value(base_arrays[size], value_to_insert_and_search)

            print(f"Ordering array with {name}...")
            ordered_arr = compute_sorting_algorithms(arr, func)

            target = value_to_insert_and_search
            compute_sequential_search(arr, target)
            compute_binary_search(ordered_arr, target)

if __name__ == "__main__":
    main()