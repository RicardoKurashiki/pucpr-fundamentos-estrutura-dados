# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 16:35:11 2025

@author: Uendel Andrade Rocha
"""

#%%
from separate_chaining_hashtable import SeparateChainingHashTable

class FoldingHashTable(SeparateChainingHashTable):
   
    
    def __init__(self, capacity, **kwargs):
        
        super().__init__(capacity, **kwargs)
        
        # Define o tamanho da dobra a partir do tamanho do bucket
        self._block_size = len(str(self._capacity)) if self._folding_block_strategy == 'dynamic' else 3        
    
    def _get_bucket_index(self, key:str):
        '''
        Localiza o bucket correspondente à chave (key).
        Retorna (valor_hash, passos_executados)
        '''
        # Converter a chave em um valor numérico
        num_key, steps = self._key_to_numkey(key)
        
        str_key = str(num_key)
        steps += 1 # Custo da conversão para string
        
        hash_value = 0
        
        # Dividir a chave numérica em partes e somá-las
        for i in range(0, len(str_key), self._block_size):
            # Pega a chave em partes
            block = str_key[i:i + self._block_size]
            hash_value += int(block)
            steps += 2 # Custo do fatiamento e da soma/conversão
        
        final_hash = hash_value % self._capacity
        steps += 1 # Custo da operação de módulo
        
        return final_hash, steps
    