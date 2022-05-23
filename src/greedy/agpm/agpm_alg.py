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
    #va de un entero a un diccionario con valor nodo 
    ady = None
    #es un diccionario con hacia un circulo 
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
    anot_dist = None 


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
def crear_aleatoria(g_k):  
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
                cr = Circulo() 
                cr.pos = [x,y] 
                env.vars[g_k].pos_nodos[k] = cr
                k = k + 1 
            x = x + 5*env.vars['rad']
        y = y - 5*env.vars['rad']
    ars = []
    for (v,x,y) in verts:  
        for u in vecinos(mat,x,y,n): 
            ars.append((v,u))
    arb = crear_arbol(ars,len(verts))
    ars_p = [] 
    r = random.randint(1,5)
    for (u,v) in arb: 
        #p = random.randint(1,50)
        p1 = env.vars[g_k].pos_nodos[u].pos
        p2 = env.vars[g_k].pos_nodos[v].pos
        ars_p.append((u,v,dist(p1,p2,r)))
    for v,x,y in verts: 
        for u in vecinos(mat,x,y,n): 
            if(random.randint(0,1) % 2 == 1): 
                #p = random.randint(1,50)
                p1 = env.vars[g_k].pos_nodos[u].pos
                p2 = env.vars[g_k].pos_nodos[v].pos
                ars_p.append((v,u,dist(p1,p2,r)))
    for (u,v,p) in ars_p: 
        agregar_arista(v,u,p,g_k) 
def dist(p1,p2,m): 
    x1,y1 = p1
    x2,y2 = p2 
    return math.floor(m*math.sqrt((x1 - x2)** 2 + (y1 - y2)**2))

