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
def vecinos(mat,x,y,n):
    vec = [] 
    for i in range(1,n):
        if(x+i >= n or y +i >= n): 
            break 
        if(mat[x+i][y+i] >= 0): 
            vec.append(mat[x+i][y+i])
            break  
    for i in range(1,n):
        if(x-i < 0 or y-i< 0): 
            break 
        if(mat[x-i][y-i] >= 0): 
            vec.append(mat[x-i][y-i])
            break  
    for i in range(x+1,n): 
        if(mat[i][y] >= 0): 
            vec.append(mat[i][y])
            break 
    for i in range(x-1,-1,-1): 
        if(mat[i][y] >= 0): 
            vec.append(mat[i][y])
            break 
    for j in range(y+1,n): 
        if(mat[x][j] >= 0): 
            vec.append(mat[x][j])
            break 
    for j in range(y-1,-1,-1): 
        if(mat[x][j] >= 0): 
            vec.append(mat[x][j])
            break 
    return vec 
def crear_arbol(ars,n):
    union_f = Union_find(n)
    arbol = []
    for (u,v) in ars: 
        if(union_f.find(u) != union_f.find(v)): 
            union_f.unite(u,v) 
            arbol.append((u,v)) 
    return arbol 
class Grafica: 
    #donde termina la grafica 
    max_x = None 
    min_y = None
    #va de un entero a un diccionario con valor nodo 
    ady = None
    # pos_nodos : dict(Int,Circulo)
    pos_nodos = None
    def __init__(self): 
        self.ady = dict() 
        self.pos_nodos = dict() 
class Nodo: 
    arista = None
    linea = None
    #la anotacion en la linea 
    anot = None 
    peso = None 
    valor = None

class Circulo: 
    img = None 
    pos = None   
    anot = None
    valor = None
class Pila: 
    nodos = None
    def __init__(self): 
        self.nodos = [] 
class Nodo_pila: 
    rect = None 
    anot = None  

class Env:
    vars = dict()  

class Union_find: 
    def __init__(self,n):
        self.parent = [i for i in range (0,n)]
        self.size = [1 for i in range (0,n) ]
    
    def unite(self,i,j): 
        pi = self.find(i)
        pj = self.find(j)
        if(pi == pj):
            return 
        if(self.size[pi] < self.size[pj]): 
            self.parent[pi] = pj
            self.size[pj] = self.size[pj] + self.size[pi]
        else: 
            self.parent[pj] = pi
            self.size[pi] = self.size[pi] + self.size[pj]
    
    def find(self,i): 
        while(self.parent[i] != i): 
            i = self.parent[i]
        return i
def crear_aleatoria():  
    n = 6
    mat = [[-1 for i in range(0,n)] for j in range(0,n)]
    verts = [] 
    x = 0 
    y = 0 
    k = 0
    for i in range(0,n): 
        x = 0 
        for j in range(0,n): 
            if(random.randint(0,1) == 1): 
                mat[i][j] = k
                verts.append((k,i,j)) 
                agregar_vertice(k,x,y)
                k = k + 1 
            x = x + 5*env.vars['rad']
        y = y - 5*env.vars['rad']
    env.vars['ax'].relim()
    env.vars['ax'].autoscale_view()
    ars = []
    for (v,x,y) in verts:  
        for u in vecinos(mat,x,y,n): 
            ars.append((v,u))
    arb = crear_arbol(ars,len(verts))
    ars_p = [] 
    for (u,v) in arb: 
        p = random.randint(1,50)
        ars_p.append((u,v,p))
    for v,x,y in verts: 
        for u in vecinos(mat,x,y,n): 
            if(random.randint(0,1) % 2 == 1): 
                p = random.randint(1,50)
                ars_p.append((v,u,p))
    for (u,v,p) in ars_p: 
        agregar_arista(v,u,p) 
    env.vars['g'].max_x = env.vars['ax'].get_xlim()[1]
    env.vars['g'].min_y = env.vars['ax'].get_ylim()[0]
