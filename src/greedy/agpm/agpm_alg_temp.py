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
def agregar_arista(u,v):
        #si ya está, no la agregues 
        if( not ((v in env.vars['g'].ady and u in env.vars['g'].ady[v]) or (u in env.vars['g'].ady and v in env.vars['g'].ady[u]))): 
            xu,yu = env.vars['g'].pos_nodos[u].img.get_center() 
            xv,yv = env.vars['g'].pos_nodos[v].img.get_center() 
            linea = PathPatch(Path([inter_points(env.vars['rad'],xu,yu,xv,yv),inter_points(env.vars['rad'],xv,yv,xu,yu)]), facecolor='none', edgecolor='black')
            env.vars['ax'].add_patch(linea)
            xm,ym = punto_medio(xu,yu,xv,yv,0.5)
            anot = env.vars['ax'].annotate("10", (xm,ym),color='black', weight='bold', fontsize=10, ha='center', va='center') 
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
            env.vars['g'].ady[u][v].peso = 10
            env.vars['g'].ady[u][v].linea = linea 
            env.vars['g'].ady[u][v].anot = anot
            #para el otro 
            env.vars['g'].ady[v][u].arista = (u,v)
            env.vars['g'].ady[v][u].peso = 10 
            env.vars['g'].ady[v][u].linea = linea 
            env.vars['g'].ady[v][u].anot = anot
            #agregar el widget 
    
class Grafica_aleatoria: 
    def generar_aristas_aleatorias(self,n): 
        union_f = Union_find(n*n)
        aristas = [] 
        for i in range(0,n*n): 
            for v in self.vecinos(i,n):
                aristas.append((i,v)) 
        arbol = []
        for (u,v) in aristas: 
            if(union_f.find(u) != union_f.find(v)): 
                union_f.unite(u,v) 
                arbol.append((u,v))
        #aqui ya tiene las aristas que forma el arbol 
        #agregar mas aristas 
        for i in range(0,n*n): 
            for v in self.vecinos(i,n): 
                r = random.randint(0,1)
                if( r % 2 == 1): 
                    arbol.append((i,v))
        ars_peso = []
        for (u,v) in arbol: 
            p = random.randint(1,50)
            ars_peso.append((u,v,p))
        return ars_peso
    def poner_nodos(self,n): 
        #una cuadricula de nodos de nxn 
        for y in range(0,n): 
            for x in range(0,n): 
                c = Circle((x*env.vars['rad']*4,y*env.vars['rad']*4),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black')
                cr = Circulo() 
                anot = env.vars['ax'].annotate("{}".format(env.vars['ind']), (x*env.vars['rad']*4,y*env.vars['rad']*4),color='black', weight='bold', fontsize=10, ha='center', va='center') 
                env.vars['ax'].add_patch(c)
                cr.pos = [y*env.vars['rad']*4,y*env.vars['rad']*4] 
                cr.img = c 
                env.vars['g'].pos_nodos[env.vars['ind']] = cr
                env.vars['ind'] = env.vars['ind'] + 1
                env.vars['max_x_g'] = max(env.vars['max_x_g'],c.get_center()[0] + 2*env.vars['rad'])
                env.vars['max_y_g'] = max(env.vars['max_y_g'],c.get_center()[1] + 2*env.vars['rad'])
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def __init__(self): 
        #poner nodos
        self.poner_nodos(4)
        ars_al = self.generar_aristas_aleatorias(4) 
        for (u,v,p) in ars_al: 
            agregar_arista(u,v)
            env.vars['g'].ady[u][v].anot.set(text = "{}".format(p))
            env.vars['g'].ady[u][v].peso = p 
        env.vars['e3'] = Ejecucion()
    def vecinos(self,v,n):
            #la grafia es de nxn y v es el vertice 
            (x,y) = v // n  , v % n
            v = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] 
            vp = []
            for (x,y) in v: 
                if (0 <= x < n and 0 <= y < n): 
                    vp.append(x*n + y)
            return vp 
