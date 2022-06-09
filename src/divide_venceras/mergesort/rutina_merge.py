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
    arr1 = None 
    arr2 = None  
    arr3 = None
    ind_i = None 
    ind_j = None 
    ind_k = None
    anots = dict()
    anot =None 
    ax_anot = None 
    def poner_anotaciones(self): 
        ax = env.vars['ax']
        self.anots['anot_a1'] = ax.text(15,5,"$A_1$",ha = 'center',va = 'center',fontsize = 11)
        self.anots['anot_a2'] = ax.text(55,5,"$A_2$",ha = 'center',va = 'center',fontsize = 11)        
        self.anots['anot_a3'] = ax.text(35,15,"$A_3$",ha = 'center',va = 'center',fontsize = 11)           
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
        text += "el siguiente paso de la rutina de combinacion." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def siguiente_paso(self):
        i,j,k = self.ind_i.valor,self.ind_j.valor,self.ind_k.valor
        if(k == len(self.arr3.elms)): 
            text= "La rutina termina. El arreglo $A_3$ esta ordenado.\n"
            self.anot.set(text = text)
            return 
        n, m = len(self.arr1.elms),len(self.arr2.elms)
        text = ""
        if(i == n): 
            text += "El indice i es igual a {}, ".format(n)
            text += "$A_3[{}] = A_2[{}]$\n".format(k,j)
            text += "Se avanza el indice j y el indice k."
            self.arr3.elms[k].valor = self.arr2.elms[j].valor
            self.arr3.elms[k].anot.set(text = self.arr3.elms[k].valor)
            self.ind_j.anot.set(x = self.ind_j.anot.get_position()[0] + 3)
            j = j + 1 
        elif(j == m): 
            text += "El indice j es igual a {}, ".format(m)
            text += "$A_3[{}] = A_1[{}]$\n".format(k,j)
            text += "Se avanza el indice i y el indice k."
            self.arr3.elms[k].valor = self.arr1.elms[i].valor
            self.arr3.elms[k].anot.set(text = self.arr3.elms[k].valor)
            self.ind_i.anot.set(x = self.ind_i.anot.get_position()[0] + 3)
            i = i + 1       
        elif(self.arr1.elms[i].valor < self.arr2.elms[j].valor): 
            text += "Ya que $A_1[{}] < A_2[{}]$, ".format(i,j)
            text += "$A_3[{}] = A_1[{}]$\n".format(k,i)
            text += "Se avanza el indice i y el indice k."
            self.arr3.elms[k].valor = self.arr1.elms[i].valor
            self.arr3.elms[k].anot.set(text = self.arr3.elms[k].valor)
            self.ind_i.anot.set(x = self.ind_i.anot.get_position()[0] + 3)
            i = i + 1 
        else: 
            text += "Ya que $ A_2[{}] \leq A_1[{}]$, ".format(j,i)
            text += "$A_3[{}] = A_2[{}]$\n".format(k,j)
            text += "Se avanza el indice j y el indice k."
            self.arr3.elms[k].valor = self.arr2.elms[j].valor
            self.arr3.elms[k].anot.set(text = self.arr3.elms[k].valor)
            self.ind_j.anot.set(x = self.ind_j.anot.get_position()[0] + 3)
            j = j + 1 
        self.ind_k.anot.set(x = self.ind_k.anot.get_position()[0] + 3)
        k = k + 1
        self.ind_i.valor = i 
        self.ind_j.valor = j 
        self.ind_k.valor = k
        self.anot.set(text = text)        
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
    def dibujar_arreglos_iniciales(self): 
        a1 = [random.randint(-20,20) for i in range(0,10)]
        a2 = [random.randint(-20,20) for i in range(0,10)]
        a1.sort()
        a2.sort() 
        a3 = [0 for i in range(0,20)]
        self.arr1 = dibujar_arreglo(a1,0,0,True)
        self.ind_i = self.dibujar_indice(1.5,-2.5,"i") 
        self.arr2 = dibujar_arreglo(a2,40,0,True)
        self.ind_j = self.dibujar_indice(41.5,-2.5,"j")
        self.arr3 = dibujar_arreglo(a3,5,10,False)
        self.ind_k = self.dibujar_indice(6.5,7.5,"k") 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale()
    def __init__(self): 
        self.config_imagen()
        self.init_anot() 
        self.config_teclas()
        self.dibujar_arreglos_iniciales()
        self.poner_anotaciones() 

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
