# Pseudo code: infix-to-postfix.pdf
# Works for the operators: "+", "-", "*" and "/"

precedence = {
  "+": 1,
  "-": 1,
  "*": 2,
  "/": 2
}

def printTitle(text, padding):
  """
  Prints an ASCII title
  
  Parameters
  ----------
  text : string
      The text for the title
  padding : int
      The width of padding either side of the text
  
  Returns
  ----------
  string : The ASCII title
  """

  text = text.strip() # Remove whitespace
  text = text.upper() # Convert text to upper case
  middle = " " + text + " " # Add whitespace around text
  middle = "#" * padding + middle + "#" * padding # Add padding of "#" either side of text
  length = len(middle) # Get length of one line
  top = "#" * length + '\n' # Top line of "#"
  bottom = '\n' + "#" * length # Bottom line of "#"
  print(top + middle + bottom)

def isOperand(symbol):
  """
  Determine if the given symbol is an operand
  
  Parameters
  ----------
  symbol : any
      A symbol
  
  Returns
  ----------
  bool : True if the symbol is an operand, False otherwise.
  """

  return type(symbol) == float or type(symbol) == int

class Infix:
  """
  A class used to represent an equation in Infix notation
  
  Attributes
  ----------
  equation : string
      The equation string
  symbols : list
      The equation symbols ordered in Infix notation

  Methods
  -------
  split()
      Splits the equation string into a list of symbols ordered in Infix notation
  """

  def __init__(self, equation):
    """
    Parameters
    ----------
    equation : str
        The equation string
    """

    self.equation = equation.replace(" ", "")
    self.symbols = self.split()

  def split(self):
    """
    Splits the equation string into a list of symbols ordered in Infix notation
    
    Returns
    ----------
    list : The list of symbols ordered in Infix notation
    """

    output = []
    i = 0
    while i < len(self.equation):
      value = self.equation[i]
      if value.isdigit(): # Operand
        while True:
          if i == len(self.equation) - 1: # Break loop if last symbol
            break
          next = self.equation[i + 1]
          if next.isdigit() == False and next != ".": # Break loop if next symbol is not a digit or "."
            break
          i += 1
          value += next
        value = int(value) if value.isdigit() else float(value) # Cast to int or float
      output.append(value)
      i += 1
    return output

  def __str__(self):
    formatted = " ".join(map(str, self.symbols)) # Have to map all symbols to strings before joining
    formatted = formatted.replace("( ", "(") # Remove spaces after open bracket
    formatted = formatted.replace(" )", ")") # Remove spaces before closing bracket
    return formatted


class Postfix:
  """
  A class used to represent an equation in Postfix notation
  
  Attributes
  ----------
  symbols : list
      The equation symbols ordered in Postfix notation

  Methods
  -------
  convert(infix)
      Converts an Infix object into a list of symbols ordered in Postfix notation

  evaluate()
      Evaluates the equation
  """

  def __init__(self, infix):
    """
    Parameters
    ----------
    infix : Infix
        An Infix object
    """

    self.symbols = self.convert(infix)

  def convert(self, infix):
    """
    Converts an Infix object into a list of symbols ordered in Postfix notation
    
    Parameters
    ----------
    infix : Infix
        An Infix object

    Returns
    ----------
    list : The list of symbols ordered in Postfix notation
    """

    stack = []
    output = []
    # Loop through symbols
    for symbol in infix.symbols:
      if isOperand(symbol): # Operand
        output.append(symbol)
      elif symbol == "(": # Open bracket
        stack.append(symbol)
      elif symbol == ")": # Closing bracket
        while stack[-1] != "(": # Pop all items before "("" from stack to output
          output.append(stack.pop())
        stack.pop() # Remove "(""
      else: # Operators
        if(len(stack) > 0): # Proceed if stack is not empty
          # Pop greater or equal precedence items from stack to output
          while stack[-1] != "(" and precedence.get(stack[-1], 0) >= precedence.get(symbol):
            output.append(stack.pop())
            if(len(stack) == 0): # Break if stack is empty
              break
        stack.append(symbol) # Push operator to stack

    while len(stack) > 0: # Pop all remaining items from stack to output
      output.append(stack.pop())
    return output

  def evaluate(self):
    """
    Evaluates the equation

    Returns
    ----------
    int/float : The answer to the equation
    """

    stack = []
    for symbol in self.symbols:
      if isOperand(symbol): # Operand
        stack.append(symbol)
      else:
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
    return stack[0]

  def __str__(self):
    return ' '.join(map(str, self.symbols)) # Have to map all symbols to strings before joining

# Running the script
printTitle("Equation Solver", 20)
solve = True
while solve:
  equation = input("Enter an equation to solve: ")
  infix = Infix(equation)
  postfix = Postfix(infix)
  print(infix.__str__() + ' = ' + str(postfix.evaluate()))
  answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  while answer != 'y' and answer != 'n':
    print("Please answer with 'y' or 'n'")
    answer = input("\nWould you like to solve another equation? (y/n) ").lower()
  solve = answer == "y"
  if solve:
    print('')
print("Goodbye")