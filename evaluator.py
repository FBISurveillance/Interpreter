#names: varDeclare, if, while, funcDeclare, funcReturn, varChange, funcCall
from parser import errorHandling, callFunc, inTokenList
from intHandler import AST, evaluate

class varList:
  def __init__(self):
    self.varNames = []
    self.variables = []

class variable:
  def __init__(self, name, type, value):
    self.name = name
    self.type = type
    self.value = value

class funcList:
  def __init__(self):
    self.funcNames = []
    self.functions = []

class function:
  def __init__(self, name, args, body, expectReturn):
    self.name = name
    self.args = args
    self.body = body
    self.expectReturn = expectReturn

class argument:
  def __init__(self, name, type):
    self.name = name
    self.type = type

class inEventList:
  def __init__(self, eList, index):
    self.eList = eList
    self.index = 0

def resolve(tokens, vList, fList):
  if tokens[0].type == "int":
    return intHandler(tokens, vList, fList)
  elif tokens[0].type == "str":
    return concatHandler(tokens, vList, fList)
  elif tokens[0].type == "bool":
    if len(tokens) == 1:
      return tokens[0].value
    else:
      errorHandling("Error: only one value expected at line " + str(tokens[0].lineNum))
  elif tokens[0].type == "function":
    return funcHandler(tokens, vList, fList)

def getConds(condTokens, vList, fList):
  cond1Tokens = []
  comparator = ""
  cond2Tokens = []
  i = 0
  while condTokens[i] != "==" and condTokens[i] != "!=" and condTokens[i] != "<" and condTokens[i] != ">" and condTokens[i] != "<=" and condTokens[i] != ">=":
    cond1Tokens.append(condTokens)
    i += 1

  comparator = condTokens[i]
  i += 1

  while i != len(condTokens):
    cond2Tokens += condTokens[i]
    i += 1

  cond1 = resolve(cond1Tokens, vList, fList)
  cond2 = resolve(cond2Tokens, vList, fList)

  condBool = None

  if comparator == "==":
    if cond1 == cond2:
      condBool = True
    else:
      condBool = False
  elif comparator == "!=":
    if cond1 != cond2:
      condBool = True
    else:
      condBool = False
  elif type(cond1) != int:
    errorHandling("Error: comparator " + comparator + " is not supported at line " + str(cond1Tokens[0].lineNum) + " for type " + type(cond1))
  else:
    if comparator == ">":
      if cond1 > cond2:
        condBool = True
      else:
        condBool = False
    if comparator == "<":
      if cond1 < cond2:
        condBool = True
      else:
        condBool = False
    if comparator == "<=":
      if cond1 <= cond2:
        condBool = True
      else:
        condBool = False
    if comparator == ">=":
      if cond1 >= cond2:
        condBool = True
      else:
        condBool = False

def ifEvent(eventsToAdd, condTokens, vList, fList, eList):
  condBool = getConds(condTokens, vList, fList)

  if condBool:
    evaluateEvents(eventsToAdd, vList, fList, False)

  eList.index += 1

def whileEvent(eventsToAdd, condTokens, vList, fList, eList):
  condBool = getConds(condTokens, vList, fList)

  while condBool:
    evaluateEvents(eventsToAdd, vList, fList, False)

  eList.index += 1

def intHandler(varContents, vList, fList): #tested everything but function
  intList = []
  index = 0

  while index < len(varContents):
    i = varContents[index]
    if type(i) == str:
      count = 0

      while vList.varNames[count] != i:
        count += 1

      intList.append(str(vList.variables[count].value))

    elif i.type == "int" or i.type == "operator":
      intList.append(i.value)

    elif i.type == "function":
      chunk = []
      while i.value != ")":
        chunk.append(i)
        index += 1
        i = varContents[index]


      chunk.append(i)
      index += 1

      varValue = funcHandler(chunk, vList, fList)
      print("called second")
      
      if varValue.type == "int":
        intList.append(varValue.value)

    elif i.type == "punctuation" and (i.value == "(" or i.value == ")"):
      intList.append(i.value)

    else:
      errorHandling("Error: Invalid type at line " + str(i.lineNum))

    index += 1

  outNode = AST(intList)
  intValue = evaluate(outNode)

  return intValue

def concatHandler(varContents, vList, fList): #checked for everything but function working
  strings = []
 
  for i in varContents:
    if type(i) == str:
      count = 0

      while vList.varNames[count] != i:
        count += 1

      strings.append(vList.variables[count].value)

    elif i.type == "str":
      strings.append(i.value)

    elif i.type == "function":
      chunk = ""
      chunk += i.value
      while i.value != ")":
        chunk += i.value
        i += 1

      chunk += i.value
      i += 1

      varValue = funcHandler(chunk, vList, fList)
      if varValue.type == "str":
        strings.append(varValue.value)
      else:
        errorHandling("Error: Invalid type at line " + str(i.lineNum))

    elif i.type == "operator":
      if i.value == "+":
        strings.append(i)
      else:
        errorHandling("Error: Invalid operator at line " + str(i.lineNum))

    else:
      errorHandling("Error: Invalid type " + i.type + " at line " + str(i.lineNum))
  
  while len(strings) != 1:
    if type(strings[0]) != str:
      errorHandling("Error: Invalid type at line " + str(i.lineNum))
    if strings[1].value != "+":
      errorHandling("Error: Expected + for concatenation at line number " + str(i.lineNum))
    if type(strings[2]) != str:
      errorHandling("Error: Invalid type at line " + str(i.lineNum))

    strings[0] = strings[0] + strings[2]
    del strings[1]
    del strings[1]

  return strings[0]

