# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 22:38:29 2025

@author: uende
"""

#%% Manipula números primos

def is_prime_number(n):
    """
    Verifica se um número é primo.
    Args:
        n (int): O número a ser verificado.
    Returns:
        bool: True se o número for primo, False caso contrário.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True  

    
def previous_prime_number(number):
    i = 1
    while True:
        # Verifica se o número para baixo (anterior) é primo
        previous = number - i
        if previous > 0 and is_prime_number(previous):
            return previous
        
        i+= 1

def later_prime_number(number):
    i = 1
    while True:
        # Verifica se o número para cima (posterior) é primo
        later = number + i
        if later > 0 and is_prime_number(later):
            return later
        
        i += 1
        
def closest_prime_number(number):
    if is_prime_number(number):
        return number
    
    i = 1
    while True:
        # Verifica se o número para baixo é primo
        previous = number - i
        if previous > 0 and is_prime_number(previous):
            return previous

        # Verifica se o número para cima é primo
        later = number + i
        if previous > 0 and is_prime_number(later):
            return later
        
        i += 1

