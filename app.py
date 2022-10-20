# Pseudo code: infix-to-postfix.pdf

operators = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

def formatNumber(number):
  if isinstance(number, float):
    if number.is_integer():
      number = int(number)
  return number

def isBracket(symbol):
  return symbol == "(" or symbol == ")"

def isNumber(symbol):
  return isinstance(symbol, (int, float))

def isOperator(symbol):
  return symbol in operators


class Infix:
  """
  A class used to represent an equation in Infix notation
  
  Attributes:
    equation (str): The equation string
    symbols (list): The equation symbols ordered in Infix notation

  Methods:
    split(): Splits the equation string into a list of symbols ordered in Infix notation
    check(): Check that the list of symbols is valid Infix notation
    checkBrackets(): Check that all brackets in the list of symbols have been closed appropriately
  """

  def __init__(self, equation):
    """
    Parameters:
      equation (str): The equation string
    
    Raises:
      Exception: If equation is invalid
    """

    self.equation = equation.replace(" ", "")
    try:
      self.symbols = self.split() # Split into symbols
      self.check() # Check for invalid equation
      self.format() # Format symbols
    except Exception as e:
      raise Exception(e)
      
  def split(self):
    """
    Splits the equation string into a list of symbols ordered in Infix notation
    
    Returns:
      list: The list of symbols ordered in Infix notation

    Raises:
      Exception: If there is an invalid symbol in the equation
    """

    output = []
    i = 0
    while i < len(self.equation):
      char = self.equation[i]
      if char.isdigit(): # Number
        value = char
        while True:
          if i == len(self.equation) - 1: # Break loop if last symbol
            break
          next = self.equation[i + 1]
          if next.isdigit() == False and next != ".": # Break loop if next symbol is not a digit or "."
            break
          i += 1
          value += next
        value = int(value) if value.isdigit() else float(value) # Cast to int/float
        output.append(value)
      elif isBracket(char) or isOperator(char):
        output.append(char)
      else:
        raise Exception("Invalid symbol in equation: '" + char + "' at position " + str(i))
      i += 1
    return output

  def check(self):
    """
    Check that the list of symbols is valid Infix notation as below:
    - Number must be followed by an operator or a bracket. E.g. 2+, 2(, 2)
    - Operator must be followed by a number or an open bracket. Cannot be first. E.g. +2, +(
    - Open bracket must be followed by a number or an open bracket. E.g. (2, ((
    - Close bracket must be followed by an operator or a close bracket. E.g. )+, ))
    
    Raises:
      Exception: If equation is invalid
    """

    prev = None
    if isOperator(self.symbols[0]):
      raise Exception("Invalid equation. Operator symbol cannot be first: '" + str(self.symbols[0]) + "' at position 0")
    for i in range(len(self.symbols)):
      symbol = self.symbols[i]
      if isNumber(prev):
        if isNumber(symbol):
          raise Exception("Invalid equation. Number cannot be followed by another number: '" + str(symbol) + "' at position " + str(i))
      elif isOperator(prev):
        if isOperator(symbol):
          raise Exception("Invalid equation. Operator cannot be followed by another operator: '" + str(symbol) + "' at position " + str(i))
        elif symbol == ")":
          raise Exception("Invalid equation. Operator cannot be followed by a close bracket: '" + str(symbol) + "' at position " + str(i))
      elif prev == "(":
        if isOperator(symbol):
          raise Exception("Invalid equation. Open bracket cannot be followed by an operator: '" + str(symbol) + "' at position " + str(i))
        elif symbol == ")":
          raise Exception("Invalid equation. Open bracket cannot be followed by a close bracket: '" + str(symbol) + "' at position " + str(i))
      elif prev == ")":
        if isNumber(symbol):
          raise Exception("Invalid equation. Close bracket cannot be followed by a number: '" + str(symbol) + "' at position " + str(i))
        elif symbol == "(":
          raise Exception("Invalid equation. Close bracket cannot be followed by an open bracket: '" + str(symbol) + "' at position " + str(i))
      prev = symbol
    # Check brackets
    try:
      self.checkBrackets()
    except Exception as e:
      raise Exception("Invalid equation. " + str(e))

  def checkBrackets(self):
    """
    Check that all brackets in the list of symbols have been closed appropriately
    
    Raises:
      Exception: If brackets have not been closed appropriately
    """

    open = 0
    for i in range(len(self.symbols)):
      symbol = self.symbols[i]
      if symbol == "(":
        open += 1
      elif symbol == ")":
        open -= 1
      
      if open < 0:
        raise Exception("Close bracket cannot come before an open bracket: '" + str(symbol) + "' at position " + str(i))
    if open > 0:
      raise Exception("All open brackets must be closed.")
  
  def format(self):
    self.formatCoefficients()
  
  def formatCoefficients(self):
    i = 0
    while i < len(self.symbols):
      if isNumber(self.symbols[i]): # Symbol at counter is a number
        if i + 1 < len(self.symbols): # Next symbol exists
          if self.symbols[i + 1] == "(": # Next symbol is an open bracket
            self.symbols.insert(i + 1, "*") # Insert "*" between number and open bracket
            i += 1 # Move counter to open bracket's new index
      i += 1
  
  def __str__(self):
    formatted = " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining
    formatted = formatted.replace("( ", "(") # Remove spaces after open bracket
    formatted = formatted.replace(" )", ")") # Remove spaces before closing bracket
    formatted = formatted.replace(" ^ ", "^") # Remove spaces around exponent
    return formatted


