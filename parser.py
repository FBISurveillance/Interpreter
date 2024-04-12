from lexer import isOperator



class eventList:
  def __init__(self):
    self.eList = []

class event:
  def __init__(self, name, contents):
    self.name = name
    self.contents = contents

  def __str__(self):
    try:
     return self.name + ": " + self.contents
    except:
      return self.name + ": " + self.contents.value

class varHandler:
  def __init__(self):
    self.varList = []
    self.varTypes = []

class funcHandler:
  def __init__(self):
    self.funcList = ["input", "output"]

class varEvent(event): #was going to have separate events for change/declare but they need the same variables so its chill (initially varDeclareEvent)
  def __init__(self, name, varName, varType, contents):
    super().__init__(name, contents)
    self.varName = varName
    self.varType = varType

  def __str__(self):
    return self.name + ": " + self.varName

class ifWhileEvent(event):
  def __init__(self, name, contents, condition):
    super().__init__(name, contents)
    self.condition = condition

  def __str__(self):
    return self.name

class funcDeclareEvent(event):
  def __init__(self, name, funcName, contents, parameters):
    super().__init__(name, contents)
    self.funcName = funcName
    self.parameters = parameters

  def __str__(self):
    return self.name + ": " + self.funcName

class funcCallEvent(event):
  def __init__(self, name, funcName, contents):
    super().__init__(name, contents)
    self.funcName = funcName

  def __str__(self):
    return self.name + ": " + self.funcName

class inTokenList:
  def __init__(self, tList):
    self.tList = tList
    self.index = 0

class token:
  def __init__(self, cl, type, value):
    self.type = type
    self.value = value
    self.lineNum = cl.lineNum

class argument:
  def __init__(self, name, type):
    self.name = name
    self.type = type

def errorHandling(error):
  print(error)
  quit()

def grabVar(tList, eList, vH):
  if tList.tList[tList.index+1].type != "identifier":
    errorHandling("Error: expected identifier")
  elif tList.tList[tList.index+2].value != "=":
    errorHandling("Error: expected '='")
  else:
    varIdentifier = tList.tList[tList.index+1].value

    for i in vH.varList:
      if i == varIdentifier:
        errorHandling("Error: variable by name " + varIdentifier + " already declared")

    varType = tList.tList[tList.index].value
    if varType == "string":
      varType = "str"
    elif varType == "integer":
      varType = "int"
    elif varType == "boolean":
      varType = "bool"

    tList.index += 3
    varContents = []
    currentLine = tList.tList[tList.index].lineNum
    while tList.index < len(tList.tList) and currentLine == tList.tList[tList.index].lineNum:
      if tList.tList[tList.index].type == varType or tList.tList[tList.index].type == "operator":
        varContents.append(tList.tList[tList.index])
        tList.index += 1
      elif tList.tList[tList.index].type == "identifier":
        foundVar = False
        for i in vH.varList:
          if tList.tList[tList.index].value == i:
            varType = vH.varTypes[vH.varList.index(i)]
            foundVar = True
            break

        if foundVar == False:
          errorHandling("Error: variable referenced but not assigned at line number " + str(tList.tList[tList.index].lineNum))

        varContents.append(tList.tList[tList.index].value)
        tList.index += 1

      elif tList.tList[tList.index].type == "function" or tList.tList[tList.index].value == "(" or tList.tList[tList.index].value == ")":
        varContents.append(tList.tList[tList.index])
        tList.index += 1
      
      else:
        errorHandling("Error: value of type " + tList.tList[tList.index].type + " assigned to variable of type " + varType + " at line " + str(tList.tList[tList.index].lineNum))

    eList.eList.append(varEvent("varDeclare", varIdentifier, varType, varContents))

    vH.varList.append(varIdentifier)
    vH.varTypes.append(varType)

#if (neek = 2) {
#  print("neek")
#}

def grabCond(tList, eList):
  if tList.tList[tList.index+1].value != "(":
    errorHandling("Error: expected '(' for condition")
  else:
    condChunk = []
    hasOp = False
    tList.index += 2
    while tList.tList[tList.index].value != ")":
      if tList.index > len(tList.tList):
        errorHandling("Error: expected ')' for condition")
      else:
        if tList.tList[tList.index].type == "operator":
          hasOp = True

        condChunk.append(tList.tList[tList.index])
        tList.index += 1

    tList.index += 1
    return condChunk

