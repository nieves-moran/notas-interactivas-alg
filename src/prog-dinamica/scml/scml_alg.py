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
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)

class Matriz: 
    celdas = None
    def __init__(self,n,m): 
        self.celdas = [[0 for j in range(0,m)] for i in range(0,n)] 
class Celda: 
    valor = None 
    rect = None
    anot = None
class Etiquetas: 
    reng = None
    cols = None
    def __init__(self,n,m): 
        self.reng = [Etiq() for i in range(0,n)]
        self.cols = [Etiq() for j in range(0,m)]
class Etiq: 
    rect = None
    anot = None 
class Env:
    vars = dict()  

class Ejecucion:  
    cad1 = ""
    cad2 = ""
    ind_i = 0 
    ind_j = 0 
    n = None 
    m = None 
    flechas = [] 
    calculados = dict() 
    #un par que dice cual es el que se esta explicando 
    act_exp = None 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
    
    def siguiente_paso(self):
        #print('ejecuta el siguiente paso')
        for f in self.flechas: 
            f.set(visible = False)
        i = self.ind_i 
        if(i == self.n): 
            return 
        mat = env.vars['mat']
        for j in range(0,self.m): 
            M = 0 
            x,y = mat.celdas[i][j].rect.get_xy() 
            if(self.cad1[i] == self.cad2[j]): 
                M = 1 
                if (0 <= i - 1 and 0 <= j -1): 
                    M = M + mat.celdas[i-1][j-1].valor
            if(0 <= i - 1 and mat.celdas[i-1][j].valor > M): 
                M = mat.celdas[i-1][j].valor
            if( 0 <= j - 1 and mat.celdas[i][j-1].valor > M ):              
                M = mat.celdas[i][j-1].valor    
            mat.celdas[i][j].valor = M 
            mat.celdas[i][j].anot.set(text = M)
            self.calculados[(i,j)] = []
        self.ind_i += 1 
    def agregar_flecha(self,i,j,u,v):
        mat = env.vars['mat']
        x1,y1 = mat.celdas[i][j].rect.get_xy() 
        x1 += 1.5
        y1 += 1.5 
        x2,y2 = mat.celdas[u][v].rect.get_xy()
        x2 += 1.5
        y2 += 1.5
        (x1,y1),(x2,y2) = inter_points(0.5,x1,y1,x2,y2),inter_points(0.5,x2,y2,x1,y1) 
        return env.vars['ax'].arrow(x1,y1, x2-x1, y2-y1,width = 0.2,head_length = 1,facecolor = 'white',length_includes_head = True) 
    
    def explicacion_sig_paso(self):
        if(not self.calculados[self.act_exp]): 
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
            env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.teclas_handler)   
            env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_click_handler)
            #limpiar las flechas y el cuadro de texto 
            return  
        #toma algun vecino 
        i,j = self.act_exp 
        u,v = self.calculados[self.act_exp][0] 
        self.calculados[self.act_exp].pop(0)
        f = self.agregar_flecha(i,j,u,v) 
        self.flechas.append(f)
    @out1.capture() 
    def explicacion_handler(self,event): 
        if(event.key == 'n'): 
            self.explicacion_sig_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    @out1.capture() 
    def mouse_click_handler(self,event): 
        #buscar en las que estan calculadas
        if(event.xdata == None or event.ydata == None): 
            return 
        for (i,j),ps in self.calculados.items():
            x,y = env.vars['mat'].celdas[i][j].rect.get_xy() 
            if(x <= event.xdata and event.xdata <= x + 3 and y <= event.ydata and event.ydata <= y + 3 ): 
                print("estoy en {}".format((i,j)))
                self.act_exp = (i,j)
                #calculando los vecinos
                vec = [] 
                if( 0 <= i - 1 ): 
                    vec.append((i-1,j))
                if(0 <= j -1 ): 
                    vec.append((i,j-1))
                if(0 <= i -1 and 0 <= j - 1 ): 
                    vec.append((i-1,j-1))
                self.calculados[(i,j)] = vec 
                env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
                env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.explicacion_handler)
                env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_m']) 
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
        self.cad1 = "ababccac"
        self.cad2 = "ababccabac"
        self.n = len(self.cad1)
        self.m = len(self.cad2)
        env.vars['mat'] = Matriz(self.n,self.m)
    def dibujar_matriz(self):
        mat = env.vars['mat']
        x,y = 0,0  
        for i in range(0,len(mat.celdas)):
            x = 0  
            for j in range(0,len(mat.celdas[0])):
                cel = Celda()
                w,h = 3,3
                cel.rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black')
                env.vars['ax'].add_patch(cel.rect) 
                cel.anot =  env.vars['ax'].text(x+w/2, y+h/2,"".format(i,j),fontsize = 9,ha='center', va='center') 
                mat.celdas[i][j] = cel
                x = x + 3
            y = y - 3 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def poner_etiquetas(self):
        mat = env.vars['mat'] 
        n = len(mat.celdas)
        m = len(mat.celdas[0])
        et = Etiquetas(n,m)
        env.vars['etq'] = et
        x,y = -3,0
        w,h = 3,3
        for i in range(0,n):
            et.reng[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.reng[i].rect) 
            et.reng[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"{}".format(self.cad1[i]),fontsize = 9,ha='center', va='center')  
            y = y - 3 
        x,y = 0,3
        for i in range(0,m):
            et.cols[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.cols[i].rect)  
            et.cols[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"{}".format(self.cad2[i]),fontsize = 9,ha='center', va='center')  
            x = x + 3 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_matriz()
        self.dibujar_matriz() 
        env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_click_handler)
        self.poner_etiquetas()

env = Env() 
env.vars['mat'] = None
env.vars['etq'] = None 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
