from cmath import atan
from glob import glob
from pydoc import visiblename
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import random 

import math

from numpy import arange 
%matplotlib nbagg
out1 = widgets.Output()
display(out1) 
""" class Entrada: 
    botones 
        dos botones 
        consulta 
        dibujar arbol 
    init(): 
        config_botones() 
        config_imagen() """ 
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
class env2: 
    vars = None
    def __init__(self): 
        self.vars = dict()

def dibujar_arbol(arr): 
    env2.vars['seg_t'] = Segment_tree(arr)
    n = len(arr)
    x = 0 
    y = 0 
    for i in range(2*n- 1,n-1,-1): 
        cl = Celda() 
        env2.vars['seg_t'].arreglo.celdas[i] = cl
        cl.padre = i//2 
        cl.valor = env2.vars['seg_t'].tree[i]
        cr = Circle((x,y),radius = env2.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        cl.anot = env2.vars['ax'].text(x, y, '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        env2.vars['ax'].add_patch(cr)
        cl.circ = cr
        r = Rectangle((x-env2.vars['rad'],y-3*env2.vars['rad']),width = 2*env2.vars['rad'],height = 2*env2.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        env2.vars['ax'].add_patch(r)
        cl.rect_anot = env2.vars['ax'].text(x, y-2*env2.vars['rad'], '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        env2.vars['ax'].text(x,y-4,i - n,fontsize = 9,va = 'center',ha = 'center')
        x = x - 2*env2.vars['rad']
        cl.rect = r 
        #poner el indice 
    for i in range(n-1,0,-1): 
        cl = Celda() 
        env2.vars['seg_t'].arreglo.celdas[i] = cl
        cl.padre = i//2 
        cl.valor = env2.vars['seg_t'].tree[i]
        cl.hijos = [2*i,2*i + 1]
        cels = env2.vars['seg_t'].arreglo.celdas
        x = (cels[2*i].circ.get_center()[0] + cels[2*i+1].circ.get_center()[0]) / 2
        y =  env2.vars['seg_t'].arreglo.celdas[2*i].circ.get_center()[1] + 3*env2.vars['rad']
        cr = Circle((x,y),radius = env2.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        cl.anot = env2.vars['ax'].text(x, y, '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        env2.vars['ax'].add_patch(cr)
        lx,ly = cels[2*i].circ.get_center() 
        rx,ry = cels[2*i+1].circ.get_center() 
        linea = PathPatch(Path([inter_points(env2.vars['rad'],x,y,lx,ly),inter_points(env2.vars['rad'],lx,ly,x,y)]), facecolor='none', edgecolor='black')
        env2.vars['ax'].add_patch(linea)
        cels[2*i].ar_p = linea 
        linea = PathPatch(Path([inter_points(env2.vars['rad'],x,y,rx,ry),inter_points(env2.vars['rad'],rx,ry,x,y)]), facecolor='none', edgecolor='black')
        env2.vars['ax'].add_patch(linea)
        cels[2*i+1].ar_p = linea 
        cl.circ = cr
    #dibujar aristas
     
    env2.vars['ax'].relim()
    env2.vars['ax'].autoscale_view()
class Segment_tree: 
    arreglo = None 
    tree = None
    def __init__(self,arr): 
        self.tree = [0 for i in range(0,2*len(arr))]
        self.arreglo = Arreglo()
        self.arreglo.celdas = [Celda() for i in range(0,2*len(arr))] 
        n = len(arr)
        for i in range(0,n): 
            self.tree[i + n] = arr[i]
        for i in range(n-1,0,-1): 
            self.tree[i] = min(self.tree[2*i],self.tree[2*i+1])  

class Arreglo: 
    celdas = None 
    def __init__(self): 
        self.celdas = [] 
class Celda: 
    padre = None 
    #linea hacia el padre
    ar_p = None 
    valor = None 
    anot = None 
    circ = None 
    hijos = None 
    #en caso de que sea hoja 
    rect = None  
    #anotacion en el rectangulo 
    rect_anot = None
    def __init__(self): 
        self.hijos = []
class Consulta: 
    rango = None
    lind = None 
    rlind = None
    ax_anot = None 
    anot = None 
    botones = None 
    @out1.capture()
    def teclas_handler(self,event): 
        if(event.key == 'n'): 
            self.siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    @out1.capture() 
    def handler_mouse(self,event): 
        if(event.xdata == None or event.ydata == None): 
            return 
        cels = env2.vars['seg_t'].arreglo.celdas
        n = len(cels)//2 
        hoja= -1
        for i in range(n,n*2):
            ##alguna de las hojas 
            r = cels[i].rect
            x,y = r.get_xy() 
            w = r.get_width() 
            #aprovechando para limpiar las hojas 
            cels[i].rect.set(facecolor = 'white')
            if(x <= event.xdata <= x + w and  y <= event.ydata <= y + w): 
                hoja = i 
        #limpia las hojas
        if(hoja != -1): 
            if(len(self.rango) == 2): 
                self.rango = [hoja]
            else: 
                #el rango es menor
                self.rango.append(hoja)
                self.rango.sort() 
            #pinta las hojas
            for i in range(self.rango[0],self.rango[-1]+1): 
                cels[i].rect.set(facecolor = 'pink')
        
    def zoom_mas(self): 
        x,y = env2.vars['fig'].get_size_inches()
        env2.vars['fig'].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env2.vars['fig'].get_size_inches()
        env2.vars['fig'].set_size_inches(x-1,y-1)
    def config_mouse(self): 
        env2.vars['cid_m'] = env2.vars['fig'].canvas.mpl_connect('button_press_event', self.handler_mouse)
    def siguiente_paso(self): 
        print("{},{}".format(self.lind,self.rind))
        if(self.lind > self.rind): 
            return
        cels = env2.vars['seg_t'].arreglo.celdas
        if(self.lind % 2 == 1): 
            cels[self.lind].circ.set(facecolor = 'red')
            self.lind = self.lind + 1 
        if(self.rind % 2 == 0):
            cels[self.rind].circ.set(facecolor = 'red')
            self.rind = self.rind - 1 
        self.lind  = self.lind //2 
        self.rind = self.rind // 2 

    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
    def handler_listo(self,event): 
        self.lind = self.rango[0]
        self.rind = self.rango[-1]
        env2.vars['fig'].canvas.mpl_disconnect(env2.vars['cid_m']) 
        env2.vars['cid_t'] = env2.vars['fig'].canvas.mpl_connect('key_press_event', self.teclas_handler)
        self.botones.children = [] 
    def poner_botones(self):  
        b = widgets.Button(description="Listo")
        b.on_click(self.handler_listo)
        if(self.botones == None): 
            self.botones = widgets.VBox([b])
            display(self.botones)
        else: 
            self.botones.children = [b]
    def init_anot(self): 
        text= "Escoge un rango haciendo click en dos casillas del arreglo.\n"
        text += "Cuando estes listo, presiona el boton."
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def __init__(self): 
        dibujar_arbol(env2.vars['inp_arr'])
        self.config_imagen() 
        self.config_mouse() 
        self.init_anot() 
        self.poner_botones() 
        self.rango = [] 
env2 = env2() 
env2.vars['fig'],env2.vars['ax'] = plt.subplots()  
env2.vars['seg_t'] = None
env2.vars['rad'] = 1
env2.vars['inp_arr'] = [random.randint(1,10) for i in range(0,16) ]
env2.vars['cid_m'] = None
env2.vars['cid_t'] = None
env2.vars['tecla_f'] = None
env2.vars['e1'] = Consulta()