from cmath import atan
from glob import glob
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import FancyArrowPatch 
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
def ang_crr(p1,p2): 
    x1,y1 = p1 
    x2,y2 = p2 
    dx,dy = x2 - x1, y2 - y1 
    if(y2 >= y1): 
        if(x2 > x1): 
            #1
            return math.atan(dy/dx)
        elif(x2 == x1):
            return math.pi/2
        else: 
            #2
            return math.pi + math.atan(dy/dx)
    else: 
        if(x2 < x1): 
            #3 
            return math.pi + math.atan(dy/dx)  
        elif(x2 == x1):
            return (3/2)*math.pi 
        else: 
            #4 
            return 2*math.pi + math.atan(dy/dx)
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
#punto medio entre dos puntos pero con una separación de s, una fraccion de la linae(frac)
def punto_medio(x1,y1,x2,y2,s,fra): 
    dx = x1 - x2 
    dy = y1 - y2 
    ang = ang_crr((x1,y1),(x2,y2))
    x = math.sqrt((x1- x2)**2 + (y1 - y2)**2)*fra
    y = s 
    xp = x*math.cos(ang) - y*math.sin(ang)
    yp = x*math.sin(ang) + y*math.cos(ang)
    ##llegué a la conclusión que tienes que trasladarlo a el que tiene la menor x 
    xp = xp + x1
    yp = yp + y1
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
class Matriz: 
    celdas = None
    def __init__(self,n,m): 
        self.celdas = [[0 for j in range(0,m)] for i in range(0,n)] 
class Celda: 
    valor = None 
    rect = None
    anot = None
    #con el fin de calcular la solución 
    ant = -1 
class Etiquetas: 
    reng = None
    cols = None
    def __init__(self,n,m): 
        self.reng = [Etiq() for i in range(0,n)]
        self.cols = [Etiq() for j in range(0,m)]
class Etiq: 
    rect = None
    anot = None 

class Circulo: 
    img = None 
    pos = None   
    anot = None
    valor = None
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

def arb_dirigido(arb,inicial):
    g =dict() 
    for u,v in arb: 
        g[u] = [] 
        g[v] = []
    for u,v in arb: 
        g[u].append(v)
        g[v].append(u)
    print(g)
    cola = [inicial]
    arb_dir = [] 
    revisados = []
    while(cola): 
        v = cola[0]
        revisados.append(v)
        cola.pop(0)
        for u in g[v]: 
            if(u not in cola and u not in revisados): 
                arb_dir.append((u,v)) 
                cola.append(u)
    return arb_dir
def crear_aleatoria():  
    n = 5
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
    inicial = random.randint(0,len(verts)-1)
    arb = arb_dirigido(arb,inicial)
    print("el inicial es {}".format(inicial))
    ars_p = [] 
    for (u,v) in arb: 
        p = random.randint(1,50)
        ars_p.append((u,v,p))
    for u,x,y in verts: 
        for v in vecinos(mat,x,y,n): 
            if((v,u) in arb or (u,v) in arb): 
                continue 
            if(random.randint(0,10) < 5): 
                p = random.randint(-20,20)
                if(random.randint(0,1) == 1): 
                    ars_p.append((u,v,p))
                    arb.append((u,v))
                else:
                    ars_p.append((v,u,p))
                    arb.append((v,u))
    for (u,v,p) in ars_p: 
        agregar_arista(u,v,p) 
    env.vars['g'].max_x = env.vars['ax'].get_xlim()[1]
    env.vars['g'].min_y = env.vars['ax'].get_ylim()[0]
def agregar_vertice(v,x,y): 
    c = Circle((x,y),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black')
    cr = Circulo() 
    anot = env.vars['ax'].text(x,y,"$V_{{{}}}$".format(v), fontsize=9, ha='center', va='center') 
    env.vars['ax'].add_patch(c)
    cr.pos = [x,y] 
    cr.img = c 
    cr.anot = anot 
    env.vars['g'].pos_nodos[v] = cr
def agregar_arista(u,v,p):
        #si ya está, no la agregues 
        if(not(u in env.vars['g'].ady and v in env.vars['g'].ady[u])): 
            xu,yu = env.vars['g'].pos_nodos[u].img.get_center() 
            xv,yv = env.vars['g'].pos_nodos[v].img.get_center() 
            xu,yu = inter_points(env.vars['rad'],xu,yu,xv,yv)
            xv,yv = inter_points(env.vars['rad'],xv,yv,xu,yu)
            linea = FancyArrowPatch((xu,yu),(xv,yv),connectionstyle = "arc3, rad = 0",color = 'black') 
            linea.set_arrowstyle("fancy", head_length=5,head_width = 5)
            env.vars['ax'].add_patch(linea)
            xa,ya = punto_medio(xv,yv,xu,yu,0,0.7)
            c = Circle((xa,ya),radius = 0.5,color = 'white')
            env.vars['ax'].add_patch(c)
            env.vars['ax'].text(xa,ya,p,fontsize = 8,va = 'center',ha = 'center')
            #agregar a la grafica 
            n = Nodo()
            if u not in env.vars['g'].ady: 
                env.vars['g'].ady[u] = dict()
            if v not in env.vars['g'].ady: 
                env.vars['g'].ady[v] = dict()
            if v not in env.vars['g'].ady[u]: 
                env.vars['g'].ady[u][v] = n
            #de un lado 
            env.vars['g'].ady[u][v].arista = (u,v)
            env.vars['g'].ady[u][v].peso = p 
            env.vars['g'].ady[u][v].linea = linea 
    
class Ejecucion:   
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
    def siguiente_paso(self):
        print("siguiente")
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
    def crear_matriz(self):
        g = env.vars['g'] 
        n = len((g.pos_nodos))
        m = len((g.pos_nodos))
        env.vars['mat'] = Matriz(n,m)
    def poner_etiquetas(self):
        mat = env.vars['mat'] 
        n = len(mat.celdas)
        m = len(mat.celdas[0])
        et = Etiquetas(n,m)
        env.vars['etq'] = et
        x,y = env.vars['g'].max_x + 1,0
        w,h = 2,2
        for i in range(0,n):
            et.reng[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.reng[i].rect) 
            et.reng[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"$V_{{{}}}$".format(i),fontsize = 9,ha='center', va='center')  
            y = y - 2 
        x,y = env.vars['g'].max_x + 3,2
        for i in range(0,m):
            et.cols[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.cols[i].rect)  
            et.cols[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"{}".format(i),fontsize = 9,ha='center', va='center')  
            x = x + 2 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def dibujar_matriz(self):
            mat = env.vars['mat']
            x,y = env.vars['ax'].get_xlim()[1] + 3 ,0  
            for i in range(0,len(mat.celdas)):
                x = env.vars['ax'].get_xlim()[1] + 3 
                for j in range(0,len(mat.celdas[0])):
                    cel = Celda()
                    w,h = 2,2
                    cel.rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black')
                    env.vars['ax'].add_patch(cel.rect) 
                    cel.anot =  env.vars['ax'].text(x+w/2, y+h/2,"".format(i,j),fontsize = 9,ha='center', va='center') 
                    mat.celdas[i][j] = cel
                    x = x + 2
                y = y - 2
            env.vars['ax'].relim()
            env.vars['ax'].autoscale_view()


    def __init__(self): 
        crear_aleatoria() 
        self.n = len(env.vars['g'].pos_nodos.keys())
        self.config_imagen()
        self.config_teclas()
        self.crear_matriz() 
        self.dibujar_matriz() 
        self.poner_etiquetas() 

env = Env() 
env.vars['g'] = Grafica()
env.vars['mat'] = None 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