def grabContents(tList, eList, type):
  if tList.tList[tList.index].value != "{":
    errorHandling("Error: expected '{' for " + type)
  else:
    tList.index += 1
    if tList.tList[tList.index].value == "}" and tList.tList[tList.index].type == "punctuation":
      errorHandling("Error: expected contents for " + type)
    else:
      contentChunk = []
      while tList.tList[tList.index].value != "}":
        if tList.index > len(tList.tList):
          errorHandling("Error: expected '}' for " + type)
        contentChunk.append(tList.tList[tList.index])
        tList.index += 1

      return contentChunk

def grabIf(tList, eList, vH, fH):
  condTokens = grabCond(tList, eList)
  contentTokens = grabContents(tList, eList, "if")
  tempTList = inTokenList(contentTokens)
  tempEList = eventList()
  eventsToAdd = getEvents(tempTList, tempEList, vH, fH, True)

  eList.eList.append(ifWhileEvent("if", eventsToAdd, condTokens))
  tList.index += 1

def grabWhile(tList, eList, vH, fH):
  condTokens = grabCond(tList, eList)
  contentTokens = grabContents(tList, eList, "while")
  tempTList = inTokenList(contentTokens)
  tempEList = eventList()
  eventsToAdd = getEvents(tempTList, tempEList, vH, fH, True)

  eList.eList.append(ifWhileEvent("while", eventsToAdd, condTokens))
  tList.index += 1


#def neek():
#  print("neek")
#  return "neek"

#text = 'def neek():\n print("neek")\nreturn "neek"'

def grabFuncDeclare(tList, eList, vH, fH):
  if tList.tList[tList.index+1].type != "function":
    errorHandling("Error: expected name for function declaration")
  else:
    funcName = tList.tList[tList.index+1].value
  if tList.tList[tList.index+2].value != "(":
    errorHandling("Error: expected '(' for function declaration")
  else:
    tList.index += 3
    paramChunk = []
    while tList.tList[tList.index].value != ")": #this isnt going to work as it cant call tList.tList[tList.index], figure it out later
      if tList.index >= len(tList.tList):
        errorHandling("Error: expected ')' for function declaration")
      else:
        paramChunk.append(tList.tList[tList.index])
        tList.index += 1

    tList.index += 1

    if tList.tList[tList.index].value != "{":
      errorHandling("Error: expected '{' for function declaration")
    else:
      contChunk = []
      tList.index += 1
      while tList.tList[tList.index].value != "}":
        if tList.index >= len(tList.tList):
          errorHandling("Error: expected '}' for function declaration")
        else:
          contChunk.append(tList.tList[tList.index])
          tList.index += 1

    tList.index += 1

    paramList = []
    paramCheck = False

    for i in paramChunk:
      if i.type != "identifier" and i.type != "str" and i.type != "int" and i.value != "True" and i.value != "False" and i.value != ",":
        errorHandling("Error: invalid argument type for function declaration")
      else:
        if i.value != ",":
          if paramCheck == True:
            errorHandling("Expected , separating parameters")
          else:
            paramList.append(argument(i.value, i.type))
            paramCheck = True

        elif i.value == ",":
          paramCheck = False
    
    tempTList = inTokenList(contChunk)

    tempEList = eventList()

    eventsToAdd = getEvents(tempTList, tempEList, vH, fH, True)
    
    eList.eList.append(funcDeclareEvent("funcDeclare", funcName, tempEList.eList, paramList))

def grabFuncReturn(tList, eList, vH):
  returnValue = []
  tList.index += 1
  currentLine = tList.tList[tList.index].lineNum
  
  while tList.index < len(tList.tList) and currentLine == tList.tList[tList.index].lineNum:
    returnValue.append(tList.tList[tList.index])
    tList.index += 1

  if len(returnValue) == 1:
    eList.eList.append(event("funcReturn", returnValue[0]))
    
  else:
    errorHandling("Error: expected only one value after return on line number " + str(currentLine))


