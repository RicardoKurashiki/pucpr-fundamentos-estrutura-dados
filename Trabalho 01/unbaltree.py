

class Node:
  def __init__(self, data):
      self.data = data
      self.rightNode = None
      self.leftNode = None
      self.height = 1

class UnBalTree:
    def __init__(self, key=None):
        self.root = None
        # Se nenhuma função de chave for fornecida para indicar como obter o índice de comparação para a árvore,
        # retorna o próprio objeto, mantendo compatibilidade com dados simples como números
        self.key = key if key is not None else lambda x: x

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, root, data):
        # Inserção padrão de uma Árvore de Busca Binária
        if root is None:
            return Node(data)

        # Usamos a função self.key para indicar o dado a ser compararado. Mecanismo de generalização da árvore
        key_data = self.key(data)
        key_root = self.key(root.data)

        if key_data < key_root:
            root.leftNode = self._insert(root.leftNode, data)
        else:
            root.rightNode = self._insert(root.rightNode, data)

        # Atualizar a altura do nó "pai" atual
        root.height = 1 + max(self._get_height(root.leftNode), self._get_height(root.rightNode))

        # Retorna o nó (potencialmente nova raiz da subárvore)
        return root

    def _get_height(self, root):
        """Retorna a altura de um nó (0 se for nulo)."""
        if not root:
            return 0
        return root.height

    def _walk_in_order(self, root):
        """Percorre a subárvore em ordem (esquerda, raiz, direita)."""
        if not root:
            return

        self._walk_in_order(root.leftNode)
        print(f"Data: {root.data}, Height: {root.height}", end=" | ")
        self._walk_in_order(root.rightNode)

    def search(self, data):
        """Busca um dado na árvore, se encontra retorna o dado, senão None."""

        # O metodo search retorna uma Variável auxiliar para medir a profundidade da busca, que equivale ao número de passos até encontrar o valor
        node, steps = self._search(self.root, data)
        metrics = {'Search Depth': steps}
        return (node.data, metrics) if node else (None, metrics)

    def _search(self, root, search_key):
        """Metodo auxiliar recursivo que retorna o Nó se encontrado, caso contrário None"""
        if not root:
            return (None, 1) # Não encontrado

        key_root = self.key(root.data)

        if search_key == key_root:
            return (root, 1)

        if search_key < key_root:
            node, steps = self._search(root.leftNode, search_key)
            return (node, steps+1)
        else:
            node, steps = self._search(root.rightNode, search_key)
            return (node, steps+1)

if __name__ == "__main__":
    myTree = UnBalTree()
    myTree.insert(10)
    myTree.insert(2)
    myTree.insert(11)
    myTree.insert(15)
    myTree.insert(8)
    myTree.insert(5)

    myTree = UnBalTree()
    myTree.insert(5)
    myTree.insert(10)
    myTree.insert(20)
    myTree.insert(30)
    myTree.insert(40)
    myTree.insert(25)
    busca = 40
    resultado, profundidade = myTree.search(busca)
    if (resultado is not None):
        print(f"Encontrado: {resultado}, profundidade: {profundidade}")
    else:
        print(f"{busca} não encontrado, profundidade: {profundidade}")
