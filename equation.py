from brackets import *
from number import *
from infix import *
from postfix import *

class Equation:
  def __init__(self, start):
    self.completed = False
    self.symbols = [Number(start)]
  
  def append(self, symbol):
    self.symbols.append(symbol)

  def closeBrackets(self):
    while self.getOpenBrackets() > 0:
      self.symbols.append(CloseBracket())

  def complete(self):
    if not isinstance(self.top(), (OpenBracket, Operator)):
      self.closeBrackets()
      self.completed = True
    return self.completed

  def getRecent(self):
    return self.solve() if self.completed else self.getPrevNumber()
  
  def getOpenBrackets(self):
    open = 0
    for symbol in self.symbols:
      if isinstance(symbol, OpenBracket):
        open += 1
      elif isinstance(symbol, CloseBracket):
        open -= 1
    return open

  def getPrevNumber(self):
    for i in range(len(self.symbols) - 1, -1, -1):
      if isinstance(self.symbols[i], Number):
        return self.symbols[i]
    raise Exception("No Number found in equation.")

  def getSymbols(self):
    return self.symbols

  def isEmpty(self):
    return not self.symbols

  def pop(self):
    popped = self.symbols.pop()
    if self.isEmpty():
      self.append(Number(None))
    return popped
  
  def setTop(self, current):
    self.symbols[-1] = current

  def solve(self):
    if self.completed:
      infix = Infix(self)
      postfix = Postfix(infix)
      return postfix.tree.evaluate()
    raise Exception("Incomplete Equation cannot be solved")

  def top(self):
    return self.symbols[-1]

  def __str__(self):
    text = "".join(map(str, self.symbols))
    if self.completed:
      text += "="
    return text