def varDeclareEvent(eList, vList, fList):
  varIdentifier = eList.eList[eList.index].varName
  varContents = eList.eList[eList.index].contents
  varType = eList.eList[eList.index].varType
  if len(varContents) == 1:
    vList.varNames.append(varIdentifier)
    vList.variables.append(variable(varIdentifier, varType, varContents[0].value))
    eList.index += 1
  else:
    if varType == "str":
      varValue = concatHandler(varContents, vList, fList)
      vList.varNames.append(varIdentifier)
      vList.variables.append(variable(varIdentifier, varType, varValue))
      eList.index += 1

    elif varType == "int":
      print("SOMETHING GOT ADDED: " + varIdentifier)
      varValue = intHandler(varContents, vList, fList)
      vList.varNames.append(varIdentifier)
      vList.variables.append(variable(varIdentifier, varType, varValue))
      eList.index += 1


def funcHandler(tokens, vList, fList):
  #adding code to grab all of function call here
  for i in vList.variables:
    print(i)
  tempTList = inTokenList(tokens)
  tempEList = inEventList([], 0)

  callFunc(tempTList, tempEList)
  
  if len(tempEList.eList) != 1:
    errorHandling("Error: nothing expected before/after function call at line " + str(tempEList.eList[0].lineNum))
  
  returnVar = evaluateEvents(tempEList, vList, fList, True)
  for i in tempEList.eList:
    print(i)
    print("SHASHUMGA")

  print(returnVar)
  if returnVar.type == "identifier":
    for i in vList.variables:  
      print("NEEEEEEEKER")
    
  return returnVar

def varChangeEvent(eList, vList, fList):
  varIdentifier = eList.eList[eList.index].varIdentifier
  varContents = eList.eList[eList.index].contents
  varType = eList.eList[eList.index].varType
  if len(varContents == 1):
    for i in vList.variables:
      if i.name == varIdentifier:
        i.value = varContents[0].value
        break
  else:
    if varType == "string":
      varValue = concatHandler(varContents, vList, fList)
      for i in vList.variables:
        if i.name == varIdentifier:
          i.value = varValue
          eList.index += 1
          break

    elif varType == "int":
      varValue = intHandler(varContents, vList, fList)
      for i in vList.variables:
        if i.name == varIdentifier:
          i.value = varValue
          eList.index += 1
          break

def funcDeclareEvent(funcName, eventsToAdd, paramList, fList, eList):
  fList.funcNames.append(funcName)

  expectReturn = False
  for i in eventsToAdd:
    if i.name == "funcReturn":
      expectReturn = True

  fList.functions.append(function(funcName, paramList, eventsToAdd, expectReturn))
  eList.index += 1


def funcCallEvent(funcName, paramList, vList, fList, eList):
  i = 0
  while i < len(fList.funcNames):
    if fList.funcNames[i] == funcName:
      break
    i += 1

  if i == len(fList.funcNames):
    errorHandling("Error: function " + funcName + " not found at line " + str(paramList[0].lineNum))

  func = fList.functions[i]
  expectReturn = func.expectReturn

  if len(func.args) != len(paramList):
    errorHandling("Error: function " + funcName + " expects " + str(len(func.args)) + " arguments at line " + str(paramList[0].lineNum))

  funcVars = varList()

  i = 0
  while i < len(func.args):
    funcVars.varNames.append(func.args[i].name)
    varValue = resolve(paramList[i], vList, fList)
    funcVars.variables.append(variable(func.args[i].name, func.args[i].type, varValue))
    i += 1

#def evaluateEvents(eList, vList, fList, expectReturn):
  tempEList = inEventList(func.body, 0)
  
  
  if func.expectReturn:
    varToReturn = evaluateEvents(tempEList, funcVars, fList, expectReturn)
    eList.index += 1
    return varToReturn

  elif func.expectReturn == False:
    evaluateEvents(func.body, funcVars, fList, expectReturn)
    eList.index += 1

def evaluateEvents(eList, vList, fList, expectReturn):
  while eList.index < len(eList.eList):
    if eList.eList[eList.index].name == "if":
      ifEvent(eList.eList[eList.index].eventsToAdd, eList.eList[eList.index].condTokens, vList, fList, eList)
    elif eList.eList[eList.index].name == "while":
      whileEvent(eList.eList[eList.index].eventsToAdd, eList.eList[eList.index].condTokens, vList, fList, eList)
    elif eList.eList[eList.index].name == "varDeclare":
      varDeclareEvent(eList, vList, fList)
    elif eList.eList[eList.index].name == "varChange":
      varChangeEvent(eList, vList, fList)
    elif eList.eList[eList.index].name == "funcDeclare":
      funcDeclareEvent(eList.eList[eList.index].funcName, eList.eList[eList.index].contents, eList.eList[eList.index].parameters, fList, eList)
    elif eList.eList[eList.index].name == "funcReturn":
      if expectReturn == True:
        return eList.eList[eList.index].contents
      else:
        errorHandling("Error: return statement not expected at line " + str(eList.eList[eList.index].contents[0].lineNum))
    elif eList.eList[eList.index].name == "funcCall":
        possibleValue = funcCallEvent(eList.eList[eList.index].funcName, eList.eList[eList.index].contents, vList, fList, eList)
        if possibleValue != None:
          return possibleValue
      

#NEED TO ADD FUNCTION THAT ADDS INITIAL FUNCTIONS (e.g. input, output)