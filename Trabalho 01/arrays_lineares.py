# -*- coding: utf-8 -*-
import numpy as np
import time
import random
import tracemalloc
import psutil as p

# INSERT ALGORITHM

def insert_array(data):
    arr_of_ids = [item[0] for item in data]

    return arr_of_ids

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