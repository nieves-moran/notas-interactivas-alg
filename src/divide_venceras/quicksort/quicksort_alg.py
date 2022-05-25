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

class Arbol: 
    raiz = None 
    vertices = None 
    aristas = None 
    n = 0 
    n_nodos = 0
    niveles = 1  
    niveles_l = []
    def __init__(self):
        self.raiz = Vertice()
        #es una lista de vertices par 
        self.vertices =  dict()
        self.vertices[0] = self.raiz 
        self.n_nodos = 1  
        self.aristas  = dict()
        self.niveles_l.append([self.raiz])
class Variable: 
    anot = None 
    valor = None 
class Vertice: 
    #para ver si los generaron o no 
    izq = False
    der = False 
    circ = None 
    anotc = None 
    padre = None
    hijos = None
    valor =None
    #es la cadena izq si es izquierdo o es der si es derecho 
    tipo_h = None 
    #arreglo : Arreglo
    arreglo = None 
    #arr : list(int)
    arr = None
    #es para la anotación del índice 
    ind_anot = None 
    ind = 0 
    pivote = None 
    def __init__(self): 
        self.hijos = []
class Arreglo: 
    elms = [] 
    def __init__(self,n): 
        self.elms = [Celda() for i in range(0,n)]
    def __init__(self,n,arr):
        self.elms = [Celda() for i in range(0,n)]
        for i in range(0,n):  
            self.elms[i].valor = arr[i] 
class Celda: 
    rect = None 
    rect_color = None 
    anot = None 
    valor = 0 
class Arista: 
    lineas = []
    anot = None
def dfs(n,arbol,prof,y): 
    if(not n.hijos): 
        prof[n] = y 
    for i in n.hijos :  
        dfs(i,arbol,prof,y - 16)

def prof_hojas(arbol): 
    prof = dict() 
    dfs(arbol.raiz,arbol,prof,0) 
    return prof
def entre_hijos(n):
    arbol = env.vars['arbol']
    ph = n.hijos[0]
    uh =  n.hijos[-1]
    xp = ph.arreglo.elms[0].rect.get_xy()[0]
    xu = uh.arreglo.elms[0].rect.get_xy()[0] + len(uh.arreglo.elms)*3
    pos = (xp + xu) /2 
    return pos 
def limpiar_arreglo(arr): 
    for c in arr.elms: 
        c.rect.set(visible = False)
        c.anot.set(visible = False)
def limpiar_arbol(): 
    arbol = env.vars['arbol']
    for _,v in arbol.vertices.items(): 
        if(v.arreglo != None): 
            limpiar_arreglo(v.arreglo)
    for (p,h),a in arbol.aristas.items():
        for l in a.lineas: 
            l.set(visible = False ) 
    arbol.aristas = dict() 
def dibujar_arreglo(n,arreglo,x,y,etiq_b): 
    ax = env.vars['ax']
    if(n.arreglo == None): 
        n.arreglo = Arreglo(len(arreglo),arreglo)
    for i in range(0,len(arreglo)): 
        n.arreglo.elms[i].rect = Rectangle((x,y),width = 3 , height = 3,facecolor = 'white',edgecolor = 'black') 
        if( n.arreglo.elms[i].rect_color != None): 
            n.arreglo.elms[i].rect.set(facecolor =  n.arreglo.elms[i].rect_color)
        ax.add_patch(n.arreglo.elms[i].rect) 
        n.arreglo.elms[i].valor = arreglo[i]
        etiq = "{}".format(arreglo[i])
        if(not etiq_b): 
            etiq = ""
        n.arreglo.elms[i].anot = ax.text(x+1.5,y+1.5,etiq,ha = 'center',va = 'center',fontsize = 9) 
        x = x + 3 
    return n.arreglo
def puntos_arista(p,h): 
    xp,yp = p.arreglo.elms[0].rect.get_xy() 
    xp = xp + (3*(len(p.arreglo.elms)))/2
    yp = yp - 3
    xh,yh = h.arreglo.elms[0].rect.get_xy()
    xh = xh + (3*(len(h.arreglo.elms)))/2 
    yh = yh + 4
    return xp,yp,xh,yh
