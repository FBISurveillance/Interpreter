def precedenceCheck(value):
  if value == "(" or value == ")":
    return 1
  if value == "+" or value == "-":
    return 2
  if value == "*" or value == "/":
    return 3
  if value == "^":
    return 4
  else:
    raise SyntaxError("Unexpected character at line EXAMPLE: " + value)

def isOperator(i):
  return i == "+" or i == "-" or i == "*" or i == "/" or i == "^"

class treeNode:
  def __init__(self, left, right, value):
    self.left = left
    self.right = right
    self.value = value

  def printTree(self, indent=0):
    print((indent*' ') + self.value)
    if self.left != None:
      self.left.printTree(indent+1)
    if self.right != None:
      self.right.printTree(indent+1)

  def __str__(self):
    return f"{self.left} {self.right} {self.value}"

class numNode(treeNode):
  def __init__(self, left, right, value):
    super().__init__(left, right, value)
    self.intValue = int(value)

class opNode(treeNode):
  def __init__(self, left, right, value):
    super().__init__(left, right, value)
    self.precedence = precedenceCheck(value)
    self.intValue = None

def AST(example):
  
  outputQueue = []
  opStack = []

  i = 0

  while i != len(example):
    if example[i].isnumeric():
      outputQueue.append(numNode(None, None, example[i]))

    else:
      if isOperator(example[i]):
        #line 51 fails if the first operator has a higher precedence than the second, saying list index out of range
        #mention having to add this check
        while len(opStack) > 0 and opStack[-1] != "(" and (opStack[-1].precedence > precedenceCheck(example[i]) or 
        (precedenceCheck(example[i]) == opStack[-1].precedence and 
         (precedenceCheck(example[i]) == 2 or precedenceCheck(example[i]) == 3))):
          toOutput = opStack.pop()
          rightSide = outputQueue.pop()
          leftSide= outputQueue.pop()
          outputQueue.append(opNode(leftSide, rightSide, toOutput.value))

      if example[i] == ",":
        while opStack[-1] != "(":
          toOutput = opStack.pop()
          rightSide = outputQueue.pop()
          leftSide= outputQueue.pop()
          outputQueue.append(opNode(leftSide, rightSide, toOutput.value))

      if example[i] == "(":
        opStack.append(opNode(None, None, example[i]))

      if example[i] == ")":
        try:
          while opStack[-1].value != "(":
            toOutput = opStack.pop()
            rightSide = outputQueue.pop()
            leftSide= outputQueue.pop()
            outputQueue.append(opNode(leftSide, rightSide, toOutput.value))
          #assert there is a left parenthesis at the top of the op stack
          opStack.pop()
        except:
          raise SyntaxError("Unmatched ')'" + " at line EXAMPLE")

      elif example[i] != "," and example[i] != "(" and example[i] != ")":
        opStack.append(opNode(None, None, example[i]))

    i += 1

  while len(opStack) != 0:
    #assert the operator on top is not a left parenthesis
    try:
      toOutput = opStack.pop()
      rightSide = outputQueue.pop()
      leftSide= outputQueue.pop()
      outputQueue.append(opNode(leftSide, rightSide, toOutput.value))
    except:
      raise SyntaxError("Unmatched '('" + " at line EXAMPLE")

  return outputQueue[0]

def evaluate(node):
  if isOperator(node.value):
    if isOperator(node.left.value):
      node.left.intValue = evaluate(node.left)
    if isOperator(node.right.value):
      node.right.intValue = evaluate(node.right)
    if node.value == "+":
      return node.left.intValue + node.right.intValue
    elif node.value == "-":
      return node.left.intValue - node.right.intValue
    elif node.value == "*":
      return node.left.intValue * node.right.intValue
    elif node.value == "/":
      return node.left.intValue / node.right.intValue
    elif node.value == "^":
     return node.left.intValue ** node.right.intValue

  print(str(node.intValue))
  return node.intValue