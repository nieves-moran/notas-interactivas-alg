
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
    indice = None 
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
    anots = dict() 
    linea = None
    def config_imagen(self): 
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        plt.axis("off")
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
        env.vars['ax'].set(yticks=[]) 
    def ajustar(self): 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
        xmin,xmax = env.vars['ax'].get_xlim()
        env.vars['ax'].add_patch(Circle((xmax + 1,0),visible = False)) 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()   
    def dibujar_peticiones(self,peticiones): 
        j = 0
        x = 0 
        y = 3*env.vars['rad'] 
        for [t,d] in peticiones:
            r = Rectangle((x,y),width = t,height = 1,facecolor = 'white',edgecolor = 'black')
            anot =  env.vars['ax'].text(x +t/2, y + 0.5,"$t_{{ {} }}={}$".format(j,t),fontsize = 9,va = 'center',ha = 'center')
            rt = Rectangle((d,y),width = 0.1,height = 1)
            r_anot =  env.vars['ax'].text(d +1, y+0.5,"$d_{{ {} }}={}$".format(j,d),fontsize = 9,va = 'center')
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
            p.indice = j
            self.peticiones.elms.append(p)
            y = y + env.vars['rad']*3  
            j = j + 1
        ##hacerla un poco más grande
        self.ajustar() 
    def actualizar_linea(self,ult_tiempo):
        if(self.linea == None ):  
            p1 = 0,-1.5
            p2 = (ult_tiempo,-1.5)
            self.linea = PathPatch(Path([p1,p2]))
            env.vars['ax'].add_patch(self.linea)
            env.vars['ax'].text(p1[0],p1[1]-1.5,"0",va='center',ha='center') 
        else: 
            p1 = self.linea.get_path().vertices[0]
            p2 =  self.linea.get_path().vertices[1]
            p2[0] = ult_tiempo
            path = [p1,p2]
            self.linea.set_path(Path(path)) 
        env.vars['ax'].text(p2[0],p2[1]-1.5,ult_tiempo,va='center',ha='center')

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
            p.ret_anot.set(x  = p.ret_rect.get_xy()[0] + 1) 
            y = y + 3 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
    def cambiar_anotaciones(self,trabajo,retraso,retraso_max): 
        self.anots['linea1'].set(text = "-Se calendarizo el trabajo $i_{{{}}}$".format(trabajo))
        self.anots['linea2'].set(text = "-El retraso del trabajo es {}".format(retraso))
        self.anots['linea3'].set(text = "-El retraso maximo en rojo es {}".format(retraso_max))
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
            retraso = max(self.ult_tiempo - sig_pet.ret_rect.get_xy()[0],0)   
            trabajo = sig_pet.indice 
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
            retraso_max = max(0,self.retraso.valor if self.retraso != None else 0)
            self.cambiar_anotaciones(trabajo,retraso,retraso_max) 
            self.actualizar_linea(self.ult_tiempo)
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
        for i in range(0,random.randint(5,7)):
            t = random.randint(5,10)
            d = random.randint(t + 1,t + 30) 
            peticiones.append([t,d])
        return peticiones 
    def poner_anotaciones(self): 
        self.anots['linea1'] = self.ax_anot.text(0.1,0.7,"")
        self.anots['linea2'] = self.ax_anot.text(0.1,0.4,"" )
        self.anots['linea3'] = self.ax_anot.text(0.1,0.1,"")
    def __init__(self): 
        self.config_imagen()
        self.config_teclas()
        self.dibujar_peticiones(self.crear_peticiones_aleatorias())
        self.poner_anotaciones()   

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()
env.vars['rad'] = 1 
env.vars['cid_t'] = None
env.vars['e1'] = Ejecucion() 
 