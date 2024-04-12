from lexer import *
from parser import *
from evaluator import inEventList, evaluateEvents, varList, funcList

import subprocess
import sys
import os
from tkinter import *
from tkinter.ttk import *
from decimal import *

from tkinter.filedialog import askopenfilename, asksaveasfilename
text = 'def neek() {\n input("neek")\nreturn "neek" }'
def mouseWheel():
  beforeScroll = inText.yview()
  numOfLines = int(inText.index('end-1c').split('.')[0])
  yViewofLines = ((beforeScroll[0]*numOfLines/1000))
  lineNums.yview_moveto(yViewofLines)
  inputBox.after(1, mouseWheel)

def newFile():  #works
  programName = os.path.abspath(__file__)
  subprocess.Popen([sys.executable, programName])

def openFile():  #works
  programName = os.path.abspath(__file__)
  subprocess.Popen([sys.executable, programName, 'enterText'])

def saveAsFile():  #works
  codeToSave = inText.get("1.0", END)
  file = asksaveasfilename(defaultextension=".txt",
                           filetypes=[("text file", "*.txt")])
  global currentFileName
  currentFileName = file
  saveToFile = open(file, 'w')
  saveToFile.write(codeToSave)
  saveToFile.close()


def saveFile():  #works
  try:
    codeToSave = inText.get("1.0", END)
    saveToFile = open(currentFileName, 'w')
    saveToFile.write(codeToSave)
    saveToFile.close()
  except:
    saveAsFile()


def exit():  #need to make this check if you've saved
  quit()


def runFile(
):  #fetching text works, edit once backend is complete to send to backend
  codeToSend = inText.get("1.0", END)
  codeToSend = codeToSend[:-1]
  text = 'int i = 3\n\nif (i==3) {\noutput("neek")\n}'
  
  cList = charaList(codeToSend)
  tList = tokenList()

  getTokens(cList, tList)

  #for i in tList.tList:
  #  print(i)
  
  eList = eventList()
  inTList = inTokenList(tList.tList)
  vH = varHandler()
  fH = funcHandler()

  getEvents(inTList, eList, vH, fH, False)

  inEList = inEventList(eList.eList, 0)

  vList = varList()
  fList = funcList()

  for i in eList.eList:
    print(i)
  
  evaluateEvents(inEList, vList, fList, False)
  
  consoleBox = Tk()
  consoleBox.title("Console")
  consoleText = Text(consoleBox)
  consoleText.pack()
  
  #for i in eList.eList:
  #  consoleText.insert(END, i)
  #  consoleText.insert(END, "\n")
  #  if i.name == "if" or i.name == "while" or i.name == "funcDeclare":
  #    for j in i.contents:
  #      consoleText.insert(END, "{")
  #      consoleText.insert(END, j)
  #      consoleText.insert(END, "}")
  #     consoleText.insert(END, "\n")



def copyText():  # works
  try:
    textToCopy = inText.selection_get()
    tkClip = Tk()
    tkClip.clipboard_clear()
    tkClip.clipboard_append(textToCopy)
    tkClip.after(1, tkClip.destroy)
  except:
    pass


def pasteText():  # i think this works who knows though
  try:
    textToDelete = inText.selection_get()
    tkClip = Tk()
    textToPaste = tkClip.clipboard_get()
    tkClip.after(1, tkClip.destroy)
    pos = inText.index(INSERT)
    inText.delete("sel.first", "sel.last")
    inText.insert(pos, textToPaste)
  except:
    tkClip = Tk()
    try:
      textToPaste = tkClip.clipboard_get()
      pos = inText.index(INSERT)
      inText.insert(pos, textToPaste)
      tkClip.after(1, tkClip.destroy)
    except:
      tkClip.after(1, tkClip.destroy)


inputBox = Tk()
inputBox.title('PUT PROGRAM NAME HERE WHEN DECIDED')
upperMenu = Menu(inputBox)
fileMenu = Menu(upperMenu, tearoff=0)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save as", command=saveAsFile)
fileMenu.add_command(label="Exit", command=exit)

upperMenu.add_cascade(label="File", menu=fileMenu)

editMenu = Menu(upperMenu, tearoff=0)
editMenu.add_command(label="Copy", command=copyText)
editMenu.add_command(label="Paste", command=pasteText)

upperMenu.add_cascade(label="Edit", menu=editMenu)

runMenu = Menu(upperMenu, tearoff=0)
runMenu.add_command(label="Run Module", command=runFile)

upperMenu.add_cascade(label="Run", menu=runMenu)

inFrame = Frame()
inFrame.pack()
inLabel = Label(text="Write code above") # DELETE THIS IT LOOKS DUMB
inLabel.pack()
inText = Text(inFrame, width = 100)
inText.pack(side='right')
lineNums = Text(inFrame, width=4)
lineNums.pack(side='left')

#inText.bind("<MouseWheel>", mouseWheel)
#inText.bind("<Button-4>", mouseWheel)
#inText.bind("<Button-5>", mouseWheel)
#inText.bind("<Key>", mouseWheel)

loopNum = 1
while loopNum != 1001:
  if len(str(loopNum)) == 1:
    loopText = "000" + str(loopNum)
    lineNums.insert(END, loopText)
  elif len(str(loopNum)) == 2:
    loopText = "00" + str(loopNum)
    lineNums.insert(END, loopText)
  elif len(str(loopNum)) == 3:
    loopText = "0" + str(loopNum)
    lineNums.insert(END, loopText)
  elif len(str(loopNum)) == 4:
    loopText = str(loopNum)
    lineNums.insert(END, loopText)
  loopNum += 1

if len(sys.argv) > 1:
  file = askopenfilename(parent=inputBox)
  global currentFileName
  currentFileName = file
  openFile = open(file, 'r')
  codeToOpen = openFile.read()
  openFile.close()
  inText.delete("1.0", END)
  inText.insert("1.0", codeToOpen)

inputBox.after(1, mouseWheel)

inputBox.config(menu=upperMenu)
lineNums.config(state=DISABLED)
inputBox.mainloop()