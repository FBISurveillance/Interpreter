class charaList:
  def __init__(self, unSplit):
    self.unSplit = unSplit
    self.cList = list(unSplit)
    self.lineNum = 1
    self.chunk = ""
    self.index = 0

class tokenList:
  def __init__(self):
    self.tList = []
    self.index = 0

class token:
  def __init__(self, cl, type, value):
    self.type = type
    self.value = value
    self.lineNum = cl.lineNum

  def __str__(self):
    return f"type: {self.type}, value: {self.value}, lineNum: {self.lineNum}"


class funcToken(token):
  def __init__(self, cl, type, parameters):
    super().__init__(cl, type, None)
    self.parameters = parameters
    self.lineNum = cl.lineNum

keywords = ["if", "else", "while", "for", "str", "int", "bool", "string", "integer", "boolean", "def", "return"]

functions = ["input", "output"]

def isOperator(i):
  return i == "+" or i == "-" or i == "*" or i == "/" or i == "^" or i == "=" or i == "<" or i == ">" or i == "!"

def isPunctuation(i):
  return i == "(" or i == ")" or i == "{" or i == "}" or i == "," or i == ":"

def getTokens(cl, tl):
  while cl.index < len(cl.cList):
    if cl.cList[cl.index] == " ":
      cl.index += 1
      continue
 
    if cl.index < len(cl.cList) and cl.cList[cl.index] == "\n":
      cl.lineNum += 1
      cl.index += 1
      continue

    if cl.index < len(cl.cList) and cl.cList[cl.index] == "#":
      while cl.cList[cl.index] != "\n":
        cl.index += 1
      cl.index += 1
      continue

    if cl.index < len(cl.cList) and cl.cList[cl.index] == "\t":
      cl.index += 1
      continue

    elif cl.index < len(cl.cList) and cl.cList[cl.index].isnumeric():
      grabInt(cl, tl)

    elif cl.index < len(cl.cList) and (cl.cList[cl.index] == '"' or cl.cList[cl.index] == "'"):
      grabStr(cl, tl)

    elif cl.index < len(cl.cList) and cl.cList[cl.index].isalpha():
      grabWord(cl, tl)

    elif cl.index < len(cl.cList) and isOperator(cl.cList[cl.index]):
      grabOperator(cl, tl)

    elif cl.index < len(cl.cList) and isPunctuation(cl.cList[cl.index]):
      tl.tList.append(token(cl, "punctuation", cl.cList[cl.index]))
      cl.index += 1

def grabInt(cl, tl):
  while cl.index < len(cl.cList) and cl.cList[cl.index].isnumeric():
    cl.chunk += cl.cList[cl.index]
    cl.index += 1
  tl.tList.append(token(cl, "int", cl.chunk))
  cl.chunk = ""

def grabStr(cl, tl):
  cl.index += 1
  while cl.index < len(cl.cList) and cl.cList[cl.index] != '"' and cl.cList[cl.index] != "'":
    cl.chunk += cl.cList[cl.index]
    cl.index += 1
  tl.tList.append(token(cl, "str", cl.chunk))
  cl.chunk = ""
  cl.index += 1

def grabWord(cl, tl):
  while cl.index < len(cl.cList) and cl.cList[cl.index] not in [" ", ",", ":", "{", "}", "(", ")", "\n"] and isOperator(cl.cList[cl.index]) == False:
    cl.chunk += cl.cList[cl.index]
    cl.index += 1
    #print(cl.chunk)
  if cl.chunk in keywords:
    tl.tList.append(token(cl, "keyword", cl.chunk))
    cl.chunk = ""
  elif cl.chunk in functions or cl.cList[cl.index] == "(":
    tl.tList.append(token(cl, "function", cl.chunk))
    cl.chunk = ""
  else:
    tl.tList.append(token(cl, "identifier", cl.chunk))
    cl.chunk = ""

def grabOperator(cl, tl):
  cl.chunk += cl.cList[cl.index]
  cl.index += 1
  if cl.index < len(cl.cList) and isOperator(cl.cList[cl.index]):
    cl.chunk += cl.cList[cl.index]
    cl.index += 1
  tl.tList.append(token(cl, "operator", cl.chunk))
  cl.chunk = ""

#this one works
#text = 'string test = "test is test"\n\nif (test == "test") {\n  output(test)\n}\nneek(neek)'

#this one also works
#text = 'int i = 0\n\nwhile i < 10 {\n  i = i + 1\n}'

#def neek():
#  print("neek")
#  return "neek"