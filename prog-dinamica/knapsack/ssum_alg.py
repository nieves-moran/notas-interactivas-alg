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
    conj = [] 
    w = 1 
    i = 1 
    calculados = dict() 
    circs = [] 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')

    def siguiente_paso(self):
        m = env.vars['mat']
        i = self.i 
        w = self.w 
        if(w == self.W+1): 
            i = i + 1
            self.i = i   
            w = 1 
        if(i >=  len(self.conj)+1): 
            return 
        self.calculados[(i,w)] = [] 
        if(w < self.conj[i-1]): 
            m.celdas[i][w].valor = m.celdas[i-1][w].valor
            self.calculados[(i,w)].append((i-1,w))
        else:  
            m.celdas[i][w].valor = max(m.celdas[i-1][w].valor, self.conj[i-1] + m.celdas[i-1][w - self.conj[i-1]].valor)
            self.calculados[(i,w)].append((i-1,w))
            self.calculados[(i,w)].append((i-1,w - self.conj[i-1]))
        m.celdas[i][w].anot.set(text="{}".format(m.celdas[i][w].valor))
        self.w = w + 1      
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
        self.crear_conj_arb() 
        self.W  = random.randint(5,20)
        n = len(self.conj) + 1
        m = self.W + 1 
        env.vars['mat'] = Matriz(n,m)
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
        x,y = -5,-3
        w,h = 3,3
        for i in range(1,n):
            et.reng[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.reng[i].rect) 
            et.reng[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"$w_{}={}$".format(i,"" if i - 1 < 0 else self.conj[i-1]),fontsize = 9,ha='center', va='center')  
            y = y - 3 
        x,y = 0,3
        for i in range(0,m):
            et.cols[i].rect = Rectangle((x,y),width = w,height = h,facecolor = 'white',edgecolor = 'black',visible = False)
            env.vars['ax'].add_patch(et.cols[i].rect)  
            et.cols[i].anot = env.vars['ax'].text(x+w/2, y+h/2,"{}".format(i),fontsize = 9,ha='center', va='center')  
            x = x + 3 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def crear_conj_arb(self): 
        for _ in range(0,random.randint(5,10)):
            r1 = random.randint(4,9)
            r2 = random.randint(2,5) 
            self.conj.append(random.randint(r1,r1 + r2))
        print(self.conj)
    def poner_circ(self,p): 
        (u,v) = p
        x,y = env.vars['mat'].celdas[u][v].rect.get_xy() 
        x,y = x + 1.5, y + 1.5 
        p = Circle((x,y),radius = 1.5)
        return p 
    @out1.capture() 
    def mouse_click_handler(self,event): 
        #buscar en las que estan calculadas
        if(event.xdata == None or event.ydata == None): 
            return 
        for (i,j),ps in self.calculados.items():
            x,y = env.vars['mat'].celdas[i][j].rect.get_xy() 
            if(x <= event.xdata and event.xdata <= x + 3 and y <= event.ydata and event.ydata <= y + 3 ): 
                for (u,v) in ps: 
                    c = self.poner_circ((u,v))
                    env.vars['ax'].add_patch(c)
                    self.circs.append(c) 
    @out1.capture() 
    def mouse_release_handler(self,event):
        for c in self.circs: 
            c.set(visible = False)
        self.circs = [] 
    def config_mouse(self): 
        env.vars['cid_mc'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_click_handler)
        env.vars['cid_mr'] = env.vars['fig'].canvas.mpl_connect('button_release_event', self.mouse_release_handler)
    def poner_ceros(self):
        m = env.vars['mat'] 
        for i in range(0,len(self.conj)+1): 
            m.celdas[i][0].valor = 0    
            m.celdas[i][0].anot.set(text = '0')
        for i in range(0,self.W+1): 
            m.celdas[0][i].valor = 0 
            m.celdas[0][i].anot.set(text = '0')
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_matriz()
        self.dibujar_matriz()
        self.poner_ceros()  
        self.poner_etiquetas()
        self.config_mouse() 

env = Env() 
env.vars['mat'] = None
env.vars['etq'] = None 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['cid_mc'] = None 
env.vars['cid_mr'] = None 
env.vars['e1'] = Ejecucion() 
