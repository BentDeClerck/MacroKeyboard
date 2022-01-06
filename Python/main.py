from tkinter.constants import S
import pyfirmata2; from pyfirmata2 import Arduino, util; import serial  
import time; import os; import fileinput; import csv
import tkinter as tk
import pynput; from pynput import keyboard; from pynput.keyboard import Listener, Key, Controller


Mykeyboard = Controller()
SleepTime = 2
listener = None


# port = serial.Serial('/dev/tty.usbserial-A9G7FD1P', 9600, timeout=1)
board = Arduino(Arduino.AUTODETECT)
it = pyfirmata2.util.Iterator(board)
it.start()

#### SETUP PINS ####
pin1 = board.digital[2]; pin2 = board.digital[3]; pin3 = board.digital[4]; pin4 = board.digital[5]; pin5 = board.digital[6]; pin6 = board.digital[7]
arduinopins = [pin1, pin2, pin3, pin4, pin5, pin6]
for i in range (len(arduinopins)):
    arduinopins[i].mode = pyfirmata2.INPUT

previousstate1 = 0; previousstate2 = 0; previousstate3 = 0; previousstate4 = 0; previousstate5 = 0; previousstate6 = 0; 


switcher = {
    'Key.cmd' : Key.cmd,
    '<Key.cmd: <55>>' : Key.cmd,
    'Key.ctrl' : Key.ctrl,
    '<Key.ctrl: <59>>' : Key.ctrl,
    'Key.ctrl_l': Key.ctrl,
    '<Key.ctrl_l: <162>>' : Key.ctrl,
    'Key.ctrl_r': Key.ctrl,
    '<Key.ctrl_r: <163>>' : Key.ctrl,
    'Key.alt' : Key.alt,
    '<Key.alt: <58>>' : Key.alt,
    'Key.alt_l' : Key.alt_l,
    '<Key.alt_l: <164>>' : Key.alt_l,
    'Key.alt_gr' : Key.alt_gr,
    '<Key.alt_gr: <165>>' : Key.alt_gr, 
    'Key.shift' : Key.shift,
    '<Key.shift: <56>>' : Key.shift,
    'Key.shift_r' : Key.shift_r,
    '<Key.shift_r: <161>>' : Key.shift_r,
    'Key.enter' : Key.enter,
    '<Key.enter: <36>>' : Key.enter,
    'Key.backspace': Key.backspace,
    '<Key.backspace: <51>>' : Key.backspace,
    'Key.menu' : Key.menu,
    '<Key.menu: <93>>' : Key.menu,
    'Key.esc' : Key.esc,
    '<Key.esc: <27>>' : Key.esc,
    'Key.space' : Key.space
}



#### DEFINE MACRO CLASS AND CREATING CLASS OBJECTS ####
class macrokey:
    def __init__(self, name, command, arduinobutton, arduinoled):
        self.name = name
        self.command = command
        self.arduinobutton = arduinobutton
        self.arduinoled = arduinoled
        

    def ExecuteCommand(self):
        try:
            [Mykeyboard.press(x) for x in self.command]
            [Mykeyboard.release(x) for x in self.command]
        except ValueError:
            print('No Value')
        

    def UpdateFile(self):
        with open('MacroLog.csv', 'w', newline='') as wf:
            writer = csv.writer(wf)
            Log[self.arduinobutton-2] = [self.name, (', '.join(map(str, self.command)).replace("'",'')), self.arduinobutton, self.arduinoled]
            writer.writerows(Log)

    def printnames(self):
        print('Naam: ',self.name)
        print('Command: ',self.command)
        print('Arduinobutton: ',self.arduinobutton)
        print('Arduinoled: ',self.arduinoled)
        print(" ")

k1 = macrokey(str(), list(), 2, 6)
k2 = macrokey(str(), list(), 3, 7)
k3 = macrokey(str(), list(), 4, 8)
k4 = macrokey(str(), list(), 5, 9)
k5 = macrokey(str(), list(), 6, 9)
k6 = macrokey(str(), list(), 7, 9)
Macros = [k1, k2, k3, k4, k5, k6]

#### FORMAT COMMAND ####
def formatCommand(command):
    try:    
        for i in range (len(command)):
            command[i] = command[i].replace(" ",'')
            if (len(command[i])) > 3 and switcher.get(command[i]) != None:
                command[i] = switcher.get(command[i])                
        return(command) 
        
    except TypeError:
        return(command)


