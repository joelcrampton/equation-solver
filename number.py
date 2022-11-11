class Number:
  def __init__(self, number):
    self.values = ["0"] if number is None else list(str(number))
    if self.values[0] == ".":
      self.values.insert(0, "0")
  
  def push(self, value):
    if self.values == ["0"] and value != ".":
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