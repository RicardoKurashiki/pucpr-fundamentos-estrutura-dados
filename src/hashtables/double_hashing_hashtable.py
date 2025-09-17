# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 12:45:15 2025
@author: Uendel A Rocha (2025)
"""
# CORRIGIDO: Herda da classe base correta.
from open_adressing_hashtable import OpenAddressingHashTable
from prime_numbers import previous_prime_number

class DoubleHashingHashTable(OpenAddressingHashTable):
    """
    Implementa a resolução de colisões usando Hashing Duplo.
    A lógica principal de insert, search e remove é herdada da classe mãe.
    Esta classe fornece as funções de hash primário e secundário para a
    estratégia de sondagem específica.
    """
    def __init__(self, capacity, **kwargs):
        super().__init__(capacity, **kwargs)
        
        # NOVO: Inicializa a tabela e as estatísticas.
        self._table = self._get_table()
        self._stats = self._get_stats()
        
        # A necessidade de um número primo menor é específica desta classe.
        self._smallest_prime_number = previous_prime_number(self._capacity)

    # --- IMPLEMENTAÇÃO DOS MÉTODOS ABSTRATOS E HELPERS ---
    
    def _primary_hash(self, key: str):
        """Função de hash primária."""
        num_key, steps = self._key_to_numkey(key)
        return num_key % self._capacity, steps + 1 # Custo da função mod

    def _secondary_hash(self, key: str):
        """Função de hash secundária para calcular o passo (step)."""
        num_key, steps = self._key_to_numkey(key)
        # A fórmula garante que o passo nunca seja zero.
        return 1 + (num_key % self._smallest_prime_number), steps + 2

    def _probe(self, key: str, attempt: int):
        """
        Calcula o próximo índice usando hashing duplo: (h1(k) + i * h2(k)) % M
        """
        h1, ph_steps = self._primary_hash(key)
        h2, sh_steps = self._secondary_hash(key)
        steps = ph_steps + sh_steps
        
        index = (h1 + attempt * h2) % self._capacity
        steps += 3 # soma, multiplicação, mod
        
        return index, steps