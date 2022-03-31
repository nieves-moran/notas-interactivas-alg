
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
import math 
%matplotlib nbagg

#antes de dibujar tienes que ajustar 

#es un diccionario es el ambiente
class envn: 
    vars = dict() 

class intervalo: 
    rect = None
    p1 = None 
    p2 = None
    intv = None 
    anot = None
class intervalos: 
    elms = None 
    mm_x = None
    mm_y = None 
    def __init__(self): 
        self.mm_x = (float('inf'),float('-inf'))
        self.mm_y = (float('inf'),float('-inf'))
        self.elms = []

class ingresar_entrada: 
    boton_listo = None
    entrada = None 
    box = None
    texto = None 
    def handler_boton_listo(self,even):  
        clear_output()
        env.vars['intervalos'] = eval(self.entrada.value)
        estado = ejecutar_algoritmo() 
    def __init__(self): 
        self.texto = ""
        self.boton_listo = widgets.Button(description='Listo')
        # displaying button and its output together
        self.boton_listo.on_click(self.handler_boton_listo)
        self.entrada = widgets.Text(description='Intervalos:',disabled=False,value= "",placeholder='',)
        self.box = widgets.VBox([self.entrada,self.boton_listo])
        display(self.box)    
    

class ejecutar_algoritmo: 
    intervalos = None  
    ordenado = None 
    boton = None
    ax = None 
    fig = None
    linea = None
    ind = 0 
    def __init__(self): 
        self.crear_intervalos(env.vars['intervalos'])
        self.config_imagen() 
        self.dibujar_intervalos()
        self.config_botones() 
        
        self.ordenado = False  
    #actualizar maximo y minimo  
    def act_mm(self,mm,x): 
        mx,Mx = mm
        mx = min(mx,x)
        Mx = max(Mx,x)
        return (mx,Mx)
    def crear_intervalos(self,ints): 
        y = 0 
        self.intervalos = intervalos() 
        mm_x  = (float('inf'),float('-inf')) 
        mm_y = (0,0)
        for i in ints: 
            intv = intervalo()
            intv.p1 = (i[0],y)
            intv.p2 = (i[1],y+1)
            intv.intv = [i[0],i[1]]
            y = y + 2 
            self.intervalos.elms.append(intv)
            mm_x = self.act_mm(mm_x,i[0])
            mm_x = self.act_mm(mm_x,i[1])
            mm_y = self.act_mm(mm_y,y)
            mm_y = self.act_mm(mm_y,y+1)
        self.intervalos.mm_x = mm_x 
        self.intervalos.mm_y = mm_y
    def config_botones(self):
        self.boton_sig = widgets.Button(description='sigiuente')
        self.boton_sig.on_click(self.boton_sig_handler)  
        self.box = widgets.VBox([self.boton_sig])
        display(self.box)
    def dibujar_intervalos(self): 
        error = 1 
        xm,xM = self.intervalos.mm_x
        ym,yM = self.intervalos.mm_y
        self.ax.set_xlim(xm-error,xM+error)
        self.ax.set_ylim(ym-error,yM+error)
        j = 0
        for i in self.intervalos.elms: 
            r = Rectangle(i.p1,width = i.p2[0] - i.p1[0],height = 1)
            anot = self.ax.annotate("$i_{}$".format(j), (i.p2[0]+0.5,i.p2[1]-0.5) ,color='black', weight='bold', fontsize=15, ha='center', va='center')
            self.ax.add_patch(r)
            i.anot = anot
            i.rect = r 
            j = j + 1
    def config_imagen(self): 
        self.fig, self.ax = plt.subplots()  
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.axis('off')
      
    def ordena_intervalos(self):
        self.intervalos.elms.sort(key = lambda x : x.intv[1]) 
        #redibujarlos 
        y = 0; 
        #va subiendo de dos en dos
        for i in self.intervalos.elms: 
            i.rect.set(xy = (i.p1[0],y))
            i.p1= (i.p1[0],y)
            i.p2 = (i.p2[0],y+1)
            i.anot.set(x = i.p2[0]+0.5)
            i.anot.set(y = i.p2[1]-0.5)
            y = y + 2 
    def boton_sig_handler(self,event): 
        if(self.ind == len(self.intervalos.elms)): 
            return
        if (not self.ordenado):
            self.ordena_intervalos()
            self.ordenado = True  
        else: 
            int_act = self.intervalos.elms[self.ind]  
            if(self.linea != None and int_act.intv[0] <= self.linea.get_xdata()): 
                int_act.rect.set(color = 'red')
            else: 
                if(self.linea == None): 
                    self.linea = self.ax.axvline(int_act.p2[0])
                int_act.rect.set(color = 'green')
                self.linea.set(xdata = int_act.p2[0])
            self.ind = self.ind + 1

env = envn()
estado = ingresar_entrada() 