from cmath import atan
from glob import glob
from turtle import width
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
class Anotacion: 
    text = None
    rect = None
    
    def __init__(self,x,y,text): 
        #tienes que saber cuantos caracteres caben uno de 1 
        self.text = env.vars['ax'].text(x, y,text,fontsize = 9)
        #con el tamano de 9 caben diez  
        nc = len(text)//10 + 1 
        self.rect = Rectangle((x,y),width = nc,height = 0.2,visible = False) 
        env.vars['ax'].add_patch(self.rect) 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale()
    def anota(self,text): 
        nc = len(text)//10 + 1 
        self.text.set(text = text)
        self.rect.set(width = nc)
    def texto(self):
        return self.text.get_text()  

class Arbol: 
    raiz = None 
    vertices = None 
    aristas = None 
    n = 0 
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
    anotc = None 
    padre = None
    hijos = None
    valor =None
    #una tabla para asociar la letra con el vertice hijo 
    alf = None 
    ax_anot = None 
    anot = None 
    def __init__(self): 
        self.hijos = []
        self.alf = [-1 for i in range(0,128)] 
class Arista: 
    linea = None
    anot = None

class Env: 
    vars = None
    def __init__(self): 
        self.vars = dict() 
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)

def dfs(n,arbol,prof,y): 
    if(not n.hijos): 
        prof[n] = y 
    for i in n.hijos : 
        dfs(i,arbol,prof,y - 4*env.vars['rad'])

def prof_hojas(arbol): 
    prof = dict() 
    dfs(arbol.raiz,arbol,prof,0) 
    return prof

#suponiendo que tiene hijos
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
        v.circ = None 
        for u in v.hijos: 
            if((v,u) in arbol.aristas): 
                if(arbol.aristas[(v,u)].linea != None): 
                    arbol.aristas[(v,u)].linea.set(visible = False)
                    arbol.aristas[(v,u)].anot.set(visible = False)
                arbol.aristas[v,u].linea = None 
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
        x = x + 4*rad
    hijos_proc = dict()
    while(cola): 
        n,x,y = cola[0]
        cola.pop(0)
        c = Circle((x,y),radius = rad,facecolor = 'white',edgecolor = 'black')
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
        for j in range(0,128): 
            if(v.alf[j] != -1):  
                xi,yi = v.circ.get_center()
                xj,yj = v.alf[j].circ.get_center()
                linea = PathPatch(Path([inter_points(env.vars['rad'],xi,yi,xj,yj),inter_points(env.vars['rad'],xj,yj,xi,yi)]), facecolor='none', edgecolor='black')
                env.vars['ax'].add_patch(linea)
                arbol.aristas[(v,v.alf[j])].linea = linea
                xm,ym = punto_medio(xi,yi,xj,yj,0.5,0.5)
                arbol.aristas[(v,v.alf[j])].anot =  env.vars['ax'].text(xm, ym,chr(j),fontsize = 9,ha='center', va='center') 
    env.vars['ax'].relim()
    env.vars['ax'].autoscale_view()
