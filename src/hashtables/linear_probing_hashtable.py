# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 12:43:56 2025
@author: Uendel A Rocha (2025)
"""
from open_adressing_hashtable import OpenAddressingHashTable

class LinearProbingHashTable(OpenAddressingHashTable):
    """
    Implementa a resolução de colisões usando Sondagem Linear.
    A lógica principal de insert, search e remove é herdada da classe mãe.
    Esta classe apenas fornece a estratégia de sondagem específica.
    """
    def __init__(self, capacity, **kwargs):
        # Herda o __init__ da classe mãe abstrata.
        super().__init__(capacity, **kwargs)
        
        # NOVO: Responsabilidade da classe concreta de inicializar a tabela e stats.
        self._table = self._get_table()
        self._stats = self._get_stats()

    # --- IMPLEMENTAÇÃO DOS MÉTODOS ABSTRATOS ---
    
    def _primary_hash(self, key: str):
        """Usa o hash built-in do Python como função de hash primária."""
        # A conversão da chave para número é feita no _key_to_numkey da BaseHashTable
        num_key, steps = self._key_to_numkey(key)
        return num_key % self._capacity, steps + 1 # Custo da operação mod
            
    def _probe(self, key: str, attempt: int):
        """
        Calcula o próximo índice usando a sondagem linear: (h(k) + i) % M
        """
        initial_index, steps = self._primary_hash(key)
        return (initial_index + attempt) % self._capacity, steps + 2