class Obtener_vertices:  
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        #poner 4 puntos en donde quieres 
        c = Circle((20,20),radius = 1, visible = False)
        env.vars['ax'].add_patch(c)
        c = Circle((0,0),radius = 1, visible = False)
        env.vars['ax'].add_patch(c)
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view() 
        plt.axis('off')
    def boton_listo_handler(self,event): 
        #pasar al siguiente estado 
        env.vars['fig'].canvas.mpl_disconnect(env.vars['cid']) 
        env.vars['e1'] = Obtener_aristas()
    def boton_aleatoria(self,event): 
        env.vars['fig'].canvas.mpl_disconnect(env.vars['cid']) 
        env.vars['e2'] = Grafica_aleatoria()
    def boton_entrada_usr_handler(self,event): 
        env.vars['cid'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.onclick)
        #quitar el boton de aleatoria 
        boton_listo = widgets.Button(description='Listo')
        boton_listo.on_click(self.boton_listo_handler)  
        env.vars['box'].children = [boton_listo]
    def config_botones(self): 
        boton_ent_usr = widgets.Button(description='Entrada de usuario')
        boton_ent_usr.on_click(self.boton_entrada_usr_handler)  
        boton_aleatoria = widgets.Button(description='Generar aleatoria')
        boton_aleatoria.on_click(self.boton_aleatoria)  
        env.vars['box'] = widgets.VBox([boton_ent_usr,boton_aleatoria])
        display(env.vars['box'])
    @out1.capture()
    def onclick(self,event): 
        #poner los vertices 
        c = Circle((event.xdata,event.ydata),radius = env.vars['rad'],facecolor = 'white',edgecolor = 'black')
        env.vars['max_x_g'] = max(env.vars['max_x_g'], event.xdata + env.vars['rad'])
        env.vars['max_y_g'] = max(env.vars['max_y_g'], event.ydata + env.vars['rad'])
        anot = env.vars['ax'].annotate("{}".format(env.vars['ind']), (event.xdata,event.ydata),color='black', weight='bold', fontsize=10, ha='center', va='center') 
        env.vars['ax'].add_patch(c)
        cr = Circulo() 
        cr.pos = [event.xdata,event.ydata] 
        cr.img = c 
        env.vars['g'].pos_nodos[env.vars['ind']] = cr
        env.vars['ind'] = env.vars['ind'] + 1
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()  
    def __init__(self): 
        print("se llama a obtener vertices")
        self.config_imagen() 
        self.config_botones()
        env.vars['g'] = Grafica()
class Obtener_aristas: 
    extremos = [] 
    def __init__(self):
        env.vars['cid'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.onclick)
        self.config_botones()
    #salida 
    def boton_listo_handler(self,event): 
        #pasar al siguiente que es escoger un inicial 
        env.vars['fig'].canvas.mpl_disconnect(env.vars['cid']) 
        env.vars['e3'] = Ejecucion()
        #self.config_ejecucion()
    def config_botones(self): 
        boton_listo = widgets.Button(description='listo')
        boton_listo.on_click(self.boton_listo_handler)  
        env.vars['box'].children = [boton_listo]
    @out1.capture()
    def onclick(self,event): 
        for i,cir in env.vars['g'].pos_nodos.items(): 
            x,y = cir.pos
            r = cir.img.get_radius()
            if(math.sqrt((x - event.xdata)**2) <= r and math.sqrt((y - event.ydata)**2) <= r ): 
                cir.img.set(facecolor = 'red')
                if (i not in self.extremos): 
                    self.extremos.append(i)
                    if(len(self.extremos) == 2): 
                        agregar_arista(self.extremos[0],self.extremos[1])
                        self.agregar_widget_peso(self.extremos[0],self.extremos[1])
                        for i in self.extremos: 
                            env.vars['g'].pos_nodos[i].img.set(facecolor = 'white')
                        self.extremos = []
                else:
                    self.extremos.remove(i)
                    cir.img.set(facecolor = 'white')

    def esc_peso_handler(self,change):
        u,v = eval(change.owner.description) 
        env.vars['g'].ady[u][v].anot.set(text = "{}".format(change.new))
        env.vars['g'].ady[u][v].peso = change.new 
    def agregar_widget_peso(self,u,v): 
        ch = list(env.vars['box'].children)
        esc_peso = widgets.BoundedIntText(value=10,min=0,max=100,step=1,description='({},{})'.format(u,v),disabled=False)
        esc_peso.observe(self.esc_peso_handler, names='value')
        ch.append(esc_peso)
        env.vars['box'].children = tuple(ch)
    
