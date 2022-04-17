
from cmath import atan
from glob import glob
from pydoc import visiblename
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

from numpy import arange 
%matplotlib nbagg
out1 = widgets.Output()
display(out1) 
class Arb_rec:
    #lista de lista de nodos  
    niveles = None
    def __init__(self): 
        self.niveles = [] 
class Nodo: 
    padre = None 
    linea_padre = None
    #una lista 
    arreglo = None
    ind = 0 
    ind_anot = None 
    def __init__(self,arr): 
        self.arreglo= Arreglo(len(arr))
        self.arreglo.arr = arr

class Arreglo:
    #lista de celdas  
    celdas = None
    #tambien vamos a tener el arreglo como tal
    arr = None
    def __init__(self,n): 
        self.celdas = [Celda() for i in range(0,n)] 

class Celda: 
    rect = None
    anot = None 

#Todo va a estar en una clase 
class Mergesort:  
    box = widgets.VBox()
    ax = None 
    fig = None 
    arb_rec = None
    arr_entrada = [random.randint(0,99) for i in range(0,32)]
    rad=  1
    cid = None
#--------------------------obtener entrada --------------------
    def config_botones_entrada(self): 
        print("config de botones")
    def __init__(self): 
        self.config_ejecucion()
        display(self.box)


#--------------------------ejecucion--------------------------
    ind_vis = 1
    level = 0 
    tecla_funcion = None
    def config_imagen_ejecucion(self): 
        self.fig,self.ax =  plt.subplots()  
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.rcParams["figure.figsize"]=20,20
        #self.fig.set_size_inches(20, 10.5)
        #print(plt.rcParams.keys())
        plt.axis('off')
   
    @out1.capture()
    def on_key(self,event):
        if(event.key in self.tecla_funcion): 
            self.tecla_funcion[event.key]()
    def config_botones_ejecucion(self):
        boton_listo = widgets.Button(description='listo')
        boton_listo.on_click(self.handler_arriba_abajo)  
        self.box.children = [boton_listo]
       
    def crear_arbol_recursion(self): 
        self.arb_rec = Arb_rec() 
        n = Nodo(self.arr_entrada) 
        cola = [n]
        self.arb_rec.niveles = []
        while(cola): 
            cola_n = []
            self.arb_rec.niveles.append(cola.copy())
            for x in cola: 
                if(len(x.arreglo.arr) > 1): 
                    n1 = Nodo(x.arreglo.arr[0:len(x.arreglo.arr)//2]) 
                    n2 = Nodo(x.arreglo.arr[len(x.arreglo.arr)//2:len(x.arreglo.arr)]) 
                    n1.padre = x 
                    n2.padre = x 
                    cola_n.append(n1) 
                    cola_n.append(n2)            
            cola = cola_n
    def dibujar_arreglo(self,nodo,x,y,vis): 
        ar = nodo.arreglo
        for i  in range(0,len(ar.arr)): 
            r = Rectangle((x,y),width = self.rad,height = 1,facecolor = 'white',edgecolor = 'black',visible = vis)
            self.ax.add_patch(r)
            anot = self.ax.annotate("{}".format(ar.arr[i]), (x+self.rad/2,y+self.rad/2) ,color='black', weight='bold', fontsize=7, ha='center', va='center',visible = vis)
            ar.celdas[i].rect = r 
            ar.celdas[i].anot = anot 
            x = x + self.rad

    def dibujar_lineas(self): 
        for i in range(1,len(self.arb_rec.niveles)): 
            for n in self.arb_rec.niveles[i]: 
                xp,yp = n.padre.arreglo.celdas[0].rect.get_xy()
                xp = xp + (len(n.padre.arreglo.arr)*self.rad) / 2  
                yp = yp - self.rad
                x,y = n.arreglo.celdas[0].rect.get_xy()
                y = y + self.rad 
                x = x + (len(n.arreglo.arr)*self.rad) / 2 
                linea = PathPatch(Path([(x,y),(xp,yp)]), facecolor='none', edgecolor='black',visible = False,linestyle = '--')
                self.ax.add_patch(linea)
                n.linea_padre = linea    

    def dibujar_arbol(self):  
        print("se dibuja el arbol")
        x = 0
        y = 0 
        #poner los primeros 
        i = len(self.arb_rec.niveles) - 1 
        cola = [] 
        for n in self.arb_rec.niveles[i]: 
            x = x + self.rad*(len(n.arreglo.arr)) + 2*self.rad
            i = i - 1
            cola.append((n,(x,y)))
        while(len(cola) > 1): 
            cola_n = []
            for j in range(0,len(cola)-1,2):  
                ln = cola[j][0]
                x,y = cola[j][1]
                self.dibujar_arreglo(ln,x,y,False)
                rn = cola[j+1][0]
                x,y = cola[j+1][1]
                self.dibujar_arreglo(rn,x,y,False)
                l1 = ln.arreglo.celdas[0].rect.get_xy()[0] 
                l2 = rn.arreglo.celdas[0].rect.get_xy()[0] + self.rad*len(rn.arreglo.arr)
                xp = (l1 + l2 - len(ln.padre.arreglo.arr)*self.rad)/2
                cola_n.append((ln.padre,(xp,y+4*self.rad)))
                j = j + 2
            cola = cola_n
        x,y = cola[0][1]
        self.dibujar_arreglo(cola[0][0],x,y,True)
        self.dibujar_lineas()
        self.ax.relim()
        self.ax.autoscale_view()


    def handler_arriba_abajo(self): 
        if(self.ind_vis == len(self.arb_rec.niveles)): 
            self.tecla_funcion['n'] = self.handler_abajo_arriba
            #self.cid = self.fig.canvas.mpl_connect('button_press_event', self.handler_abajo_arriba)
            #poner en blanco todo los que no son hojas 
            return 
        if(self.ind_vis == len(self.arb_rec.niveles)-1): 
            for i in range(0,len(self.arb_rec.niveles)-1): 
                for n in self.arb_rec.niveles[i]:
                    for c in n.arreglo.celdas: 
                        c.anot.set(text = "")
            self.inicializar_ind_nivel(self.ind_vis)

        for n in self.arb_rec.niveles[self.ind_vis]: 
            n.linea_padre.set(visible = True ) 
            for c in n.arreglo.celdas: 
                c.rect.set(visible = True)
                c.anot.set(visible = True)
        self.ind_vis = self.ind_vis + 1
    def inicializar_ind_nivel(self,nivel): 
        #limpiar el nivel anterior 
        if(nivel < len(self.arb_rec.niveles)-1): 
            for n in self.arb_rec.niveles[nivel+1]: 
                n.ind_anot.set(visible = False)
        for i in range(0,len(self.arb_rec.niveles[nivel]),2): 
            n1 = self.arb_rec.niveles[nivel][i]
            n2 = self.arb_rec.niveles[nivel][i+1]
            p = n1.padre 
            x1,y1 = n1.arreglo.celdas[0].rect.get_xy(); 
            x2,y2 = n2.arreglo.celdas[0].rect.get_xy(); 
            xp,yp = p.arreglo.celdas[0].rect.get_xy(); 
            if(n1.ind_anot == None): 
                anot_i = self.ax.text(x1+self.rad/2, y1-self.rad, '$i$',fontsize = 9) 
                n1.ind_anot = anot_i
            else: 
                n1.ind_anot.set(x = x1+self.rad/2)
                n1.ind_anot.set(text = '$i$')
            if(n2.ind_anot == None): 
                anot_j = self.ax.text(x2+self.rad/2, y2-self.rad, '$j$',fontsize = 9) 
                n2.ind_anot = anot_j
            else: 
                n2.ind_anot.set(x = x2+self.rad/2)
                n2.ind_anot.set(text = '$j$')
            if(p.ind_anot == None): 
                anot_k = self.ax.text(xp+self.rad/2, yp-self.rad, '$k$',fontsize = 9) 
                p.ind_anot = anot_k
            else: 
                p.ind_anot.set(x = xp+self.rad/2)
                p.ind_anot.set(text = '$k$')
            n1.ind = 0 
            n2.ind = 0 
            p.ind = 0 

    def handler_abajo_arriba(self): 
        if(self.level == 0): 
            return 
        #a partir de aquí no está en el nivel 1 
        prim_niv_ant = self.arb_rec.niveles[self.level-1][0]
        if( prim_niv_ant.ind == len(prim_niv_ant.arreglo.arr)): 
            self.level = self.level - 1 
            #si ahora el nivel es 0 ya no inicializar nada 
            if(self.level == 0): 
                #limpiar los indices que quedan en el primer y segundo nivel 
                for n in self.arb_rec.niveles[0]: 
                    n.ind_anot.set(visible = False)
                for n in self.arb_rec.niveles[1]: 
                    n.ind_anot.set(visible = False)
                return 
            self.inicializar_ind_nivel(self.level)
        else:  
            for i in range(0,len(self.arb_rec.niveles[self.level]),2): 
                n1 = self.arb_rec.niveles[self.level][i] 
                n2 = self.arb_rec.niveles[self.level][i+1]
                p = n1.padre
                p.ind_anot.set(x = p.ind_anot.get_position()[0] + self.rad)
                if(n1.ind == len(n1.arreglo.arr)): 
                    p.arreglo.arr[p.ind] = n2.arreglo.arr[n2.ind]
                    p.arreglo.celdas[p.ind].anot.set(text = p.arreglo.arr[p.ind])
                    n2.ind = n2.ind + 1
                    n2.ind_anot.set(x = n2.ind_anot.get_position()[0] + self.rad)
                    p.ind = p.ind + 1
                    continue 
                if(n2.ind == len(n2.arreglo.arr)): 
                    p.arreglo.arr[p.ind] = n1.arreglo.arr[n1.ind]
                    p.arreglo.celdas[p.ind].anot.set(text = p.arreglo.arr[p.ind])
                    n1.ind = n1.ind + 1
                    n1.ind_anot.set(x = n1.ind_anot.get_position()[0] + self.rad)
                    p.ind = p.ind + 1 
                    continue 
                if(n1.arreglo.arr[n1.ind] <= n2.arreglo.arr[n2.ind]): 
                    p.arreglo.arr[p.ind] = n1.arreglo.arr[n1.ind]
                    p.arreglo.celdas[p.ind].anot.set(text = p.arreglo.arr[p.ind])
                    n1.ind = n1.ind + 1
                    n1.ind_anot.set(x = n1.ind_anot.get_position()[0] + self.rad)
                    p.ind = p.ind + 1 
                else: 
                    p.arreglo.arr[p.ind] = n2.arreglo.arr[n2.ind]
                    p.arreglo.celdas[p.ind].anot.set(text = p.arreglo.arr[p.ind])
                    n2.ind = n2.ind + 1
                    n2.ind_anot.set(x = n2.ind_anot.get_position()[0] + self.rad)
                    p.ind = p.ind + 1
        
    def zoom_mas(self): 
        x,y = self.fig.get_size_inches()
        self.fig.set_size_inches(x+1,y+1)
    def zoom_menos(self): 
        x,y = self.fig.get_size_inches()
        self.fig.set_size_inches(x-1,y-1)
    def config_teclas(self): 
        self.cid1 = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.tecla_funcion = dict()
        self.tecla_funcion['n'] = self.handler_arriba_abajo
        self.tecla_funcion['+'] = self.zoom_mas
        self.tecla_funcion['-'] = self.zoom_menos
    #entrada 
    def config_ejecucion(self):    
        self.config_imagen_ejecucion()
        self.config_botones_ejecucion()
        self.config_teclas()
        self.crear_arbol_recursion()
        self.dibujar_arbol() 
        #self.cid = self.fig.canvas.mpl_connect('button_press_event', self.handler_arriba_abajo)
        self.level = len(self.arb_rec.niveles)  -1

estado = Mergesort() 