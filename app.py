# Pseudo code: infix-to-postfix.pdf
from tkinter import *


OPERATORS = ["+", "-", "*", "/", "^"]
icons = {"+": "\u002b", "-": "\u2212", "*": "\u00d7", "/": "\u00f7"}

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

# Symbols
class Number:
  def __init__(self, number):
    self.values = ["0"] if number is None else list(str(number))
  
  def push(self, value):
    if self.values == ["0"]:
      self.values[0] = value
    elif not self.isMaxLength():
      self.values.append(value)
  
  def hasDecimal(self):
    return "." in self.values

  def isMaxLength(self):
    return (len(self.values) == 16 and not self.hasDecimal()) or (len(self.values) == 17 and self.hasDecimal())

  def result(self):
    result = float("".join(self.values))
    if result % 1 == 0 and not self.hasDecimal(): # Don't cast to int if has decimal
      result = int(result)
    return result
  
  def __str__(self):
    return str(self.result())

class Operator:
  pass

class Add(Operator):
  precedence = 1
  def __str__(self):
    return "+"

class Subtract(Operator):
  precedence = 1
  def __str__(self):
    return "-"

class Multiply(Operator):
  precedence = 2
  def __str__(self):
    return "*"

class Divide(Operator):
  precedence = 2
  def __str__(self):
    return "/"

class Exponent(Operator):
  precedence = 3
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

# Expression tree
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

class Infix:
  def __init__(self, input):
    try:
      self.input = None
      if isinstance(input, str): # String input
        self.input = input.replace(" ", "")
        self.symbols = self.split() # Split into symbols
      else: # List input
        self.symbols = input
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
        elif isinstance(symbol, OpenBracket):
          raise Exception("Invalid equation. Close bracket cannot be followed by an open bracket: '" + str(symbol) + "' at position " + str(i))
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
  
  def formatCoefficients(self):
    i = 0
    while i < len(self.symbols):
      if isinstance(self.symbols[i], Number): # Symbol at counter is a Number
        if i + 1 < len(self.symbols): # Next symbol exists
          if isinstance(self.symbols[i + 1], OpenBracket): # Next symbol is an OpenBracket
            self.symbols.insert(i + 1, Multiply()) # Insert Multiply between Number and OpenBracket
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

class App:
  def __init__(self):
    self.WIDTH = 400
    self.HEIGHT = 600
    self.BUTTON_HEIGHT = 3
    self.BUTTON_WIDTH = 7

    self.equation = [Number(None)]
    self.equations = []
    self.overwrite = False

    self.window = Tk()
    self.window.title("Calculator")
    self.window.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))
    self.window.resizable(0, 0)

    frame = Frame()
    frame.pack()

    # Buttons
    values = [["CE", "(", ")", "%"], ["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["0", ".", "=", "+"]]
    for row in range(len(values)):
      for col in range(len(values[0])):
        value = values[row][col]
        text = icons.get(value) if value in OPERATORS else value
        button = Button(frame, text=text, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, font=36, relief=FLAT, bd=0, command=lambda value=value: self.press(value)) # Default keyword parameter used: https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-a-for-loop-with-lambda
        button.grid(row=row, column=col)
    self.run()
    self.window.mainloop()

  def closeBrackets(self):
    while self.getOpenBrackets() > 0:
      self.equation.append(CloseBracket())
  
  def getOpenBrackets(self):
    open = 0
    for symbol in self.equation:
      if isinstance(symbol, OpenBracket):
        open += 1
      elif isinstance(symbol, CloseBracket):
        open -= 1
    return open

  def printEquation(self, equals):
    text = ""
    for symbol in self.equation:
      text += str(symbol)
    if equals:
      text += "="
    print(text)

  def printPrevNumber(self):
    for i in range(len(self.equation) - 1, -1, -1):
      symbol = self.equation[i]
      if isinstance(symbol, Number):
        print(symbol)
        return
    raise Exception("No Number found in equation.")

  def press(self, command):
    current = self.equation[-1]
    # Number
    if command.isdigit():
      if type(current) is not CloseBracket: # Can't have Number after CloseBracket
        if self.overwrite: #Overwrite Number
          current = Number(command)
          self.equation[-1] = current
        elif type(current) is not Number: #Insert Number
          current = Number(command)
          self.equation.append(current)
        else: #Push to Number
          current.push(command)
    # Decimal
    if command == ".":
      if type(current) is not Number:
        current = Number(None)
        self.equation.append(current)
      if not current.hasDecimal():
        current.push(command)
    # Operator
    if command in OPERATORS:
      if isinstance(current, Operator):
        self.equation[-1] = getOperator(command)
      else:
        self.equation.append(getOperator(command))
    # Open bracket
    if command == "(":
      self.equation.append(OpenBracket())
    # Close bracket
    if command == ")":
      if type(current) is not Operator and self.getOpenBrackets() > 0:
        self.equation.append(CloseBracket())
    # CE (Clear Entry)
    if command == "CE":
      self.equation.pop()
      if not self.equation:
        self.equation.append(Number(None))
    # Equals
    if command == "=":
      if type(current) is not Operator:
        self.closeBrackets()
        self.equations.append(self.equation)
        # Solve
        infix = Infix(self.equation)
        postfix = Postfix(infix)
        solution = postfix.tree.solve()

        self.equation = [Number(solution)]
        self.overwrite = True
        print(str(postfix.tree) + " =")
        print(solution)
    else:
      self.overwrite = False
      self.printEquation(False)
      self.printPrevNumber()
  
  def ask(self):
    while True:
      try:
        equation = input("Enter an equation: ")
        postfix = Postfix(Infix(equation))
        print(str(postfix.tree) + " = " + str(postfix.tree.solve()))
        break
      except Exception as e:
        print(e)
        print("Please try again\n")

  def printTitle(self, text, padding):
    text = text.strip() # Remove whitespace
    text = text.upper() # Convert text to upper case
    middle = " " + text + " " # Add whitespace around text
    middle = "#" * padding + middle + "#" * padding # Add padding of "#" either side of text
    length = len(middle) # Get length of one line
    top = "#" * length + "\n" # Top line of "#"
    bottom = "\n" + "#" * length # Bottom line of "#"
    print(top + middle + bottom)

  def repeat(self):
    answer = input("\nWould you like to solve another equation? (y/n) ").lower()
    while answer != "y" and answer != "n":
      print("Please answer with 'y' or 'n'")
      answer = input("\nWould you like to solve another equation? (y/n) ").lower()
    if answer == "y":
      print()
    return answer == "y"

  def run(self):
    self.printTitle("Equation Solver", 20)
    """while True:
      self.ask()
      if self.repeat() == False:
        print("Goodbye")
        break"""

# Run app.py
app = App()