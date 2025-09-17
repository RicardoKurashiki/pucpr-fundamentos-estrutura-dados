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


# ==============================================================================
# PASSO 2: Modificamos a classe para escolher e usar uma das funções acima.
# ==============================================================================

class HashTable:
    # Adicionamos o parâmetro 'hash_function' ao construtor
    def __init__(self, size, hash_function='modulo'):
        self.size = size
        self.table = [[] for _ in range(size)]

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

    # A antiga 'hash_function' agora é um método privado que chama a função escolhida
    def _get_hash(self, key):
        return self._hash_function(key, self.size)

    def insert(self, key, value):
        # A única mudança aqui é chamar _get_hash em vez de hash_function
        index = self._get_hash(key)

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def search(self, key):
        # A única mudança aqui é chamar _get_hash em vez de hash_function
        index = self._get_hash(key)
        search_steps = 0
        for pair in self.table[index]:
            search_steps += 1
            if pair[0] == key:
                return pair[1], {'Search Steps': search_steps}
        # Adicionamos a contagem de passos mesmo se não encontrar
        return None, {'Search Steps': search_steps + 1}

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