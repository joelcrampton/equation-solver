from brackets import *
from number import *
from operators import *

OPERATORS = ["+", "-", "*", "/", "^"]

def getOperator(char):
  if char == "+":
    return Add()
  if char == "-":
    return Subtract()
  if char == "*":
    return Multiply()
  if char == "/":
    return Divide()
  if char == "^":
    return Exponent()

class Infix:
  def __init__(self, input):
    try:
      self.input = None
      if isinstance(input, str): # String input
        self.input = input.replace(" ", "")
        self.symbols = self.split() # Split into symbols
      else: # Equation input
        self.symbols = input.getSymbols()
      self.check() # Check for invalid equation
      self.format() # Format symbols
    except Exception as e:
      raise Exception(e)

  def check(self):
    prev = None
    if not isinstance(self.symbols[0], Number):
      raise Exception("Invalid equation. First symbol must be a number: '" + str(self.symbols[0]) + "' at position 0")
    if not isinstance(self.symbols[-1], (Number, CloseBracket)):
      raise Exception("Invalid equation. Last symbol must be a number or close bracket: '" + str(self.symbols[-1]) + "' at position " + str(len(self.symbols) - 1))
    for i in range(len(self.symbols)):
      symbol = self.symbols[i]
      if isinstance(prev, Number):
        if isinstance(symbol, Number):
          raise Exception("Invalid equation. Number cannot be followed by another number: '" + str(symbol) + "' at position " + str(i))
      elif isinstance(prev, Operator):
        if isinstance(symbol, Operator):
          raise Exception("Invalid equation. Operator cannot be followed by another operator: '" + str(symbol) + "' at position " + str(i))
        elif isinstance(symbol, CloseBracket):
          raise Exception("Invalid equation. Operator cannot be followed by a close bracket: '" + str(symbol) + "' at position " + str(i))
      elif isinstance(prev, OpenBracket):
        if isinstance(symbol, Operator):
          raise Exception("Invalid equation. Open bracket cannot be followed by an operator: '" + str(symbol) + "' at position " + str(i))
        elif isinstance(symbol, CloseBracket):
          raise Exception("Invalid equation. Open bracket cannot be followed by a close bracket: '" + str(symbol) + "' at position " + str(i))
      elif isinstance(prev, CloseBracket):
        if isinstance(symbol, Number):
          raise Exception("Invalid equation. Close bracket cannot be followed by a number: '" + str(symbol) + "' at position " + str(i))
      prev = symbol
    # Check brackets
    try:
      self.checkBrackets()
    except Exception as e:
      raise Exception("Invalid equation. " + str(e))

  def checkBrackets(self):
    open = 0
    for i in range(len(self.symbols)):
      symbol = self.symbols[i]
      if isinstance(symbol, OpenBracket):
        open += 1
      elif isinstance(symbol, CloseBracket):
        open -= 1
      
      if open < 0:
        raise Exception("Close bracket cannot come before an open bracket: '" + str(symbol) + "' at position " + str(i))
    # Close brackets
    for i in range(open):
      self.symbols.append(CloseBracket())
  
  def format(self):
    self.formatCoefficients()
  
  # Coefficient is a CloseBracket or a Number before an OpenBracket
  def formatCoefficients(self):
    i = 0
    while i < len(self.symbols):
      if isinstance(self.symbols[i], (CloseBracket, Number)): # Symbol at counter is a CloseBracket or a Number
        if i + 1 < len(self.symbols): # Next symbol exists
          if isinstance(self.symbols[i + 1], OpenBracket): # Next symbol is an OpenBracket
            self.symbols.insert(i + 1, Multiply()) # Insert Multiply between coefficient and OpenBracket
            i += 1 # Move counter to Multiply
      i += 1

  def isPartOfNumber(self, char, value):
    return char.isdigit() or (char == "." and "." not in value)
  
  def isStartOfNumber(self, i, char, output):
    if char == ".":
      if i < len(self.input) - 1:
        next = self.input[i + 1]
        return next.isdigit() # Allow if next char is a digit
    if char == "-":
      if len(output) > 0:
        return isinstance(output[-1], Operator) # Allow if previous symbol is an Operator
      return True # Allow if first char
    return char.isdigit()

  def split(self):
    output = []
    i = 0
    while i < len(self.input):
      char = self.input[i]
      if self.isStartOfNumber(i, char, output): # Number
        value = char
        while i < len(self.input) - 1: # Loop until last symbol
          next = self.input[i + 1]
          if self.isPartOfNumber(next, value): 
            i += 1
            value += next
          else: 
            break # Break loop if next symbol is not part of the number
        # Cast to int/float
        value = float(value)
        if value % 1 == 0:
          value = int(value)
        output.append(Number(value))
      elif char in OPERATORS:
        output.append(getOperator(char))
      elif char == "(":
        output.append(OpenBracket())
      elif char == ")":
        output.append(CloseBracket())
      else:
        raise Exception("Invalid symbol in equation: '" + char + "' at position " + str(i))
      i += 1
    return output