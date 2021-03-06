
from cmath import atan
from glob import glob
from sys import ps1
from matplotlib.patches import Circle, FancyArrow
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as patches 
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
class Arreglo: 
    class Celda: 
        valor = None 
        rect = None 
        anot = None 
        ant = None 
    elms = [] 
    def __init__(self,n): 
        self.elms = [self.Celda() for i in range(0,n)]

class Intervalo: 
    rect = None
    p1 = None 
    p2 = None
    intv = None 
    valor = None
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
    ind = 1  
    arr_dp = None
    flechas = [] 
    coloreados = [] 
    solucion = [] 
    terminar = False 
    flecha = 0 
    #es el dialogo sobre las flechas
    anot_dial = None 
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
        text += "el siguiente paso del algoritmo.\n"
        text += "Presiona +/- para hacer mas grande/chica la imagen." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
       
    def fun_p(self,i): 
        for j in range(i-2,-1,-1): 
            if( self.intervalos.elms[j].intv[1] < self.intervalos.elms[i-1].intv[0]):
                return j + 1 
        return 0 
  
    def poner_flechas(self,s,d): 
        for f in self.flechas: 
            f.set(visible = False)
        sx,sy = self.arr_dp.elms[s].rect.get_xy() 
        dx,dy = self.arr_dp.elms[d].rect.get_xy()
        sx,sy  = sx + 1.5 , sy + 3 
        dx,dy = dx + 1.5 , dy + 3 
        p = FancyArrowPatch((sx,sy),(dx,dy),connectionstyle = "arc3, rad = 0.8",color = 'black') 
        p.set_arrowstyle("fancy", head_length=5,head_width = 5)
        env.vars['ax'].add_patch(p)
        self.flechas = [p]

    def pintar_intervalos(self,i,p):
        #limpiar previos 
        for r in self.coloreados: 
            r.set(facecolor = 'white')
        self.coloreados = [] 
        self.intervalos.elms[i-1].rect.set(facecolor = '#0E6655') 
        self.coloreados.append(self.intervalos.elms[i-1].rect)
        for j in range(0,p): 
            self.intervalos.elms[j].rect.set(facecolor = '#48C9B0')
            self.coloreados.append(self.intervalos.elms[j].rect)
    
    def colorear_solucion(self): 
        for r in self.coloreados: 
            r.set(facecolor = 'white')
        for i in self.solucion: 
            self.intervalos.elms[i-1].rect.set(facecolor = "#5DADE2")
    def obtener_solucion(self):
        i = len(self.arr_dp.elms) - 1  
        while(i != 0): 
            if(self.arr_dp.elms[i].ant != - 1): 
                self.solucion.append(i)
                i = self.arr_dp.elms[i].ant
            else: 
                i = i -1 
        self.solucion.reverse() 
    def siguiente_paso(self):
        if(self.terminar):
            return
        if(self.ind == len(self.arr_dp.elms)):
            self.obtener_solucion() 
            self.colorear_solucion() 
            self.terminar = True
            text = "Termina el algoritmo. La solucion es {}\n".format(self.arr_dp.elms[len(self.arr_dp.elms)-1].valor) 
            text += "La suma de los valores de los intervalos pintados en azul."
            self.anot.set(text = text)
            self.anot_dial.set(visible = False)
            #quitar la flechas
            for f in self.flechas: 
                f.set(visible = False)
            return 
        i = self.ind 
        p = self.fun_p(i)
        #la primera posibilidad 
        if(self.flecha == 0): 
            self.poner_flechas(i,i-1)
            self.flecha = (self.flecha + 1) % 2 
            self.arr_dp.elms[i].valor = self.arr_dp.elms[i-1].valor
            self.arr_dp.elms[i].ant = -1
            self.arr_dp.elms[i].anot.set(text = self.arr_dp.elms[i].valor)
            text = "La primera posibilidad a considerar" 
            text += " es OPT({})={}.".format(i,self.arr_dp.elms[i-1].valor)
            self.anot_dial.set(visible = True)
            self.anot_dial.set(text =  text)
            x,y =  self.arr_dp.elms[i].rect.get_xy() 
            y = y + 4 
            x = x + 4 
            self.anot_dial.set(position = (x,y))
        else: 
            #la segunda posibilidad y ultima, por eso se incrementa el indice 
            self.poner_flechas(i,p)
            self.flecha = (self.flecha + 1) % 2 
            self.pintar_intervalos(i,p) 
            if(self.arr_dp.elms[p].valor +self.intervalos.elms[i-1].valor >= self.arr_dp.elms[i-1].valor): 
                self.arr_dp.elms[i].valor = self.arr_dp.elms[p].valor +self.intervalos.elms[i-1].valor
                self.arr_dp.elms[i].ant = p 
                self.arr_dp.elms[i].anot.set(text = self.arr_dp.elms[i].valor)
                text = "Se considera a OPT({}) + {} = {} + {} = {} y es mejor \n".format(p,self.intervalos.elms[i-1].valor,self.arr_dp.elms[p].valor,self.intervalos.elms[i-1].valor,self.arr_dp.elms[p].valor +self.intervalos.elms[i-1].valor)
                text += "que el valor {} que se tenia ".format(self.arr_dp.elms[i-1].valor)
                self.anot_dial.set(visible = True)
                self.anot_dial.set(text =  text)
                x,y =  self.arr_dp.elms[i].rect.get_xy() 
                y = y + 4 
                x = x + 4 
                self.anot_dial.set(position = (x,y))
            else: 
                text = "Se considera a OPT({}) + {} = {} + {} = {} pero es mejor \n".format(p,self.intervalos.elms[i-1].valor,self.arr_dp.elms[p].valor,self.intervalos.elms[i-1].valor,self.arr_dp.elms[p].valor +self.intervalos.elms[i-1].valor)
                text += "el valor {} que se tiene ".format(self.arr_dp.elms[i-1].valor)
                self.anot_dial.set(visible = True)
                self.anot_dial.set(text =  text)
                x,y =  self.arr_dp.elms[i].rect.get_xy() 
                y = y + 4 
                x = x + 4 
                self.anot_dial.set(position = (x,y))
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
        j = 1
        for i in self.intervalos.elms: 
            r = Rectangle(i.p1,width = i.p2[0] - i.p1[0],height = 2,facecolor = 'white',edgecolor = 'black')
            x,y = i.p1
            w = i.p2[0] - x 
            anot = env.vars['ax'].annotate("", (i.p2[0]+1,i.p2[1]-0.5) ,color='black', weight='bold', fontsize=12, ha='center', va='center')
            env.vars['ax'].text(x+w/2,y+2.5,"$v_{{{}}}={}$".format(j,i.valor))
            env.vars['ax'].add_patch(r)
            i.anot = anot
            i.rect = r 
            j = j + 1
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def ordena_intervalos(self):
        self.intervalos.elms.sort(key = lambda x : x.intv[1]) 
    def crear_estr_intervalos(self,ints): 
        self.intervalos= Intervalos() 
        y = 10
        ints.sort(key = lambda x : x[1])
        for i in ints: 
            intv = Intervalo()
            intv.p1 = (i[0],y)
            intv.p2 = (i[1],y+4)
            intv.intv = [i[0],i[1]]
            intv.valor = i[2]
            y = y + 4 
            self.intervalos.elms.append(intv)
    def crear_intervalos_aleatorios(self):
        intervalos = [] 
        #va a hacer de 1 a 15 
        num_ints = random.randint(5,10) 
        st = 0 
        for i in range(0,num_ints): 
            tam = random.randint(3,20)
            val = random.randint(5,25)
            intervalos.append([st,st+tam,val])
            n = random.randint(3,15)
            st = st + n 
        return intervalos
    def dibujar_arreglo_dp(self): 
        self.arr_dp = Arreglo(len(self.intervalos.elms)+1)
        x,y = 0,-6
        for i in range(0,len(self.arr_dp.elms)):
            r = Rectangle((x,y),width = 3, height = 3,facecolor = 'white',edgecolor = 'black')
            env.vars['ax'].add_patch(r)
            self.arr_dp.elms[i].anot = env.vars['ax'].text(x + 1.5,y  + 1.5 , "",va = 'center',ha = 'center')
            env.vars['ax'].text(x + 1.5,y  - 1.5 , i,va = 'center',ha = 'center')
            self.arr_dp.elms[i].valor = 0
            self.arr_dp.elms[i].rect = r  
            x = x + 3
        self.arr_dp.elms[0].anot.set(text = "0")
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def init_dial(self): 
        props = dict(boxstyle='round', facecolor='#48C9B0', alpha=1 ) 
        self.anot_dial = env.vars['ax'].text(0,0,"",va='top',fontsize = 8,bbox = props,visible = False)
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_estr_intervalos(self.crear_intervalos_aleatorios())
        self.dibujar_intervalos() 
        self.dibujar_arreglo_dp()
        self.init_anot() 
        self.init_dial()

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
 