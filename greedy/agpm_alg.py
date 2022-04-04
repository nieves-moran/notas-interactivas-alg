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

import math 
%matplotlib nbagg
out1 = widgets.Output()
display(out1)
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
#punto medio entre dos puntos pero con una separación de s 
def punto_medio(x1,y1,x2,y2,s): 
    dx = x1 - x2 
    dy = y1 - y2 
    ang = (math.pi/2 if dy > 0 else (3*math.pi)/2) if dx == 0 else math.atan(dy/dx)
    ang = ang + 2* math.pi if ang < 0 else ang
    x = (math.sqrt((x1- x2)**2 + (y1 - y2)**2))/2
    y = s 
    xp = x*math.cos(ang) - y*math.sin(ang)
    yp = x*math.sin(ang) + y*math.cos(ang)
    ##llegué a la conclusión que tienes que trasladarlo a el que tiene la menor x 
    xp = xp + (x1 if x1 < x2 else x2) 
    yp = yp + (y1 if x1 < x2 else y2 )
    return (xp,yp)
class Anot_grupos: 
    renglones = None
    def __init__(self): 
        self.renglones = [] 
class Renglon: 
    cuadro_color = None 
    anotacion = None 
class Grafica: 
    #va de un entero a un diccionario con valor nodo 
    ady = None
    #es un diccionario con nodo y un par 
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

class Envir:
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
#Todo el código va a estar en una clase, esto porque 
#si lo divido en varias clases no se puede realizar la conexión con el mouse 
class AGPM: 
    ax = None 
    fig = None 
    g = None 
    cid = None 
    box = None
    rad = 1
    ind = 0
    #va a ser el máximo x de la gráfica 
    max_x_g = float('-inf')
    max_y_g = float('-inf')
    def __init__(self): 
        self.config_imagen() 
        self.config_botones()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick_pos_vert)
        self.g = Grafica()
    @out1.capture()
    def onclick_pos_vert(self,event): 
        #poner los vertices 
        c = Circle((event.xdata,event.ydata),radius = self.rad,facecolor = 'white',edgecolor = 'black')
        self.max_x_g = max(self.max_x_g, event.xdata + self.rad)
        self.max_y_g = max(self.max_y_g, event.ydata + self.rad)
        anot = self.ax.annotate("{}".format(self.ind), (event.xdata,event.ydata),color='black', weight='bold', fontsize=10, ha='center', va='center') 
        self.ax.add_patch(c)
        cr = Circulo() 
        cr.pos = [event.xdata,event.ydata] 
        cr.img = c 
        self.g.pos_nodos[self.ind] = cr
        self.ind = self.ind + 1
        self.ax.relim()
        self.ax.autoscale_view()  
    def config_imagen(self): 
        self.fig,self.ax =  plt.subplots()  
        plt.gca().set_aspect('equal', adjustable='box')
        #poner 4 puntos en donde quieres 
        c = Circle((20,20),radius = 1, visible = False)
        self.ax.add_patch(c)
        c = Circle((0,0),radius = 1, visible = False)
        self.ax.add_patch(c)
        self.ax.relim()
        self.ax.autoscale_view() 
        plt.axis('off')
    def boton_listo_handler_vert(self,event): 
        #pasar al siguiente estado 
        self.fig.canvas.mpl_disconnect(self.cid) 
        self.config_obtener_aristas()
    def config_botones(self): 
        boton_listo = widgets.Button(description='listo')
        boton_listo.on_click(self.boton_listo_handler_vert)  
        self.box = widgets.VBox([boton_listo])
        display(self.box)

##-------------------funciones de la parte para obtener aristas-----------------------------
    #elegidos para formar arista 
    extremos = [] 
    def config_obtener_aristas(self):
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick_aristas)
        self.config_botones_aristas()
    #salida 
    def boton_listo_handler_arist(self,event): 
        #pasar al siguiente que es escoger un inicial 
        self.fig.canvas.mpl_disconnect(self.cid) 
        self.config_ejecucion()
    def config_botones_aristas(self): 
        boton_listo = widgets.Button(description='listo')
        boton_listo.on_click(self.boton_listo_handler_arist)  
        self.box.children = [boton_listo]
    @out1.capture()
    def onclick_aristas(self,event): 
        for i,cir in self.g.pos_nodos.items(): 
            x,y = cir.pos
            r = cir.img.get_radius()
            if(math.sqrt((x - event.xdata)**2) <= r and math.sqrt((y - event.ydata)**2) <= r ): 
                cir.img.set(facecolor = 'red')
                if (i not in self.extremos): 
                    self.extremos.append(i)
                    if(len(self.extremos) == 2): 
                        self.agregar_arista(self.extremos[0],self.extremos[1])
                else:
                    self.extremos.remove(i)
                    cir.img.set(facecolor = 'white')

    def esc_peso_handler(self,change):
        u,v = eval(change.owner.description) 
        self.g.ady[u][v].anot.set(text = "{}".format(change.new))
        self.g.ady[u][v].peso = change.new 
    def agregar_widget_peso(self,u,v): 
        ch = list(self.box.children)
        esc_peso = widgets.BoundedIntText(value=10,min=0,max=100,step=1,description='({},{})'.format(u,v),disabled=False)
        esc_peso.observe(self.esc_peso_handler, names='value')
        ch.append(esc_peso)
        self.box.children = tuple(ch)
    def agregar_arista(self,u,v):
        #si ya está, no la agregues 
        if( not ((v in self.g.ady and u in self.g.ady[v]) or (u in self.g.ady and v in self.g.ady[u]))): 
            xu,yu = self.g.pos_nodos[u].img.get_center() 
            xv,yv = self.g.pos_nodos[v].img.get_center() 
            linea = PathPatch(Path([inter_points(self.rad,xu,yu,xv,yv),inter_points(self.rad,xv,yv,xu,yu)]), facecolor='none', edgecolor='black')
            self.ax.add_patch(linea)
            xm,ym = punto_medio(xu,yu,xv,yv,0.5)
            anot = self.ax.annotate("10", (xm,ym),color='black', weight='bold', fontsize=10, ha='center', va='center') 
            #agregar a la grafica 
            n = Nodo()
            if u not in self.g.ady: 
                self.g.ady[u] = dict()
            if v not in self.g.ady[u]: 
                self.g.ady[u][v] = n

            if v not in self.g.ady: 
                self.g.ady[v] = dict()
            if u not in self.g.ady[v]: 
                self.g.ady[v][u] = n
            #de un lado 
            self.g.ady[u][v].arista = (u,v)
            self.g.ady[u][v].peso = 10
            self.g.ady[u][v].linea = linea 
            self.g.ady[u][v].anot = anot
            #para el otro 
            self.g.ady[v][u].arista = (u,v)
            self.g.ady[v][u].peso = 10 
            self.g.ady[v][u].linea = linea 
            self.g.ady[v][u].anot = anot
            #agregar el widget 
            self.agregar_widget_peso(u,v)
        for i in self.extremos: 
            self.g.pos_nodos[i].img.set(facecolor = 'white')
        self.extremos = []
