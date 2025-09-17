# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 18:09:43 2025

@author: Uendel Andrade Rocha
"""
from separate_chaining_hashtable import SeparateChainingHashTable

class ModuloHashTable(SeparateChainingHashTable):
    
    def _get_bucket_index(self, key:str):
        numkey, steps = self._key_to_numkey(key)
        
        return numkey % self._capacity, steps + 1 # 1 é o custo da op mod (%)
