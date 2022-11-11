# Pseudo code: infix-to-postfix.pdf
from tkinter import *
from brackets import *
from infix import *
from number import *
from operators import *
from postfix import *
from nodes import *

class App:
  def __init__(self):
    self.ICONS = {"*": "\u00d7", "/": "\u00f7"}
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
    self.history = StringVar()
    self.input = StringVar()
    self.input.set(self.getPrevNumberText())

    labelHistory = Label(self.window, textvariable=self.history, font=14, bg="white", fg="black", width = 24, height=2)
    labelInput = Label(self.window, textvariable=self.input, font=("consolas", 20), bg="white", fg="black", width = 24, height=2)
    labelHistory.pack()
    labelInput.pack()

    frame = Frame()
    frame.pack()
    # Buttons
    top = 1
    values = [["CE", "(", ")", "%"], ["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["0", ".", "=", "+"]]
    for row in range(len(values)):
      for col in range(len(values[0])):
        value = values[row][col]
        text = self.ICONS.get(value, value)
        button = Button(frame, text=text, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, font=36, relief=FLAT, bd=0, command=lambda value=value: self.press(value)) # Default keyword parameter used: https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-a-for-loop-with-lambda
        button.grid(row=row+top, column=col)
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
  
  def getEquationText(self, equals):
    text = ""
    for symbol in self.equation:
      text += str(symbol)
    if equals:
      text += "="
    return text

  def getPrevNumberText(self):
    for i in range(len(self.equation) - 1, -1, -1):
      symbol = self.equation[i]
      if isinstance(symbol, Number):
        return str(symbol)
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
      if self.overwrite: #Overwrite Number
        current = Number(command)
        self.equation[-1] = current
      elif type(current) is not Number: #Insert Number
        current = Number(command)
        self.equation.append(current)
      elif not current.hasDecimal(): #Push to Number
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
        self.history.set(str(postfix.tree) + " =")
        self.input.set(solution)
        self.overwrite = True
        print(str(postfix.tree) + " =")
        print(solution)
    else:
      self.history.set(self.getEquationText(False))
      self.input.set(self.getPrevNumberText())
      self.overwrite = False
      print(self.getEquationText(False))
      print(self.getPrevNumberText())
    
  def printTitle(self, text, padding):
    text = text.strip() # Remove whitespace
    text = text.upper() # Convert text to upper case
    middle = " " + text + " " # Add whitespace around text
    middle = "#" * padding + middle + "#" * padding # Add padding of "#" either side of text
    length = len(middle) # Get length of one line
    top = "#" * length + "\n" # Top line of "#"
    bottom = "\n" + "#" * length # Bottom line of "#"
    print(top + middle + bottom)

  def run(self):
    self.printTitle("calculator", 20)

# Run app.py
app = App()