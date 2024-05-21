# WATCHDOG
from threading import Timer

class Watchdog(Exception):
    def __init__(self, timeout, userHandler=None):
        self.timeout = timeout
        self.handler = userHandler if userHandler else None
        self.timer = Timer(self.timeout, self.handler)
    
    def start(self):
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        
    def addHandler(self, h):
        self.handler = h
        
# declaro por adelantado para que el compilador sepa de esto en las funciones de parseo
wdMPPT = Watchdog(3.0)
wdKART = Watchdog(3.0)

# SERIAL
import serial
from serial.tools import list_ports
import re

serialMPPT = None
serialKART = None
bufferMPPT = ""
bufferKART = ""

puerto_mppt = None
puerto_kart = None
available_ports = {i:p.device for i,p in enumerate(list_ports.comports())}
if len(available_ports) > 0:
    print("Seleccione puerto para el MPPT: " + str(available_ports))
    j = int(input("Seleccione nro de lista (-1 para no elegir nada): "))
    if j != -1:
        puerto_mppt = available_ports[j]
        del available_ports[j]
if len(available_ports) > 0:
    print("Seleccione puerto para el Karting: " + str(available_ports))
    j = int(input("Seleccione nro de lista (-1 para no elegir nada): "))
    if j != -1:
        puerto_kart = available_ports[j]
        del available_ports[j]

if puerto_mppt:
    serialMPPT = serial.Serial(puerto_mppt, baudrate=19200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1)
if puerto_kart:
    serialKART = serial.Serial(puerto_kart, baudrate=19200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1)

V_pan, I_pan, P_pan, V_bat, I_bat, P_bat, I_load, P_load = "0"*8
V_kart, I_kart, P_kart = "0"*3

def lecturaMPPT():
    global bufferMPPT   

    try:
        nuevo = serialMPPT.read(serialMPPT.inWaiting()).decode()
        bufferMPPT += nuevo
        if re.search(r"[\r\n]", nuevo):
            parseoMPPT()
    except:
        pass

def lecturaKART():
    global bufferKART
    
    try:
        nuevo = serialKART.read(serialKART.inWaiting()).decode()
        bufferKART += nuevo
        if re.search(r"[\r\n]", nuevo):
            parseoKART()
    except:
        pass

def parseoMPPT():
    global V_pan, I_pan, P_pan, V_bat, I_bat, P_bat, P_load, I_load
    global bufferMPPT
    
    if not re.search(r"[\r\n]", bufferMPPT):
        V_pan = I_pan = P_pan = V_bat = I_bat = P_bat = I_load = P_load = "?"
        bufferMPPT = ""
        wdMPPT.reset()
        return
        
    tokens = re.split(r"[\r\n]+", bufferMPPT)
    bufferMPPT = tokens[-1]
    
    V_pan_f = P_pan_f = V_bat_f = I_bat_f = I_load_f = None    
    
    for t in tokens[0:-1]:
        m = re.search(r"^(\S+)\s+([0-9-]+)$", t)
        
        if not m:
            continue
           
        campo, valor = m.group(1), float(m.group(2))
           
        if campo == "VPV":
            V_pan = f"{valor:.2f}"
            V_pan_f = valor
        elif campo == "I":
            valor /= 1000
            I_bat = f"{valor:.2f}"
            I_bat_f = valor
        elif campo == "V":
            valor /= 1000
            V_bat = f"{valor:.2f}"
            V_bat_f = valor
        elif campo == "PPV":
            P_pan = f"{valor:.2f}"
            P_pan_f = valor
        elif campo == "IL":
            valor /= 1000
            I_load = f"{valor:.2f}"
            I_load_f = valor
       
    if V_pan_f or P_pan_f:
        I_pan_f = (P_pan_f if P_pan_f else float(P_pan)) / (V_pan_f if V_pan_f else float(V_pan))
        I_pan = f"{I_pan_f:.2f}"
    
    if V_bat_f or I_bat_f:
        P_bat_f = (I_bat_f if I_bat_f else float(I_bat)) * (V_bat_f if V_bat_f else float(V_bat))
        P_bat = f"{P_bat_f:.2f}"
    
    if I_load_f or V_bat_f:
        P_load_f = (V_bat_f if V_bat_f else float(V_bat)) * (I_load_f if I_load_f else float(I_load))
        P_load = f"{P_load_f:.2f}"
        
    wdMPPT.reset()
    
