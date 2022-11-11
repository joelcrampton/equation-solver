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
