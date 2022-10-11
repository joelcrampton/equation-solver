# Pseudo code: infix-to-postfix.pdf
# Works for operators: '+', '-', '*' and '/'

precedence = {
  '+': 1,
  '-': 1,
  '*': 2,
  '/': 2
}

def isOperand(symbol):
  return type(symbol) == float or type(symbol) == int

class Infix:
  def __init__(self, equation):
    self.symbols = self.split(equation)

  def split(self, equation):
    output = []
    i = 0
    while i < len(equation):
      value = equation[i]
      if value.isdigit(): # Operand
        while True:
          if i == len(equation) - 1: # Break loop if last symbol
            break
          next = equation[i + 1]
          if next.isdigit() == False and next != '.': # Break loop if next symbol is not a digit or '.'
            break
          i += 1
          value += next
        value = int(value) if value.isdigit() else float(value) # Cast to int or float
      output.append(value)
      i += 1
    return output

  def __str__(self):
    formatted = ' '.join(map(str, self.symbols)) # Have to map all symbols to strings before joining
    formatted = formatted.replace('( ', '(') # Remove spaces after open bracket
    formatted = formatted.replace(' )', ')') # Remove spaces before closing bracket
    return formatted


class Postfix:
  def __init__(self, infix):
    self.symbols = self.convert(infix)

  # Convert infix to postfix
  def convert(self, infix):
    stack = []
    output = []
    # Loop through symbols
    for symbol in infix.symbols:
      if isOperand(symbol): # Operand
        output.append(symbol)
      elif symbol == '(': # Open bracket
        stack.append(symbol)
      elif symbol == ')': # Closing bracket
        while stack[-1] != '(': # Pop all items before '(' from stack to output
          output.append(stack.pop())
        stack.pop() # Remove '('
      else: # Operators
        if(len(stack) > 0): # Proceed if stack is not empty
          # Pop greater or equal precedence items from stack to output
          while stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(symbol):
            output.append(stack.pop())
            if(len(stack) == 0): # Break if stack is empty
              break
        stack.append(symbol) # Push operator to stack

    while len(stack) > 0: # Pop all remaining items from stack to output
      output.append(stack.pop())
    return output

  def evaluate(self):
    stack = []
    for symbol in self.symbols:
      if isOperand(symbol): # Operand
        stack.append(symbol)
      else:
        b = stack.pop()
        a = stack.pop()
        if symbol == '+':
          stack.append(a + b)
        elif symbol == '-':
          stack.append(a - b)
        elif symbol == '*':
          stack.append(a * b)
        elif symbol == '/':
          stack.append(a / b)
    return stack[0]

  def __str__(self):
    return ' '.join(map(str, self.symbols)) # Have to map all symbols to strings before joining

infix = Infix('3*(52+4)-18')
postfix = Postfix(infix)
print('Infix: ' + infix.__str__())
print('Postfix: ' + postfix.__str__())
print(infix.__str__() + ' = ' + str(postfix.evaluate()))