def parseoKART():
    global V_kart, I_kart, P_kart
    global bufferKART
    
    if not re.search(r"[\r\n]", bufferKART):
        V_kart, I_kart, P_kart = 3*"?"
        bufferKART = ""
        wdKART.reset()
        return
    
    tokens = re.split(r"[\r\n]+", bufferKART)
    bufferKART = tokens[-1]
    
    for t in tokens[0:-1]:
        m = re.search(r"^([0-9-]+)\s+([0-9-]+)$", t)
        if not m:
            continue

        V_kart_f, I_kart_f = float(m.group(1))/1000, float(m.group(2))/1000
        P_kart_f = V_kart_f * I_kart_f
        
        V_kart = f"{V_kart_f:.2f}"
        I_kart = f"{I_kart_f:.2f}"
        P_kart = f"{P_kart_f:.2f}"
    
    wdKART.reset()
    
# TKINTER
import tkinter
from tkinter import messagebox
from tkinter import PhotoImage
mw=tkinter.Tk()
mw.title("Interfaz gráfica")
#mw.geometry("400x300")

#Stringvars de lo que va a variar
V_panS=tkinter.StringVar()
I_panS=tkinter.StringVar()
P_panS=tkinter.StringVar()
V_batS=tkinter.StringVar()
I_batS=tkinter.StringVar()
P_batS=tkinter.StringVar()
V_loadS=tkinter.StringVar()
I_loadS=tkinter.StringVar()
P_loadS=tkinter.StringVar()

V_kartS=tkinter.StringVar()
I_kartS=tkinter.StringVar()
P_kartS=tkinter.StringVar()

P_efS=tkinter.StringVar()

def visualizacion():
    global V_pan, I_pan, P_pan, V_bat, I_bat, P_bat, P_load, I_load
    global V_kart, I_kart, P_kart
    
    V_panS.set(V_pan+"V")
    I_panS.set(I_pan+"A")
    P_panS.set(P_pan+"W")
    V_batS.set(V_bat+"V")
    I_batS.set(I_bat+"A")
    P_batS.set(P_bat+"W")
    V_loadS.set(V_bat+"V")
    I_loadS.set(I_load+"A")
    P_loadS.set(P_load+"W")
    V_kartS.set(V_kart+"V")
    I_kartS.set(I_kart+"A")
    P_kartS.set(P_kart+"W")
    
    if re.search(r"[1-9]", P_load):
        P_efS.set(f"{(float(P_kart)/float(P_load)*100.0):.2f}"+"%")

mw['bg'] = '#000000'

#Labels titulos
lbl_Titulo=tkinter.Label(text="Estacion de carga Inalambrica Verde\n de Vehiculos Electricos(ECIVVE)",bg='#000000',fg='#FFFFFF',font=("Roboto Cn",14),justify="center")
lbl_Titulo2=tkinter.Label(text="Monitoreo de Potencia",bg='#000000',fg='#FFFFFF',font=("Roboto Cn",20),justify="center")
lbl_V_batS=tkinter.Label(text="Tension Bateria:",bg='#000000',fg='#FFFFFF')
lbl_P_batS=tkinter.Label(text="Potencia Bateria:",bg='#000000',fg='#FFFFFF')
lbl_I_loadS=tkinter.Label(text="Corriente Carga:",bg='#000000',fg='#FFFFFF')


lbl_V_kartS=tkinter.Label(text="Tension Kart:",bg='#000000',fg='#FFFFFF')
lbl_I_kartS=tkinter.Label(text="Corriente Kart:",bg='#000000',fg='#FFFFFF')
lbl_P_kartS=tkinter.Label(text="Potencia Kart:",bg='#000000',fg='#FFFFFF')


