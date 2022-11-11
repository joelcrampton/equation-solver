from operators import *

class ExpressionNode:
  parent = None
  def __init__(self, left, right):
    self.left = left
    self.right = right
    left.parent = self if isinstance(left, ExpressionNode) else None
    right.parent = self if isinstance(right, ExpressionNode) else None

class AddNode(Add, ExpressionNode):
  def __init__(self, left, right):
    super().__init__(left, right)
  
  def solve(self):
    answer = self.left.solve() + self.right.solve()
    return int(answer) if answer % 1 == 0 else float(answer)

  def __str__(self):
    content = str(self.left) + " + " + str(self.right)
    return content if self.parent is None or self.parent.precedence == self.precedence else "(" + content + ")"

class SubtractNode(Subtract, ExpressionNode):
  def __init__(self, left, right):
    super().__init__(left, right)
  
  def solve(self):
    answer = self.left.solve() - self.right.solve()
    return int(answer) if answer % 1 == 0 else float(answer)

  def __str__(self):
    content = str(self.left) + " - " + str(self.right)
    return content if self.parent is None or self.parent.precedence == self.precedence else "(" + content + ")"

class MultiplyNode(Multiply, ExpressionNode):
  def __init__(self, left, right):
    super().__init__(left, right)
  
  def solve(self):
    answer = self.left.solve() * self.right.solve()
    return int(answer) if answer % 1 == 0 else float(answer)

  def __str__(self):
    content = str(self.left) + " * " + str(self.right)
    return content if self.parent is None or isinstance(self.parent, MultiplyNode) else "(" + content + ")"

class DivideNode(Divide, ExpressionNode):
  def __init__(self, left, right):
    super().__init__(left, right)
  
  def solve(self):
    answer = self.left.solve() / self.right.solve()
    return int(answer) if answer % 1 == 0 else float(answer)
  
  def __str__(self):
    content = str(self.left) + " / " + str(self.right)
    return content if self.parent is None or isinstance(self.parent, DivideNode) else "(" + content + ")"

class ExponentNode(Exponent, ExpressionNode):
  def __init__(self, left, right):
    super().__init__(left, right)
  
  def solve(self):
    answer = self.left.solve() ** self.right.solve()
    return int(answer) if answer % 1 == 0 else float(answer)

  def __str__(self):
    content = str(self.left) + "^" + str(self.right)
    return content if self.parent is None else "(" + content + ")"

class NumberNode:
  def __init__(self, value):
    self.parent = None
    self.value = value
  
  def solve(self):
    return self.value
  
  def __str__(self):
    return str(self.value)