class Ejecucion: 
    nodo_act = 0 
    ind = 0
    cad_entrada = ""
    ars_color = [] 
    nodos_color = [] 
    def crear_arbol(self,ars,n):
        arbol = env.vars['arbol']
        for i in range(0,n): 
            arbol.vertices[i] = Vertice()  
        arbol.raiz = arbol.vertices[0]
        for n,h in ars.items():  
            for l,i in h: 
                arbol.vertices[n].hijos.append(arbol.vertices[i])
                arbol.vertices[n].alf[ord(l)] = arbol.vertices[i]
                arbol.aristas[(arbol.vertices[n],arbol.vertices[i])] = Arista() 
                arbol.vertices[i].padre = arbol.vertices[n] 
    def zoom_mas(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = env.vars['fig'].get_size_inches()
        env.vars['fig'].set_size_inches(x-1,y-1)
    def colorear_aristas(self): 
        arbol = env.vars['arbol']
        for (v,u)  in self.ars_color:
            arbol.aristas[(v,u)].linea.set(color = 'red')
            arbol.aristas[(v,u)].linea.set(linewidth = 3)
    def colorear_nodos(self): 
        for n in self.nodos_color: 
            n.circ.set(facecolor = 'red')
    def siguiente_paso(self):       
        arbol = env.vars['arbol']
        if(self.ind == len(self.cad_entrada)): 
            self.config_teclas_inicial() 
            self.nodo_act = arbol.raiz 
            self.ind = 0 
            self.cad_entrada = ""
            self.ars_color = [] 
            self.nodos_color = [arbol.raiz] 
            text = "Escribe alguna palabra en el cuadro de texto bajo la imagen.\n"
            text += "Cuando estes listo presiona el boton."
            self.anot.set(text =text)
            #volver a poner los botones 
            t = widgets.Text(
                        value='',
                        description='Cadena:',
                        disabled=False
                        )
            b = widgets.Button(description="Listo")
            b.on_click(self.handler_boton)
            self.botones.children = [t,b]
            return
        if(self.nodo_act.alf[ord(self.cad_entrada[self.ind])] != -1): 
            #print("esta en el arbol")
            self.ars_color.append((self.nodo_act,self.nodo_act.alf[ord(self.cad_entrada[self.ind])]))
            self.nodo_act = self.nodo_act.alf[ord(self.cad_entrada[self.ind])]
            text = "El nodo actual tiene una arista etiquetada con {}.\n".format(self.cad_entrada[self.ind])
            text += "Se toma la arista."
            self.anot.set(text =text)
            self.nodos_color.append(self.nodo_act)

        else: 
            #print("no esta en el arbol")
            nuevo = Vertice() 
            #info del nuevo 
            arbol.vertices[arbol.n_nodos] = nuevo  
            nuevo.padre = self.nodo_act
            nuevo.hijos  = []
            nuevo.valor = arbol.n_nodos 
            #info del padre  
            self.nodo_act.alf[ord(self.cad_entrada[self.ind])] = nuevo
            self.ars_color.append((self.nodo_act,nuevo)) 
            self.nodo_act.hijos.append(nuevo)
            #info aristas 
            #print("agrega a {}".format(nuevo))
            arbol.aristas[(self.nodo_act,nuevo)] = Arista() 
            #info del arbol 
            arbol.n_nodos = arbol.n_nodos + 1
            self.nodo_act = nuevo
            text = "El nodo actual no tiene una arista etiquetada con {}.\n".format(self.cad_entrada[self.ind])
            text += "Se crea un nuevo nodo. La arista se etiqueta con {} y se toma la arista".format(self.cad_entrada[self.ind])
            self.anot.set(text =text)
            self.nodos_color.append(nuevo)
        dibujar_arbol()
        self.colorear_aristas()
        self.colorear_nodos() 
        self.ind = self.ind + 1    
        #eliminar arbol 
    @out1.capture() 
    def handler_teclas_ejecucion(self,event): 
        if(event.key == 'n'):    
            self.siguiente_paso() 
        elif(event.key == '+'): 
            self.zoom_mas() 
        elif(event.key == '-'): 
            self.zoom_menos() 
    def config_ejecucion(self): 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_teclas_ejecucion)

    def init_anot(self): 
        text= "Escribe alguna palabra en cuadro de texto bajo la imagen.\n" 
        text += "Cuando estes listo presiona el boton"
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    
            
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
        
    def config_teclas_inicial(self): 
        if(env.vars['cid_t'] != None): 
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
        env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.handler_teclas_inicial)

    def handler_teclas_inicial(self,event): 
        if(event.key == '+'): 
            self.zoom_mas() 
        elif(event.key == '-'): 
            self.zoom_menos() 
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
    def handler_boton(self,event): 
        #conectar las teclas 
        self.cad_entrada = self.botones.children[0].value + "$"
        self.config_ejecucion() 
        self.botones.children = [] 
        text = "Haz click en la imagen, cada vez que presiones n se ejecutara\n"
        text += "un paso mas del algortmo.\n"
        text += "Para hacer mas grande/chica la imagen presiona +/-.\n"
        text += "El nodo actual es la raiz, coloreada en rojo"
        self.nodos_color = [env.vars['arbol'].raiz]
        dibujar_arbol() 
        self.colorear_nodos() 
        self.anot.set(text = text)
        return 
    def poner_botones(self): 
        t = widgets.Text(
                        value='',
                        description='Cadena:',
                        disabled=False
                        )
        b = widgets.Button(description="Listo")
        b.on_click(self.handler_boton)
        self.botones = widgets.VBox([t,b])
        display(self.botones)
    def __init__(self): 
        self.nodo_act = env.vars['arbol'].raiz
        #poner anotacion 
        self.config_imagen() 
        self.desactivar_letras_gui() 
        self.config_teclas_inicial() 
        self.nodos_color = [env.vars['arbol'].raiz]
        dibujar_arbol() 
        self.poner_botones() 
        self.init_anot() 
env = Env() 
env.vars['arbol'] = Arbol() 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['fig'].canvas.draw()
env.vars['rad'] = 1
env.vars['cid_m'] = None 
env.vars['cid_t'] = None 
env.vars['e1'] = Ejecucion() 