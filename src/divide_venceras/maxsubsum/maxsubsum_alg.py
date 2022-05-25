from cmath import atan
from glob import glob
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse 
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

class Vertice: 
    ind_l = 0
    ind_r = 0 
    circ = None 
    anotc = None 
    padre = None
    hijos = None
    valor =None
    #arreglo : Arreglo
    arreglo = None 
    #arr : list(int)
    arr = None
    #es para la anotación del índice 
    ind_anot = None 
    ind = 0 
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
    anot = None 
    valor = 0 
class Arista: 
    linea = None
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
    return (xp + xu) /2 
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
        a.linea.set(visible = False)
    arbol.aristas = dict() 
def dibujar_arreglo(arreglo,x,y,etiq_b): 
    ax = env.vars['ax']
    arr = Arreglo(len(arreglo),arreglo)
    for i in range(0,len(arreglo)): 
        arr.elms[i].rect = Rectangle((x,y),width = 3 , height = 3,facecolor = 'white',edgecolor = 'black') 
        ax.add_patch(arr.elms[i].rect) 
        arr.elms[i].valor = arreglo[i]
        etiq = "{}".format(arreglo[i])
        if(not etiq_b): 
            etiq = ""
        arr.elms[i].anot = ax.text(x+1.5,y+1.5,etiq,ha = 'center',va = 'center',fontsize = 9) 
        x = x + 3 
    return arr
def puntos_arista(p,h): 
    xp,yp = p.arreglo.elms[0].rect.get_xy() 
    xp = xp + (3*(len(p.arreglo.elms)))/2
    yp = yp - 3
    xh,yh = h.arreglo.elms[0].rect.get_xy()
    xh = xh + (3*(len(h.arreglo.elms)))/2 
    yh = yh + 4
    return xp,yp,xh,yh
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
        x = x + (len(h.arr)*3)*2
    hijos_proc = dict()
    while(cola): 
        n,x,y = cola[0]
        cola.pop(0)
        n.arreglo = dibujar_arreglo(n.arr,x - (len(n.arr)*3)/2,y,True)
        p = n.padre
        if(p != None): 
            if(p not in hijos_proc): 
                hijos_proc[p] = 0 
            hijos_proc[p] = hijos_proc[p] + 1
            if(hijos_proc[p] == len(p.hijos)): 
                cola.append((p,entre_hijos(p),y + 16)) 
    #dibujar aristas
    for i,p in arbol.vertices.items():
        for h in p.hijos:  
            xp,yp,xh,yh = puntos_arista(p,h)  
            linea = PathPatch(Path([(xp,yp),(xh,yh)]), facecolor='none', edgecolor='black',linestyle = '--')
            env.vars['ax'].add_patch(linea)
            arbol.aristas[(p,h)] = Arista() 
            arbol.aristas[(p,h)].linea = linea 
    env.vars['ax'].relim(visible_only = True)
    env.vars['ax'].autoscale_view()
#frecuencias es un diccionario de letra a un numero

class Env:
    vars = dict()  

