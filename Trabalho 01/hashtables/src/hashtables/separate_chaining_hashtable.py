# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 11:08:47 2025

@author: uende
"""
from abc import abstractmethod
from dataclasses import dataclass
from base_hashtable import BaseHashTable, profile_operation, operations, variables
from prime_numbers import is_prime_number, later_prime_number
import math

import matplotlib.pyplot as plt

@dataclass
class BucketStats:
    """
    Armazena e gerencia as estatísticas agregadas de um único bucket da 
    HashTable.
    """    
    length: int = 0     # Comprimento da lista no bucket
    min_key = None      # Menor chave DENTRO do bucket
    max_key = None      # Maior chave DENTRO do bucket
    
    # Reinicia as métricas para cada nova instância
    def __post_init__(self):
        # Métricas de performance para este bucket
        self.metrics = {o: {v: [] for v in variables} for o in operations}

class SeparateChainingHashTable(BaseHashTable):
    
    def __init__(self, capacity, **kwargs):
        """
        Inicializa a tabela de hash.
        """
        super().__init__(capacity=capacity, **kwargs)        
        self._set_capacity(capacity) # Quantidade total de slots/buckets
        self._table = self._get_table() # Cria a tabela hash
        self._stats = self._get_stats() # Cria as estatísticas

        self._min_len = self._max_len = 0



    # ===================================================================
    # PROPRIEDADES
    # ===================================================================

    # ...

    # ===================================================================
    # MÉTODOS PÚBLICOS DE OPERAÇÃO (DECORADOS)
    # ===================================================================

    @profile_operation('search')
    def search(self, key):
        index, position, steps = self._find_item_location(key)
        
        # A busca retorna uma posição. Verificamos se a chave nessa posição realmente bate.
        if position != -1 and self._stats[index].length > 0:
            if self._table[index][position][0] == key:
                return index, steps, self._table[index][position][1] # Retorna o valor

        return index, steps, None # Retorna None se não encontrado

    @profile_operation('insert')
    def insert(self, key, value):
        total_steps = 0
        
        # Garante que há espaço antes de inserir, para simplificar a lógica
        if self._get_load_factor() >= self._max_load_factor:
            new_capacity = math.ceil(self._capacity * self._growth_factor)
            resize_steps, _ = self.resize(new_capacity)
            total_steps += resize_steps
        
        # Chama a lógica de inserção "silenciosa"
        index, insert_steps, result = self._internal_insert(key, value)
        total_steps += insert_steps
        
        return index, total_steps, result

    @profile_operation('remove')
    def remove(self, key):
        index, position, steps = self._find_item_location(key)
        
        # Se o item foi encontrado, executa a remoção
        if position != -1 and self._table[index]:
            if self._table[index][position][0] == key:
                
                # Tamanho do bucket ANTES da remoção
                bucket_size = len(self._table[index])
                
                # Realiza a deleção física
                del self._table[index][position]
                
                # Adiciona o custo do deslocamento dos elementos
                # O número de elementos deslocados é igual ao tamanho original
                # menos a posição do elemento apagado (position) - 1
                shifting_steps = bucket_size - 1 - position
                steps += shifting_steps
                
                self._size -= 1
                self._remove_statistics(index, key)
                
                # Verifica a necessidade de redimensionamento para um tamanho menor
                # O shrink só acontece se o hiperparâmetro estiver ativado
                if self._auto_shrinking \
                    and self._get_load_factor() < self._min_load_factor \
                        and self._capacity > 1:
                    
                    new_capacity = math.ceil(self._capacity * self._shrink_factor)
                    resize_steps, _ = self.resize(new_capacity)
                    
                    # O custo do resize é somado ao custo total da remoção
                    steps += resize_steps
                    
                    # Index precisa ser recalculado por causa do resize
                    index, steps_locating = self._get_bucket_index(index)
                    steps += steps_locating
        
        # Retorna (index, steps, resultado) conforme o contrato do decorador
        return index, steps, (index, position) # result era None

    @profile_operation('resize')
    def resize(self, new_capacity:int):
        steps = 0
        
        if new_capacity < 1: new_capacity = 1

        old_table = self._table
        
        if self._use_prime_capacity:
            self._capacity = new_capacity if is_prime_number(new_capacity) else later_prime_number(new_capacity)
        else:
            self._capacity = new_capacity
        
        # Recria a tabela e as estatísticas
        self._table = [[] for _ in range(self._capacity)]
        self._stats = [BucketStats() for _ in range(self._capacity)]
        steps += (2 * self._capacity) # Custo da alocação
        
        # Zera contadores para a re-inserção
        self._size = 0

        # Re-insere todos os elementos usando a lógica interna "silenciosa"
        for bucket in old_table:
            steps += 1
            for key, value in bucket:
                # Soma os passos de cada inserção interna
                _, insert_steps, _ = self._internal_insert(key, value)
                steps += insert_steps
        
        # Retorna None para o índice, pois a operação é global
        return None, steps, (steps, self._capacity)
        
    # ===================================================================
    # MÉTODOS AUXILIARES/HELPERS (NÃO DECORADOS)
    # ===================================================================
    
    def _internal_insert(self, key, value):
        """Lógica de inserção pura que retorna (index, steps, result)."""
        index, position, search_steps = self._find_item_location(key)
        slot_table = self._table[index]
        
        # Caso 1: A chave já existe, apenas atualiza o valor.
        if position != -1 and position < len(slot_table):
            if slot_table[position][0] == key:
                slot_table[position] = (key, value)
                update_steps = 1
                return index, search_steps + update_steps, (index, position)
        
        # Caso 2: A chave não existe, realiza a inserção.
        insert_steps = 0
        
        if self._bucket_strategy == 'sorted':
            # Modo otimizado: insere na posição correta para manter a ordem.
            # 'position' retornado pela busca binária já é o ponto de inserção.
            insertion_point = position
            slot_table.insert(insertion_point, (key, value))
            
            # O método list.insert reposiciona todos os elementos posteriores
            # Assim, a complexidade de inserir um posição no meio de uma lista
            # é O(n) sendo n a quantidade de elementos posteriores.
            # Isso anula qualquer benefício com a busca binária da posição.
            insert_steps = len(slot_table) - insertion_point
        elif self._bucket_strategy == 'append':
            # Modo não otimizado: simplesmente anexa ao final. É mais rápido.
            slot_table.append((key, value))
            insertion_point = len(slot_table) - 1
            
            # O método list.append tem complexidade O(1): muito eficiente
            # Entretanto, no modo não otimizado a busca é linear com 
            # complexidade O(n).
            insert_steps += 1
    
        self._size += 1
        self._insert_statistics(index, key)
        
        return index, search_steps + insert_steps, (index, insertion_point)
    
    def _find_item_location(self, key):
        """Localiza um item e retorna (index, position_in_bucket, steps)."""
        index, steps = self._get_bucket_index(key)
        
        # Bifurcação baseada no modo de otimização
        if self._bucket_strategy == 'sorted':
            position, search_steps = self._binary_search(index, key)
        elif self._bucket_strategy == 'append':
            position, search_steps = self._linear_search(index, key)
                
        return index, position, steps + search_steps
    
    def _binary_search(self, index, key):
        """
        Busca a chave em um bucket ordenado.
        Retorna (position, steps).
        'position' é o índice se encontrado, 
        ou o ponto de inserção se não encontrado.
        
        A busca binária possui complexidade O(log n).
        """
        steps = 0
        bucket = self._table[index]
        low, high = 0, len(bucket) - 1
    
        while low <= high:
            steps += 1
            mid = (low + high) // 2
            mid_key = bucket[mid][0]
    
            if mid_key == key:
                return mid, steps
            elif mid_key < key:
                low = mid + 1
            else:
                high = mid - 1
        
        # Se não encontrado, 'low' é o ponto de inserção
        return low, steps

    def _linear_search(self, index, key):
        """Retorna (position, steps). position é -1 se não encontrado."""
        bucket = self._table[index]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                return i, i + 1
        return -1, len(bucket)
    
    def _insert_statistics(self, index, key):
        slot_stats = self._stats[index]
        slot_stats.length += 1
        if slot_stats.length > self._max_len:
            self._max_len = slot_stats.length
            
        if slot_stats.min_key is None or key < slot_stats.min_key:
            slot_stats.min_key = key
        if slot_stats.max_key is None or key > slot_stats.max_key:
            slot_stats.max_key = key
        
    def _remove_statistics(self, index, key):
        slot_stats = self._stats[index]
        
        curr_length = slot_stats.length
        slot_stats.length -= 1
        if curr_length == self._max_len:
            # Se o bucket que foi reduzido era o mais longo, recalcule
            self._max_len = max(s.length for s in self._stats) if self._size > 0 else 0            
        
        # Recalcular min/max se a chave removida era um extremo
        if slot_stats.length == 0:
            slot_stats.min_key = None
            slot_stats.max_key = None
        elif key == slot_stats.min_key:
            slot_stats.min_key = min(k[0] for k in self._table[index])
        elif key == slot_stats.max_key:
            slot_stats.max_key = max(k[0] for k in self._table[index])

        
        
    # ===================================================================
    # UTILITÁRIOS
    # ===================================================================

    # ...
            
    # ===================================================================
    
    # ===================================================================
    


    # ===================================================================
    # NOVOS MÉTODOS ABSTRATOS PARA AS SUBCLASSES
    # ===================================================================
    
    @abstractmethod
    def _get_bucket_index(self, key:str):
        raise NotImplementedError
        
    
    # ===================================================================
    # IMPLEMENTAÇÃO DE MÉTODOS ABSTRATOS DA BASE
    # ===================================================================

    # --- Métodos auxiliares/helpers (não decorados) --------------------------

    def _set_capacity(self, capacity):
        if self._use_prime_capacity:
            if is_prime_number(capacity):
                self._capacity = capacity
            else:
                self._capacity = later_prime_number(capacity)
        else:
            self._capacity = capacity
                
    def _get_table(self):
        if self._table is None:
            self._table = [[] for _ in range(self._capacity)]

        return self._table
            
    def _get_stats(self):
        if self._stats is None:
            self._stats = [BucketStats() for _ in range(self._capacity)]
        
        return self._stats

    def _update_slot_metrics(self, index, operation, metrics_data):
        slot_stats = self._stats[index]
        
        for var, value in metrics_data.items():
            slot_stats.metrics[operation][var].append(value)
            slot_stats.metrics['total'][var].append(value)


    # --- Métodos de suporte --------------------------------------------------
        
    def __iter__(self):
        """Itera sobre todos os pares (chave, valor) na tabela."""
        for bucket in self.table:
            for key, value in bucket:
                yield (key, value)


    # --- Métodos de análise e estatística de buckets -------------------------
    
    
    def max_length(self):
        """Retorna o comprimento do bucket mais longo."""
        # Esta implementação é O(1), mas requer recalcular _max_len na remoção.
        # Uma alternativa mais robusta seria: return max(s.length for s in self._stats) if self._size > 0 else 0
        return self._max_len

    def min_length(self):
        """Retorna o comprimento do bucket mais curto entre os que não estão vazios."""
        # Esta implementação é O(1), mas requer recalcular _min_len na remoção.
        # Alternativa: return min(s.length for s in self._stats if s.length > 0) if self._size > 0 else 0
        return self._min_len


    def empty(self):
        """Retorna os buckets vazios, None ou marcados com self._deleted."""
        return [(i, k) for i, k in enumerate(self._table) if len(k) == 0]
        
    def filled(self):
        """Retorna os buckets que contêm pelo menos um elemento."""
        # É mais eficiente calcular baseado no número de buckets com comprimento > 0
        # do que iterar. Para isso, precisaríamos de um contador adicional.
        # A forma abaixo é O(Capacidade), mas é a mais simples sem contadores extras.
        return [(i, k) for i, k in enumerate(self._table) if len(k) > 0]
    
    def min_filled_length(self):
        """
        Retorna o comprimento do menor bucket preenchido (não vazio).
        Um valor de 1 é o ideal.
        """        
        if self._size == 0:
            return 0
        
        # Usa uma generator expression para encontrar o comprimento mínimo
        # apenas entre os buckets que têm comprimento > 0.
        # É O(Capacidade), mas sempre preciso.
        return min(s.length for s in self._stats if s.length > 0)
    
    def _sum_of_squares(self):
        """Retorna a soma dos quadrados dos desvios da média."""
        c = self.avg_length()
        ss = sum((len(k) - c)**2 for k in self._table)
        return ss
    
    def count(self):
        """
        Conta a quantidade de elementos em todos os buckets.
        Essa informação pode ser obtida mais rapidamente com self.size.
        """
        return sum([len(k[1]) for k in self.filled()])
    