

class Node:
  def __init__(self, data) -> None:
      self.data = data
      self.rightNode = None
      self.leftNode = None
      self.height = 1

class AVLTree:
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

        # Calcular o fator de desbalanceamento
        balance = self._get_balance(root)

        # Caso haja desbalanceamento (|balance|>1), aplicar um dos 4 casos de rotação

        # Caso 1: Rotação Simples à Direita (Left-Left)
        if balance > 1 and key_data < self.key(root.leftNode.data):
            #print(f"Desbalanceamento Simples à Esquerda em {root.data}, aplicando Rotação à Direita.")
            return self._right_rotate(root)

        # Caso 2: Rotação Simples à Esquerda (Right-Right)
        if balance < -1 and key_data > self.key(root.rightNode.data):
            #print(f"Desbalanceamento Simples à Direita em {root.data}, aplicando Rotação à Esquerda.")
            return self._left_rotate(root)

        # Caso 3: Rotação Dupla Esquerda-Direita (Left-Right)
        if balance > 1 and key_data > self.key(root.leftNode.data):
            #print(f"Desbalanceamento LR em {root.data}, aplicando Rotação Esquerda-Direita.")
            root.leftNode = self._left_rotate(root.leftNode)
            return self._right_rotate(root)

        # Caso 4: Rotação Dupla Direita-Esquerda (Right-Left)
        if balance < -1 and key_data < self.key(root.rightNode.data):
            # print(f"Desbalanceamento RL em {root.data}, aplicando Rotação Direita-Esquerda.")
            root.rightNode = self._right_rotate(root.rightNode)
            return self._left_rotate(root)

        # Retorna o nó (potencialmente nova raiz da subárvore)
        return root

    def _left_rotate(self, z):
        """Executa a rotação à esquerda na subárvore com raiz em z."""
        y = z.rightNode
        T2 = y.leftNode

        # Realiza a rotação
        y.leftNode = z
        z.rightNode = T2

        # Atualiza as alturas (a ordem importa: primeiro o filho, depois o novo pai)
        z.height = 1 + max(self._get_height(z.leftNode), self._get_height(z.rightNode))
        y.height = 1 + max(self._get_height(y.leftNode), self._get_height(y.rightNode))

        # Retorna a nova raiz da subárvore
        return y

    def _right_rotate(self, z):
        """Executa a rotação à direita na subárvore com raiz em z."""
        y = z.leftNode
        T2 = y.rightNode

        # Realiza a rotação
        y.rightNode = z
        z.leftNode = T2

        # Atualiza as alturas
        z.height = 1 + max(self._get_height(z.leftNode), self._get_height(z.rightNode))
        y.height = 1 + max(self._get_height(y.leftNode), self._get_height(y.rightNode))

        # Retorna a nova raiz da subárvore
        return y

    def _get_height(self, root):
        """Retorna a altura de um nó (0 se for nulo)."""
        if not root:
            return 0
        return root.height

    def _get_balance(self, root):
        """Retorna o fator de balanceamento de um nó."""
        if not root:
            return 0
        return self._get_height(root.leftNode) - self._get_height(root.rightNode)

    def _walk_in_order(self, root):
        """Percorre a subárvore em ordem (esquerda, raiz, direita)."""
        if not root:
            return

        self._walk_in_order(root.leftNode)
        print(f"Data: {root.data}, Height: {root.height}", end=" | ")
        self._walk_in_order(root.rightNode)

    def search(self, data):
        """Busca um dado na árvore, se encontra retorna o dado, senão None."""

        # O metodo search retorna uma Variável auxiliar para medir a profundidade da busca, que equivale a número de passos até encontrar o valor
        node, steps = self._search(self.root, data)
        return (node.data, steps) if node else (None, steps)

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
    myTree = AVLTree()
    myTree.insert(10)
    myTree.insert(2)
    myTree.insert(11)
    myTree.insert(15)
    myTree.insert(8)
    myTree.insert(5)

    myTree = AVLTree()
    myTree.insert(30)
    myTree.insert(40)
    myTree.insert(20)
    myTree.insert(10)
    myTree.insert(25)
    myTree.insert(5)
    busca = 5
    resultado, profundidade = myTree.search(busca)
    if (resultado is not None):
        print(f"Encontrado: {resultado}, profundidade: {profundidade}")
    else:
        print(f"{busca} não encontrado, profundidade: {profundidade}")
