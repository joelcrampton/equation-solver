from infix import *
from nodes import *

class Postfix:
  def __init__(self, infix):
    if not isinstance(infix, Infix):
      raise Exception("Invalid argument. Postfix() must take 1 Infix object argument")
    self.symbols = self.convert(infix)
    self.tree = self.build()

  def build(self):
    stack = []
    for symbol in self.symbols:
      if isinstance(symbol, Number): # Number
        stack.append(NumberNode(symbol.result()))
      else: # Operator
        b = stack.pop()
        a = stack.pop()
        if isinstance(symbol, Add):
          stack.append(AddNode(a, b))
        elif isinstance(symbol, Subtract):
          stack.append(SubtractNode(a, b))
        elif isinstance(symbol, Multiply):
          stack.append(MultiplyNode(a, b))
        elif isinstance(symbol, Divide):
          stack.append(DivideNode(a, b))
        elif isinstance(symbol, Exponent):
          stack.append(ExponentNode(a, b))
    return stack[0]

  def convert(self, infix):
    stack = []
    output = []
    for symbol in infix.symbols:
      if isinstance(symbol, Number): # Number
        output.append(symbol)
      elif isinstance(symbol, OpenBracket): # OpenBracket
        stack.append(symbol)
      elif isinstance(symbol, CloseBracket): # CloseBracket
        while type(stack[-1]) is not OpenBracket: # Pop all items before OpenBracket from stack to output
          output.append(stack.pop())
        stack.pop() # Remove open bracket
      else: # Operator
        if(len(stack) > 0): # Proceed if stack is not empty
          # Pop items before OpenBracket from stack to output
          while type(stack[-1]) is not OpenBracket:
            if isinstance(stack[-1], Operator):
              if stack[-1].precedence < symbol.precedence: # Break if item lower precedence 
                break
            output.append(stack.pop())
            if len(stack) == 0: # Break if stack is empty
              break
        stack.append(symbol) # Push operator to stack
    while len(stack) > 0: # Pop all remaining items from stack to output
      output.append(stack.pop())
    return output

  def __str__(self):
    return " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining