
from cmath import atan
from glob import glob
from matplotlib.patches import Circle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import math 
%matplotlib nbagg

def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
class arbol: 
    vertices = None 
    aristas = None 
    mm_x = None 
    mm_y = None
    n = 0 
    def __init__(self,ll,n,etiq):
        tam = n
        self.vertices = dict()
        self.aristas = dict()
        for i in range(0,n): 
            self.vertices[i] = vertice()
        for i in etiq.keys(): 
            self.vertices[i].etiq = etiq[i]
        for i in range(0,n): 
            hjs = ll[i]
            self.vertices[i].hijos = hjs
            self.vertices[i].valor = i 
            for j in hjs: 
                self.vertices[j].padre = i  
                self.aristas[(i,j)] = arista()      


class vertice: 
    circulo = None 
    pos = [0,0]
    anotc = None 
    etiq = ""
    padre = None
    hijos = None
    valor =None
class arista: 
    linea = None
    anotc = None

class anotacion_1: 
    renglones= None
    mm_x = (float('inf'),float('-inf')) 
    mm_y = (float('inf'),float('-inf')) 
    def __init__(self,letras): 
        self.renglones = dict()
        for i in letras: 
            self.renglones[i] = renglon_nodo()
class renglon_nodo: 
    #es una lista de anotaciones 
    anots = None 
    x = None 
    y = None 
    def __init__(self): 
        self.anots = []
