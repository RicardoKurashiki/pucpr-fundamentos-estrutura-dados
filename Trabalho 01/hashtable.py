class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # cada posição tem uma lista (encadeamento)

    def hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def search(self, key):
        index = self.hash_function(key)
        search_steps = 0
        for pair in self.table[index]:
            search_steps += 1
            if pair[0] == key:
                return pair[1], {'Search Steps': search_steps}
        return None, {'Search Steps': search_steps}

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")

if __name__ == "__main__":
    hash_table = HashTable(100)  # tabela de tamanho 10
    hash_table.insert(100, "Alice")
    hash_table.insert(232, "Bob")
    hash_table.insert(335, "Charlie")
    hash_table.insert(900, "Diana")

    print("\nBusca por chave 232:", hash_table.search(232))
    print("Busca por chave 100:", hash_table.search(100))
    print("\nBusca por chave 232:", hash_table.search(600))

    print("Tabela Hash:")
    hash_table.display()

