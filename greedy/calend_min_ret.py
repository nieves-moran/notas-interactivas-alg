from cmath import atan
from glob import glob
from sys import ps1
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import math 
%matplotlib nbagg
def punto_med(x1,y1,x2,y2): 
    return (x1+y1/2), (x2 + y2)/2
class obtener_entrada: 
    boton = None  

class envn: 
    vars = dict() 
class peticion:
    pet = None
    rect = None 
    p1 = None 
    p2 = None 
    anot = None
    ret = None 
    ret_rect = None
    #anotacion en el retraso  
    ret_anot = None
class peticiones:
    elms = None  
    mm_x = None 
    mm_y = None
    def __init__(self): 
        self.elms = []
class Retraso: 
    linea = None 
    anot = None 
    valor = 0 
class ejecutar_algoritmo: 
    ordenados = False 
    #el ultimo intervalo  
    ult_int = None 
    ind = 0
    fig = None 
    boton_sig = None 
    box = None 
    ax = None
    peticiones = None
    ult_tiempo = 0
    retraso = None
    def config_botones(self):
        self.boton_sig = widgets.Button(description='sigiuente')
        self.boton_sig.on_click(self.boton_sig_handler)  
        self.box = widgets.VBox([self.boton_sig])
        display(self.box)
    def config_imagen(self): 
        self.fig, self.ax = plt.subplots()  
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.axis('off')
    def __init__(self): 
        self.config_imagen() 
        self.config_botones()
        self.obtener_posiciones() 
        print(self.peticiones.mm_x)
        print(self.peticiones.mm_y)
        self.ajusta_limites(self.peticiones.mm_x[0],self.peticiones.mm_y[0])
        self.ajusta_limites(self.peticiones.mm_x[1],self.peticiones.mm_y[1])
        self.dibujar_peticiones() 
    def dibujar_peticiones(self): 
        j = 0
        for p in self.peticiones.elms:
            r = Rectangle(p.p1,width = p.p2[0] - p.p1[0],height = 1,facecolor = 'white',edgecolor = 'black')
            x = p.p1[0] + r.get_width()/2
            y = p.p1[1] + 0.5 
            anot = self.ax.annotate("$i_{}$".format(j), (x,y) ,color='black', weight='bold', fontsize=14, ha='center', va='center')
            rt = Rectangle(p.ret,width = 0.1,height = 1)
            r_anot = self.ax.annotate("$i_{}$".format(j), (rt.get_xy()[0] + 0.5,rt.get_xy()[1]+0.5) ,color='black', weight='bold', fontsize=14, ha='center', va='center')
            self.ax.add_patch(r)
            self.ax.add_patch(rt) 
            p.rect = r 
            p.ret_rect = rt
            p.anot = anot 
            p.ret_anot = r_anot  
            j = j + 1
         
    def ajusta_limites(self,x,y):
        error = 1; 
        (xm,xM) = self.ax.get_xlim() 
        (ym,yM) = self.ax.get_ylim() 
        if x >= xM: 
            xM = x + error 
        if x <= xm: 
            xm = x -error 
        if y >= yM: 
            yM = y + error
        if y <= ym: 
            ym = y - error 
        self.ax.set_xlim(xm,xM)
        self.ax.set_ylim(ym,yM)
    #la linea de todos los intervalos va a estar en 0 
    def obtener_posiciones(self): 
        print("obtener posiciones")
        mx = float('0')
        Mx = float('-inf')
        my = float('0')
        My = float('-inf')
        y = 4
        pet = env.vars['peticiones']
        #p= [t,r] tiempo y retraso 
        self.peticiones = peticiones()
        for p in pet: 
            pt = peticion()
            pt.pet = p
            pt.p1 = [0,y]
            pt.p2 = [0 + p[0],y+1]
            pt.ret = [p[1],y]
            self.peticiones.elms.append(pt)
            #actualiza_limites
            mx = min(mx,pt.p1[0],pt.p2[0],pt.ret[0])
            Mx = max(Mx,pt.p1[0],pt.p2[0],pt.ret[0])
            my = min(my,pt.p1[1],pt.p2[1],pt.ret[1])
            My = max(My,pt.p1[1],pt.p2[1],pt.ret[1])
            y = y + 2  
        self.peticiones.mm_x = [mx,Mx]
        self.peticiones.mm_y = [my,My]
   
    def ordenar_pet(self): 
        self.peticiones.elms.sort(key = lambda p : p.pet[1])
        #reacomodarlos 
        y = 4 
        for p in self.peticiones.elms: 
            p.p1 = [p.p1[0],y]
            p.p2 = [p.p2[0],y+1] 
            p.rect.set(xy = p.p1)
            p.ret = [p.ret[0],y]
            p.ret_rect.set(xy = p.ret)
            p.anot.set(x= p.p1[0] + p.rect.get_width()/2)  
            p.anot.set(y = p.p1[1] + 0.5)
            p.ret_anot.set(y  = p.ret_rect.get_xy()[1] + 0.5) 
            p.ret_anot.set(x  = p.ret_rect.get_xy()[0] + 0.5) 
            y = y + 2 
    def boton_sig_handler(self,event): 
        if(self.ind == len(self.peticiones.elms) ): 
            return 
        if(not self.ordenados): 
            self.ordenar_pet()
            self.ordenados = True
        else: 
            sig_pet = self.peticiones.elms[self.ind]
            #ajustar la imagen 
            self.ajusta_limites(self.ult_tiempo + sig_pet.pet[0],0)
            #es 0 porque ahi (en esa y) estan los que vamos agregando
            sig_pet.rect.set(xy = (self.ult_tiempo,0))
            sig_pet.p1 = (self.ult_tiempo,0)
            sig_pet.p2 = (sig_pet.p1[0]+sig_pet.pet[0],1)
            self.ult_tiempo = self.ult_tiempo + sig_pet.pet[0]
            sig_pet.anot.set(x = sig_pet.p1[0] + sig_pet.rect.get_width()/2)
            sig_pet.anot.set(y = sig_pet.p1[1] + 0.5)
            self.ind = self.ind  + 1
            #poner y mover la linea de retraso  
            if(self.ult_tiempo > sig_pet.ret_rect.get_xy()[0]):   
                if(self.retraso == None): 
                    self.retraso = Retraso()
                    self.retraso.valor = self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]
                    self.retraso.linea = PathPatch(Path([(sig_pet.ret_rect.get_xy()[0],2),(self.ult_tiempo,2)]), edgecolor='red')
                    self.retraso.anot = self.ax.annotate("${}$".format(self.retraso.valor), (sig_pet.ret_rect.get_xy()[0] + self.retraso.valor/2,2.5) ,color='black', weight='bold', fontsize=10, ha='center', va='center')
                    self.ax.add_patch(self.retraso.linea) 
                else: 
                    if(self.retraso.valor < self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]): 
                        self.retraso.valor = self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]
                        self.retraso.anot.set(x = sig_pet.ret_rect.get_xy()[0] + self.retraso.valor/2)
                        self.retraso.anot.set(text = "${}$".format(self.retraso.valor))
                        self.retraso.linea.set(path = Path([(sig_pet.ret_rect.get_xy()[0],2),(self.ult_tiempo,2)]))
    
env = envn()
env.vars['peticiones'] = [(3,6),(5,10),(1,2),(3,12),(2,4),(5,17),(6,10),(3,6)]
estado = ejecutar_algoritmo() 