class Ejecucion:  
    anot = None 
    ax_anot = None 
    cola = [] 
    hojas = [] 
    hojas_n = [] 
    limpiar = [] 
    #son los 3 circulos 
    circs = [] 
    def crear_arbol_inicial(self):
        arr =  [random.randint(-30,20) for i in range(0,16)]
        arbol = env.vars['arbol']
        arbol.raiz.arr = arr
        self.cola = [arbol.raiz] 
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
        text += "el siguiente paso del algoritmo." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def crear_arbol_rec(self):
        cola_n = []  
        arbol = env.vars['arbol']
        for c in self.cola:
            v1 = Vertice() 
            v2 = Vertice()
            c.hijos = [v1,v2]
            v1.padre = c
            v1.arr = c.arr[0:len(c.arr)//2]
            arbol.vertices[arbol.n_nodos] = v1 
            arbol.n_nodos += 1 
            arbol.vertices[arbol.n_nodos] = v2
            arbol.n_nodos += 1 
            v2.padre = c
            v2.arr = c.arr[len(c.arr)//2:]
            if(len(v1.arr) > 1 ): 
                cola_n.append(v1)
            else: 
                self.hojas.append(v1)
            if(len(v2.arr) > 1 ): 
                cola_n.append(v2)
            else: 
                self.hojas.append(v2) 
        self.cola = cola_n
        dibujar_arbol()  

    def colorear(self,n):
        l,r = n.ind_l,n.ind_r
        for i in range(l,r+1): 
            n.arreglo.elms[i].rect.set(facecolor = '#9999FF')
    def calcular_indices(self,nodo): 
        arr = nodo.arr
        n = len(arr) 
        i = n//2 - 1
        l = i 
        sum = arr[i]
        left_sum = arr[i] 
        i = i - 1 
        while i >= 0 : 
            sum += arr[i]
            if(left_sum < sum): 
                left_sum = sum 
                l = i 
            i = i - 1
        j = n//2 
        r = j 
        sum = arr[j]
        right_sum = arr[j]
        j = j + 1 
        while j < n: 
            sum += arr[j]
            if(right_sum < sum): 
                right_sum = sum 
                r = j
            j = j + 1 
        nodo.ind_l = l 
        nodo.ind_r = r
    def act_max_padre(self,p,h1,h2): 
        sp = sum(p.arr[p.ind_l:p.ind_r + 1 ])
        sh1 = sum(h1.arr[h1.ind_l:h1.ind_r + 1 ])
        sh2 =  sum(h2.arr[h2.ind_l:h2.ind_r + 1 ])
        max_sum = sp 
        max_s = 1  
        if(max_sum < sh1): 
            max_sum = sh1 
            p.ind_l = h1.ind_l 
            p.ind_r = h1.ind_r
            max_s = 2  
        if(max_sum < sh2): 
            max_sum = sh2 
            p.ind_l = h2.ind_l + len(h2.arr)
            p.ind_r = h2.ind_r + len(h2.arr) 
            max_s = 3 
        return sp,sh1,sh2,max_s 
    def poner_circulos(self,nodos):
        if(not self.circs):
            i = 1 
            for n in nodos:
                x,y =  n.arreglo.elms[0].rect.get_xy()
                y += 1.5 
                x += ((len(n.arr))*3)/2 
                r = (len(n.arr)*3)
                c = Ellipse((x,y),width = r+5, height = 5 ,facecolor = 'none',edgecolor = '#0000FF')
                env.vars['ax'].add_patch(c)
                y += 5 
                anot = env.vars['ax'].text(x,y,i,fontsize = 9)
                self.circs.append((c,anot))
                i += 1 
        else: 
            i = 0
            for n in nodos: 
                x,y =  n.arreglo.elms[0].rect.get_xy() 
                x,y =  n.arreglo.elms[0].rect.get_xy()
                y += 1.5 
                x += ((len(n.arr))*3)/2 
                r = (len(n.arr)*3)
                c = self.circs[i][0]
                anot = self.circs[i][1]
                c.width = r + 5 
                c.set(center = (x,y))
                y += 5 
                anot.set(position = (x,y))
                i += 1 
    #va a colorear los 3 arreglos 
    def calc_max(self): 
        for n in self.limpiar: 
            for e in n.arreglo.elms: 
                e.rect.set(facecolor = 'white')
        if(self.limpiar): 
            self.colorear(self.limpiar[0])
        self.limpiar = [] 
        if(not self.hojas): 
            self.hojas = self.hojas_n 
            self.hojas_n = [] 
        #quita los colores anteriores salvo el que tenia mayor
        if(len(self.hojas) == 1): 
            for c,a in self.circs: 
                c.set(visible = False)
                a.set(visible = False)
            r = self.hojas[0]
            s = sum(r.arr[r.ind_l:r.ind_r+1])
            text = "El algoritmo termina. La suma maxima es {}".format(s)
            self.anot.set(text = text)
            return 
        h1,h2 = self.hojas[0],self.hojas[1]
        self.hojas.pop(0)
        self.hojas.pop(0)
        self.colorear(h1)
        self.colorear(h2)
        p = h1.padre
        self.calcular_indices(p)
        self.colorear(p)
        self.hojas_n.append(p)
        #pon los circulos
        self.poner_circulos([p,h1,h2])
        s1,s2,s3,sm = self.act_max_padre(p,h1,h2)
        self.limpiar = [p,h1,h2] 
        text = "Las sumas de los subarreglos son las siguentes: \n"
        text += "El subarreglo 1: {}\n".format(s1) 
        text += "El subarreglo 2: {}\n".format(s2) 
        text += "El subarreglo 3: {}\n".format(s3)
        text += "El subarreglo con la suma maxima es {} \n".format(sm)
        self.anot.set(text = text)

    def siguiente_paso(self):
        if(self.cola):
            self.crear_arbol_rec() 
        else: 
            self.calc_max() 
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
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_arbol_inicial()
        self.init_anot() 
        dibujar_arbol() 
env = Env() 
env.vars['arbol'] = Arbol() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