def puntos_area(p, h): 
    xp,yp = p.arreglo.elms[0].rect.get_xy()
    xh,yh = h.arreglo.elms[0].rect.get_xy()
    if(h.tipo_h == 'izq'): 
        p1 = xp,yp 
        p2 = xp + p.pivote*3, yp 
        p3 = xh,yh + 3 
        p4 = xh + len(h.arreglo.elms)*3, yh + 3 
    else: 
        p1 = xp + (p.pivote+1)*3, yp 
        p2 = xp + len(p.arreglo.elms)*3,yp 
        p3 =  xh,yh + 3  
        p4 =  xh + len(h.arreglo.elms)*3, yh + 3 
    #p y h son nodos 
    return ((p1,p2),(p3,p4))
def dibujar_arbol():  
    limpiar_arbol() 
    rad = env.vars['rad']
    arbol = env.vars['arbol']
    prof_h = prof_hojas(arbol) 
    cola = [] 
    x = 0
    for i,v in arbol.vertices.items(): 
        v.circ = None 
    for h,p in prof_h.items():
        cola.append((h,x,p))
        x = x + (len(arbol.raiz.arr)*3)*0.7 + 5
    hijos_proc = dict()
    while(cola): 
        n,x,y = cola[0]
        cola.pop(0)
        n.arreglo = dibujar_arreglo(n,n.arr,x,y,True)
        if(n.pivote != None): 
            n.arreglo.elms[n.pivote].rect.set(facecolor = '#CCFFE5')
        p = n.padre
        if(p != None): 
            if(p not in hijos_proc): 
                hijos_proc[p] = 0 
            hijos_proc[p] = hijos_proc[p] + 1
            if(hijos_proc[p] == len(p.hijos)): 
                cola.append((p,entre_hijos(p)-(len(p.arr)*3)/2,y + 16)) 
    #dibujar aristas
    for i,p in arbol.vertices.items():
        for h in p.hijos:  
            (p1,p2),(p3,p4) = puntos_area(p,h)  
            linea1 = PathPatch(Path([p1,p3]), facecolor='none', edgecolor='black',linestyle = '--')
            env.vars['ax'].add_patch(linea1)
            linea2 = PathPatch(Path([p2,p4]), facecolor='none', edgecolor='black',linestyle = '--')
            env.vars['ax'].add_patch(linea2)
            arbol.aristas[(p,h)] = Arista() 
            arbol.aristas[(p,h)].lineas = [linea1,linea2] 
    env.vars['ax'].relim(visible_only=True)
    env.vars['ax'].autoscale_view()
#frecuencias es un diccionario de letra a un numero

def partition(arr):
    def swap(i,j,arr): 
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
    r = len(arr)-1
    x = arr[r]
    i = -1
    for j in range(0,r):  
        if(arr[j] <= x): 
            i = i + 1 
            swap(i,j,arr)
    swap(i+1,r,arr)
    arr1 = arr[0:i+1]  
    arr2 = arr[i+2:]
    return (arr1,arr2,i+1)
class Env:
    vars = dict()  