def dibujar_vertices(g_k,ax_k):
    g = env.vars[g_k]
    for v in g.pos_nodos.keys(): 
        x,y = g.pos_nodos[v].pos
        c = Circle((x,y),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black')
        anot = env.vars[ax_k].annotate("{}".format(v), (x,y),color='black', weight='bold', fontsize=10, ha='center', va='center') 
        env.vars[ax_k].add_patch(c)
        g.pos_nodos[v].img = c 
        g.pos_nodos[v].anot = anot 
    env.vars[ax_k].relim()
    env.vars[ax_k].autoscale_view()

def dibujar_aristas(g_k,ax_k): 
    g = env.vars[g_k]
    for u,v_u in g.ady.items(): 
        for v,n in v_u.items(): 
            if(n.linea == None and n.anot == None ): 
                xu,yu = env.vars[g_k].pos_nodos[u].img.get_center() 
                xv,yv = env.vars[g_k].pos_nodos[v].img.get_center() 
                xu,yu = inter_points(env.vars['rad'],xu,yu,xv,yv)
                xv,yv = inter_points(env.vars['rad'],xv,yv,xu,yu)
                linea = PathPatch(Path([(xu,yu),(xv,yv)]), facecolor='none', edgecolor='black')
                env.vars[ax_k].add_patch(linea)
                xm,ym = punto_medio(xu,yu,xv,yv,0.5,0.2)
                anot = env.vars[ax_k].annotate("{}".format(n.peso), (xm,ym),color='black', weight='bold', fontsize=7, ha='center', va='center') 
                n.linea = linea 
                n.anot = anot 
def dibujar_grafica(g_k,ax_k):
    g = env.vars[g_k] 
    ax = env.vars[ax_k]
    dibujar_vertices(g_k,ax_k) 
    dibujar_aristas(g_k,ax_k)

def dibujar_arista(u,v,ax_k,g_k):
    n = env.vars[g_k].ady[u][v]
    xu,yu = env.vars[g_k].pos_nodos[u].img.get_center() 
    xv,yv = env.vars[g_k].pos_nodos[v].img.get_center() 
    xu,yu = inter_points(env.vars['rad'],xu,yu,xv,yv)
    xv,yv = inter_points(env.vars['rad'],xv,yv,xu,yu)
    linea = PathPatch(Path([(xu,yu),(xv,yv)]), facecolor='none', edgecolor='black')
    env.vars[ax_k].add_patch(linea)
    xm,ym = punto_medio(xu,yu,xv,yv,0.5,0.2)
    anot = env.vars[ax_k].annotate("{}".format(n.peso), (xm,ym),color='black', weight='bold', fontsize=7, ha='center', va='center') 
    n.linea = linea 
    n.anot = anot 
def agregar_arista(u,v,p,g_k):
        #si ya está, no la agregues 
        agregada = False
        if( not ((v in env.vars[g_k].ady and u in env.vars[g_k].ady[v]) or (u in env.vars[g_k].ady and v in env.vars[g_k].ady[u]))): 
           #agregar a la grafica 
            n = Nodo()
            if u not in env.vars[g_k].ady: 
                env.vars[g_k].ady[u] = dict()
            if v not in env.vars[g_k].ady[u]: 
                env.vars[g_k].ady[u][v] = n

            if v not in env.vars[g_k].ady: 
                env.vars[g_k].ady[v] = dict()
            if u not in env.vars[g_k].ady[v]: 
                env.vars[g_k].ady[v][u] = n
            #de un lado 
            env.vars[g_k].ady[u][v].arista = (u,v)
            env.vars[g_k].ady[u][v].peso = p 
            #para el otro 
            env.vars[g_k].ady[v][u].arista = (u,v)
            env.vars[g_k].ady[v][u].peso = p
            #agregar el widget
            agregada = True 
        return agregada 
def clonar_grafica(g):
    gc = Grafica() 
    for v,c in g.pos_nodos.items(): 
        gc.pos_nodos[v] = Circulo() 
        gc.pos_nodos[v].valor = c.valor
        gc.pos_nodos[v].pos = c.pos[0],c.pos[1] 
    for u,vec_u in g.ady.items(): 
        for v,n in vec_u.items():
            if u not in gc.ady: 
                gc.ady[u] = dict()
            if v not in gc.ady: 
                gc.ady[v] = dict() 
            if(v not in gc.ady[u]): 
                gc.ady[u][v] = Nodo()  
                gc.ady[u][v].peso = g.ady[u][v].peso  
                gc.ady[v][u] = gc.ady[u][v]
    return gc
class Kruskal:  
    ind_ar = 0 
    n = None
    array_col = None 
    union_f = None 
    ar_ord = None
    ax_anot = None 
    anot = None
    peso = 0 
    ind_nods = 0 
    extremos = [] 
    def config_imagen(self): 
        env.vars[self.ax_k].set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas()
        self.zoom_mas() 
    def actualizar_anot(self,a,esc):
        (u,v,p) = a  
        if(esc): 
            self.peso = self.peso + p 
            text = "-La arista ({},{}) no crea un ciclo. Se agrega al arbol \n".format(u,v)
            text = text + "-el peso del arbol generador de peso minimo es {}\n".format(self.peso)
        else: 
            text = "-La arista ({},{}) crea un ciclo. Se ignora\n".format(u,v) 
            text = text + "-El peso del arbol permanece como {}".format(self.peso)
        self.anot.set(text = text)
    def siguiente_paso(self):
        g = env.vars[self.g_k]
        if(self.ind_ar == len(self.ar_ord)):
            return
        (u,v,peso) = self.ar_ord[self.ind_ar]
        escogida = False
        if(self.union_f.find(u) !=  self.union_f.find(v)):
            #colorea a todos con el color del grupo mas grande 
            escogida = True
            pu = self.union_f.find(u)
            pv = self.union_f.find(v)
            #el nuevo padre
            self.union_f.unite(pu,pv)
            g.pos_nodos[u].img.set(facecolor = '#DAF7A6')
            g.pos_nodos[v].img.set(facecolor = '#DAF7A6')
            g.ady[u][v].linea.set(color = '#17A589')     
            g.ady[u][v].linea.set(linewidth = 3)
        else: 
            g.ady[u][v].linea.set(linestyle = '--')
            g.ady[u][v].linea.set(color = 'lightgray')
        self.ind_ar = self.ind_ar + 1
        self.actualizar_anot((u,v,peso),escogida) 
    @out1.capture()
    def teclas_handler(self,event): 
        if(event.key == 'n'): 
            self.siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    def zoom_mas(self): 
        x,y = env.vars[self.fig_k].get_size_inches()
        env.vars[self.fig_k].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars[self.fig_k].get_size_inches()
        env.vars[self.fig_k].set_size_inches(x-1,y-1)
    def config_teclas(self): 
        env.vars[self.cid_t_k] = env.vars[self.fig_k].canvas.mpl_connect('key_press_event', self.teclas_handler)
 
    def obtener_aristas_ord(self): 
        ars = [] 
        ars_sp = [] 
        for i in env.vars[self.g_k].ady.keys(): 
            for j in env.vars[self.g_k].ady[i].keys(): 
                if((i,j) not in ars_sp): 
                    ars_sp.append((i,j))
                    ars_sp.append((j,i))
                    ars.append((i,j,env.vars[self.g_k].ady[i][j].peso))
        ars.sort(key = lambda x : x[2])
        return ars
    def init_anot(self): 
        text= "Escoge entrada de usuario o generar grafica aleatoria con los botones bajo la imagen"
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def handler_al(self,event): 
        texto = "Presiona la imagen. A partir de aqui, cada vez que presiones n se ejecutara \n" 
        texto += "el siguiente paso."
        self.anot.set(text = texto)
        self.botones.children = [] 
        self.array_col = []
        crear_aleatoria('g1')
        dibujar_grafica(self.g_k,self.ax_k) 
        self.ar_ord = self.obtener_aristas_ord() 
        self.n = len(env.vars[self.g_k].pos_nodos.keys())
        self.union_f = Union_find(self.n)
        env.vars['g2'] = clonar_grafica(env.vars['g1'])
        env.vars['fig2'],env.vars['ax2'] = plt.subplots()
        env.vars['e2'] = Prim('g2','ax2','fig2','cid_t2',True)
        color_map = plt.get_cmap('tab20c', 1000)
    @out1.capture() 
    def poner_nodo(self,event):
        if(event.inaxes== self.ax_anot): 
            return 
        if(event.xdata == None or event.ydata == None): 
            return 
        x,y = event.xdata,event.ydata
        if(x < 1 or y < 1 or y > 24 or x > 24): 
            return 
        c = Circle((x , y),radius = 1, facecolor = 'white',edgecolor = 'black')
        env.vars['ax1'].add_patch(c)
        circ = Circulo() 
        circ.img = c 
        circ.pos = [x,y]
        circ.anot = env.vars['ax1'].text(x,y,self.ind_nods,va='center',ha='center')
        circ.valor = self.ind_nods
        env.vars['g1'].pos_nodos[self.ind_nods] = circ  
        self.ind_nods = self.ind_nods + 1 
    @out1.capture() 
    def poner_aristas(self,event): 
        if(event.inaxes== self.ax_anot): 
            return 
        if(event.xdata == None or event.ydata == None): 
            return
        x,y = event.xdata,event.ydata
        for i,c in env.vars['g1'].pos_nodos.items():
            xc,yc = c.pos 
            if((x-xc)**2 + (y-yc)**2 <= 1 ):
                if( len(self.extremos) == 1):
                    if(self.extremos[0] != i):
                        p1 = env.vars['g1'].pos_nodos[self.extremos[0]].pos 
                        p2 = xc,yc 
                        ag = agregar_arista(self.extremos[0],i,dist(p1,p2,5),self.g_k)
                        if(ag): 
                            dibujar_arista(self.extremos[0],i,self.ax_k,self.g_k)
                        self.extremos = [] 
                    else: 
                        break 
                else: 
                    self.extremos.append(i)
                break
    def conexa(self): 
        cola = [0] 
        revisados = []
        while(cola): 
            x = cola[0]
            cola.pop(0) 
            revisados.append(x)
            #si no tiene hijos pues solo haz continue 
            if(x not in env.vars[self.g_k].ady): 
                continue 
            for y in env.vars[self.g_k].ady[x].keys():
                if(y not in revisados and y not in cola):  
                    cola.append(y)
        return len(revisados) == len(env.vars[self.g_k].pos_nodos)
    def listo_aristas_handler(self,event): 
        if(self.conexa()): 
            self.n = len(env.vars['g1'].pos_nodos.keys())
            text = "Presiona la imagen.\n"
            text += "A partir de aqui, cada vez que presiones n se ejecutara \n" 
            text += "el siguiente paso del algoritmo de Kruskal."
            self.anot.set(text = text)
            env.vars['fig1'].canvas.mpl_disconnect(env.vars['cid_c'])
            self.botones.children = [] 
            self.n = len(env.vars[self.g_k].pos_nodos.keys())
            self.union_f = Union_find(self.n)
            self.ar_ord = self.obtener_aristas_ord()
            #redibujar la grafica
            dibujar_grafica(self.g_k,self.ax_k)
            #poner la figura de prim  
            env.vars['g2'] = clonar_grafica(env.vars['g1'])
            env.vars['fig2'],env.vars['ax2'] = plt.subplots()
            env.vars['e2'] = Prim('g2','ax2','fig2','cid_t2',False)

        else: 
            text = "La grafica tiene que ser conexa." 
            self.anot.set(text = text)
    def listo_nodos_handler(self,event): 
        if(len(env.vars['g1'].pos_nodos) < 2):
            texto = "Debe haber al menos un par de nodos."
            self.anot.set(text = texto) 
        else: 
            texto = "Agrega las aristas presionando el par de nodos que quieres unir.\n"
            texto += "Una vez listo presiona el boton bajo la imagen"
            self.anot.set(text = texto)
            env.vars['fig1'].canvas.mpl_disconnect(env.vars['cid_c'])
            env.vars['cid_c'] = env.vars['fig1'].canvas.mpl_connect('button_press_event', self.poner_aristas)
            boton_listo =  widgets.Button(description="Guardar aristas")
            boton_listo.on_click(self.listo_aristas_handler)
            self.botones.children = [boton_listo] 
            self.rect_nodos.set(visible = False)
    def handler_us(self,event): 
        texto = "Presiona los lugares dentro el cuadro donde quieres los nodos. \n" 
        texto += "Una vez listo presiona el boton bajo la imagen"
        self.anot.set(text = texto)
        env.vars['cid_c'] = env.vars['fig1'].canvas.mpl_connect('button_press_event', self.poner_nodo)
        #hacer de 10x10 el ax
        self.rect_nodos = Rectangle((0,0),width = 25,height = 25,facecolor = 'white',edgecolor = 'black')
        env.vars['ax1'].add_patch(self.rect_nodos)
        env.vars['ax1'].relim()
        env.vars['ax1'].autoscale_view()
        boton_listo =  widgets.Button(description="Guardar nodos")
        boton_listo.on_click(self.listo_nodos_handler)
        self.botones.children = [boton_listo] 
    def agregar_botones(self): 
        boton_us = widgets.Button(description="Entrada de usuario")
        boton_al = widgets.Button(description="Grafica aleatoria")
        boton_al.on_click(self.handler_al)
        boton_us.on_click(self.handler_us)
        self.botones = widgets.HBox([boton_us,boton_al])
        display(self.botones)
    def __init__(self,g_k,ax_k,fig_k,cid_t_k): 
        self.g_k = g_k 
        self.ax_k = ax_k 
        self.fig_k = fig_k 
        self.cid_t_k = cid_t_k 
        #para el número de colores 
        self.config_imagen()
        self.config_teclas()
        self.init_anot()
        self.agregar_botones()
class Prim:  
    ind_ar = 0 
    n = None
    cost = dict() 
    padre= dict() 
    heap = [] 
    S = [] 
    inicial = None
    ax_anot = None 
    anot = None
    peso = 0 
    aleat = False
    def config_imagen(self): 
        env.vars[self.ax_k].set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        #el cuadrado se añade cuando sea una gráfica ingresada por el usuario 
        if(not self.aleat): 
            env.vars[self.ax_k].add_patch(Rectangle((0,0),width = 25,height = 25,visible = False))
            env.vars[self.ax_k].relim()
            env.vars[self.ax_k].autoscale_view()
        #hacer la figura más grande
        self.zoom_mas()
        self.zoom_mas() 
    def actualizar_anot(self,u):
        self.heap.sort(key = lambda x :  x[1])
        if(self.heap): 
            heap = "{"
            for i in range(0,len(self.heap)-1):
                (v,_) = self.heap[i] 
                heap = heap + "{},".format(v)
            heap += "{}".format(self.heap[len(self.heap)-1][0])
            heap += "}"
        else: 
            heap = "{}"
        text = "-Se agrega el nodo {} al conjunto $S$ \n".format(u)
        text = text + "-El heap contiene los nodos: {}\n".format(heap)
        text = text + "-El peso es ahora {} \n".format(self.peso)
        self.anot.set(text = text)
        return  
    def siguiente_paso(self):
        if(not self.heap): 
            return 
        g = env.vars[self.g_k]
        self.heap.sort(key = lambda x :  x[1])
        (u,c) = self.heap[0] 
        self.heap.pop(0)
        g.pos_nodos[u].img.set(facecolor = '#F4D03F') 
        self.S.append(u) 
        self.peso = self.peso + c
        for (v,n) in g.ady[u].items(): 
            if(v not in self.S): 
                if(v not in self.cost): 
                    self.cost[v] = n.peso
                    self.heap.append((v, n.peso)) 
                    self.padre[v] = u
                if(n.peso < self.cost[v]): 
                    self.heap.remove((v,self.cost[v]))
                    g.ady[self.padre[v]][v].linea.set(color = 'black')
                    g.ady[self.padre[v]][v].linea.set(linewidth = 1)
                    self.heap.append((v, n.peso))
                    self.cost[v] = n.peso
                    self.padre[v] = u
                g.ady[self.padre[v]][v].linea.set(color = '#F5B041')
                g.ady[self.padre[v]][v].linea.set(linewidth = 3)
        self.actualizar_anot(u) 
    @out1.capture()
    def teclas_handler(self,event): 
        if(event.key == 'n'): 
            self.siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    def zoom_mas(self): 
        x,y = env.vars[self.fig_k].get_size_inches()
        env.vars[self.fig_k].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars[self.fig_k].get_size_inches()
        env.vars[self.fig_k].set_size_inches(x-1,y-1)
    def config_teclas(self): 
        env.vars[self.cid_t_k] = env.vars[self.fig_k].canvas.mpl_connect('key_press_event', self.teclas_handler)
    
    def escoger_inicial(self): 
        self.inicial = random.randint(0,self.n-1)
        self.heap = [(self.inicial,0)]
    def init_anot(self): 
        text = "Presiona la imagen.\n"
        text += "A partir de aqui, cada vez que presiones n se ejecutara\n"
        text += "el siguiente paso del algoritmo de Prim."
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def __init__(self,g_k,ax_k,fig_k,cid_t_k,aleat):
        self.g_k = g_k
        self.ax_k = ax_k 
        self.fig_k = fig_k 
        self.cid_t_k = cid_t_k 
        self.aleat = aleat
        dibujar_grafica(self.g_k,ax_k) 
        self.array_col = []
        self.n = len(env.vars[self.g_k].pos_nodos.keys())
        self.escoger_inicial()
        self.config_imagen()
        self.config_teclas()
        self.init_anot() 



env = Env() 
env.vars['g1'] = Grafica()
env.vars['g2'] = Grafica()
env.vars['fig1'],env.vars['ax1'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t1'] = None
env.vars['cid_t2'] = None
env.vars['cid_c'] = None
env.vars['e1'] = Kruskal('g1','ax1','fig1','cid_t2') 
#env.vars['g2'] = clonar_grafica(env.vars['g1'])
#env.vars['fig2'],env.vars['ax2'] = plt.subplots()
#env.vars['e2'] = Prim('g2','ax2','fig2','cid_t2')
