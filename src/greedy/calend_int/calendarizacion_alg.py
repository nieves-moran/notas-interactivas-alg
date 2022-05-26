
from cmath import atan
from glob import glob
from sys import ps1
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import random 
import math 
%matplotlib nbagg

#antes de dibujar tienes que ajustar 
out1 = widgets.Output()
display(out1)
#es un diccionario es el ambiente
class Env: 
    vars = dict() 

class Intervalo: 
    rect = None
    p1 = None 
    p2 = None
    intv = None 
    anot = None
class Intervalos: 
    #list(Intervalo)
    elms = None 
    def __init__(self): 
        self.elms = []
class Ejecucion:   
    intervalos = None
    ordenado = False 
    ind = 0 
    linea = None 
    ax_anot = None 
    anot = None 
    res = 0 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
       
  
    def siguiente_paso(self):
        if(self.ind == len(self.intervalos.elms)): 
                text = "El algoritmo termina el resultado es {}\n".format(self.res)
                text += "El numero de intervalos marcados en verde"
                self.anot.set(text = text)
                return
        if (not self.ordenado):
            self.ordena_intervalos()
            self.ordenado = True  
        else: 
            int_act = self.intervalos.elms[self.ind]  
            if(self.linea != None and int_act.intv[0] <= self.linea.get_xdata()): 
                int_act.rect.set(facecolor = '#CC0000')
                text = "El intervalo {} no es compatible con el ultimo intervalo agregado".format(int_act.anot.get_text())
                self.anot.set(text = text)
            else: 
                if(self.linea == None): 
                    self.linea = env.vars['ax'].axvline(int_act.p2[0],linestyle ='--',color= 'black')
                int_act.rect.set(facecolor = '#66FF66')
                self.linea.set(xdata = int_act.p2[0])
                text = "El intervalo {} es compatible se agrega a la solucion.".format(int_act.anot.get_text())
                self.res += 1 
                self.anot.set(text = text)
            self.ind = self.ind + 1

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
    def dibujar_intervalos(self): 
        j = 0
        for i in self.intervalos.elms: 
            r = Rectangle(i.p1,width = i.p2[0] - i.p1[0],height = 1,facecolor = 'white',edgecolor = 'black')
            anot = env.vars['ax'].text(i.p2[0]+1,i.p2[1]-0.5,"$i_{{{}}}$".format(j) ,color='black', weight='bold', fontsize=12, ha='center', va='center')
            env.vars['ax'].add_patch(r)
            i.anot = anot
            i.rect = r 
            j = j + 1
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def ordena_intervalos(self):
        self.intervalos.elms.sort(key = lambda x : x.intv[1]) 
        #redibujarlos 
        y = 0; 
        #va subiendo de dos en dos
        for i in self.intervalos.elms: 
            i.rect.set(xy = (i.p1[0],y))
            i.p1= (i.p1[0],y)
            i.p2 = (i.p2[0],y+1)
            i.anot.set(x = i.p2[0]+0.8)
            i.anot.set(y = i.p2[1]-0.5)
            y = y + 2 
    def crear_estr_intervalos(self,ints): 
        self.intervalos= Intervalos() 
        y = 0 
        for i in ints: 
            intv = Intervalo()
            intv.p1 = (i[0],y)
            intv.p2 = (i[1],y+1)
            intv.intv = [i[0],i[1]]
            y = y + 2 
            self.intervalos.elms.append(intv)
    def crear_intervalos_aleatorios(self):
        intervalos = [] 
        #va a hacer de 1 a 15 
        num_ints = random.randint(5,15) 
        for i in range(0,num_ints): 
            pnt_inicial = random.randint(2,50)
            tam = random.randint(3,10)
            intervalos.append([pnt_inicial,pnt_inicial+tam])
        return intervalos
    def config_imagen(self): 
        env.vars['ax'].set_yticks([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
    def init_anot(self): 
        text= "Haz click en la imagen, cada vez que presiones n se ejecutara \n"
        text += "el siguiente paso del algoritmo.\n"
        text += "Para hacer la imagen mas grande/chica presiona +/-." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_estr_intervalos(self.crear_intervalos_aleatorios())
        self.dibujar_intervalos() 
        self.init_anot() 

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
 