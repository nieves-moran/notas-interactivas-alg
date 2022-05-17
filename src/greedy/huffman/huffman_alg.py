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
    n_nodos = 0 
    def __init__(self):
        self.raiz = Vertice()
        #es una lista de vertices par 
        self.vertices =  dict()
        self.vertices[0] = self.raiz 
        self.n_nodos = 1  
        self.aristas  = dict()

class Vertice: 
    circ = None 
    anotf = None 
    etiq = None
    padre = None
    hijos = None
    valor = 0
    letra = ""
    def __init__(self): 
        self.hijos = []
class Arista: 
    linea = None
    anot = None
def dfs(n,arbol,prof,y): 
    if(not n.hijos): 
        prof[n] = y 
    for i in n.hijos :  
        dfs(i,arbol,prof,y - 4*env.vars['rad'])

def prof_hojas(arbol): 
    prof = dict() 
    dfs(arbol.raiz,arbol,prof,0) 
    return prof
def entre_hijos(n):
    arbol = env.vars['arbol']
    ph = n.hijos[0]
    uh =  n.hijos[-1]
    xp,_ = ph.circ.get_center()
    xu,_ = uh.circ.get_center()
    return (xp + xu) /2 
def limpiar_arbol(): 
    arbol = env.vars['arbol']
    for _,v in arbol.vertices.items(): 
        if(v.circ != None): 
            v.circ.set(visible = False)
            v.anotf.set(visible = False)
            v.etiq.set(visible = False)
        v.circ = None 
    for (v,u) in arbol.aristas.keys():
        if(arbol.aristas[(v,u)].linea != None): 
            arbol.aristas[(v,u)].linea.set(visible = False)
        if(arbol.aristas[(v,u)].anot != None): 
            arbol.aristas[(v,u)].anot.set(visible = False)
    arbol.aristas = dict() 
def dibujar_arbol():  
    limpiar_arbol() 
    rad = env.vars['rad']
    arbol = env.vars['arbol']
    prof_h = prof_hojas(arbol) 
    inv = [arbol.raiz]
    cola = [] 
    x = 0
    for i,v in arbol.vertices.items(): 
        v.circ = None 
    for h,p in prof_h.items():
        cola.append((h,x,p))
        x = x + 4*rad
    hijos_proc = dict()
    while(cola): 
        n,x,y = cola[0]
        cola.pop(0)
        vis = True
        if(n in inv):
            vis = False 
        c = Circle((x,y),radius = rad,facecolor = 'white',edgecolor = 'black',visible = vis)
        n.anotf =  env.vars['ax'].text(x, y+0.3,"{:.2f}".format(n.valor),fontsize = 9,ha='center', va='center',visible = vis) 
        n.etiq =  env.vars['ax'].text(x, y-0.3,"{}".format(n.letra).format(n.valor),fontsize = 9,ha='center', va='center',visible = vis) 
        n.circ = c  
        env.vars['ax'].add_patch(c)
        p = n.padre
        if(p != None): 
            if(p not in hijos_proc): 
                hijos_proc[p] = 0 
            hijos_proc[p] = hijos_proc[p] + 1
            if(hijos_proc[p] == len(p.hijos)): 
                cola.append((p,entre_hijos(p),y + 4*rad)) 
    for i,v in arbol.vertices.items(): 
        for h in v.hijos:  
            vis = True 
            if v in inv: 
                vis = False
            xi,yi = v.circ.get_center()
            xj,yj = h.circ.get_center()
            linea = PathPatch(Path([inter_points(env.vars['rad'],xi,yi,xj,yj),inter_points(env.vars['rad'],xj,yj,xi,yi)]), facecolor='none', edgecolor='black',visible = vis)
            env.vars['ax'].add_patch(linea)
            if((v,h) not in arbol.aristas): 
                arbol.aristas[(v,h)] = Arista() 
            arbol.aristas[(v,h)].linea = linea
            xm,ym = punto_medio(xi,yi,xj,yj,1,0.5)
            if(env.vars['anotar']): 
                etiq = '0'
                if(v != arbol.raiz and h == v.hijos[1]): 
                    etiq = '1'
                arbol.aristas[(v,h)].anot = env.vars['ax'].text(xm, ym, etiq,fontsize = 9,ha='center', va='center',visible = vis) 
    env.vars['ax'].relim()
    env.vars['ax'].autoscale_view()
class Cuadro_codigo: 
    anot = None 
    rect = None 
#frecuencias es un diccionario de letra a un numero
class Env:
    vars = dict()  

