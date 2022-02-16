##Minizinc
from logging import exception, root
from minizinc import Instance, Model, Solver, model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame,Tk,Button,Label,Entry,Text,END,StringVar,Checkbutton,IntVar
from tkinter import ttk

import os
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')

data = []
ciudadX = []
ciudadY = []
ciudades = []
m = 0
responseX = 0
responseY = 0





#=========================================FUNCIONES================================================================


def executeProgram():

    
    salida = "["
    for i in ciudades:
        
        salida =  salida + "|" + str(i[0]) + "," + str(i[1])

    salida = salida + "|]"

    n ="n = " + nText.get()+ ";\n"
    m ="m = " +  str(len(ciudades))+ ";\n"
    c = "ciudades = " + salida + ";\n"

    data = [n,m,c];

    #print(data)

    if os.path.exists("Datos.dzn"):
        #print("LISTA",data)
        os.remove("Datos.dzn")
        #print("File exists, deleted")
    else:
        #print("The file does not exist")
        f = open("Datos.dzn", "w")
        #print("File created")

    
    f = open("Datos.dzn", "w")
    f.writelines(data)
    f.close()
    file1 = open('Datos.dzn', 'r')
    #print(file1.read())

    conectMinizinc()


def addCiudad():
    varCiudad = [int(xText.get()),int(yText.get())]
    ciudades.append(varCiudad)
    
    ciudadX.append(int(xText.get()))
    ciudadY.append(int(yText.get()))
    m = ciudadX.__len__();
    my_var.set(ciudadX.__len__())
    #print(ciudades)
    plot(-1,-1)
    xText.delete(0,END)
    yText.delete(0,END)

def cutCiudad():
    ciudadX.pop()
    ciudadY.pop()
    ciudades.pop()
    my_var.set(ciudadX.__len__())
    #print(ciudades)
    plot(-1,-1)



#=============================================INTERFAZ GRAFICA=============================================

ventana = Tk()
ventana.geometry("600x700")
ventana.wm_title("Complejidad y optimización")
ventana.minsize(width=450, height=500)
ventana.maxsize(width=450, height=500)




frame = Frame(ventana, bg='blue')
frame.grid(row=2, column=2)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(1, weight=1)

gecode = IntVar()
coinbc = IntVar()
c1 = Checkbutton(ventana, text='Gecode',variable=gecode, onvalue=1, offvalue=0)
c1.grid(row=1, column=1)
c1.grid_rowconfigure(1, weight=1)
c1.grid_columnconfigure(1, weight=1)

c2 = Checkbutton(ventana, text='Coin-bc',variable=gecode, onvalue=0, offvalue=1)
c2.grid(row=1, column=3)
c2.grid_rowconfigure(1, weight=1)
c2.grid_columnconfigure(1, weight=1)



etiquetaC = Label(ventana, text="Cantidad de ciudades : ")
etiquetaC.grid(row=3, column=1)
etiquetaC.grid_rowconfigure(1, weight=1)
etiquetaC.grid_columnconfigure(1, weight=1)

my_var = StringVar()
my_var.set("0")


etiquetaCC = Label(ventana, textvariable=my_var)
etiquetaCC.grid(row=3, column=2)
etiquetaCC.grid_rowconfigure(1, weight=1)
etiquetaCC.grid_columnconfigure(1, weight=1)

etiquetaN = Label(ventana, text="Digite el valor de N")
etiquetaN.grid(row=4, column=1)
etiquetaN.grid_rowconfigure(1, weight=1)
etiquetaN.grid_columnconfigure(1, weight=1)

nText = Entry(ventana, font= "Arial 10")
nText.grid(row=4, column=2)
nText.grid_rowconfigure(1, weight=1)
nText.grid_columnconfigure(1, weight=1)



etiqueta = Label(ventana, text="Ingrese las ciudades")
etiqueta.grid(row=5, column=2)
etiqueta.grid_rowconfigure(1, weight=1)
etiqueta.grid_columnconfigure(1, weight=1)

etiquetaX = Label(ventana, text="Posicion X: ")
etiquetaX.grid(row=6, column=1)
etiquetaX.grid_rowconfigure(1, weight=1)
etiquetaX.grid_columnconfigure(1, weight=1)