def changeVar(tList, eList, vH):
  if tList.tList[tList.index+1].value != "=" and tList.tList[tList.index+1].value != "+=":
    errorHandling("Error: expected '=' or '+=' for variable reassignment on line number " + str(tList.tList[tList.index].lineNum) + " not " + tList.tList[tList.index+1].value)
  else:
    foundVar = False
    for i in vH.varList:
      if tList.tList[tList.index].value == i:
        varType = vH.varTypes[vH.varList.index(i)]
        foundVar = True
        break

    if foundVar == False: #not this one
      errorHandling("Error: variable referenced but not assigned")

  varIdentifier = tList.tList[tList.index].value
  tList.index += 2
  varContents = []
  currentLine = tList.tList[tList.index].lineNum
  while tList.index < len(tList.tList) and currentLine == tList.tList[tList.index].lineNum:
    if tList.tList[tList.index].type == varType:
      varContents.append(tList.tList[tList.index])
      tList.index += 1
    else:
      if tList.tList[tList.index].type == "identifier":
        foundVar = False
        for i in vH.varList:
          if tList.tList[tList.index].value == i:
            identifType = vH.varTypes[vH.varList.index(i)]
            foundVar = True
            break

        if foundVar == False:
          errorHandling("Error: variable referenced but not assigned")

        if identifType == varType:
          varContents.append(tList.tList[tList.index])
          tList.index += 1

      elif tList.tList[tList.index].type == "operator":
        varContents.append(tList.tList[tList.index])
        tList.index += 1

      else:
        errorHandling("Error: value of type " + tList.tList[tList.index].type + " assigned to variable of type " + varType + " at line " + str(tList.tList[tList.index].lineNum))

  if len(varContents) == 0:
    errorHandling("Error: expected value for variable reassignment")

  eList.eList.append(varEvent("varChange", varIdentifier, varType, varContents))
  tList.index += 1

def callFunc(tList, eList):
  if tList.tList[tList.index+1].value != "(":
    errorHandling("Error: expected '(' for function call")

  funcIdentifier = tList.tList[tList.index].value
  tList.index += 2

  paramChunk = []
  while tList.tList[tList.index].value != ")": #this isnt going to work as it cant call tList.tList[tList.index], figure it out later
    if tList.index >= len(tList.tList):
      errorHandling("Error: expected ')' for function declaration")
    else:
      paramChunk.append(tList.tList[tList.index])
      tList.index += 1

  paramCheck = False
  paramList = []

  for i in paramChunk:
    if i.value != ",":
      if paramCheck == True:
        errorHandling("Expected , separating parameters")
      else:
        paramList.append(argument(i.value, i.type))
        paramCheck = True

    elif i.value == ",":
      paramCheck = False

  eList.eList.append(funcCallEvent("funcCall", funcIdentifier, paramList))
  tList.index += 1

def getEvents(tList, eList, vH, fH, ifWhileConditional):
  while tList.index < len(tList.tList):
    if tList.tList[tList.index].type == "keyword":
      if tList.tList[tList.index].value in ["str", "int", "bool", "string", "integer", "boolean"]:
        grabVar(tList, eList, vH)
      elif tList.tList[tList.index].value == "if":
        grabIf(tList, eList, vH, fH)
      elif tList.tList[tList.index].value == "while":
        grabWhile(tList, eList, vH, fH)
      elif tList.tList[tList.index].value == "def":
        grabFuncDeclare(tList, eList, vH, fH)
      elif tList.tList[tList.index].value == "return":
        grabFuncReturn(tList, eList, vH)
      else:
        errorHandling("Unrecognised keyword: " + tList.tList[tList.index].value + " at line number: " + str(tList.tList[tList.index].lineNum))

    elif tList.tList[tList.index].type == "identifier":
      if tList.tList[tList.index].value in vH.varList:
        changeVar(tList, eList, vH)
      else:
        errorHandling("Undefined variable: " + tList.tList[tList.index].value + " called at line number: " + str(tList.tList[tList.index].lineNum))

    elif tList.tList[tList.index].type == "function":
      if tList.tList[tList.index].value in fH.funcList:
        callFunc(tList, eList)
      else:
        errorHandling("Undefined function: " + tList.tList[tList.index].value + " called at line number: " + str(tList.tList[tList.index].lineNum))

  if ifWhileConditional == True:
    return eList.eList