class Ejecucion:
    siguientes = []  
    nuevo = None  
    aristas_coloreadas = []
    cuad_cod = None  
    def dibujar_cuadro_codigo(self,x,y): 
        #dibuja el cuadro con el codigo
        self.cuad_cod =  Cuadro_codigo() 
        self.cuad_cod.rect  = Rectangle((x,y),width = 10,height = 3) 
        env.vars['ax'].add_patch(self.cuad_cod.rect)
        self.cuad_cod.anot = env.vars['ax'].text(x, y,"la codificacion es",fontsize = 9,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1',alpha=0.1)) 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def limpiar_cuadro_codigo(self): 
        if(self.cuad_cod != None): 
            self.cuad_cod.rect.set(visible = False)
            self.cuad_cod.anot.set(visible = False)
    def obtener_frecuencias(self): 
        cad = "hfjadhfjhadkfhadjfhakhfdjkhadkjfhadkjhfsqiequropqjdhfjkadh"
        freq = dict() 
        for c in cad: 
            if(c not in freq): 
                freq[c] = 0
            freq[c] = freq[c] + 1
        n = len(cad) 
        for c in freq.keys(): 
            freq[c] = freq[c]/n 
        return freq
    def crear_arbol_inicial(self,frecuencias): 
        arbol = env.vars['arbol']
        for l,f in frecuencias.items():
            v = Vertice()  
            v.valor = f 
            v.padre = arbol.raiz
            arbol.raiz.hijos.append(v)
            v.letra = l  
            arbol.vertices[arbol.n_nodos] = v 
            arbol.n_nodos = arbol.n_nodos + 1
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis("off")
    def dos_mas_chicos(self):
        arbol = env.vars['arbol'] 
        lista = []
        for v in arbol.raiz.hijos: 
            lista.append((v.valor,v))
        lista.sort(key = (lambda elem : elem[0]))
        return lista
    def colorea_siguientes_nuevo(self,nuevo):
        #elimina los cambios en los anteriores 
        if(self.nuevo != None): 
            self.nuevo.circ.set(edgecolor = 'black')
        for v in self.siguientes: 
            v.circ.set(facecolor = 'white')
        l = self.dos_mas_chicos() 
        #si solo hay un nodo solo pintalo de rojo 
        if(len(l) == 1): 
            nuevo.circ.set(edgecolor = 'red')
            self.nuevo = nuevo 
            return 
        #si hay dos o más, pinta de amarillo los nuevo y de rojo el combinado 
        v1 = l[0][1]
        v2 = l[1][1]
        v1.circ.set(facecolor = 'yellow')
        v2.circ.set(facecolor = 'yellow')
        if(nuevo != None): 
            nuevo.circ.set(edgecolor = 'red')
        self.siguientes = [v1,v2]
        self.nuevo = nuevo
    def construye(self): 
        arbol = env.vars['arbol']
        lista = []
        for v in arbol.raiz.hijos: 
            lista.append((v.valor,v))
        lista.sort(key = (lambda elem : elem[0]))
        #tomas los dos primeros n1 n2 
        v1 = lista[0][1]
        lista.pop(0)
        v2 = lista[0][1]
        lista.pop(0)
        n_vert = Vertice() 
        n_vert.valor = v1.valor + v2.valor 
        arbol.vertices[arbol.n_nodos] = n_vert 
        arbol.n_nodos = arbol.n_nodos + 1
        v1.padre = n_vert  
        v2.padre = n_vert
        n_vert.hijos = [v1,v2]
        #eliminar hijos del 0
        arbol.raiz.hijos.remove(v1) 
        arbol.raiz.hijos.remove(v2)
        arbol.raiz.hijos.append(n_vert)
        n_vert.padre = arbol.raiz 
        dibujar_arbol() 
        self.colorea_siguientes_nuevo(n_vert) 
    def colorea_aristas(self,actual): 
        arbol = env.vars['arbol']
        #quitar el color a las que están coloreadas 
        for (u,v) in self.aristas_coloreadas: 
            arbol.aristas[(u,v)].linea.set(color = 'black')
            arbol.aristas[(u,v)].linea.set(linewidth = 1)
        while(actual.padre != None): 
            arbol.aristas[(actual.padre,actual)].linea.set(color = 'blue')
            arbol.aristas[(actual.padre,actual)].linea.set(linewidth = 3)
            self.aristas_coloreadas.append((actual.padre,actual))
            actual = actual.padre 

    @out1.capture() 
    def handler_mouse(self,event): 
        if(event.xdata == None or event.ydata == None): 
            return 
        arbol = env.vars['arbol']
        for k,h in arbol.vertices.items():
            if(not h.hijos): 
                x,y = h.circ.get_center() 
                if((x - event.xdata)**2 + (y - event.ydata)**2 <= env.vars['rad']):
                    self.colorea_aristas(h)
                    self.dibujar_cuadro_codigo(x,y-3) 
                    break
    @out1.capture() 
    def handler_mouse_release(self,event): 
        self.limpiar_cuadro_codigo() 
    def configuracion_mouse_codif(self):  
        env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.handler_mouse)
        env.vars['cid_m_r'] = env.vars['fig'].canvas.mpl_connect('button_release_event', self.handler_mouse_release)
    def etiqueta_arbol(self): 
        if(env.vars['anotar']): 
            return
        env.vars['anotar'] = True
        dibujar_arbol()
        self.configuracion_mouse_codif()  
    def siguiente_paso(self):
        #tomar los dos nodos hijos del 0 que tienen la frecuencia mas chica 
        arbol = env.vars['arbol']
        if(len(arbol.raiz.hijos) == 1): 
            self.etiqueta_arbol() 
        else: 
            self.construye() 
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
        self.crear_arbol_inicial(self.obtener_frecuencias())
        dibujar_arbol() 
        self.colorea_siguientes_nuevo(None) 
env = Env() 
env.vars['arbol'] = Arbol() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['cid_m_r'] = None
env.vars['anotar'] = False
env.vars['e1'] = Ejecucion() 