class Ejecucion:  
    ax_anot = None
    anot = None 
    cola = [] 
    arr_ab = True
    hojas = [] 
    termina = False 
    partition = True
    i = -1 
    j = 0 
    r = None
    anot_i = None 
    anot_j  = None 
    anot_r = None 
    nodo_act = None
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
        text += "el siguiente paso de quicksort." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    
    def crear_nodo_hijo(self,lado): 
        arbol = env.vars['arbol']
        v1 = Vertice()
        if(lado == 'izq'): 
            arr = self.nodo_act.arr[0:self.nodo_act.pivote]   
            v1.tipo_h = 'izq'
        else: 
            arr = self.nodo_act.arr[self.nodo_act.pivote+1:]   
            v1.tipo_h = 'der'
        v1.padre = self.nodo_act
        v1.arr = arr 
        self.nodo_act.hijos.append(v1)
        arbol.vertices[arbol.n_nodos] = v1 
        arbol.n_nodos = arbol.n_nodos + 1 
        self.nodo_act = v1 
        dibujar_arbol()
        #poner los indices 
        n = len(self.nodo_act.arr)
        self.r = n - 1
        x,y =  self.nodo_act.arreglo.elms[0].rect.get_xy() 
        self.anot_i.set(position  = (x - 1.5,y + 8))
        self.anot_j.set(position =  (x+1.5,y+6))
        self.anot_r.set(position = (x + 3*n - 1.5,y+4))
        self.partition = True
        #poner bien los indices 
        self.i = -1 
        self.j = 0 
    def arriba_abajo(self): 
        if(self.nodo_act.pivote > 0  and  not self.nodo_act.izq):
                text = "Se produce una llamada recursiva sobre el subarreglo izquierdo"
                self.anot.set(text = text)
                self.nodo_act.izq = True 
                self.crear_nodo_hijo('izq')
        elif(self.nodo_act.pivote < len(self.nodo_act.arr) -  1 and not self.nodo_act.der): 
                text = "Se produce una llamada recursiva sobre el subarreglo derecho"
                self.anot.set(text = text)
                self.nodo_act.der= True 
                self.crear_nodo_hijo('der')
        else:
            self.hojas = [self.nodo_act] 
            self.abajo_arriba() 
       
    def abajo_arriba(self):
        text = "La llamada recursiva regresa el resultado."
        self.anot.set(text = text)
        self.anot_i.set(visible = False)
        self.anot_j.set(visible = False)
        self.anot_r.set(visible = False)
        if(self.termina): 
            return 
        h= self.hojas[0]
        self.hojas.pop(0)
        #ve a tu padre 
        p = h.padre 
        if(p == None): 
            self.termina = True
            text= "El algoritmo termina, todo el arreglo esta ordenado.\n"
            self.anot.set(text = text)
            return 
        if(h.tipo_h == 'izq'): 
            for i in range(0,len(h.arr)): 
                p.arr[i] = h.arr[i]
                p.arreglo.elms[i].rect_color = '#CCFFE5'
        else: 
            for i in range(p.pivote + 1,len(p.arr)): 
                p.arr[i] = h.arr[i - (p.pivote+1)]
                p.arreglo.elms[i].rect_color = '#CCFFE5'
        p.hijos.remove(h)
        if(not p.hijos): 
            self.hojas.append(p)
            self.nodo_act= p  
        #elimino el nodo  
        #dibujar el arbol 
        dibujar_arbol()
    def swap(self,i,j):
        temp = self.nodo_act.arr[i]
        self.nodo_act.arr[i] = self.nodo_act.arr[j]
        self.nodo_act.arr[j] = temp 
        self.nodo_act.arreglo.elms[i].anot.set(text = self.nodo_act.arr[i])
        self.nodo_act.arreglo.elms[j].anot.set(text = self.nodo_act.arr[j])
        self.nodo_act.arreglo.elms[i].valor = self.nodo_act.arr[i]
        self.nodo_act.arreglo.elms[j].valor = self.nodo_act.arr[j]

    def ejecuta_part(self): 
        text= "Subrutina para partir el arreglo:\n"
        text += "El pivote {} esta marcado por el indice r\n".format(self.nodo_act.arr[self.r])
        if(self.j == self.r): 
            self.swap(self.i+1,self.r)
            self.anot_r.set(x = self.anot_i.get_position()[0] + 3)
            self.partition = False
            self.nodo_act.pivote = self.i+1 
            text += "La rutina para partir concluye, se intercambia el pivote"
            self.anot.set(text = text)
            return 
        if(self.nodo_act.arr[self.j]  <= self.nodo_act.arr[self.r]): 
            self.i = self.i + 1 
            self.anot_i.set(x = self.anot_i.get_position()[0] + 3)
            self.swap(self.i ,self.j)
            text += "Hay un intercambio entre {} y {}, y el indice i se incrementa\n".format(self.nodo_act.arr[self.j],self.nodo_act.arr[self.i])
        self.j = self.j + 1  
        self.anot_j.set(x = self.anot_j.get_position()[0] + 3)
        self.anot.set(text = text)
    
    def siguiente_paso(self):
        if(self.partition): 
            self.anot_i.set(visible = True)
            self.anot_j.set(visible = True)
            self.anot_r.set(visible = True)
            self.ejecuta_part() 
        else: 
            self.arriba_abajo() 
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
    def crear_arbol_inicial(self):
        arr =  [2,9,8,5,6,7,10,12,1,3]
        arbol = env.vars['arbol']
        arbol.raiz.arr = arr
        self.cola = [(arbol.raiz,0)] 
        self.nodo_act = arbol.raiz
    def poner_ind_ini(self): 
        n = len(self.nodo_act.arr)
        self.r = n - 1
        x,y =  self.nodo_act.arreglo.elms[0].rect.get_xy() 
        self.anot_i = env.vars['ax'].text(x - 1.5,y + 8,"i")
        self.anot_j = env.vars['ax'].text(x+1.5,y+6,"j")
        self.anot_r = env.vars['ax'].text(x + 3*n - 1.5,y+4,"r")
    def __init__(self): 
        self.config_imagen()
        self.config_teclas() 
        self.init_anot()    
        self.crear_arbol_inicial() 
        dibujar_arbol() 
        self.poner_ind_ini()
env = Env() 
env.vars['arbol'] = Arbol() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
