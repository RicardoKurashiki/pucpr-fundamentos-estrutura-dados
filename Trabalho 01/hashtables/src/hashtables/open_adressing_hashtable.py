# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 20:37:00 2025
@author: Uendel A Rocha (2025)
"""
from abc import abstractmethod
from base_hashtable import BaseHashTable, profile_operation, operations, variables
from prime_numbers import is_prime_number, later_prime_number
import math

class OpenAddressingHashTable(BaseHashTable):
    def __init__(self, capacity, **kwargs):
        super().__init__(capacity, **kwargs)
        
        # RESPONSABILIDADE MOVIDA: A criação da tabela e estatísticas agora é
        # responsabilidade das classes filhas concretas.
        self._table = None
        self._stats = None
        
        # Marcador especial (tombstone) continua sendo uma ótima prática.
        self._deleted = object()
        
    # ===================================================================
    # MÉTODOS PÚBLICOS DE OPERAÇÃO (DECORADOS)
    # LÓGICA CENTRALIZADA AQUI PARA EVITAR DUPLICAÇÃO
    # ===================================================================

    @profile_operation('insert')
    def insert(self, key, value):
        steps = 0
        # CORRIGIDO: Verificação do fator de carga e chamada de resize.
        if self._get_load_factor() >= self.max_load_factor:
            new_capacity = math.ceil(self._capacity * self._growth_factor)
            # O resize já é decorado e retorna seus próprios steps.
            _, resize_steps, _ = self.resize(new_capacity)
            steps += resize_steps
        
        # Usa o helper interno para a inserção real.
        index, insert_steps, result = self._internal_insert(key, value)
        steps += insert_steps
        
        return index, steps, result

    @profile_operation('search')
    def search(self, key):
        steps = 0

        for i in range(self._capacity):
            index, steps_probe = self._probe(key, i)
            steps += steps_probe
            slot = self._table[index]

            if slot is None:
                # Se encontramos um slot vazio, a chave não existe.
                return index, steps, None

            if slot is not self._deleted and slot[0] == key:
                # Chave encontrada.
                return index, steps, slot[1]
        
        # Chave não encontrada após percorrer toda a tabela.
        return None, steps, None

    @profile_operation('remove')
    def remove(self, key):
        steps = 0
        for i in range(self._capacity):
            index, steps_probe = self._probe(key, i)
            steps += steps_probe
            slot = self._table[index]

            if slot is None:
                # A chave não existe na tabela.
                return index, steps, False

            if slot is not self._deleted and slot[0] == key:
                self._table[index] = self._deleted
                self._size -= 1
                # self._remove_statistics(index, key) # Implementação opcional
                return index, steps, True
        
        return None, steps, False
        
    @profile_operation('resize')
    def resize(self, new_capacity:int):
        steps = 0
        
        old_table = self._table
        self._set_capacity(new_capacity)
        
        # Recria a tabela e as estatísticas com a nova capacidade.
        self._table = self._get_table()
        self._stats = self._get_stats()
        self._size = 0
        steps += (2 * self._capacity)

        # Re-insere todos os elementos usando a lógica interna "silenciosa".
        for item in old_table:
            if item is not None and item is not self._deleted:
                key, value = item
                _, insert_steps, _ = self._internal_insert(key, value)
                steps += insert_steps
        
        return None, steps, None

    # ===================================================================
    # HELPERS (CENTRALIZADOS E NÃO DECORADOS)
    # ===================================================================

    def _internal_insert(self, key, value):
        steps = 0
        first_slot_deleted = None
        index_to_insert = -1

        for i in range(self._capacity):
            index, steps_probe  = self._probe(key, i)
            steps += steps_probe
            slot = self._table[index]

            # Caso 1: A chave já existe, atualiza o valor.
            if slot is not None and slot is not self._deleted and slot[0] == key:
                self._table[index] = (key, value)
                return index, steps, (index, value)

            # Guarda o primeiro slot deletado para reutilização.
            if slot is self._deleted and first_slot_deleted is None:
                first_slot_deleted = index

            # Se encontramos um slot vazio, este é o local de inserção.
            if slot is None:
                index_to_insert = first_slot_deleted if first_slot_deleted is not None else index
                break
        
        # Se o loop terminou sem encontrar um slot vazio (tabela cheia),
        # ainda podemos ter um slot deletado para usar.
        if index_to_insert == -1 and first_slot_deleted is not None:
            index_to_insert = first_slot_deleted

        self._table[index_to_insert] = (key, value)
        self._size += 1
        # self._insert_statistics(index_to_insert, key) # Implementação opcional
        
        return index_to_insert, steps, (index_to_insert, value)

    # ===================================================================
    # IMPLEMENTAÇÃO DE MÉTODOS ABSTRATOS DA BASE
    # ===================================================================
    
    def _set_capacity(self, capacity):
        self._capacity = capacity if is_prime_number(capacity) else later_prime_number(capacity)
    
    def _get_table(self):
        # Retorna uma nova tabela se não existir
        return [None] * self._capacity
        
    def _get_stats(self):
        # Retorna uma nova estrutura de stats se não existir
        return [{o: {v: [] for v in variables} for o in operations}] * self._capacity

    def _update_slot_metrics(self, index, operation, metrics_data):
        slot_stats = self._stats[index]
        for var, value in metrics_data.items():
            slot_stats[operation][var].append(value)
            slot_stats['total'][var].append(value)
            
    def __iter__(self):
        """Itera sobre todos os pares (chave, valor) na tabela."""
        for slot in self.table:
            if slot is not None and slot is not self._deleted:
                key, value = slot
                yield (key, value)
                
    def empty(self):
        """Retorna os buckets vazios, None ou marcados com self._deleted."""
        return [(i, x) for i, x in enumerate(self._table) if x is None or x is self._deleted]

    def filled(self):
        """Retorna os buckets que contêm pelo menos um elemento."""
        # É mais eficiente calcular baseado no número de buckets com comprimento > 0
        # do que iterar. Para isso, precisaríamos de um contador adicional.
        # A forma abaixo é O(Capacidade), mas é a mais simples sem contadores extras.
        # VERIFICAR SE REMOVIDOS PODE SER ENCARADO COMO FILLED (PREEENCHIDO)
        return [(i, x) for i, x in enumerate(self._table) if x is not None and x is not self._deleted]


    def _sum_of_squares(self):
        """Retorna a soma dos quadrados dos desvios da média."""
        c = self.avg_length()
        ss = 0
        for x in self._table:
            if x is not None and x is not self._deleted:
                ss += (1 - c) ** 2
            else:
                ss += (0 - c) ** 2
        return ss


    # ===================================================================
    # NOVOS MÉTODOS ABSTRATOS PARA AS SUBCLASSES
    # ===================================================================
    
    @abstractmethod
    def _primary_hash(self, key: str):
        """Calcula o índice inicial (hash primário)."""
        raise NotImplementedError

    @abstractmethod
    def _probe(self, key: str, attempt: int):
        """Calcula o índice para a i-ésima tentativa de sondagem."""
        raise NotImplementedError
        