class Ejecucion: 
    ind_ar = 0 
    ar_ord = None 
    union_f = None
    array_col = None 
    color_map = None
    anotacion_g = None 
    def config_boton(self): 
        boton_listo = widgets.Button(description='siguiente')
        boton_listo.on_click(self.boton_listo_handler_ej)  
        env.vars['box'].children = [boton_listo]
    def obtener_aristas_ord(self): 
        ars = [] 
        ars_sp = [] 
        for i in env.vars['g'].ady.keys(): 
            for j in env.vars['g'].ady[i].keys(): 
                if((i,j) not in ars_sp): 
                    ars_sp.append((i,j))
                    ars_sp.append((j,i))
                    ars.append((i,j,env.vars['g'].ady[i][j].peso))
        ars.sort(key = lambda x : x[2])
        return ars
    def colorear_vert(self): 
        for i in range(0,env.vars['ind']): 
            vert = env.vars['g'].pos_nodos[i]
            vert.img.set(facecolor = self.array_col[i])
    #entrada 
    def __init__(self): 
        self.config_boton()
        self.union_f = Union_find(env.vars['ind'])
        self.ar_ord = self.obtener_aristas_ord()
        self.color_map = plt.get_cmap('tab20c', 1000)
        #para el número de colores 
        frac = 1/env.vars['ind']
        self.array_col = [self.color_map((i+1)*frac) for i in range(0,env.vars['ind'])]
        self.anotacion_g  = Anot_grupos()
        self.colorear_vert()
    def limpiar_anotacion_grupos(self): 
        for r in self.anotacion_g.renglones: 
            r.cuadro_color.set(visible = False)
            r.anotacion.set(visible = False) 
        self.anotacion_g.renglones = []
    def actualiza_anot_grupos(self): 
        grupos = dict() 
        #esta en env.vars['max_x_g'] 
        x = env.vars['max_x_g'] + env.vars['rad'] 
        y = env.vars['max_y_g'] 
        self.limpiar_anotacion_grupos() 
        #crear los grupos de colores 
        for i in range(0,len(env.vars['g'].pos_nodos)):
            if(self.union_f.find(i) not in grupos ): 
                grupos[self.union_f.find(i)] = [] 
            grupos[self.union_f.find(i)].append(i)
        for j,g in grupos.items(): 
            r = Rectangle((x,y),width = env.vars['rad'],height = 1,facecolor = self.array_col[j],edgecolor = 'black') 
            env.vars['ax'].add_patch(r)
            ren = Renglon() 
            ren.cuadro_color = r
            ren.anotacion = env.vars['ax'].text(x +3*env.vars['rad'],y,"{}".format(g))
            self.anotacion_g.renglones.append( ren)
            y = y - 2*env.vars['rad']  
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
            for i in range(0,env.vars['ind']): 
                if(self.union_f.find(i) == p): 
                    env.vars['g'].pos_nodos[i].img.set(facecolor = self.array_col[p])
            env.vars['g'].ady[u][v].linea.set(linewidth = 3)
        else: 
            env.vars['g'].ady[u][v].linea.set(linestyle = '--')
            env.vars['g'].ady[u][v].anot.set(visible = False)
            env.vars['g'].ady[u][v].linea.set(visible = False)
        self.actualiza_anot_grupos()
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
        self.ind_ar = self.ind_ar + 1
env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()  
env.vars['cid'] = None
env.vars['box'] = None
env.vars['max_x_g'] = float('-inf')
env.vars['max_y_g'] = float('-inf')
env.vars['g'] = None
env.vars['ind'] = 0
env.vars['rad'] = 1

estado = Obtener_vertices() 