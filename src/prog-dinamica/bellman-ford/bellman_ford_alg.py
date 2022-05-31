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
    destino = None 
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
    ant = -1 
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

def arb_dirigido(arb,destino):
    g =dict() 
    for u,v in arb: 
        g[u] = [] 
        g[v] = []
    for u,v in arb: 
        g[u].append(v)
        g[v].append(u)
    cola = [destino]
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
    destino = random.randint(0,len(verts)-1)
    env.vars['g'].destino = destino 
    arb = arb_dirigido(arb,destino)
    ars_p = [] 
    for (u,v) in arb: 
        p = random.randint(-20,30)
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
    ind = 1 
    g_inv = dict()
    camino_col = []  
    ax_anot = None 
    anot =None 
    calculados = dict() 
    par_act = None 
    flechas =  []
    val_act = float('inf')
    ar_col = []
    sol_par = None 
    f_sol = [] 
    ar_sol = [] 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        self.zoom_mas() 
        self.zoom_mas() 
    def init_anot(self): 
        text= "Haz click en la imagen, cada vez que presiones n se ejecutara \n"
        text += "el siguiente paso del algoritmo." 
        text += "Cuando hayas generado algunos valores puedes\n"
        text += "hacer click en las celdas para ver paso a paso\n"
        text += "el calculo de su valor."
        self.anot = self.ax_anot.text(0.1,0.7,text,va = 'top',ha = "left")
    
    def camino(self,v,j): 
        sol = [v]
        mat = env.vars['mat']
        if(mat.celdas[v][j].valor == float('inf')): 
            return [] 
        else: 
            while(j > 0): 
                if(mat.celdas[v][j].ant == -1): 
                    j = j - 1 
                else: 
                    sol.append(mat.celdas[v][j].ant)
                    v = mat.celdas[v][j].ant 
                    j = j - 1 
        return sol 
 
    
    def calcular_sol(self):
        for f in self.f_sol: 
            f.set(visible = False)
        self.f_sol = [] 
        for ni,nu,a in self.ar_sol: 
            ni.set(facecolor = 'white')
            nu.set(facecolor = 'white')
            a.set(color = 'black')
        i,j = self.sol_par
        mat = env.vars['mat'] 
        g = env.vars['g']
        while(j != 0):
            u = mat.celdas[i][j].ant
            v = j - 1
            f = self.agregar_flecha(i,j,u,v)
            ni = g.pos_nodos[i].img
            ni.set(facecolor = '#66FF66')
            nu = g.pos_nodos[u].img
            nu.set(facecolor = '#66FF66')
            a = None 
            if u in g.ady[i]: 
                a = g.ady[i][u].linea 
                a.set(color = '#009900')
                self.ar_sol.append((ni,nu,a))
            self.f_sol.append(f)
            j = v
            i = u 
    @out1.capture() 
    def handler_respuesta(self,event): 
        if(event.xdata == None or event.ydata == None): 
            return 
        xe,ye = event.xdata, event.ydata 
        g = env.vars['g']
        n = len(g.pos_nodos)
        mat = env.vars['mat']
        for i in range(0,n): 
            x,y = mat.celdas[i][n - 1].rect.get_xy() 
            if(x <= xe <= x + 2 and y <= ye <= y + 2 ): 
                self.sol_par = (i,n-1)
                self.calcular_sol() 
    def siguiente_paso(self):
        j = self.ind 
        mat = env.vars['mat']
        g = env.vars['g']
        n = len(mat.celdas)
        if(j == n):
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_mp'])
            env.vars['cid_mp'] = env.vars['fig'].canvas.mpl_connect('button_press_event',self.handler_respuesta)
            for i in range(0,n): 
                mat.celdas[i][n-1].rect.set(facecolor = '#66FF66')
            text = "Presiona alguno de los cuadrados verdes para ver el camino mas \n"
            text += "corto en la grafica. La secuencia de flechas son las opciones optimas\n"
            text += "para cada casilla. \n"
            text += "Recuerda que puedes hacer la imagen mas grande con +."
            self.anot.set(text = text)
            return 
        dp = mat.celdas
        for i in range(0,n): 
            dp[i][j].valor = dp[i][j-1].valor
            dp[i][j].ant = i
            for w,nodo in g.ady[i].items():  
                if((dp[w][j-1].valor + nodo.peso if dp[w][j-1].valor != float('inf') else float('inf')) <= dp[i][j].valor): 
                    dp[i][j].valor = dp[w][j-1].valor + nodo.peso if dp[w][j-1].valor != float('inf') else float('inf')  
                    if(dp[i][j].valor != float('inf')): 
                        dp[i][j].ant = w
                else:  
                    dp[i][j].valor = dp[i][j].valor
            self.calculados[(i,j)] = [] 
            dp[i][j].anot.set(text = "{}".format("$\infty$" if  dp[i][j].valor == float('inf') else dp[i][j].valor))
        self.ind = j + 1 
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
    def inicializar_matriz(self):
        g = env.vars['g']
        m = env.vars['mat'] 
        n = len(m.celdas)
        destino = g.destino 
        for i in range(0,n):
            m.celdas[i][0].valor = float('inf')
            m.celdas[i][0].anot.set(text = "$\infty$")
        print(destino)
        for i in range(0,n):
            m.celdas[destino][i].valor = 0  
            m.celdas[destino][i].anot.set(text = "{}".format(0))
    

    def agregar_flecha(self,i,j,u,v):
        mat = env.vars['mat']
        x1,y1 = mat.celdas[i][j].rect.get_xy() 
        x1 += 1
        y1 += 1 
        x2,y2 = mat.celdas[u][v].rect.get_xy()
        x2 += 1
        y2 += 1
        (x1,y1),(x2,y2) = inter_points(0.5,x1,y1,x2,y2),inter_points(0.5,x2,y2,x1,y1) 
        return env.vars['ax'].arrow(x1,y1, x2-x1, y2-y1,width = 0.2,head_length = 1,facecolor = 'white',length_includes_head = True) 
    
    def exp_siguiente_paso(self):
        if(not self.calculados[self.par_act]): 
            env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
            env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.teclas_handler)        
            env.vars['cid_mp'] = env.vars['fig'].canvas.mpl_connect('button_press_event',self.handler_mouse_press)
            for f in self.flechas: 
                f.set(visible = False)
            self.anot_dial.set(visible = False )
            self.val_act = float('inf')
            for f in self.ar_col: 
                f.set(color = 'black')
            text= "Haz click en la imagen, cada vez que presiones n se ejecutara \n"
            text += "el siguiente paso del algoritmo." 
            text += "Cuando hayas generado algunos valores puedes\n"
            text += "hacer click en las celdas para ver paso a paso\n"
            text += "el calculo de su valor."
            self.anot.set(text =text)
            return 
        i,j = self.par_act 
        mat = env.vars['mat']
        g = env.vars['g']
        u,v = self.calculados[self.par_act][0] 
        self.calculados[self.par_act].pop(0)
        if(i == u): 
            f = self.agregar_flecha(i,j,u,v)
            self.flechas.append(f)
            text = "$OPT({},{})=$\n".format(i,j)
            text += "$min(OPT({},{}),OPT({},{}))=$\n".format(i,j,u,v)
            text += "$min({},{})$=".format('\infty' if self.val_act == float('inf') else self.val_act ,'\infty' if mat.celdas[u][v].valor == float('inf') else mat.celdas[u][v].valor)
            text += "${}$".format('\infty' if min(self.val_act,mat.celdas[u][v].valor) == float('inf') else min(self.val_act,mat.celdas[u][v].valor))
            self.anot_dial.set(text = text)
        else: 
            f = self.agregar_flecha(i,j,u,v)
            self.flechas.append(f)
            text = "OPT({},{}) =\n".format(i,j)
            text += "$min(OPT({},{}),\lambda_{{({},{})}} + OPT({},{}))=$\n".format(i,j,i,u,u,v)
            val_acts = "\infty" if float('inf') == self.val_act else  str(self.val_act) 
            text += "$min({},{}+{})=$\n".format(val_acts,g.ady[i][u].peso,
                                                '\infty' if mat.celdas[u][v].valor == float('inf') else mat.celdas[u][v].valor)
            text += "$min({},{})=$".format(val_acts,
                                            '\infty' if g.ady[i][u].peso + mat.celdas[u][v].valor == float('inf') else g.ady[i][u].peso + mat.celdas[u][v].valor )
            text += "${}$".format('\infty' if min(self.val_act,g.ady[i][u].peso + mat.celdas[u][v].valor) == float('inf') else min(self.val_act,g.ady[i][u].peso + mat.celdas[u][v].valor))
            self.val_act = min(self.val_act,g.ady[i][u].peso + mat.celdas[u][v].valor)
            mat.celdas[i][j].anot.set(text =  '$\infty$' if min(self.val_act,g.ady[i][u].peso + mat.celdas[u][v].valor) == float('inf') else min(self.val_act,g.ady[i][u].peso + mat.celdas[u][v].valor) )
            self.anot_dial.set(text = text)
            f = g.ady[i][u].linea
            f.set(color = '#009900')
            self.ar_col.append(f)

    @out1.capture()
    def explicacion_handler(self,event): 
        if(event.key == 'n'): 
            self.exp_siguiente_paso() 
        if(event.key == '-'):
            self.zoom_menos()  
        elif(event.key == '+'): 
            self.zoom_mas() 
    @out1.capture()
    def handler_mouse_press(self,event):
        if(event.xdata == None or event.ydata == None): 
            return 
        xe,ye = event.xdata, event.ydata 
        g = env.vars['g']
        n = len(g.pos_nodos)
        mat = env.vars['mat']
        for i in range(0,n): 
            for j in range(0,n):  
                x,y = mat.celdas[i][j].rect.get_xy()
                if(x <= xe <= x + 2 and y <= ye <= y +2 and (i,j) in self.calculados): 
                    env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_t']) 
                    env.vars['fig'].canvas.mpl_disconnect(env.vars['cid_mp']) 
                    env.vars['cid_t'] = env.vars['fig'].canvas.mpl_connect('key_press_event', self.explicacion_handler)
                    for u,nodo in env.vars['g'].ady[i].items(): 
                        self.calculados[(i,j)].append((u,j-1))
                    self.calculados[(i,j)].append((i,j-1))
                    self.par_act = (i,j)
                    x,y = mat.celdas[i][j].rect.get_xy() 
                    self.anot_dial.set(position = (x+3,y+2))
                    self.anot_dial.set(visible = True)
                    text_d = "$OPT({},{})=\infty$".format(i,j)
                    env.vars['mat'].celdas[i][j].anot.set(text = '$\infty$')
                    self.anot_dial.set(text = text_d)
                    text = "Cada vez que presiones n veras las diferentes opciones que\n"
                    text += "tiene esta celda para calcular el valor optimo."
                    self.anot.set(text = text)
    def limpiar_camino(self): 
        g = env.vars['g']
        for i in range(0,len(self.camino_col)-1): 
                        g.ady[self.camino_col[i]][self.camino_col[i+1]].linea.set(color = 'black')
        self.camino_col = []
    @out1.capture() 
    def handler_mouse_release(self,event):
        self.limpiar_camino()
    def config_mouse(self): 
        env.vars['cid_mp'] = env.vars['fig'].canvas.mpl_connect('button_press_event', self.handler_mouse_press)
        env.vars['cid_mr'] = env.vars['fig'].canvas.mpl_connect('button_release_event', self.handler_mouse_release)
    
    def init_dial(self): 
        props = dict(boxstyle='round', facecolor='wheat', alpha=1 ) 
        self.anot_dial = env.vars['ax'].text(0,0,"",va='top',fontsize = 8,bbox = props,visible = False)
    
    def __init__(self): 
        crear_aleatoria() 
        self.n = len(env.vars['g'].pos_nodos.keys())
        self.config_imagen()
        self.config_teclas()
        self.crear_matriz() 
        self.dibujar_matriz() 
        self.poner_etiquetas() 
        self.inicializar_matriz() 
        self.config_mouse() 
        self.init_anot() 
        self.init_dial() 

env = Env() 
env.vars['g'] = Grafica()
env.vars['mat'] = None 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['cid_mp'] = None
env.vars['cid_mr'] = None 
env.vars['e1'] = Ejecucion() 
