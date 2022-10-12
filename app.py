# Pseudo code: infix-to-postfix.pdf
# Works for the operators: "+", "-", "*", "/" and "^"

from ast import Sub
from multiprocessing.sharedctypes import Value

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

class Operand:
  def __init__(self, value):
    """
    Parameters:
      value (int/float): The operand value
    """

    if isinstance(value, (int, float)) == False:
      raise Exception("Operand value must be of type int or float")
    elif isinstance(value, float):
      if value.is_integer():
        value = int(value)
    self.value = value
  
  def __str__(self):
    return str(self.value)

class Operator:
  pass

class Add(Operator):
  def __init__(self):
    self.precedence = 1

  def __str__(self):
    return "+"

class Subtract(Operator):
  def __init__(self):
    self.precedence = 1

  def __str__(self):
    return "-"

class Multiply(Operator):
  def __init__(self):
    self.precedence = 2

  def __str__(self):
    return "*"

class Divide(Operator):
  def __init__(self):
    self.precedence = 2

  def __str__(self):
    return "/"

class Exponent(Operator):
  def __init__(self):
    self.precedence = 3

  def __str__(self):
    return "^"

class Bracket:
  pass

class OpenBracket(Bracket):
  def __str__(self):
    return "("

class CloseBracket(Bracket):
  def __str__(self):
    return ")"

class Infix:
  """
  A class used to represent an equation in Infix notation
  
  Attributes:
    equation (str): The equation string
    symbols (list): The equation symbols ordered in Infix notation

  Methods:
    split(): Splits the equation string into a list of symbols ordered in Infix notation
    isValid(): Determines if the list of symbols is valid Infix notation
  """

  def __init__(self, equation):
    """
    Parameters:
      equation (str): The equation string
    """

    self.equation = equation.replace(" ", "")
    self.symbols = self.split()
    if self.isValid() == False:
      raise Exception
      
  def split(self):
    """
    Splits the equation string into a list of symbols ordered in Infix notation
    
    Returns:
      list: The list of symbols ordered in Infix notation
    """

    output = []
    i = 0
    while i < len(self.equation):
      char = self.equation[i]
      if char.isdigit(): # Operand
        value = char
        while True:
          if i == len(self.equation) - 1: # Break loop if last symbol
            break
          next = self.equation[i + 1]
          if next.isdigit() == False and next != ".": # Break loop if next symbol is not a digit or "."
            break
          i += 1
          value += next
        value = float(value) # Cast to float
        output.append(Operand(value))
      elif char == "(":
        output.append(OpenBracket())
      elif char == ")":
        output.append(CloseBracket())
      elif char == "+":
        output.append(Add())
      elif char == "-":
        output.append(Subtract())
      elif char == "*":
        output.append(Multiply())
      elif char == "/":
        output.append(Divide())
      elif char == "^":
        output.append(Exponent())
      else:
        raise Exception("Invalid symbol in equation: " + char)
      i += 1
    return output

  def isValid(self):
    """
    Determines if the list of symbols is valid Infix notation
    
    Returns:
      bool: True if valid, False otherwise.
    """

    # VALID ORDERING
    # Operand must be followed by an Operator or a Bracket, e.g. 2+, 2(, 2)
    # Operator must be followed by an Operand or an OpenBracket, e.g. +2, +(
    # OpenBracket must be followed by an Operand or an OpenBracket, e.g. (2, ((
    # CloseBracket must be followed by an Operator or a CloseBracket, e.g. )+, ))
    prev = None
    for symbol in self.symbols:
      if isinstance(symbol, type(prev)) and isinstance(symbol, (Operand, Operator)): # Invalid if two Operands or Operators in a row
        return False
      prev = symbol
    return self.hasClosedBrackets()

  def hasClosedBrackets(self):
    """
    Determines if all Brackets in the list of symbols have been closed appropriately
    
    Returns:
      bool: True if closed, False otherwise.
    """

    open = 0
    for symbol in self.symbols:
      if isinstance(symbol, OpenBracket):
        open += 1
      elif isinstance(symbol, CloseBracket):
        open -= 1
      
      if open < 0: # At any point, there should never be more brackets closed than have been opened
        return False
    return open == 0 # At the end, all brackets should be closed

  def __str__(self):
    formatted = " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining
    formatted = formatted.replace("( ", "(") # Remove spaces after open bracket
    formatted = formatted.replace(" )", ")") # Remove spaces before closing bracket
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
    """

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
      if isinstance(symbol, Operand): # Operand
        output.append(symbol)
      elif isinstance(symbol, OpenBracket): # OpenBracket
        stack.append(symbol)
      elif isinstance(symbol, CloseBracket): # CloseBracket
        while isinstance(stack[-1], OpenBracket) == False: # Pop all items before OpenBracket from stack to output
          output.append(stack.pop())
        stack.pop() # Remove OpenBracket
      else: # Operator
        if(len(stack) > 0): # Proceed if stack is not empty
          while isinstance(stack[-1], OpenBracket) == False: # Pop items before OpenBracket from stack to output
            if stack[-1].precedence < symbol.precedence: # Don't pop items with lower precedence
              break
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
      if isinstance(symbol, Operand): # Operand
        stack.append(symbol)
      else: # Operator
        b = stack.pop().value
        a = stack.pop().value
        if isinstance(symbol, Add):
          stack.append(Operand(a + b))
        elif isinstance(symbol, Subtract):
          stack.append(Operand(a - b))
        elif isinstance(symbol, Multiply):
          stack.append(Operand(a * b))
        elif isinstance(symbol, Divide):
          stack.append(Operand(a / b))
        elif isinstance(symbol, Exponent):
          stack.append(Operand(a ** b))
    return stack[0].value

  def __str__(self):
    return " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining

def ask():
  infix = None
  while True:
    equation = input("Enter an equation: ")
    try:
      infix = Infix(equation)
      break
    except Exception:
      print("Invalid equation, please try again\n")
  postfix = Postfix(infix)
  print(infix.__str__() + " = " + str(postfix.evaluate()))

def repeat():
  answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  while answer != "y" and answer != "n":
    print("Please answer with 'y' or 'n'")
    answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  return answer == "y"

# Running the script
printTitle("Equation Solver", 20)
while True:
  ask() # Ask for and solve equation
  if repeat(): # Ask the user if they want to repeat
    print("")
  else:
    break
print("Goodbye")