def agregar_vertice(v,x,y): 
    c = Circle((x,y),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black')
    cr = Circulo() 
    anot = env.vars['ax'].annotate("{}".format(v), (x,y),color='black', weight='bold', fontsize=10, ha='center', va='center') 
    env.vars['ax'].add_patch(c)
    cr.pos = [x,y] 
    cr.img = c 
    cr.anot = anot 
    env.vars['g'].pos_nodos[v] = cr
def agregar_arista(u,v,p):
        #si ya está, no la agregues 
        if( not ((v in env.vars['g'].ady and u in env.vars['g'].ady[v]) or (u in env.vars['g'].ady and v in env.vars['g'].ady[u]))): 
            xu,yu = env.vars['g'].pos_nodos[u].img.get_center() 
            xv,yv = env.vars['g'].pos_nodos[v].img.get_center() 
            xu,yu = inter_points(env.vars['rad'],xu,yu,xv,yv)
            xv,yv = inter_points(env.vars['rad'],xv,yv,xu,yu)
            linea = PathPatch(Path([(xu,yu),(xv,yv)]), facecolor='none', edgecolor='black')
            env.vars['ax'].add_patch(linea)
            #agregar a la grafica 
            n = Nodo()
            if u not in env.vars['g'].ady: 
                env.vars['g'].ady[u] = dict()
            if v not in env.vars['g'].ady[u]: 
                env.vars['g'].ady[u][v] = n

            if v not in env.vars['g'].ady: 
                env.vars['g'].ady[v] = dict()
            if u not in env.vars['g'].ady[v]: 
                env.vars['g'].ady[v][u] = n
            #de un lado 
            env.vars['g'].ady[u][v].arista = (u,v)
            env.vars['g'].ady[u][v].peso = p 
            env.vars['g'].ady[u][v].linea = linea 
            #para el otro 
            env.vars['g'].ady[v][u].arista = (u,v)
            env.vars['g'].ady[v][u].peso = p
            env.vars['g'].ady[v][u].linea = linea 
            #agregar el widget 
    
class Ejecucion:  
    alcanzados = None 
    primero = None 
    pila = None
    expandidos = None
    pila_img = None
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
       
    def dibujar_pila(self): 
        g = env.vars['g']
        x = g.max_x 
        y = g.min_y 
        for n in self.pila_img.nodos:
            n.rect.set(visible = False)
            n.anot.set(visible = False) 
        r = env.vars['rad']
        for i in self.pila: 
            n = Nodo_pila()
            n.rect = Rectangle((x,y),width = 2*r,height = 2*r,facecolor = 'white',edgecolor = 'black') 
            env.vars['ax'].add_patch(n.rect)
            n.anot = env.vars['ax'].text(x + r, y + r,i,fontsize = 9,ha='center', va='center') 
            self.pila_img.nodos.append(n)
            y = y + 2*env.vars['rad']
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def siguiente_paso(self):
        g = env.vars['g']
        t,exp = self.pila[-1],self.expandidos[-1]
        if(exp): 
            g.pos_nodos[t].img.set(facecolor = 'black')
            g.pos_nodos[t].anot.set(color = 'white')
            self.alcanzados.append(t)
            self.pila.pop()
            self.expandidos.pop() 
        else: 
            self.expandidos[-1] = True 
            for i in g.ady[t].keys(): 
                #si no estan en la pila 
                if i not in self.pila and i not in self.alcanzados: 
                    self.pila.append(i)
                    self.expandidos.append(False)
                    g.pos_nodos[i].img.set(facecolor = 'gray')
        self.dibujar_pila() 
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
    def escoger_primero(self): 
        self.primero = random.randint(0,self.n-1)
        g = env.vars['g']
        g.pos_nodos[self.primero].img.set(facecolor = 'gray')
        self.pila = [self.primero]
        self.expandidos = [False]
    def __init__(self): 
        crear_aleatoria() 
        self.n = len(env.vars['g'].pos_nodos.keys())
        self.alcanzados = []
        self.escoger_primero()
        self.config_imagen()
        self.pila_img = Pila() 
        self.dibujar_pila() 
        self.config_teclas()

env = Env() 
env.vars['g'] = Grafica()
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