#### HANDLE ARDUINO ####
def RunArduino():
    global previousstate1; global previousstate2; global previousstate3; global previousstate4; global previousstate5; global previousstate6;  

    pinstate1 = pin1.read()
    pinstate2 = pin2.read()
    pinstate3 = pin3.read()
    pinstate4 = pin4.read()
    pinstate5 = pin5.read()
    pinstate6 = pin6.read()


    if (pinstate1 == True and previousstate1 == 0):
        print(f'{Macros[0].name} pressed')
        previousstate1 = 1
        Macros[0].ExecuteCommand()

    elif pinstate2 == True and previousstate2 == 0:
        print(f'{Macros[1].name} pressed')
        Macros[1].ExecuteCommand() 
        previousstate2 = 1

    elif pinstate3 == True and previousstate3 == 0:
        print(f'{Macros[2].name} pressed')
        Macros[2].ExecuteCommand()  
        previousstate3 = 1

    elif pinstate4 == True and previousstate4 == 0:
        print(f'{Macros[3].name} pressed')
        Macros[3].ExecuteCommand() 
        previousstate4 = 1
        
    elif pinstate5 == True and previousstate5 == 0:
        print(f'{Macros[4].name} pressed')
        Macros[4].ExecuteCommand() 
        previousstate5 = 1

    elif pinstate6 == True and previousstate6 == 0:
        print(f'{Macros[5].name} pressed')
        Macros[5].ExecuteCommand() 
        previousstate6 = 1
    

    if (pinstate1 == False and previousstate1 == 1):
        previousstate1 = 0

    elif (pinstate2 == False and previousstate2 == 1):
        previousstate2 = 0

    elif (pinstate3 == False and previousstate3 == 1):
        previousstate3 = 0

    elif (pinstate4 == False and previousstate4 == 1):
        previousstate4 = 0

    elif (pinstate5 == False and previousstate5 == 1):
        previousstate5 = 0

    elif (pinstate6 == False and previousstate6 == 1):
        previousstate6 = 0
        
           
    main.after(SleepTime, RunArduino)


#### HANDLE KEYPRESSES ####
def KeyLog(macrokey):
    def on_press(key):           
        if switcher.get(key) != None:
            key = switcher.get(key)
        macrokey.command.append(key) 

    def StartListener():
        global listener 
        if not listener:
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            print('Listener Started')
        macrokey.command = []
        
    StartListener()

def StopListener():
    global listener
    if listener:
        listener.stop()
        listener.join()
        listener = None
        print('Listener Stopped')


#### OPEN NEW WINDOW ####
def OpenEditWindow():
    global EditWindow
    EditWindow = tk.Toplevel()
    EditWindow.title('Edit')

    for i in range (len(Macros)):
        tk.Label(EditWindow, text=i+1, width=1, bg='White').grid(row=i+1, column=1)
        tk.Label(EditWindow, text='Set Name:', width=8, bg='grey').grid(row=i+1, column=2)
        tk.Label(EditWindow, text='Set:', width=4, bg='grey').grid(row=i+1, column=4)

    global naam1; global naam2; global naam3; global naam4; global naam5; global naam6
    naam1 = tk.Entry(EditWindow); naam1.grid(row=1, column=3)
    naam2 = tk.Entry(EditWindow); naam2.grid(row=2, column=3)
    naam3 = tk.Entry(EditWindow); naam3.grid(row=3, column=3)
    naam4 = tk.Entry(EditWindow); naam4.grid(row=4, column=3)
    naam5 = tk.Entry(EditWindow); naam5.grid(row=5, column=3)
    naam6 = tk.Entry(EditWindow); naam6.grid(row=6, column=3)

    tk.Button(EditWindow, text='Macro 1', width=7, command= lambda: KeyLog(Macros[0])).grid(row=1, column=5)
    tk.Button(EditWindow, text='Macro 2', width=7, command= lambda: KeyLog(Macros[1])).grid(row=2, column=5)
    tk.Button(EditWindow, text='Macro 3', width=7, command= lambda: KeyLog(Macros[2])).grid(row=3, column=5)
    tk.Button(EditWindow, text='Macro 4', width=7, command= lambda: KeyLog(Macros[3])).grid(row=4, column=5)
    tk.Button(EditWindow, text='Macro 5', width=7, command= lambda: KeyLog(Macros[4])).grid(row=5, column=5)
    tk.Button(EditWindow, text='Macro 6', width=7, command= lambda: KeyLog(Macros[5])).grid(row=6, column=5)

    tk.Button(EditWindow, text='Quit',command=EditWindow.withdraw).grid(row=(len(Macros)+1),column=1,pady=3, padx=2)
    tk.Button(EditWindow, text='Save',command=SaveButton).grid(row=(len(Macros)+1),column=5,pady=3, padx=2)
    
    RunArduino()

