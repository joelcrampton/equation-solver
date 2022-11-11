class Bracket:
  pass

class CloseBracket(Bracket):
  def __str__(self):
    return ")"

class OpenBracket(Bracket):
  def __str__(self):
    return "("