xText = Entry(ventana, font= "Arial 10")
xText.grid(row=6, column=2)
xText.grid_rowconfigure(1, weight=1)
xText.grid_columnconfigure(1, weight=1)

etiquetaY = Label(ventana, text="Posicion Y: ")
etiquetaY.grid(row=7, column=1)
etiquetaY.grid_rowconfigure(1, weight=1)
etiquetaY.grid_columnconfigure(1, weight=1)

yText = Entry(ventana, font= "Arial 10")
yText.grid(row=7, column=2)
yText.grid_rowconfigure(1, weight=1)
yText.grid_columnconfigure(1, weight=1)



boton = Button(ventana, text="Agregar ciudad", command= addCiudad)
boton.grid(row=8, column=1)
boton.grid_rowconfigure(1, weight=1)
boton.grid_columnconfigure(1, weight=1)

boton2 = Button(ventana, text="Quitar ciudad", command= cutCiudad)
boton2.grid(row=8, column=2)
boton2.grid_rowconfigure(1, weight=1)
boton2.grid_columnconfigure(1, weight=1)

boton2 = Button(ventana, text="Ejecutar programa", command= executeProgram)
boton2.grid(row=8, column=3)
boton2.grid_rowconfigure(1, weight=1)
boton2.grid_columnconfigure(1, weight=1)




etiquetaC = Label(ventana, text="Respuesta : ")
etiquetaC.grid(row=9, column=2)
etiquetaC.grid_rowconfigure(1, weight=1)
etiquetaC.grid_columnconfigure(1, weight=1)

my_response = StringVar()
my_response.set("")


etiquetaCC = Label(ventana, textvariable=my_response)
etiquetaCC.grid(row=10, column=2)
etiquetaCC.grid_rowconfigure(1, weight=1)
etiquetaCC.grid_columnconfigure(1, weight=1)


#=====================================================================





#=====================================================================


# plot
fig, ax = plt.subplots()

ax.set(xlim=(0, 8), xticks=np.arange(0,11),
        ylim=(0, 8), yticks=np.arange(0,11))

canvas =  FigureCanvasTkAgg(fig, master = frame)
canvas.draw()
canvas.get_tk_widget().grid(column=0,row=0,rowspan=3)


#=============================================PLOT PUNTOS=============================================
def plot(bX,bY):
    
    # make the data
    np.random.seed(3)
    x = ciudadX
    y = ciudadY
    tamano = int(nText.get())
    n = np.arange(0,tamano)
    # size and color:
    colors = np.random.randint(0, len(x), len(x))

    # plot
    fig, ax = plt.subplots()


    ax.scatter(x, y,c = "green", vmin=0, vmax=100)

    if(float(bX)>=0 and float(bY)>=0):
        ax.scatter(float(bX), float(bY),c = "red", vmin=0, vmax=100)
    

    

    ax.set(xlim=(0, 8), xticks=n+1,
        ylim=(0, 8), yticks=n+1)

    canvas =  FigureCanvasTkAgg(fig, master = frame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0,row=0,rowspan=3)

#===============================================================================================
def conectMinizinc(): 
    
    #print("GECODE ", gecode.get())
    if(gecode.get()):
        #print("EJECUTANDO CON GECODE")
        my_response.set("")
        project = Model("modelo_proyecto_int_gecode.mzn")
        solver = Solver.lookup("gecode")
    else:
        #print("EJECUTANDO CON COINBC")
        project = Model("modelo_proyecto_float_coinbc.mzn")
        solver = Solver.lookup("coin-bc")

    # Load  model from file
    
    #project = Model("modelo_proyecto_int_gecode.mzn")
    # Find the MiniZinc solver configuration 
    ##Para hacerlo con Gecode, cambiar chuffed por gecode
    
    # Create an Instance of the project model for solver
    instance = Instance(solver, project)
    # Assign the values from a dzn
    instance.add_file("Datos.dzn")
    result = instance.solve()
    # Output
    ##print([result["docks"],result["arrivalTime"],result["unloadStartTime"]])
    response = str([result.solution][0])
    responseArray = response.splitlines()
    responseX = responseArray[0].strip().split("=",1)[1].replace('"','')
    responseY = responseArray[1].strip().split("=",1)[1].replace('"','')

    #print(responseX,responseY)
    plot(responseX, responseY)
    my_response.set(response.replace('"',''))
    return ([result])





ventana.mainloop()