class ejemp_1: 
    box = None
    boton = None
    fig = None 
    ax = None
    arb = None 
    ars_ord = None 
    rad = 1
    ind = 0 
    aristas_col = None
    anot1 = None
    def __init__(self): 
        self.aristas_col = []
        etiq = {7:"a",8:"b",9 : "c",10 :"d",5:"e",6:"f"}
        self.arb = arbol([[1,2],[3,4],[5,6],[7,8],[9,10],[],[],[],[],[],[]],11,etiq)
        self.ars_ord = self.recorrido([['a',0,1,3,7],['b',0,1,3,8],['c',0,1,4,9],
                                ['d',0,1,4,10],['e',0,2,5],['f',0,2,6]])
        self.config_imagen()
        self.config_botones() 
        self.dibujar_arbol()
        self.dibujar_anotacion1()
    def recorrido(self,cams):
        ars = [] 
        for c in cams: 
            l = c[0]
            for i in range(1,len(c)-1): 
                ars.append((c[i],c[i+1],l))
        return ars
    def agregar_bit(self,u,v,l): 
        #tomamos la ultima anotacion y anotamos despues 
        ult_anot = self.anot1.renglones[l].anots[-1] 
        x,y = ult_anot.xy
        r = self.rad 
        #va a poner el siguiente simbolo en (x+r,y)
        self.ajustar_limites(x+r,y)
        simb = "$0$"
        if(self.arb.vertices[u].hijos[1] == v): 
            simb = "$1$"
        anot = self.ax.annotate(simb, (x+r, y),color='black', weight='bold', fontsize=15, ha='center', va='center') 
        self.anot1.renglones[l].anots.append(anot)


    def boton_sig_handler(self,event):
        if(self.ind == len(self.ars_ord)):
            return
        (u,v,l) = self.ars_ord[self.ind] 
        if(u == 0): 
            for a in self.aristas_col: 
                a.linea.set(color = 'black')
                a.linea.set(linewidth = 1)
            self.aristas_col = []
        a = self.arb.aristas[(u,v)]
        a.linea.set(color = 'blue')
        a.linea.set(linewidth = 3)
        self.aristas_col.append(a)
        self.ind = self.ind + 1
        self.agregar_bit(u,v,l)
    def config_botones(self):
        self.boton_sig = widgets.Button(description='sigiuente')
        self.boton_sig.on_click(self.boton_sig_handler)  
        self.box = widgets.VBox([self.boton_sig])
        display(self.box)
    def config_imagen(self): 
        self.fig, self.ax = plt.subplots()  
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
    def dfs(self,nd,p,profd,hojas): 
        profd[nd] = p 
        if(not self.arb.vertices[nd].hijos): 
            hojas.append(nd)
        for i in self.arb.vertices[nd].hijos: 
            self.dfs(i,p-self.rad*3,profd,hojas)
    def punto_medio_hijos(self,p): 
            lc = self.arb.vertices[p].hijos[-1] 
            fc = self.arb.vertices[p].hijos[0] 
            x1 = self.arb.vertices[fc].pos[0]
            x2 =  self.arb.vertices[lc].pos[0] 
            return (x1+x2)/2
    def obtener_pos(self): 
        #obtener las posiciones del arbol 
        mm_x = (float('inf'),float('-inf'))
        mm_y = (float('inf'),float('-inf'))
        profd = dict()
        hojas = []
        self.dfs(0,1,profd,hojas)
        x = 0 
        #las posiciones de las hojas
        for h in hojas: 
            self.arb.vertices[h].pos = [x,profd[h]]
            x = x + 3*self.rad 
        hijos_completos = dict()
        while(hojas):
            h = hojas.pop(0)  
            [x,y] = self.arb.vertices[h].pos
            mm_x = (min(mm_x[0],x),max(mm_x[1],x))
            mm_y = (min(mm_y[0],y),max(mm_y[1],y)) 
            p = self.arb.vertices[h].padre
            if(p == None): 
                continue; 
            if(p not in hijos_completos): 
                hijos_completos[p] = 0 
            hijos_completos[p] = hijos_completos[p]+1
            if(hijos_completos[p] == len(self.arb.vertices[p].hijos)): 
                hojas.append(p)
                self.arb.vertices[p].pos = [self.punto_medio_hijos(p), self.arb.vertices[h].pos[1] + 3*self.rad]
        mm_x = (mm_x[0] - 3*self.rad,mm_x[1]+3*self.rad)
        mm_y = (mm_y[0] - 3*self.rad,mm_y[1]+3*self.rad)
        return (mm_x,mm_y)
    def dibujar_nodos(self): 
        for v in self.arb.vertices.keys(): 
            [x,y] = self.arb.vertices[v].pos
            c = Circle((x,y),radius = self.rad,facecolor = 'white',edgecolor = 'black')
            self.ax.add_patch(c)
            self.arb.vertices[v].circulo = c 
            anot = self.ax.annotate(self.arb.vertices[v].etiq, (x, y),color='black', weight='bold', fontsize=7, ha='center', va='center')
            self.arb.vertices[v].anotc = anot 
   
    def dibujar_aristas(self):
        for u,v in self.arb.aristas: 
            [xu,yu] = self.arb.vertices[u].pos
            [xv,yv] = self.arb.vertices[v].pos 
            linea = PathPatch(Path([inter_points(self.rad,xu,yu,xv,yv),inter_points(self.rad,xv,yv,xu,yu)]), facecolor='none', edgecolor='black')
            self.ax.add_patch(linea)
            self.arb.aristas[(u,v)].linea = linea 
    def dibujar_arbol(self):
        mm_x,mm_y = self.obtener_pos()
        self.ax.set_xlim(mm_x[0],mm_x[1])
        self.ax.set_ylim(mm_y[0],mm_y[1])
        self.arb.mm_x = mm_x 
        self.arb.mm_y = mm_y 
        self.dibujar_nodos()
        self.dibujar_aristas()
    def obtener_pos_anot1(self):
        x = self.arb.mm_x[1] + self.rad
        y = self.arb.mm_y[1] - self.rad
        for i in self.anot1.renglones.keys(): 
            self.anot1.renglones[i].x = x
            self.anot1.renglones[i].y = y 
            y = y - self.rad 
            mm_x = self.anot1.mm_x
            mm_y = self.anot1.mm_y 
            mm_x = (min(mm_x[0],x),max(mm_x[1],x))
            mm_y = (min(mm_y[0],y),max(mm_y[1],y))
            self.anot1.mm_x = mm_x 
            self.anot1.mm_y = mm_y 
        #cambiar los limites de la anotacion
    #se van a pasar x y y, se va a agrandar la imagen para que el punto (x,y ) quepa
    #además se agrega un r para el error que tengan las figuras 
    def ajustar_limites(self,x,y):  
        r = 1
        (xm,xM) = self.ax.get_xlim() 
        (ym,yM) = self.ax.get_ylim() 
        if x > xM: 
            xM = x + r 
        if x < xm: 
            xm = x -r 
        if y > yM: 
            yM = y + r 
        if y < ym: 
            ym = y - r 
        self.ax.set_xlim(xm,xM)
        self.ax.set_ylim(ym,yM)

    def dibujar_rengs(self): 
        for i in self.anot1.renglones.keys():
            nod = self.anot1.renglones[i]
            anot = self.ax.annotate("$\gamma({})$".format(i), (nod.x, nod.y),color='black', weight='bold', fontsize=15, ha='center', va='center')
            self.anot1.renglones[i].anots.append(anot)
            anot = self.ax.annotate("$=$", (nod.x+1.5, nod.y),color='black', weight='bold', fontsize=15, ha='center', va='center')
            self.anot1.renglones[i].anots.append(anot)


    def dibujar_anotacion1(self): 
        self.anot1 = anotacion_1(["a","b","c","d","e","f"]) 
        self.obtener_pos_anot1()
        self.ajustar_limites(self.anot1.mm_x[0],self.anot1.mm_y[0])
        self.ajustar_limites(self.anot1.mm_x[1],self.anot1.mm_y[1])
        self.dibujar_rengs()

    

e = ejemp_1()