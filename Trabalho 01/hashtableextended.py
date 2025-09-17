import math


# ==============================================================================
# PASSO 1: Definimos as funções de hash fora da classe, como "ferramentas"
# que a classe poderá usar.
# ==============================================================================

def modulo_hash(key, table_size):
    """Sua função original: hash baseado no operador módulo."""
    if not isinstance(key, int):
        # A versão original só funcionava para números. Adicionamos suporte
        # a outros tipos usando a função hash() nativa do Python.
        key = hash(key)
    return key % table_size


def folding_hash(key, table_size, chunk_size=2):
    """Função de hash por dobra (folding). Ideal para chaves longas."""
    key_str = str(key)
    total = 0

    # Se a chave for muito pequena, use o hash de módulo como fallback
    if len(key_str) < chunk_size:
        return modulo_hash(key, table_size)

    for i in range(0, len(key_str), chunk_size):
        chunk_str = key_str[i:i + chunk_size]
        # Garante que o chunk seja um número válido
        if chunk_str.isdigit():
            total += int(chunk_str)

    return total % table_size


def golden_ratio_hash(key, table_size):
    """Função de hash baseada na multiplicação pela razão áurea."""
    A = (math.sqrt(5) - 1) / 2  # Constante A ≈ 0.618

    # Garante que a chave seja um número para o cálculo matemático
    if not isinstance(key, (int, float)):
        key = hash(key)

    fractional_part = (key * A) % 1
    index = math.floor(table_size * fractional_part)
    return int(index)



class HashTable:
    # Adicionamos o parâmetro 'hash_function' ao construtor
    def __init__(self, size, hash_function='modulo'):
        self.size = size
        self.table = [[] for _ in range(size)]

        # Métricas internas
        self.collision_count = 0
        self._size_elements = 0 # Contador interno de elementos

        # Criamos um dicionário que mapeia o nome da função para a função real
        hash_functions = {
            'modulo': modulo_hash,
            'folding': folding_hash,
            'golden_ratio': golden_ratio_hash
        }

        # Verificamos se a função escolhida é válida
        if hash_function not in hash_functions:
            raise ValueError(
                f"Hash function '{hash_function}' not recognized. Available: {list(hash_functions.keys())}")

        # Armazenamos a FUNÇÃO a ser usada, não apenas seu nome
        self._hash_function = hash_functions[hash_function]
        print(f"-> Tabela Hash de tamanho {self.size} criada com a função de hash '{hash_function}'.")

    # Metodo privado que chama a função escolhida
    def _get_hash(self, key):
        return self._hash_function(key, self.size)

    def insert(self, key, value):
        index = self._get_hash(key)
        bucket = self.table[index]

        # Verifica se a chave já existe (caso de atualização)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket[i] = (key, value)  # Atualiza o valor
                return

        # --- LÓGICA DE CONTAGEM DE COLISÃO ---
        # Se o bucket não estava vazio e a chave é nova, é uma colisão.
        if len(bucket) > 0:
            self.collision_count += 1

        bucket.append((key, value))
        self._size_elements += 1

    def search(self, key):
        index = self._get_hash(key)
        search_steps = 0
        for pair in self.table[index]:
            search_steps += 1
            if pair[0] == key:
                return pair[1], {'Search Steps': search_steps}
        return None, {'Search Steps': search_steps + 1}

    def get_structural_metrics(self):
        """
        Calcula e retorna um dicionário com métricas estruturais da tabela.
        """
        if self.size == 0:
            return {}

        bucket_lengths = [len(bucket) for bucket in self.table]
        non_empty_buckets = [length for length in bucket_lengths if length > 0]

        metrics = {
            'Load Factor': self._size_elements / self.size,
            'Total Collisions': self.collision_count,
            'Max Bucket Size': max(bucket_lengths) if bucket_lengths else 0,
            'Min Bucket Size (non-empty)': min(non_empty_buckets) if non_empty_buckets else 0,
            'Empty Buckets': bucket_lengths.count(0)
        }
        return metrics

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")


# ==============================================================================
# PASSO 3: Demonstração do uso das diferentes funções.
# ==============================================================================
if __name__ == "__main__":
    # Nossos dados de teste
    data = {
        100: "Alice",
        232: "Bob",
        335: "Charlie",
        900: "Diana",
        432: "Eve",
        567: "Frank",
        12345678: "George"  # Uma chave longa para testar o folding
    }

    print("\n----- Usando 'modulo' hash -----")
    ht_modulo = HashTable(10, hash_function='modulo')
    for key, value in data.items():
        ht_modulo.insert(key, value)
    ht_modulo.display()

    print("\n----- Usando 'folding' hash -----")
    ht_folding = HashTable(10, hash_function='folding')
    for key, value in data.items():
        ht_folding.insert(key, value)
    ht_folding.display()

    print("\n----- Usando 'golden_ratio' hash -----")
    ht_golden = HashTable(10, hash_function='golden_ratio')
    for key, value in data.items():
        ht_golden.insert(key, value)
    ht_golden.display()

    print("\n--- Teste de Busca ---")
    print("Buscando pela chave 900 na tabela 'golden_ratio':", ht_golden.search(900))
    print("Buscando por chave inexistente 999:", ht_golden.search(999))