#labels datos variantes
entry_V_panS=tkinter.Label(mw, textvar=V_panS,bg='#000000',fg='#FFFFFF')
entry_I_panS=tkinter.Label(mw, textvar=I_panS,bg='#000000',fg='#FFFFFF')
entry_P_panS=tkinter.Label(mw, textvar=P_panS,bg='#000000',fg='#FFFFFF')
entry_V_batS=tkinter.Label(mw, textvar=V_batS,bg='#000000',fg='#FFFFFF')
entry_I_batS=tkinter.Label(mw, textvar=I_batS,bg='#000000',fg='#FFFFFF')
entry_P_batS=tkinter.Label(mw, textvar=P_batS,bg='#000000',fg='#FFFFFF')
entry_V_loadS=tkinter.Label(mw, textvar=V_loadS,bg='#000000',fg='#FFFFFF')
entry_I_loadS=tkinter.Label(mw, textvar=I_loadS,bg='#000000',fg='#FFFFFF')
entry_P_loadS=tkinter.Label(mw, textvar=P_loadS,bg='#000000',fg='#FFFFFF')
entry_P_efS=tkinter.Label(mw, textvar=P_efS,bg='#000000',fg='#FFFFFF')


entry_V_kartS=tkinter.Label(mw, textvar=V_kartS,bg='#000000',fg='#FFFFFF')
entry_I_kartS=tkinter.Label(mw, textvar=I_kartS,bg='#000000',fg='#FFFFFF')
entry_P_kartS=tkinter.Label(mw, textvar=P_kartS,bg='#000000',fg='#FFFFFF')


#grids
entry_V_panS.grid(row=3, column=0, pady=5,padx=15,sticky="SW")
entry_I_panS.grid(row=4, column=0, pady=5,padx=15,sticky="SW")
entry_P_panS.grid(row=5, column=0, pady=5,padx=15,sticky="SW")
entry_V_batS.grid(row=7, column=0, pady=5,padx=15,sticky="SW")
entry_I_batS.grid(row=8, column=0, pady=5,padx=15,sticky="SW")
entry_P_batS.grid(row=9, column=0, pady=5,padx=15,sticky="SW")
entry_V_loadS.grid(row=4, column=2, pady=5,padx=30,sticky="Sw")
entry_I_loadS.grid(row=5, column=2, pady=5,padx=30,sticky="w")
entry_P_loadS.grid(row=6, column=2, pady=5,padx=30,sticky="nw",rowspan=1)
entry_P_efS.grid(row=6, column=2, pady=5,padx=15,sticky="s")



lbl_Titulo.grid(row=0, column=2,pady=5,padx=15)
lbl_Titulo2.grid(row=1, column=2,pady=5,padx=15)
#lbl_V_batS.grid(row=6, column=2,pady=5,padx=15,sticky="SW")
#lbl_P_batS.grid(row=7, column=2,pady=5,padx=15,sticky="SW")
#lbl_I_loadS.grid(row=8, column=2,pady=5,padx=15,sticky="SW")


entry_V_kartS.grid(row=4, column=3, pady=5,padx=15,sticky="SE")
entry_I_kartS.grid(row=5, column=3, pady=5,padx=15,sticky="e")
entry_P_kartS.grid(row=6, column=3, pady=5,padx=15,sticky="ne")

#lbl_V_kartS.grid(row=4, column=3,pady=5,padx=15,sticky="SW")
#lbl_I_kartS.grid(row=5, column=3,pady=5,padx=15,sticky="SW")
#lbl_P_kartS.grid(row=6, column=3,pady=5,padx=15,sticky="SW")
#imagenes
img_mppt=tkinter.PhotoImage(file="MPPT.png")
lbl_mppt=tkinter.Label(image=img_mppt)
lbl_mppt.grid(row=1, column=1,padx=30,rowspan=100)

img_bat=tkinter.PhotoImage(file="bateria.png")
lbl_bat=tkinter.Label(image=img_bat)
lbl_bat.grid(row=6, column=0,padx=15)

img_pan=tkinter.PhotoImage(file="panel.png")
lbl_pan=tkinter.Label(image=img_pan)
lbl_pan.grid(row=2, column=0,padx=15)

img_tf=tkinter.PhotoImage(file="transferencia.png")
lbl_tf=tkinter.Label(image=img_tf)
lbl_tf.grid(row=1, column=2,padx=250,rowspan=100)

img_kart=tkinter.PhotoImage(file="kart.png")
lbl_kart=tkinter.Label(image=img_kart)
lbl_kart.grid(row=1, column=4,rowspan=100,padx=15)

# "MAIN"
wdMPPT.addHandler(parseoMPPT)
wdKART.addHandler(parseoKART)
wdMPPT.start()
wdKART.start()
parseoMPPT()
parseoKART()
mw.after(lecturaMPPT, 10)
mw.after(lecturaKART, 10)
mw.after(visualizacion, 500)
mw.mainloop()