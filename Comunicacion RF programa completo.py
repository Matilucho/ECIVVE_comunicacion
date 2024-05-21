import tkinter
import string
from tkinter import messagebox
from tkinter import PhotoImage
import serial
from datetime import datetime

mw=tkinter.Tk()
mw.title("Interfaz gráfica")
#mw.geometry("400x300")

txt=open("MPPT.log",mode="r")
txtKART=open("MPPT_20240515.log",mode="r")

'''
PORT = 'COM6'

# abre port serie indicado
ser = serial.Serial(PORT, timeout=0.2)

# configura port
ser.baudrate = 9600
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
'''
#global RecibidoMPPT
RecibidoMPPT=""
RecibidoKART=""
tiempoMPPT=datetime.now()
tiempoKART=datetime.now()

V_pan="0"
I_pan="0"
P_pan="0"
V_bat="0"
I_bat="0"
P_bat="0"
V_load="0"
I_load="0"
P_load="0"

V_kart=""
I_kart=""
P_kart=""

def lecturaMPPT():
    global RecibidoMPPT
    m=txt.read(1)
    
    
    
    '''
    m = ser.read(1) #Leo hasta 70 caracteres de lo que recibo
    if m !=b'':
        Recibido=m.decode()
    '''
    
    
    if m!=b'':
        RecibidoMPPT=RecibidoMPPT+m
        if m=='\n':
            #print("renglon")
            #print(RecibidoMPPT)
            parseoMPPT(RecibidoMPPT)
            RecibidoMPPT=""

    mw.after(2, lecturaMPPT)
mw.after(2, lecturaMPPT)


def lecturaKART():
    global RecibidoKART
    m=txtKART.read(1)
    
 
    
    '''
    m = ser.read(1) #Leo hasta 70 caracteres de lo que recibo
    if m !=b'':
        Recibido=m.decode()
    
    '''
    
    if m!=b'':
        RecibidoKART=RecibidoKART+m
        if m=='\n':
            print("renglonkart")
            print(RecibidoKART)
            parseoKART(RecibidoKART)
            RecibidoKART=""

    mw.after(3, lecturaKART)
mw.after(3, lecturaKART)




def parseoMPPT(RecibidoMPPT):
    global V_pan
    global I_pan
    global P_pan
    global V_bat
    global P_bat
    global I_load
    #global RecibidoMPPT
    global tiempoMPPT
    #print(tiempoMPPT)
    m=datetime.now()
    dif=m-tiempoMPPT
    #print(dif)
    if dif.total_seconds()<1.5:
        tiempoMPPT=m
        #print("Todo correcto\n")
    else:
        print("TIMEOUT")
        V_pan="?"
        I_pan="?"
        P_pan="?"
        V_bat="?"   
        P_bat="?"
        I_load="?"
        return 0
        
  
    
    

    RecibidoMPPT=RecibidoMPPT.replace("","")  
    #Hago la verificación de lo recibido
    calcverif=RecibidoMPPT[1:-4] #Sin contar el signo pesos y la verificación recibida
    suma=0
    
    for n in calcverif:
        suma=suma^ord(n)
    verif=RecibidoMPPT[-4:-2]
    suma=str(hex(suma)) #lo pasamos a string para poder sacar el 0x del formato hexa
    suma=suma[2:4]
    
   #Si la verificación es correcta
    #if(suma==verif):
    if(1):
        #print(RecibidoMPPT)
        #Formato RecibidoMPPT $T:ttt.tt;H:hhh.hh;P:ppp.pp;G:ggg.gg;D:ddd.dd;O:ooo.oo&
        
        #V_pan=RecibidoMPPT[37:42]
        #I_pan=RecibidoMPPT[45:46]    
        #V_bat=RecibidoMPPT[51:52]    
        #P_bat=RecibidoMPPT[57:58]
        #I_load=RecibidoMPPT[103:104]
        
        
        
        
       
        
   #########################################################################################################
        #####   VER CUALES SON LOS BORDES, LOS TAB Y LOS /N   ###############################
        guardado=0
        i=0
        while i <len(RecibidoMPPT)-1:           
            if(RecibidoMPPT[i-1]=='\n' and RecibidoMPPT[i]=='V' and RecibidoMPPT[i+1]=='\t' and guardado==0):
                i=i+2                             #### esto es para poder arrancar a escribir luego de los tabs
                guardado=1
                V_pan=""
            if(RecibidoMPPT[i]=='I' and RecibidoMPPT[i+1]=='	'and guardado==0):
                i=i+2
                guardado=2
                I_pan=""
            if(RecibidoMPPT[i]=='V' and RecibidoMPPT[i+1]=='P' and RecibidoMPPT[i+2]=='V' and RecibidoMPPT[i+3]=='	'and guardado==0):
                i=i+4
                guardado=3
                V_bat=""
            if(RecibidoMPPT[i]=='P'and RecibidoMPPT[i+1]=='P' and RecibidoMPPT[i+2]=='V' and RecibidoMPPT[i+3]=='	'and guardado==0):
                i=i+4
                guardado=4
                P_bat=""
            if(RecibidoMPPT[i]=='I'and RecibidoMPPT[i+1]=='L' and RecibidoMPPT[i+2]=='	'and guardado==0):
                i=i+3
                guardado=5
                I_load=""
            
            
            if guardado==1:
                V_pan=V_pan+RecibidoMPPT[i]
                if RecibidoMPPT[i+1]=='\n':
                    guardado=0
                    V_pan=str(float(V_pan)/1000)
                    
            if guardado==2:
                I_pan=I_pan+RecibidoMPPT[i]
                if RecibidoMPPT[i+1]=='\n':
                    guardado=0
                    I_pan=str(float(I_pan)/1000)
                    
            if guardado==3:
                V_bat=V_bat+RecibidoMPPT[i]
                if RecibidoMPPT[i+1]=='\n':
                    guardado=0
                    
            if guardado==4:
                P_bat=P_bat+RecibidoMPPT[i]
                if RecibidoMPPT[i+1]=='\n':
                    guardado=0
                    
            if guardado==5:
                I_load=I_load+RecibidoMPPT[i]
                if RecibidoMPPT[i+1]=='\n':
                    guardado=0
                    I_load=str(float(I_load)/1000)
                    
            i=i+1    
        #I_pan=I_pan.replace("\n","")
        #I_pan=str(float(I_pan)/1000)
        #print(I_pan*3)
        #P_pan=str(I_panF*V_panF)
        #print(float(I_pan)*3)
        #I_pan=str(float(I_pan)/1000)
        #P_pan=str(float(I_pan)*float(V_pan))
        
                
    #mw.after(100, lectura) #Que la funcion se ejecute cada 100 ms
    
