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

class Vertice: 
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
    env.vars['ax'].relim()
    env.vars['ax'].autoscale_view()
#frecuencias es un diccionario de letra a un numero

class Env:
    vars = dict()  

class Ejecucion:  
    cola = []
    nivel = 0 
    def crear_arbol_inicial(self):
        arr =  [random.randint(5,50) for i in range(0,16)]
        arbol = env.vars['arbol']
        arbol.raiz.arr = arr
        self.cola = [arbol.raiz] 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis("off")

    def inicializar_ind_nivel(self,nivel): 
        #limpiar el nivel anterior 
        arbol = env.vars['arbol']
        if(nivel < len(arbol.niveles_l)-1): 
            for n in arbol.niveles_l[nivel+1]: 
                if(n.ind_anot != None): 
                    n.ind_anot.set(visible = False)
        for i in range(0,len(arbol.niveles_l[nivel]),2): 
            n1 = arbol.niveles_l[nivel][i]
            n2 = arbol.niveles_l[nivel][i+1]
            p = n1.padre 
            x1,y1 = n1.arreglo.elms[0].rect.get_xy(); 
            x2,y2 = n2.arreglo.elms[0].rect.get_xy(); 
            xp,yp = p.arreglo.elms[0].rect.get_xy(); 
            if(n1.ind_anot == None): 
                anot_i = env.vars['ax'].text(x1+3/2, y1-3, '$i$',fontsize = 9) 
                n1.ind_anot = anot_i
            else: 
                n1.ind_anot.set(x = x1+3/2)
                n1.ind_anot.set(text = '$i$')
            if(n2.ind_anot == None): 
                anot_j = env.vars['ax'].text(x2+3/2, y2-3, '$j$',fontsize = 9) 
                n2.ind_anot = anot_j
            else: 
                n2.ind_anot.set(x = x2+3/2)
                n2.ind_anot.set(text = '$j$')
            if(p.ind_anot == None): 
                anot_k = env.vars['ax'].text(xp+3/2, yp-3, '$k$',fontsize = 9) 
                p.ind_anot = anot_k
            else: 
                p.ind_anot.set(x = xp+3/2)
                p.ind_anot.set(text = '$k$')
            n1.ind = 0 
            n2.ind = 0 
            p.ind = 0 
    def arriba_abajo(self): 
        arbol = env.vars['arbol']
        cola_n = []
        for n in self.cola: 
            lc = [n.arr[i] for i in range(0,len(n.arr)//2)]  
            rc = [n.arr[i] for i in range(len(n.arr)//2,len(n.arr))]
            v1 = Vertice()
            v2 = Vertice() 
            v1.padre = n  
            v1.arr = lc 
            v2.padre = n 
            v2.arr = rc 
            arbol.vertices[arbol.n_nodos] = v1 
            arbol.vertices[arbol.n_nodos+1] = v2 
            arbol.n_nodos = arbol.n_nodos+2
            n.hijos = [v1,v2]
            cola_n.append(v1)
            cola_n.append(v2)
        self.cola = cola_n
        arbol.niveles = arbol.niveles + 1 
        arbol.niveles_l.append(cola_n.copy())
        dibujar_arbol()
    def abajo_arriba(self): 
        arbol = env.vars['arbol']
        if(self.nivel == 0): 
            return 
        #a partir de aquí no está en el nivel 1 
        prim_niv_ant = arbol.niveles_l[self.nivel-1][0]
        if( prim_niv_ant.ind == len(prim_niv_ant.arreglo.elms)): 
            self.nivel = self.nivel - 1 
            #si ahora el nivel es 0 ya no inicializar nada 
            if(self.nivel == 0): 
                #limpiar los indices que quedan en el primer y segundo nivel 
                for n in arbol.niveles_l[0]: 
                    n.ind_anot.set(visible = False)
                for n in arbol.niveles_l[1]: 
                    n.ind_anot.set(visible = False)
                return 
            self.inicializar_ind_nivel(self.nivel)
        else:   
            for i in range(0,len(arbol.niveles_l[self.nivel]),2): 
                n1 = arbol.niveles_l[self.nivel][i] 
                n2 = arbol.niveles_l[self.nivel][i+1]
                p = n1.padre
                p.ind_anot.set(x = p.ind_anot.get_position()[0] + 3)
                if(n1.ind == len(n1.arr)): 
                    p.arr[p.ind] = n2.arr[n2.ind]
                    p.arreglo.elms[p.ind].anot.set(text = p.arr[p.ind])
                    n2.ind = n2.ind + 1
                    n2.ind_anot.set(x = n2.ind_anot.get_position()[0] + 3)
                    p.ind = p.ind + 1
                    continue 
                if(n2.ind == len(n2.arr)): 
                    p.arr[p.ind] = n1.arr[n1.ind]
                    p.arreglo.elms[p.ind].anot.set(text = p.arr[p.ind])
                    n1.ind = n1.ind + 1
                    n1.ind_anot.set(x = n1.ind_anot.get_position()[0] + 3)
                    p.ind = p.ind + 1 
                    continue 
                if(n1.arr[n1.ind] <= n2.arr[n2.ind]): 
                    p.arr[p.ind] = n1.arr[n1.ind]
                    p.arreglo.elms[p.ind].anot.set(text = p.arr[p.ind])
                    n1.ind = n1.ind + 1
                    n1.ind_anot.set(x = n1.ind_anot.get_position()[0] + 3)
                    p.ind = p.ind + 1 
                else: 
                    p.arr[p.ind] = n2.arr[n2.ind]
                    p.arreglo.elms[p.ind].anot.set(text = p.arr[p.ind])
                    n2.ind = n2.ind + 1
                    n2.ind_anot.set(x = n2.ind_anot.get_position()[0] + 3)
                    p.ind = p.ind + 1

    def siguiente_paso(self):
        arbol = env.vars['arbol']
        if( len(arbol.raiz.arreglo.elms) < 2 ** arbol.niveles ): 
            self.abajo_arriba()
        else: 
            self.arriba_abajo()
            if(len(arbol.raiz.arreglo.elms) ==  2 ** (arbol.niveles - 1) ): 
                self.inicializar_ind_nivel(len(arbol.niveles_l)-1)
                self.nivel = arbol.niveles - 1
       
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
        dibujar_arbol() 
env = Env() 
env.vars['arbol'] = Arbol() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
