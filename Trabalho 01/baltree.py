

class BalNode:
  def __init__(self, data) -> None:
      self.data = data
      self.rightNode = None
      self.leftNode = None
      self.height = 1

class BalTree:
  def __init__(self, data) -> None:
      self.root = BalNode(data)

  def push(self, data):

    if self.root is None:
      print("Entrei no teste do root")
      self.root = BalTree(data)

    if data >= self.root.data:
      if self.root.rightNode == None:
        self.root.rightNode = BalTree(data)
      else:
        self.root.rightNode.push(data)
    else:
      if self.root.leftNode == None:
        self.root.leftNode = BalTree(data)
      else:
        self.root.leftNode.push(data)

    print(f"{self.root.data} / {self.root}")
    left_height = self.root.leftNode.root.height if self.root.leftNode else 0
    right_height = self.root.rightNode.root.height if self.root.rightNode else 0
    self.root.height = 1 + max(left_height, right_height)

    balance = left_height - right_height

    if balance > 1 or balance < -1:
      print(f"{left_height} - {right_height} - {balance} = Desbalanceou {data} no nó {self.root.data}")

    if balance > 1 and data < self.root.leftNode.root.data:
      print("Rodando à direita")
      self.root = self.right_rotate(self.root)

    if balance < -1 and data > self.root.rightNode.root.data:
      print("Rodando à Esquerda")
      self.root = self.left_rotate(self.root)

    print(f"Terminada a inserção de {data}")

  def right_rotate(self, m):
    new_root = m.leftNode.root
    new_root.rightNode = BalTree(m.data)

    left_height = new_root.leftNode.root.height if new_root.leftNode else 0
    right_height = new_root.rightNode.root.height if new_root.rightNode else 0
    new_root.height = 1 + max(left_height, right_height)

    return new_root

  def left_rotate(self, m):
    new_root = m.rightNode.root
    new_root.leftNode = BalTree(m.data)

    left_height = new_root.leftNode.root.height if new_root.leftNode else 0
    right_height = new_root.rightNode.root.height if new_root.rightNode else 0
    new_root.height = 1 + max(left_height, right_height)

    return new_root
  def walk_in_order(self):
    if self.root.leftNode:
      self.root.leftNode.walk_in_order()
    print(f"Data: {self.root.data}, Height: {self.root.height}")
    if self.root.rightNode:
      self.root.rightNode.walk_in_order()

myTree = BalTree(50)
myTree.push(20)
myTree.push(70)
myTree.push(10)
myTree.push(40)
myTree.push(60)
#myTree.push(25)
myTree.push(42)
myTree.push(45)