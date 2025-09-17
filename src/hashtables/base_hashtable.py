# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 00:34:29 2025

@author: Uendel A Rocha (2025)
"""

from abc import ABC, abstractmethod
import os, tracemalloc
from time import perf_counter, process_time
import psutil
import math

# ===================================================================
# VARIÁVEIS
# ===================================================================

# Operações de primeira classe (atômicas)
operations = ['search', 'insert', 'remove', 'resize', 'total']

# Métricas
variables = ['steps', 'process_time', 'perf_counter', 
             'user_cpu_time', 'system_cpu_time', 
             'memory_peak_python', 'memory_delta_python', 'memory_rss_os']

# ===================================================================
# DECORADOR
# ===================================================================

def profile_operation(operation_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # -----------------------------------------------------------------
            # --- Início da Coleta --------------------------------------------
            tracemalloc.start()
            
            start_perf = perf_counter()
            start_process = process_time()
            # start_cpu = os.times() # Preterido em prol de psutil
            start_cpu = self._process.cpu_times() # Mais preciso e melhor
            
            # Desnecessário se tracemalloc é desligado ao final da coleta
            # tracemalloc.clear_traces()
            # mem_before, _ = tracemalloc.get_traced_memory()

            # --- Executa a Função Original -----------------------------------
            # Contrato: a função deve retornar (index, steps, result)
            index, steps, result = func(self, *args, **kwargs)

            # --- Fim da Coleta -----------------------------------------------
            mem_after_python, peak_mem_python = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # Captura a memória RSS do processo do S.O.
            rss_mem_os = self._process.memory_info().rss
            # -----------------------------------------------------------------
            
            # end_cpu = os.times() # Preterido em prol de psutil
            end_cpu = self._process.cpu_times()
            end_perf = perf_counter()
            end_process = process_time()

            # --- Cálculo dos Deltas ---
            elapsed_perf = end_perf - start_perf
            elapsed_process = end_process - start_process
            user_cpu_delta = end_cpu.user - start_cpu.user
            system_cpu_delta = end_cpu.system - start_cpu.system
            
            # Útil apenas se tracemalloc não for parado
            # mem_delta = mem_after - mem_before
            
            mem_delta_python = mem_after_python
            # 'memory_peak_python', 'memory_delta_python', 'memory_rss_os'
            # --- Atualiza as Métricas ---
            self._record_metrics(operation_name, index, steps, 
                                 elapsed_process, elapsed_perf,
                                 user_cpu_delta, system_cpu_delta, 
                                 peak_mem_python, mem_delta_python, rss_mem_os)

            return result
        return wrapper
    return decorator



class BaseHashTable(ABC):
    def __init__(self, capacity:int, **kwargs):
        
        """
        Inicializa a HashTable com configurações granulares.
    
        Hiperparâmetros (via kwargs):
            - use_prime_capacity (bool): Se True, ajusta a capacidade para um número primo.
            - key_hashing_strategy (str): 'simple_sum' ou 'positional'.
            - bucket_strategy (str): 'append' (busca linear) ou 'sorted' (busca binária).
            - auto_shrinking (bool): Recomendado que seja False
            - ... outros parâmetros ...
        """        
        
        # Define as configurações padrão (não otimizadas)
        config = {
            'use_prime_capacity': False,
            'key_hashing_strategy': 'simple_sum',
            'bucket_strategy': 'append',
            'auto_shrinking': False,
            'folding_block_strategy': 'fixed',
        }
        
        # Se o preset 'optimized=True' for passado, ele sobrescreve os padrões
        if kwargs.get('optimized') is True:
            config.update({
                'use_prime_capacity': True,
                'key_hashing_strategy': 'positional',
                'bucket_strategy': 'sorted',
                'auto_shrinking': False,
                'folding_block_strategy': 'dynamic',
            })
            
        # Permite que o usuário sobrescreva qualquer configuração individualmente
        config.update(kwargs)
    
        # Armazena as configurações finais
        self._use_prime_capacity = config['use_prime_capacity']
        self._key_hashing_strategy = config['key_hashing_strategy']
        self._bucket_strategy = config['bucket_strategy']
        self._auto_shrinking = config['auto_shrinking']
        self._folding_block_strategy = config['folding_block_strategy']
        
        # ... inicialização básica de métricas ...
        self.reset_global_metrics()
        
        # --- Configurações básicas de funcionamento da classe ---
        self._capacity = capacity # Quantidade de buckets na hashtable
        self._size = 0  # Quantidade total de elementos na tabela inteira
        self._table = None
        self._stats = None
        self._growth_factor = 1.5 # Fator de crescimento da capacidade (resize)
        self._shrink_factor = 0.5 # Fator de redução da capacidade (resize)
        self._max_load_factor = 0.75
        self._min_load_factor = 0.25
        
        # --- Variáveis para estatísticas e métricas
        self._min_key = self._max_key = None
        
        self._process = psutil.Process(os.getpid())
        
        # ALTERAÇÃO: CLASSE NÃO INICIARÁ O MOTOR DE RASTREAMENTO DE MEMÓRIA
        # Ele será iniciado e parado no profile de cada operação
        # tracemalloc.start() # Inicia o rastreamento de memória para a instância
        
        
    # ===================================================================
    # SEÇÃO DE MÉTRICAS
    # ===================================================================

    def reset_global_metrics(self):
        self._metrics = {o: {v: [] for v in variables} for o in operations}

    def _record_metrics(self, operation, index, steps, 
                        process_time, perf_counter, 
                        user_cpu_time, system_cpu_time, 
                        memory_peak_python, memory_delta_python, 
                        memory_rss_os):
        # Cria o dicionário dinamicamente usando eval
        # metrics_data = {var: eval(var) for var in variables}
        # Mapeamento explícito, mais seguro e claro que eval()
        metrics_data = {
            'steps': steps, 'process_time': process_time, 'perf_counter': perf_counter,
            'user_cpu_time': user_cpu_time, 'system_cpu_time': system_cpu_time,
            'memory_peak_python': memory_peak_python, 
            'memory_delta_python': memory_delta_python,
            'memory_rss_os': memory_rss_os,
        }
        
        # 1. Atualiza as métricas GLOBAIS
        for var, value in metrics_data.items():
            self._metrics[operation][var].append(value)
            self._metrics['total'][var].append(value)

        # Atualiza métricas do BUCKET/SLOT (se index for válido)
        if index is not None:
            self._update_slot_metrics(index, operation, metrics_data)
            
            # COMENTADO POIS CADA SUBCLASSE SERÁ RESPONSÁVEL PELA IMPLEMENTAÇÃO
            # CÓDIGO CAUSA FORTE ACOMPLAMENTO
            # slot_stats = self._stats[index]
            
            # # Se for a estrutura da SeparateChainingHashTable (com BucketStats)
            # if hasattr(slot_stats, 'metrics'):
            #     for var, value in metrics_data.items():
            #         slot_stats.metrics[operation][var].append(value)
            #         slot_stats.metrics['total'][var].append(value)
            # # Se for a estrutura de Endereçamento Aberto (dicionário direto)
            # else:
            #     for var, value in metrics_data.items():
            #         slot_stats[operation][var].append(value)
            #         slot_stats['total'][var].append(value)
                
    # ===================================================================
    # OPERAÇÕES DE PRIMEIRA CATEGORIA (FUNÇÕES ABSTRATAS)
    # ===================================================================
    
    # Métodos que todas as tabelas devem implementar
    @abstractmethod
    def insert(self, key, value):
        raise NotImplementedError
    
    @abstractmethod
    def search(self, key):
        raise NotImplementedError

    @abstractmethod
    def remove(self, key):
        raise NotImplementedError
        
    @abstractmethod
    def resize(self, new_capacity):
        """
        Redimensiona a tabela hash para uma nova capacidade.
        Esta é uma operação custosa que envolve a recriação da tabela
        e o rehashing de todos os elementos existentes.
        """
        raise NotImplementedError
        

    # ===================================================================
    # HELPERS (FUNÇÕES AUXILIARES)
    # ===================================================================

    # --- Funções abstratas  --------------------------------------------------

    @abstractmethod
    def _get_table(self):
        raise NotImplementedError

    @abstractmethod
    def _get_stats(self):
        raise NotImplementedError
        
    @abstractmethod
    def _set_capacity(self, capacity:int):
        raise NotImplementedError
        
    @abstractmethod
    def _update_slot_metrics(self, index, operation, metrics_data):
        raise NotImplementedError        
        

    # --- Métodos de suporte --------------------------------------------------

    def _key_to_numkey(self, key: str):
        """
        Converte uma chave para um valor numérico.
        RETORNA: Uma tupla (numeric_key, steps_count).
        """
        steps = 0
        if not isinstance(key, str):
            key = str(key)
            steps += 1 # Custo da conversão de tipo
            
        if self._key_hashing_strategy == 'positional':
            num_key = sum(ord(char) * (i + 1) for i, char in enumerate(key))
            steps += 2 * len(key) # 1 para a multiplicação/soma, 1 para o ord()
        else:
            num_key = sum(ord(char) for char in key)
            steps += 1 * len(key) # 1 para a soma/ord()
            
        return num_key, steps
        

    def _get_load_factor(self):
        if self._capacity > 0:
            return self._size / self._capacity
        return 0
    
    def __len__(self):
        return self._size
    
    @abstractmethod
    def __iter__(self):
        """Deve retornar um iterador sobre os pares (chave, valor) da tabela."""
        raise NotImplementedError    
    
    # --- Estatísticas e métricas

    @abstractmethod    
    def max_length(self):
        """Retorna o comprimento do bucket mais longo."""
        # Esta implementação é O(1), mas requer recalcular _max_len na remoção.
        # Uma alternativa mais robusta seria: return max(s.length for s in self._stats) if self._size > 0 else 0
        raise NotImplementedError        

    @abstractmethod    
    def min_length(self):
        """Retorna o comprimento do bucket mais curto entre os não vazios."""
        # Esta implementação é O(1), mas requer recalcular _min_len na remoção.
        # Alternativa: return min(s.length for s in self._stats if s.length > 0) if self._size > 0 else 0
        raise NotImplementedError        


    @abstractmethod
    def empty(self):
        """Retorna os buckets vazios, None ou marcados com self._deleted."""
        raise NotImplementedError        


    def avg_length(self):
        """Retorna o comprimento médio dos buckets (load factor)."""
        return self._get_load_factor()


    def calc_empty(self):
        """Calcula o número de buckets/slots vazios."""
        return self._capacity - self.count_filled()
    
    def count_empty(self):
        """Conta o número de buckets vazios."""
        return len(self.empty())


    @abstractmethod
    def count(self):
        """
        Conta a quantidade de elementos em todos os buckets.
        Essa informação pode ser obtida mais rapidamente com self.size.
        """
        raise NotImplementedError    
    
    
    def flat(self):
        """
        Cria uma lista contendo todos os elementos (pares chave-valor) 
        da hashtable
        """
        return list(self)
    
    
    
    # --- MÉTODOS DE ANÁLISE (templates concretos)


    # Template Method: A lógica é universal, mas depende de filled().
    def avg_filled(self):
        """
        Calcula o comprimento médio APENAS dos buckets/slots não vazios.
        Esta métrica é um excelente indicador da qualidade da função de hash,
        revelando o nível de clustering (agrupamento) de colisões.
        """
        filled_buckets = self.count_filled() # Usa o método já existente
        if filled_buckets > 0:
            return self._size / filled_buckets
        return 0


    # Template Method: A lógica é universal, mas depende de filled().
    def count_filled(self):
        """  
        Conta o número de buckets/slots preenchidos.
        """
        return len(self.filled())
    
    # Template Method: A fórmula da variância é universal.
    def variance(self, dof = 0):
        """Calcula a variância do comprimento dos buckets."""        
        n = self._capacity
        if n < (1 + dof):
            return 0
        
        # Delega o cálculo específico para o método abstrato _sum_of_squares            
        ss = self._sum_of_squares()
        return ss / (n - dof)
    

    # Template Method: A fórmula do desvio padrão é universal.
    def stddev(self, dof = 0):
        """
        Calcula o desvio padrão do comprimento dos buckets.
        Utiliza o cálculo sobre a população como default (dof=0).
        Caso queira calcular sobre uma amostra, informe dof=1.
        Um desvio padrão baixo é o sinal de uma excelente função hash, 
        que está distribuindo as chaves de forma uniforme.
        """        
        return self.variance(dof) ** 0.5


    # --- MÉTODOS PRIMITIVOS (Hooks Abstratos) ---
    
    
    @abstractmethod
    def filled(self):
        """Retorna os buckets que contêm pelo menos um elemento."""
        # É mais eficiente calcular baseado no número de buckets com comprimento > 0
        # do que iterar. Para isso, precisaríamos de um contador adicional.
        # A forma abaixo é O(Capacidade), mas é a mais simples sem contadores extras.
        raise NotImplementedError        
    

    @abstractmethod
    def _sum_of_squares(self):
        """Retorna a soma dos quadrados dos desvios da média."""
        raise NotImplementedError        

        
    # ===================================================================
    # PROPRIEDADES
    # ===================================================================
    
    @property
    def load_factor(self):
        return self._get_load_factor()
    
    @property
    def max_load_factor(self):
        return self._max_load_factor
    
    @max_load_factor.setter
    def max_load_factor(self, value:float):
        if self._min_load_factor < value <= 1.00:
            self._max_load_factor = value
        else:
            raise ValueError(f'Valor deve estar entre {self._min_load_factor} e 1.00')
        
    @property
    def min_load_factor(self):
        return self._min_load_factor
    
    @min_load_factor.setter
    def min_load_factor(self, value:float):
        if 0.00 <= value < self._max_load_factor:
            self._min_load_factor = value
        else:
            raise ValueError(f'Valor deve estar entre 0.00 e {self._min_load_factor}')
            
    @property
    def growth_factor(self):
        return self._growth_factor

    @growth_factor.setter
    def growth_factor(self, value):
        if value < 1.5:
            raise ValueError("O fator de crescimento deve ser no mínimo 1.5")
        self._growth_factor = value

    @property
    def shrink_factor(self):
        return self._shrink_factor

    @shrink_factor.setter
    def shrink_factor(self, value):
        if not (0 < value <= 0.5):
            raise ValueError("O fator de redução deve ser maior do que 0 (zero) e menor ou igual a 0.5")
        self._shrink_factor = value

    @property
    def metrics(self):
        return self._metrics
        
    @property
    def length(self):
        return self._size
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def table(self):
        return self._get_table()
    
    @property
    def stats(self):
        return self._get_stats()
    
    @property
    def size(self):
        return self._size
    
    @property
    def pid(self):
        return self._process
    
    
    # ===
    # UTILITÁRIOS
    # ===
    
    def shrink_to_fit(self):
        """
        Redimensiona a tabela para a capacidade ideal baseada no número
        atual de elementos, liberando memória não utilizada.
        """
        # Calcula a capacidade que teria se estivesse no limite do fator de carga
        if self._size == 0:
            ideal_capacity = 1 # Ou uma capacidade mínima padrão
        else:
            ideal_capacity = math.ceil(self._size / self._max_load_factor)
        
        # Só redimensiona se a mudança for significativa
        if ideal_capacity < self._capacity:
            self.resize(ideal_capacity)    
    
    def info(self):
    
        info = {
            'class_name': self.__class__.__name__,
            'use_prime_capacity': self._use_prime_capacity,
            'key_hashing_strategy': self._key_hashing_strategy,
            'bucket_strategy': self._bucket_strategy,
            'auto_shrinking': self._auto_shrinking,
            'folding_block_strategy': self._folding_block_strategy,
            'table_stats': {
                'capacity': self._capacity, 'size': self._size, 
                'load_factor': self.load_factor,
                'min_len': self.min_length(), 'max_len': self.max_length(), 
                'avg_len': self.avg_length,
                'variance_len': self.variance(), 'stdev_len': self.stddev(),
                'count_filled': self.count_filled(), 
                'count_empty': self.count_empty(),
                'min_filled': self.min_filled_length(),
                'avg_filled': self.avg_filled(),
                'min_key': self._min_key, 'max_key': self._max_key,
                },
            'slot_stats': {
                'length': [], 'min_key': [], 'max_key': []
                },
            'metrics': {
                'operation': [], 'metric': [],
                'sum': [], 'count': [], 'avg': [], 
                'variance': [], 'stdev': [], 
                'min': [], 'max': []
                }
            }
        
        info['slot_stats']['length']  = [k.length for k in self.stats]
        info['slot_stats']['min_key'] = [k.min_key for k in self.stats]
        info['slot_stats']['max_key'] = [k.max_key for k in self.stats]
            
        for operacao, metricas in self.metrics.items():
            for metrica, valor in metricas.items():
                if valor:
                    info['metrics']['operation'].append(operacao)
                    info['metrics']['metric'].append(metrica)
                    soma = sum(valor)
                    length = len(valor)
                    avg = soma / length
                    ss = sum((x - avg)**2 for x in valor)
                    variance = (ss / length)
                    stdev = variance ** 0.5
                    info['metrics']['sum'].append(soma)
                    info['metrics']['count'].append(length)
                    info['metrics']['avg'].append(avg)
                    info['metrics']['variance'].append(variance)
                    info['metrics']['stdev'].append(stdev)
                    info['metrics']['min'].append(min(valor))
                    info['metrics']['max'].append(max(valor))
                    
        return info