
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
import random 
import math 
%matplotlib nbagg

#antes de dibujar tienes que ajustar 
out1 = widgets.Output()
display(out1)
#es un diccionario es el ambiente
class Env: 
    vars = dict() 

class Peticion:
    pet = None
    rect = None 
    p1 = None 
    p2 = None 
    anot = None
    ret = None 
    ret_rect = None
    #anotacion en el retraso  
    ret_anot = None
class Peticiones:
    elms = None  
    def __init__(self): 
        self.elms = []
class Retraso: 
    linea = None 
    anot = None 
    valor = 0 
class Ejecucion:   
    peticiones = Peticiones()
    ordenados = False  
    ind = 0 
    retraso = None 
    ult_tiempo = 0 
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
    def dibujar_peticiones(self,peticiones): 
        j = 0
        x = 0 
        y = 3*env.vars['rad'] 
        for [t,d] in peticiones:
            r = Rectangle((x,y),width = t,height = 1,facecolor = 'white',edgecolor = 'black')
            anot =  env.vars['ax'].text(x +t/2, y + 0.5,"$t_{{ {} }}$".format(j),fontsize = 9,va = 'center',ha = 'center')
            rt = Rectangle((d,y),width = 0.1,height = 1)
            r_anot =  env.vars['ax'].text(d +0.5, y+0.5,"$d_{{ {} }}$".format(j),fontsize = 9,va = 'center',ha = 'center')
            env.vars['ax'].add_patch(r)
            env.vars['ax'].add_patch(rt) 
            p = Peticion() 
            p.p1 = [0,y]
            p.p2 = [0 + t,y+1]
            p.pet = [t,d]
            p.rect = r 
            p.ret = [d,y]
            p.ret_rect = rt
            p.anot = anot 
            p.ret_anot = r_anot
            self.peticiones.elms.append(p)
            y = y + env.vars['rad']*3  
            j = j + 1
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
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
            y = y + 3 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def siguiente_paso(self):
        if(self.ind == len(self.peticiones.elms) ): 
            return 
        if(not self.ordenados): 
            self.ordenar_pet()
            self.ordenados = True
        else: 
            sig_pet = self.peticiones.elms[self.ind]
            #es 0 porque ahi (en esa y) estan los que vamos agregando
            sig_pet.rect.set(xy = (self.ult_tiempo,0))
            sig_pet.p1 = (self.ult_tiempo,0)
            sig_pet.p2 = (sig_pet.p1[0]+sig_pet.pet[0],1)
            sig_pet.anot.set(x = sig_pet.p1[0] + sig_pet.rect.get_width()/2)
            sig_pet.anot.set(y = sig_pet.p1[1] + 0.5)
            self.ult_tiempo = self.ult_tiempo + sig_pet.pet[0]
            self.ind = self.ind  + 1
            #poner y mover la linea de retraso  
            if(self.ult_tiempo > sig_pet.ret_rect.get_xy()[0]):   
                if(self.retraso == None): 
                    self.retraso = Retraso()
                    self.retraso.valor = self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]
                    self.retraso.linea = PathPatch(Path([(sig_pet.ret_rect.get_xy()[0],2),(self.ult_tiempo,2)]), edgecolor='red')
                    self.retraso.anot = env.vars['ax'].text(sig_pet.ret_rect.get_xy()[0] + self.retraso.valor/2, 2.5,"${}$".format(self.retraso.valor),color='black', weight='bold', fontsize=10, ha='center', va='center')
                    env.vars['ax'].add_patch(self.retraso.linea) 
                else: 
                    if(self.retraso.valor < self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]): 
                        self.retraso.valor = self.ult_tiempo - sig_pet.ret_rect.get_xy()[0]
                        self.retraso.anot.set(x = sig_pet.ret_rect.get_xy()[0] + self.retraso.valor/2)
                        self.retraso.anot.set(text = "${}$".format(self.retraso.valor))
                        self.retraso.linea.set(path = Path([(sig_pet.ret_rect.get_xy()[0],2),(self.ult_tiempo,2)]))
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()

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
    
    def crear_peticiones_aleatorias(self): 
        peticiones = [] 
        for i in range(0,random.randint(5,10)):
            t = random.randint(5,15)
            d = random.randint(t + 1,t + 50) 
            peticiones.append([t,d])
        return peticiones 
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.dibujar_peticiones(self.crear_peticiones_aleatorias())  

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
 