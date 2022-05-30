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
    ant = None
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
    #n son los renglones 
    n = None 
    #m las columnas 
    m = None 
    flechas = [] 
    calculados = dict() 
    #un par que dice cual es el que se esta explicando 
    valor_act = 0 
    act_exp = None 
    anot_dial = None 
    sol = []
    ind_sol1 = [] 
    ind_sol2 = []
    termina = False 
    def calc_sol(self): 
        par_act = (self.n-1,self.m-1)
        mat = env.vars['mat']
        while( mat.celdas[par_act[0]][par_act[1]].ant != None ):
            i,j =  par_act
            u,v = mat.celdas[i][j].ant 
            if(u == i-1 and v == j-1 ): 
                self.ind_sol1.append(i)
                self.ind_sol2.append(j)
            self.agregar_flecha(i,j,u,v)
            self.sol.append(par_act)
            par_act = mat.celdas[i][j].ant 
        i,j = par_act 
        if(self.cad1[i] == self.cad2[j]): 
            self.ind_sol1.append(i)
            self.ind_sol2.append(j)
    
    def poner_circ_sol(self): 
        mat = env.vars['mat']
        for i in self.ind_sol1: 
            x,y = mat.celdas[i][0].rect.get_xy()
            x,y = x -1.5 ,y + 1.5 
            c = Circle((x,y),radius = 1, color = '#FF00FF',alpha = .5)
            env.vars['ax'].add_patch(c)
        for i in self.ind_sol2: 
            x,y = mat.celdas[0][i].rect.get_xy()
            x,y = x + 1.5 , y + 4.5 
            c = Circle((x,y),radius = 1, color = '#FF00FF',alpha = 0.5)
            env.vars['ax'].add_patch(c)
    @out1.capture() 
    def mouse_sol_handler(self,event): 
        xe,ye = event.xdata,event.ydata 
        if(xe == None or ye == None): 
            return 
        mat= env.vars['mat']
        x,y = mat.celdas[self.n-1][self.m-1].rect.get_xy()
        if(x <= xe <= x + 3 and  y <= ye <= y + 3): 
            self.calc_sol() 
            self.poner_circ_sol()
            text = ""
            text += "Las flechas se dirigen hacia la mejor opcion para cada celda.\n"
            text += "La solucion se compone de los caracteres que son iguales en esta .\n"
            text += "secuencia de flechas, marcados en rosa.\n"
            text += "Recuerda que puedes presionar + para hacer mas grande la imagen."
            self.anot.set(text = text)
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_m']) 
    def siguiente_paso(self):
        i = self.ind_i 
        if(self.termina ): 
            return 
        if(i == self.n): 
            text = "El algoritmo termina."
            text += "La respuesta esta en OPT({},{})\n".format(len(self.cad1)-1,len(self.cad2)-1)
            text += "Presiona la casilla OPT({},{}) para calcular la respuesta".format(len(self.cad1)-1,len(self.cad2)-1)
            self.anot.set(text= text)
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_m']) 
            env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_sol_handler)
            env.vars['mat'].celdas[self.n-1][self.m-1].rect.set(facecolor = '#FF00FF')
            env.vars['mat'].celdas[self.n-1][self.m-1].rect.set(alpha = .5)
            self.termina = True 
            return 
        mat = env.vars['mat']
        for j in range(0,self.m): 
            M = 0 
            x,y = mat.celdas[i][j].rect.get_xy() 
            if(self.cad1[i] == self.cad2[j]): 
                M = 1 
                if (0 <= i - 1 and 0 <= j -1): 
                    M = M + mat.celdas[i-1][j-1].valor
                    mat.celdas[i][j].ant = ((i-1,j-1))
            if(0 <= i - 1 and mat.celdas[i-1][j].valor > M): 
                M = mat.celdas[i-1][j].valor
                mat.celdas[i][j].ant = ((i-1,j))
            if( 0 <= j - 1 and mat.celdas[i][j-1].valor > M ):              
                M = mat.celdas[i][j-1].valor    
                mat.celdas[i][j].ant = ((i,j-1))
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
    #caso diagonal
    def caso_diag(self,i,j,u,v):
        text = "" 
        mat = env.vars['mat']
        if(self.cad1[i] == self.cad2[j]):
            if(self.valor_act <= 1 + mat.celdas[i-1][j-1].valor): 
                self.valor_act = 1 + mat.celdas[i-1][j-1].valor
                text += "1 + OPT({},{}) es\n".format(u,v)
                text += "mejor que el actual\n"
                text += "OPT({},{})={}".format(i,j,self.valor_act) 
            else: 
                text += "1 + OPT({},{}) no es\n".format(u,v)
                text += "mejor que el actual\n"
                text += "OPT({},{})={}".format(i,j,self.valor_act)
        else:  
            text += "Ya que ${}\\neq {}$\n".format(self.cad1[i],self.cad2[j])
            text += "no podemos considerar\n"
            text += "a OPT({},{})\n".format(u,v)
            text += "para calcular a OPT({},{})".format(i,j)
        mat.celdas[i][j].anot.set(text = self.valor_act)
        f = self.agregar_flecha(i,j,u,v) 
        self.flechas.append(f)
        self.anot_dial.set(text = text)
    #caso hacia la izquierda
    def caso_izq(self,i,j,u,v): 
        mat = env.vars['mat']
        text = ""
        if(self.valor_act <= mat.celdas[i][j-1].valor): 
            self.valor_act = mat.celdas[i][j-1].valor
            text += "El valor de OPT({},{}) es\n".format(u,v)
            text += "mejor o igual que el actual\n"
            text += "OPT({},{})={}".format(i,j,self.valor_act) 
        else: 
            text += "El valor de OPT({},{}) no es\n".format(u,v)
            text += "mejor que el actual\n"
            text += "OPT({},{})={}".format(i,j,self.valor_act) 
        mat.celdas[i][j].anot.set(text = self.valor_act)
        f = self.agregar_flecha(i,j,u,v) 
        self.flechas.append(f)
        self.anot_dial.set(text = text)
    #caso hacia arriba 
    def caso_arr(self,i,j,u,v): 
        mat = env.vars['mat']
        text = ""
        if( self.valor_act <= mat.celdas[i-1][j].valor): 
            self.valor_act = mat.celdas[i-1][j].valor
            text += "El valor de OPT({},{}) es\n".format(u,v) 
            text += "mejor o igual que el actual\n"
            text += "OPT({},{})={}".format(i,j,self.valor_act) 
        else: 
            text += "El valor de OPT({},{}) no es\n".format(u,v)
            text += "mejor que el actual\n"
            text += "OPT({},{})={}".format(i,j,self.valor_act) 
        mat.celdas[i][j].anot.set(text = self.valor_act)
        f = self.agregar_flecha(i,j,u,v) 
        self.flechas.append(f)
        self.anot_dial.set(text = text)
    def explicacion_sig_paso(self):
        if(not self.calculados[self.act_exp]): 
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
            env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.teclas_handler)   
            env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_click_handler)
            #limpiar las flechas y el cuadro de texto 
            text= "Haz click en la imagen, cada vez que presiones n calcularan \n"
            text += "los valores para la siguiente linea. Una vez calculados,\n"
            text += "puedes hacer click en las celdas para saber como fueron calculados."
            self.anot.set(text = text) 
            for f in self.flechas: 
                f.set(visible = False)
            self.anot_dial.set(visible = False)
            return  
        #toma algun vecino  
        i,j = self.act_exp 
        u,v = self.calculados[self.act_exp][0] 
        self.calculados[self.act_exp].pop(0)
        #si es diagonal 
        if(u == i -1 and v == j -1):
            self.caso_diag(i,j,u,v)
        elif(u == i -1 ): 
            self.caso_arr(i,j,u,v) 
        else :
            self.caso_izq(i,j,u,v) 
      
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
                self.act_exp = (i,j)
                #calculando los vecinos
                env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
                env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.explicacion_handler)
                env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_m']) 
                self.anot_dial.set(visible = True)
                vec = [] 
                if(0 <= i- 1): 
                    vec.append((i-1,j))
                if(0 <= j - 1): 
                    vec.append((i,j-1))
                if(0 <= j -1 and 0 <= i - 1): 
                    vec.append((i-1,j-1))
                text_d = ""
                self.calculados[(i,j)] = vec 
                if(self.cad1[i] == self.cad2[j]): 
                    text_d += "El valor inicial de OPT({},{})=1\n".format(i,j)
                    text_d += "ya que $ {}= {}$".format(self.cad1[i],self.cad2[j])
                    self.valor_act = 1 
                else: 
                    text_d += "El valor inicial de OPT({},{})=0\n".format(i,j)
                    text_d += "ya que ${}\\neq {}$".format(self.cad1[i],self.cad2[j])
                    self.valor_act = 0 
                text = ""
                text += "Cada vez que presiones n veras la explicaciones\n"
                text += "de cada una de las opciones que se tienen considerar\n"
                text += "para calcular OPT({},{})".format(i,j)
                self.anot.set(text = text)
                env.vars['mat'].celdas[i][j].anot.set(text = self.valor_act)
                self.anot_dial.set(text = text_d)
                self.anot_dial.set(position = (x+4,y+3))
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
    def generar_cadenas(self): 
        #que solo tome de un set de caracteres 
        letr = ['a','b','c','d','e']
        for i in range(0,random.randint(5,10)): 
            self.cad1 = self.cad1 + letr[random.randint(0,len(letr)-1)]
        for i in range(0,random.randint(5,10)): 
            self.cad2 = self.cad2 + letr[random.randint(0,len(letr)-1)]
    def crear_matriz(self): 
        self.generar_cadenas() 
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
    def init_dial(self): 
        props = dict(boxstyle='round', facecolor='wheat', alpha=1 ) 
        self.anot_dial = env.vars['ax'].text(0,0,"",va='top',fontsize = 8,bbox = props,visible = False)
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
    def init_anot(self): 
        text= "Haz click en la imagen, cada vez que presiones n calcularan \n"
        text += "los valores para la siguiente linea. Una vez calculados,\n"
        text += "puedes hacer click en las celdas para saber como fueron calculados." 
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.crear_matriz()
        self.dibujar_matriz() 
        env.vars['cid_m'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.mouse_click_handler)
        self.poner_etiquetas()
        self.init_dial() 
        self.init_anot() 

env = Env() 
env.vars['mat'] = None
env.vars['etq'] = None 
env.vars['fig'],env.vars['ax'] = plt.subplots() 
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