#mw.after(100, lectura)


def parseoKART(RecibidoKART):
    
    global V_kart
    global I_kart
    global P_kart
    #global P_bat
    #global I_load
    #global RecibidoMPPT
    global tiempoKART
    #print(tiempoKART)
    m=datetime.now()
    dif=m-tiempoKART
    #print(dif)
    if dif.total_seconds()<1.5:
        tiempoKART=m
        #print("Todo correcto\n")
    else:
        #print("TIMEOUT")
        V_kart="?"
        I_kart="?"   
        V_kart="?"   
        #P_bat="?"
        #I_load="?"
        return 0
        
  
    
    

    RecibidoKART=RecibidoKART.replace("","")  
    #Hago la verificación de lo recibido
    calcverif=RecibidoKART[1:-4] #Sin contar el signo pesos y la verificación recibida
    suma=0
    
    for n in calcverif:
        suma=suma^ord(n)
    verif=RecibidoKART[-4:-2]
    suma=str(hex(suma)) #lo pasamos a string para poder sacar el 0x del formato hexa
    suma=suma[2:4]
    
   #Si la verificación es correcta
    #if(suma==verif):
    if(1):
        #print(RecibidoKART)
        #Formato RecibidoKART $T:ttt.tt;H:hhh.hh;P:ppp.pp;G:ggg.gg;D:ddd.dd;O:ooo.oo&
        
        #V_pan=RecibidoKART[37:42]
        #I_pan=RecibidoKART[45:46]    
        #V_bat=RecibidoKART[51:52]    
        #P_bat=RecibidoKART[57:58]
        #I_load=RecibidoKART[103:104]
        
        
        
        
        
        
   #########################################################################################################
        #####   VER CUALES SON LOS BORDES, LOS TAB Y LOS /N   ###############################
        guardado=0
        ikart=0
        while ikart <len(RecibidoKART)-1:           
            if(RecibidoKART[ikart-1]=='\n' and RecibidoKART[ikart]=='V' and RecibidoKART[ikart+1]=='\t' and guardado==0):
                ikart=ikart+2                             #### esto es para poder arrancar a escribir luego de los tabs
                guardado=1
                print("Leo tension kart")
                V_kart=""
            if(RecibidoKART[ikart]=='I' and RecibidoKART[ikart+1]=='	'and guardado==0):
                ikart=ikart+2
                guardado=2
                I_kart=""
            if(RecibidoKART[ikart]=='P'and RecibidoKART[ikart+1]=='P' and RecibidoKART[ikart+2]=='V' and RecibidoKART[ikart+3]=='	'and guardado==0):
                ikart=ikart+4
                guardado=4
                P_kart=""
            
            
            if guardado==1:
                V_kart=V_kart+RecibidoKART[ikart]
                if RecibidoKART[ikart+1]=='\n':
                    guardado=0
                    print(V_kart)
                    V_kart=str(float(V_kart)/1000)
                    
                    
            if guardado==2:
                I_kart=I_kart+RecibidoKART[ikart]
                if RecibidoKART[ikart+1]=='\n':
                    guardado=0
                    #I_kart=str(float(I_kart)/1000)
                    
            if guardado==4:
                P_kart=P_kart+RecibidoKART[ikart]
                if RecibidoKART[ikart+1]=='\n':
                    guardado=0

                    
            ikart=ikart+1    

       
  




