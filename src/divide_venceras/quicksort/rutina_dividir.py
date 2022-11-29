from cmath import atan
from glob import glob
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import random 

import math

from numpy import array
%matplotlib nbagg
out1 = widgets.Output()
display(out1)
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
#punto medio entre dos puntos pero con una separación de s, una fraccion de la linae(frac)
def punto_medio(x1,y1,x2,y2,s,fra): 
    dx = x1 - x2 
    dy = y1 - y2 
    ang = (math.pi/2 if dy > 0 else (3*math.pi)/2) if dx == 0 else math.atan(dy/dx)
    ang = ang + 2* math.pi if ang < 0 else ang
    x = math.sqrt((x1- x2)**2 + (y1 - y2)**2)*fra
    y = s 
    xp = x*math.cos(ang) - y*math.sin(ang)
    yp = x*math.sin(ang) + y*math.cos(ang)
    ##llegué a la conclusión que tienes que trasladarlo a el que tiene la menor x 
    xp = xp + (x1 if x1 < x2 else x2) 
    yp = yp + (y1 if x1 < x2 else y2 )
    return (xp,yp)
class Arreglo: 
    elms = [] 
    def __init__(self,n): 
        self.elms = [Celda() for i in range(0,n)]

class Celda: 
    rect = None 
    valor = None 
    anot = None 

def dibujar_arreglo(arreglo,x,y,etiq_b): 
    ax = env.vars['ax']
    arr = Arreglo(len(arreglo))
    for i in range(0,len(arreglo)): 
        arr.elms[i].rect = Rectangle((x,y),width = 3 , height = 3,facecolor = 'white',edgecolor = 'black') 
        ax.add_patch(arr.elms[i].rect) 
        arr.elms[i].valor = arreglo[i]
        etiq = "{}".format(arreglo[i])
        if(not etiq_b): 
            etiq = ""
        arr.elms[i].anot = ax.text(x+1.5,y+1.5,etiq,ha = 'center',va = 'center',fontsize = 9) 
        ax.text(x+1.5,y-1,i,ha = 'center',va = 'center',fontsize = 9)
        x = x + 3 
    return arr
class Ind: 
    letra = None
    anot = None 
    valor = 0 
    def __init__(self,l): 
        self.letra = l
class Env:
    vars = dict()  

class Ejecucion: 
    arr = None 
    anot =None 
    ax_anot = None 
    ind_i_anot = None 
    ind_j_anot = None 
    ind_r_anot = None 
    terminar = False
    def poner_indices(self): 
        ax = env.vars['ax']
        self.ind_i = -1 
        self.ind_i_anot = ax.text(-1.5,6,"i")
        self.ind_j = 0 
        self.ind_j_anot = ax.text(1.5,4,"j")
        self.ind_r = len(self.arr.elms) - 1   
        self.ind_r_anot = ax.text(len(self.arr.elms)*3 - 1.5,5, "r")  
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
    def init_anot(self): 
        text= "Haz click en la imagen, cada vez que presiones n se ejecutara \n"
        text += "el siguiente paso de la rutina de division." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def swap(self,i,j): 
        a = self.arr.elms
        temp = a[i].valor 
        a[i].valor = a[j].valor 
        a[j].valor = temp
        a[i].anot.set(text = a[i].valor)
        a[j].anot.set(text = a[j].valor) 
    def colorear_subarr(self):
        a = self.arr.elms 
        for i in range(0,self.ind_i+1): 
            a[i].rect.set(facecolor = '#99ccff')
        for i in range(self.ind_i+2,len(self.arr.elms)): 
            a[i].rect.set(facecolor = '#9999ff')
        a[self.ind_i+1].rect.set(facecolor = '#0080ff')
    def siguiente_paso(self):
        if(self.terminar): 
            text = "Los numeros en el arreglo que son menores o iguales que el pivote {}\n".format(self.arr.elms[self.ind_i+1].valor)
            text += "estan coloreados en azul claro, el pivote en azul marino \n"
            text += "y los numeros mayores en morado"
            self.anot.set(text = text)
            self.colorear_subarr() 
            return 
        a = self.arr.elms
        r = self.ind_r
        j = self.ind_j 
        i = self.ind_i 
        if(j == r):   
            self.swap(i+1,r)
            x,y = self.ind_i_anot.get_position() 
            self.ind_r_anot.set(position = (x + 3 ,5 ))
            self.terminar = True
            text = "El indice j ha llegado al indice r\n"
            text += "Se intercambia el A[{}] con A[{}]".format(i+1,r)
            self.anot.set(text = text)
            return 
        if( a[j].valor <= a[r].valor): 
            i += 1
            x,y = self.ind_i_anot.get_position()
            self.ind_i_anot.set(position = (x+3, y))   
            self.swap(i,j)
            text = "El valor en el indice j es menor o igual que el valor en el indice r (pivote).\n"
            text += "Se intercambia A[{}] con A[{}]".format(i,j)
            self.anot.set(text = text)
        else: 
            text = "El valor en el indice j es mayor que el valor en el indice r\n"
            text += "Simplemente avanza j"
            self.anot.set(text = text)
        j += 1 
        self.ind_i = i 
        self.ind_j = j 
        self.ind_r = r 
        #avanzar a j 
        x,y = self.ind_j_anot.get_position()
        self.ind_j_anot.set(position = (x+3, y ))  
    @out1.capture()
    def teclas_handler(self,event): 
        if(event.key == 'n'): 
            self.siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    def zoom_mas(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x-1,y-1)
    def config_teclas(self): 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.teclas_handler)
    def dibujar_indice(self,x,y,l): 
        ind = Ind(l)
        ind.anot = env.vars['ax'].text(x,y,l,va = 'center',ha ='center',fontsize = 9)
        return ind
    def dibujar_arreglo_inicial(self):
        a = [9,8,5,6,7,1,2,3,4]
        self.arr = dibujar_arreglo(a,0,0,True)
        env.vars['ax'].relim()
        env.vars['ax'].autoscale()
    def __init__(self): 
        self.config_imagen()
        self.init_anot() 
        self.config_teclas()
        self.dibujar_arreglo_inicial()
        self.poner_indices() 

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