#--------------------------------------------ejecucion del algoritmo -------------------------
    #indice de la arista 
    ind_ar = 0 
    ar_ord = None 
    union_f = None
    array_col = None 
    color_map = None
    anotacion_g = None 
    def config_boton_listo_ej(self): 
        boton_listo = widgets.Button(description='siguiente')
        boton_listo.on_click(self.boton_listo_handler_ej)  
        self.box.children = [boton_listo]
    def obtener_aristas_ord(self): 
        ars = [] 
        ars_sp = [] 
        for i in self.g.ady.keys(): 
            for j in self.g.ady[i].keys(): 
                if((i,j) not in ars_sp): 
                    ars_sp.append((i,j))
                    ars_sp.append((j,i))
                    ars.append((i,j,self.g.ady[i][j].peso))
        ars.sort(key = lambda x : x[2])
        return ars
    def colorear_vert(self): 
        for i in range(0,self.ind): 
            vert = self.g.pos_nodos[i]
            vert.img.set(facecolor = self.array_col[i])
    #entrada 
    def config_ejecucion(self): 
        self.config_boton_listo_ej()
        self.union_f = Union_find(self.ind)
        self.ar_ord = self.obtener_aristas_ord()
        self.color_map = plt.get_cmap('tab20c', 1000)
        #para el número de colores 
        frac = 1/self.ind
        self.array_col = [self.color_map((i+1)*frac) for i in range(0,self.ind)]
        self.anotacion_g  = Anot_grupos()
        self.colorear_vert()
    def limpiar_anotacion_grupos(self): 
        for r in self.anotacion_g.renglones: 
            r.cuadro_color.set(visible = False)
            r.anotacion.set(visible = False) 
        self.anotacion_g.renglones = []
    def actualiza_anot_grupos(self): 
        grupos = dict() 
        #esta en self.max_x_g 
        x = self.max_x_g + self.rad 
        y = self.max_y_g 
        self.limpiar_anotacion_grupos() 
        #crear los grupos de colores 
        for i in range(0,len(self.g.pos_nodos)):
            if(self.union_f.find(i) not in grupos ): 
                grupos[self.union_f.find(i)] = [] 
            grupos[self.union_f.find(i)].append(i)
        for j,g in grupos.items(): 
            r = Rectangle((x,y),width = self.rad,height = 1,facecolor = self.array_col[j],edgecolor = 'black') 
            self.ax.add_patch(r)
            ren = Renglon() 
            ren.cuadro_color = r
            ren.anotacion = self.ax.text(x +3*self.rad,y,"{}".format(g))
            self.anotacion_g.renglones.append( ren)
            y = y - 2*self.rad  
    def boton_listo_handler_ej(self,event): 
        if(self.ind_ar == len(self.ar_ord)):
            return
        (u,v,p) = self.ar_ord[self.ind_ar]
        if(self.union_f.find(u) !=  self.union_f.find(v)):
            #colorea a todos con el color del grupo mas grande 
            pu = self.union_f.find(u)
            pv = self.union_f.find(v)
            #el nuevo padre
            p = pu
            if(self.union_f.size[pu] < self.union_f.size[pv]): 
                p = pv
            self.union_f.unite(u,v)
            for i in range(0,self.ind): 
                if(self.union_f.find(i) == p): 
                    self.g.pos_nodos[i].img.set(facecolor = self.array_col[p])
            self.g.ady[u][v].linea.set(linewidth = 3)
        else: 
            self.g.ady[u][v].linea.set(linestyle = '--')
            self.g.ady[u][v].anot.set(visible = False)
            self.g.ady[u][v].anot.set(color = 'grey')
        self.actualiza_anot_grupos()
        self.ax.relim()
        self.ax.autoscale_view()
        self.ind_ar = self.ind_ar + 1



estado = AGPM() 