def visualizacion():
    global V_pan
    global I_pan

    global V_bat
    global P_bat
    
    
    global I_load
    
    global V_kart
    global I_kart
    global P_kart
    print("muestro")
    
    #P_bat="150"
    P_pan=str(f'{float(V_pan)*float(I_pan):.3f}')
    if float(V_bat) !=0:
        I_bat=str(float(P_bat)/float(V_bat))
    else:
        I_bat="0"
    P_load=str(float(I_load)*float(V_bat))
    print(V_kart)
    #V_kart="AAA"
    #I_kart="AAA"
    #P_kart="AAA"
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
    mw.after(1000, visualizacion)

mw.after(1000, visualizacion) #muestra los valores en pantalla cada 1 segundo

mw['bg'] = '#000000'

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

entry_V_kartS=tkinter.Label(mw, textvar=V_kartS,bg='#000000',fg='#FFFFFF')
entry_I_kartS=tkinter.Label(mw, textvar=I_kartS,bg='#000000',fg='#FFFFFF')
entry_P_kartS=tkinter.Label(mw, textvar=P_kartS,bg='#000000',fg='#FFFFFF')


#grids
entry_V_panS.grid(row=2, column=0, pady=5,padx=15,sticky="SW")
entry_I_panS.grid(row=3, column=0, pady=5,padx=15,sticky="SW")
entry_P_panS.grid(row=4, column=0, pady=5,padx=15,sticky="SW")
entry_V_batS.grid(row=7, column=0, pady=5,padx=15,sticky="SW")
entry_I_batS.grid(row=8, column=0, pady=5,padx=15,sticky="SW")
entry_P_batS.grid(row=9, column=0, pady=5,padx=15,sticky="SW")
entry_V_loadS.grid(row=2, column=2, pady=5,padx=30,sticky="Sw")
entry_I_loadS.grid(row=3, column=2, pady=5,padx=30,sticky="w")
entry_P_loadS.grid(row=4, column=2, pady=5,padx=30,sticky="w",rowspan=1)


lbl_Titulo.grid(row=0, column=2,pady=5,padx=15)
lbl_Titulo2.grid(row=1, column=2,pady=5,padx=15)
lbl_V_batS.grid(row=6, column=2,pady=5,padx=15,sticky="SW")
lbl_P_batS.grid(row=7, column=2,pady=5,padx=15,sticky="SW")
lbl_I_loadS.grid(row=8, column=2,pady=5,padx=15,sticky="SW")


entry_V_kartS.grid(row=4, column=4, pady=5,padx=15,sticky="SW")
entry_I_kartS.grid(row=5, column=4, pady=5,padx=15,sticky="SW")
entry_P_kartS.grid(row=6, column=4, pady=5,padx=15,sticky="SW")

lbl_V_kartS.grid(row=4, column=3,pady=5,padx=15,sticky="SW")
lbl_I_kartS.grid(row=5, column=3,pady=5,padx=15,sticky="SW")
lbl_P_kartS.grid(row=6, column=3,pady=5,padx=15,sticky="SW")
#imagenes
img_mppt=tkinter.PhotoImage(file="MPPT.png")
lbl_mppt=tkinter.Label(image=img_mppt)
lbl_mppt.grid(row=1, column=1,padx=30,rowspan=100)

img_bat=tkinter.PhotoImage(file="bateria.png")
lbl_bat=tkinter.Label(image=img_bat)
lbl_bat.grid(row=6, column=0)

img_pan=tkinter.PhotoImage(file="panel.png")
lbl_pan=tkinter.Label(image=img_pan)
lbl_pan.grid(row=2, column=0)

img_pc=tkinter.PhotoImage(file="transferencia.png")
lbl_pc=tkinter.Label(image=img_pc)
lbl_pc.grid(row=2, column=2,padx=250)

img_kart=tkinter.PhotoImage(file="kart.png")
lbl_kart=tkinter.Label(image=img_kart)
lbl_kart.grid(row=2, column=3)

mw.mainloop()