#### SAVING AND REFRESHING MAIN WINDOW ####
def SaveButton():
    lijst = [naam1, naam2, naam3, naam4, naam5, naam6]
    for i in range (len(Macros)):
        if (len(lijst[i].get())) != 0:
            Macros[i].name = lijst[i].get()
            lijst[i].delete(0, tk.END)
        Macros[i].UpdateFile()
    
    Refresh()
    StopListener()

def Refresh():
    for i in range (len(Macros)):
        tk.Button(text=(Macros[i].name), command=(Macros[i].ExecuteCommand), width=20).grid(row=i+1, column=1)
        text = ''
        for f in range (len(Macros[i].command)):
            lijst = Macros[i].command
            if f == 0:
                text = text + format(lijst[f]).replace("'",'').replace('Key.', '')
            else:
                text = text + '+' + format(lijst[f]).replace("'",'').replace('Key.', '')
            tk.Label(text=text, width=20).grid(row=i+1, column=2)
            
           
      
      
           
           
            
#### OPENING FILE ####    
def ReadFile():
    with open('MacroLog.csv', 'r', newline='') as rf:
        reader = csv.reader(rf)
        global Log
        Log = list(reader)

try:
    if os.path.getsize('MacroLog.csv') > 0:
        print("File Found!")
        with open ('MacroLog.csv', 'r', newline='') as rf:
            reader = csv.reader(rf)
            Log = list(reader)

            for i in range (len(Log)):
                data = Log[i]
                
                try:     
                    if data[2] != '':  
                        data[1] = (lambda data: data.split(','))(data[1])                  
                        data[1] = formatCommand(data[1])
                        Macros[int(data[2])-2] = macrokey(data[0], data[1], int(data[2]), int(data[3]))
                        Macros[int(data[2])-2].UpdateFile()
                except IndexError:
                    pass   
                             
    else:
        print("File Empty")    
        with open('MacroLog.csv', 'w', newline='') as wf:
            writer = csv.writer(wf)
            [writer.writerow(['','',str(i+2),str(i+7)]) for i in range(len(Macros))]
        ReadFile()
        print('Filled In File')

except FileNotFoundError:
    print("No file Found")
    with open('MacroLog.csv', 'w', newline='') as wf:
        print('File Created')
        writer = csv.writer(wf)
        [writer.writerow(['','',str(i+2),str(i+7)]) for i in range(len(Macros))]
    ReadFile()
    print('Filled In File')  
        

#### START MAIN WINDOW AND ARDUINO ####
global main
main = tk.Tk()
main.title('Main')


tk.Label(text='Macro',fg='White',bg='Grey', borderwidth=2, relief='solid', width=20, padx=2, pady=2).grid(row=0, column=1)
tk.Label(text='Command', fg='White',bg='Grey', borderwidth=2, relief='solid', width=20, padx=2, pady=2).grid(row=0, column=2)


tk.Button(text='Quit',command=main.quit).grid(row=(len(Macros)+2),column=1,pady=3, padx=2)
tk.Button(text='Edit', command=OpenEditWindow).grid(row=(len(Macros)+2),column=2,pady=3, padx=2)


RunArduino()
Refresh()
main.mainloop()

if listener:
    listener.stop()
    listener.join()



#board.analog[2].enable_reporting()
#print(board.analog[2].read())
#time.sleep(0.5)#time.sleep(0.5)

# http://www.aemn.pt/formacao/Arduino/DVD_tutorial%20-%20Arduino/arduino%20eBook%20Collection/Python%20Programming%20for%20Arduino.pdf
# https://pypi.org/project/pyFirmata2/