class Postfix:
  """
  A class used to represent an equation in Postfix notation
  
  Attributes:
    symbols (list): The equation symbols ordered in Postfix notation

  Methods:
    convert(infix): Converts an Infix object into a list of symbols ordered in Postfix notation
    evaluate(): Evaluates the equation
  """

  def __init__(self, infix):
    """
    Parameters:
      infix (Infix): An Infix object
    
    Raises:
      Exception: If infix is not an Infix object
    """
    if isinstance(infix, Infix) == False:
      raise Exception("Invalid argument. Postfix() must take 1 Infix object argument")
    self.symbols = self.convert(infix)

  def convert(self, infix):
    """
    Converts an Infix object into a list of symbols ordered in Postfix notation
    
    Parameters:
      infix (Infix): An Infix object

    Returns:
      list: The list of symbols ordered in Postfix notation
    """

    stack = []
    output = []
    # Loop through symbols
    for symbol in infix.symbols:
      if isNumber(symbol): # Number
        output.append(symbol)
      elif symbol == "(": # Open bracket
        stack.append(symbol)
      elif symbol == ")": # Close bracket
        while stack[-1] != "(": # Pop all items before open bracket from stack to output
          output.append(stack.pop())
        stack.pop() # Remove open bracket
      else: # Operator
        if(len(stack) > 0): # Proceed if stack is not empty
          # Pop items with greater or equal precedence before open bracket from stack to output
          while stack[-1] != "(" and operators.get(stack[-1], 0) >= operators.get(symbol, 0):
            output.append(stack.pop())
            if len(stack) == 0: # Break if stack is empty
              break
        stack.append(symbol) # Push operator to stack

    while len(stack) > 0: # Pop all remaining items from stack to output
      output.append(stack.pop())
    return output

  def evaluate(self):
    """
    Evaluates the equation

    Returns:
      int/float: The answer to the equation
    """

    stack = []
    for symbol in self.symbols:
      if isNumber(symbol): # Number
        stack.append(symbol)
      else: # Operator
        b = stack.pop()
        a = stack.pop()
        if symbol == "+":
          stack.append(a + b)
        elif symbol == "-":
          stack.append(a - b)
        elif symbol == "*":
          stack.append(a * b)
        elif symbol == "/":
          stack.append(a / b)
        elif symbol == "^":
          stack.append(a ** b)
    return formatNumber(stack[0])

  def __str__(self):
    return " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining

def printTitle(text, padding):
  """
  Prints an ASCII title
  
  Parameters:
    text (str): The text for the title
    padding (int): The width of padding either side of the text
  
  Returns:
    string: The ASCII title
  """

  text = text.strip() # Remove whitespace
  text = text.upper() # Convert text to upper case
  middle = " " + text + " " # Add whitespace around text
  middle = "#" * padding + middle + "#" * padding # Add padding of "#" either side of text
  length = len(middle) # Get length of one line
  top = "#" * length + "\n" # Top line of "#"
  bottom = "\n" + "#" * length # Bottom line of "#"
  print(top + middle + bottom)

def ask():
  while True:
    try:
      equation = input("Enter an equation: ")
      infix = Infix(equation)
      postfix = Postfix(infix)
      print(str(infix) + " = " + str(postfix.evaluate()))
      break
    except Exception as e:
      print(e)
      print("Please try again\n")

def repeat():
  answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  while answer != "y" and answer != "n":
    print("Please answer with 'y' or 'n'")
    answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  if answer == "y":
    print()
  return answer == "y"

def main():
  printTitle("Equation Solver", 20)
  while True:
    ask()
    if repeat() == False:
      print("Goodbye")
      break

main()