# Pseudo code: infix-to-postfix.pdf
from tkinter import *
from brackets import *
from equation import *
from infix import *
from number import *
from operators import *
from postfix import *
from nodes import *

ICONS = {"*": "\u00d7", "/": "\u00f7"}

class App:
  def __init__(self):
    self.equation = Equation(None)
    self.equations = []
    self.overwrite = False

    window = Tk()
    window.title("Calculator")
    window.geometry("400x600")
    window.resizable(0, 0)

    self.history = StringVar()
    self.recent = StringVar()
    self.recent.set(str(self.equation.getRecent()))
    Label(window, textvariable=self.history, font=14, bg="white", fg="black", width = 24, height=2).pack()
    Label(window, textvariable=self.recent, font=("consolas", 20), bg="white", fg="black", width = 24, height=2).pack()

    frame = Frame()
    frame.pack()
    # Buttons
    top = 1
    values = [["CE", "(", ")", "%"], ["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["0", ".", "=", "+"]]
    for row in range(len(values)):
      for col in range(len(values[0])):
        value = values[row][col]
        text = ICONS.get(value, value)
        # Default keyword parameter used: https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-a-for-loop-with-lambda
        Button(frame, text=text, height=3, width=7, font=36, relief=FLAT, bd=0, command=lambda value=value: self.press(value)).grid(row=row+top, column=col)
    self.run()
    window.mainloop()

  def press(self, command):
    top = self.equation.top()
    # Digit or decimal
    if command.isdigit() or command == ".":
      if type(top) is not CloseBracket: # Can't have Number after CloseBracket
        if self.overwrite: #Overwrite Number
          self.equation.setTop(Number(command))
        elif type(top) is not Number: #Insert Number
          self.equation.append(Number(command))
        else: #Push to Number
          top.push(command)
    # Operator
    if command in OPERATORS:
      if isinstance(top, Operator):
        self.equation.setTop(getOperator(command))
      elif type(top) is not OpenBracket:
        self.equation.append(getOperator(command))
    # Open bracket
    if command == "(":
      self.equation.append(OpenBracket())
    # Close bracket
    if command == ")":
      if not isinstance(top, (OpenBracket, Operator)) and self.equation.getOpenBrackets() > 0:
        self.equation.append(CloseBracket())
    # CE (Clear Entry)
    if command == "CE":
      self.equation.pop()
    # Equals
    if command == "=":
      if self.equation.complete():
        solution = self.equation.solve()
        self.update()
        
        self.equations.append(self.equation)
        self.equation = Equation(solution)
        self.overwrite = True
    else:
      self.update()
      self.overwrite = False
    
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

  def update(self):
    self.history.set(str(self.equation))
    self.recent.set(str(self.equation.getRecent()))
    print(self.history.get())
    print(self.recent.get())

# Run app.py
app = App()