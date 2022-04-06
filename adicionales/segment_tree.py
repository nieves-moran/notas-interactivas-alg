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
class Env: 
    vars = None
    def __init__(self): 
        self.vars = dict()

def dibujar_arbol(arr): 
    env.vars['seg_t'] = Segment_tree(arr)
    n = len(arr)
    x = 0 
    y = 0 
    for i in range(2*n- 1,n-1,-1): 
        cl = Celda() 
        env.vars['seg_t'].arreglo.celdas[i] = cl
        cl.padre = i//2 
        cl.valor = env.vars['seg_t'].tree[i]
        cr = Circle((x,y),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        cl.anot = env.vars['ax'].text(x, y, '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        env.vars['ax'].add_patch(cr)
        cl.circ = cr
        r = Rectangle((x-env.vars['rad'],y-3*env.vars['rad']),width = 2*env.vars['rad'],height = 2*env.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        env.vars['ax'].add_patch(r)
        cl.rect_anot = env.vars['ax'].text(x, y-2*env.vars['rad'], '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        x = x - 2*env.vars['rad']
        cl.rect = r 
    for i in range(n-1,0,-1): 
        cl = Celda() 
        env.vars['seg_t'].arreglo.celdas[i] = cl
        cl.padre = i//2 
        cl.valor = env.vars['seg_t'].tree[i]
        cl.hijos = [2*i,2*i + 1]
        cels = env.vars['seg_t'].arreglo.celdas
        x = (cels[2*i].circ.get_center()[0] + cels[2*i+1].circ.get_center()[0]) / 2
        y =  env.vars['seg_t'].arreglo.celdas[2*i].circ.get_center()[1] + 3*env.vars['rad']
        cr = Circle((x,y),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black') 
        cl.anot = env.vars['ax'].text(x, y, '${}$'.format(cl.valor),fontsize = 9,ha='center', va='center') 
        env.vars['ax'].add_patch(cr)
        lx,ly = cels[2*i].circ.get_center() 
        rx,ry = cels[2*i+1].circ.get_center() 
        linea = PathPatch(Path([inter_points(env.vars['rad'],x,y,lx,ly),inter_points(env.vars['rad'],lx,ly,x,y)]), facecolor='none', edgecolor='black')
        env.vars['ax'].add_patch(linea)
        cels[2*i].ar_p = linea 
        linea = PathPatch(Path([inter_points(env.vars['rad'],x,y,rx,ry),inter_points(env.vars['rad'],rx,ry,x,y)]), facecolor='none', edgecolor='black')
        env.vars['ax'].add_patch(linea)
        cels[2*i+1].ar_p = linea 
        cl.circ = cr
    #dibujar aristas
     
    env.vars['ax'].relim()
    env.vars['ax'].autoscale_view()
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
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]  

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
    @out1.capture()
    def handler_tecla(self,event): 
        if(event.key in env.vars['tecla_f']): 
            env.vars['tecla_f'][event.key]()
    @out1.capture() 
    def handler_mouse(self,event): 
        if(event.xdata == None or event.ydata == None): 
            return 
        cels = env.vars['seg_t'].arreglo.celdas
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
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x-1,y-1)
    def config_mouse(self): 
        print("config mouse")
        env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.handler_mouse)
        print(env.vars['cid_m'])
    def handler_sig(self): 
        if(self.lind > self.rind): 
            return
        print("los indices son {} {}".format(self.lind,self.rind))
        cels = env.vars['seg_t'].arreglo.celdas
        if(self.lind % 2 == 1): 
            cels[self.lind].circ.set(facecolor = 'red')
            self.lind = self.lind + 1 
        if(self.rind % 2 == 0):
            cels[self.rind].circ.set(facecolor = 'red')
            self.rind = self.rind - 1 
        self.lind  = self.lind //2 
        self.rind = self.rind // 2 
    def handler_listo(self): 
        #desconecta el mouse 
        if(self.rango): 
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_m']) 
            print("el rango es {}".format(self.rango))
            self.lind = self.rango[0]
            self.rind = self.rango[-1]
            env.vars['tecla_f']['n'] =  self.handler_sig
        else: 
            print("no has escogido el rango")

    def config_teclas(self): 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_tecla)
        print(env.vars['cid_t'])
        env.vars['tecla_f'] = dict()
        env.vars['tecla_f']['+'] = self.zoom_mas
        env.vars['tecla_f']['-'] = self.zoom_menos
        env.vars['tecla_f']['enter'] = self.handler_listo
        print("config teclas")
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
    def __init__(self): 
        dibujar_arbol(env.vars['inp_arr'])
        self.config_imagen() 
        self.config_mouse() 
        self.config_teclas()  
        self.rango = [] 

class Modificacion:  
    hoja = None 
    ind = None
    def zoom_mas(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x-1,y-1)
    def handler_tecla(self,event): 
        if(event.key == 'l'):
            print("hola")
            return  
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
        else: 
            return 
    @out1.capture()
    def handler_mouse(self,event):  
        if(event.xdata == None or event.ydata == None): 
            return 
        cels = env.vars['seg_t'].arreglo.celdas
        n = len(cels)//2 
        self.hoja= -1
        for i in range(n,n*2):
            ##alguna de las hojas 
            r = cels[i].rect
            x,y = r.get_xy() 
            w = r.get_width() 
            if(x <= event.xdata <= x + w and  y <= event.ydata <= y + w): 
                self.hoja = i 
        #si hizo click en una hoja la pinta de verde 
        if(self.hoja != -1): 
            cels[self.hoja].rect.set(facecolor = 'green')
            cels[self.hoja].rect_anot.set(text = "")
            self.config_teclas_numero()
    @out1.capture()
    def config_teclas_numero(self): 
            print("se desconecta la tecla")
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
            #desconecta el mouse 
            env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_ingresar_numero)
    @out1.capture()
    def handler_ingresar_numero(self,event): 
        if(event.key.isdigit()): 
            cels = env.vars['seg_t'].arreglo.celdas
            t = cels[self.hoja].rect_anot.get_text()
            t = t + event.key
            cels[self.hoja].rect_anot.set(text = t)
        elif(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
        elif(event.key == 'enter'): 
            self.config_teclas_ej() 
            return 
    def config_teclas_ej(self): 
        env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
            #desconecta el mouse 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_teclas_ej)
    def siguiente_paso(self): 
        print("un paso mas")
        cels = env.vars['seg_t'].arreglo.celdas
        if(self.ind == None): 
            self.ind = self.hoja
            cels[self.ind].circ.set(facecolor= 'green')
            cels[self.ind].valor = int(cels[self.ind].rect_anot.get_text()) 
            cels[self.ind].anot.set(text = cels[self.ind].valor)
        else: 
            cels = env.vars['seg_t'].arreglo.celdas
            lc = self.ind*2
            rc = self.ind*2 + 1
            cels[self.ind].circ.set(facecolor= 'green')
            cels[self.ind].valor = cels[lc].valor + cels[rc].valor
            cels[self.ind].anot.set(text = cels[self.ind].valor)
        self.ind = self.ind // 2 
    @out1.capture()
    def handler_teclas_ej(self,event): 
        if(event.key == 'n'): 
            self.siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    def config_mouse(self): 
        print("config mouse")
        env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.handler_mouse)
        print(env.vars['cid_m'])
    def config_teclas(self): 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_tecla)
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
    def __init__(self): 
        dibujar_arbol(env.vars['inp_arr']) 
        self.config_imagen()
        self.desactivar_letras_gui() 
        self.config_mouse() 
        self.config_teclas()
    def desactivar_letras_gui(self): 
        plt.rcParams["keymap.home"] = [] 
        plt.rcParams["keymap.back"] = [] 
        plt.rcParams["keymap.forward"] = [] 
        plt.rcParams["keymap.pan"] = [] 
        plt.rcParams["keymap.zoom"] = [] 
        plt.rcParams["keymap.save"] = [] 
        plt.rcParams["keymap.fullscreen"] = [] 
        plt.rcParams["keymap.grid"] = [] 
        plt.rcParams["keymap.grid_minor"] = [] 
        plt.rcParams["keymap.xscale"] = []
        plt.rcParams["keymap.yscale"] = []
        plt.rcParams["keymap.quit"] = [] 
    def submit(self,text):
        print("hola")

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()  
env.vars['seg_t'] = None
env.vars['rad'] = 1
env.vars['inp_arr'] = [random.randint(1,10) for i in range(0,32) ]
env.vars['cid_m'] = None
env.vars['cid_t'] = None
env.vars['tecla_f'] = None
env.vars['e1'] = Modificacion()