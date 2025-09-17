# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:15:50 2025

@author: uende
"""

import math

# Proporção áurea
phi = (1 + math.sqrt(5))/2

# Inverso da proporção áurea (apenas a parte decimal da proporção áurea)
A = phi - 1 # Equivalente a 1/phi e a (math.sqrt(5) + 1)/2 % 1.

# Proporção do número de Euler (apenas a parte decimal do número de Euler)
E = math.e - 2 # Equivalente a math.e % 1.

# Proporção da razão pi (apenas a parte decimal de pi)
P = math.pi - 3 # Equivalente a math.pi % 1.


from separate_chaining_hashtable import SeparateChainingHashTable

class MultiplicationHashTable(SeparateChainingHashTable):
    """
    Implementa a função de hash usando o método da multiplicação.
    """
    
    def __init__(self, capacity, ratio:float, **kwargs):
        """
        Inicializa a classe com a capacidade da tabela e a razão de multiplicação.
        
        Argumentos:
            capacity (int): A capacidade (m) da tabela hash.
            ratio (float): Uma constante entre 0 e 1, usada no método da multiplicação.
        
        # --- Exemplo de Uso da Classe ---
        # m = 100
        # A = 0.6180339887  # Inverso da proporção áurea
        # hasher = MultiplicationHashTable(capacity=m, ratio=A)
        # 
        # indice = hasher.search("minha_chave") # Usa os métodos da classe base
        # print(f"Índice Hash para a chave: {indice}")
        """
        if not (0 < ratio < 1):
            raise ValueError("A constante 'ratio' deve estar no intervalo (0, 1).")
        
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("O tamanho da tabela deve ser um inteiro positivo.")            

        super().__init__(capacity, **kwargs)
        
        self._ratio = ratio
        
    @property
    def ratio(self):
        return self._ratio
        
    
    def _get_bucket_index(self, key:str):
        # Converter a chave em um valor numérico
        key, steps = self._key_to_numkey(key)
        
        product = key * self._ratio
        steps += 1 # Custo da multiplicação
        fractional_part = product % 1
        steps += 1 # Custo da operação mod
        
        hash_value = self._capacity * fractional_part
        steps += 1 # Custo da multiplicação
        
        return math.floor(hash_value), steps + 1 # Custo do arredondamento
    
PolynomialHashTable = MultiplicationHashTable

class GoldenRatioHashTable(MultiplicationHashTable):
    def __init__(self, capacity, **kwargs):
        super().__init__(capacity = capacity, ratio = A, **kwargs)
        
FibonacciHashing = GoldenRatioHashTable

class EulerHashTable(MultiplicationHashTable):    
    def __init__(self, capacity, **kwargs):
        super().__init__(capacity = capacity, ratio = E, **kwargs)
        
class PiHashTable(MultiplicationHashTable):
    def __init__(self, capacity, **kwargs):
        super().__init__(capacity = capacity, ratio = P, **kwargs)

CircularHashTable = PiHashTable