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
import os
%matplotlib nbagg


display(out1)
class Env: 
    vars = dict()

def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
                    
class run:  
    vertices = dict()
    def config_imagen(self): 
        env.vars['ax'].set_yticks([])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplots_adjust(bottom=0.3)
        self.ax_anot = plt.axes([0.1, 0.1, 0.8, 0.15])
        plt.axis("off")
    def poner_vertices(self): 
        posiciones = [(0,0),
                        (-2,-5),(6,-5),
                        (-4,-10),(0,-10),(4,-10),(8,-10), 
                        (-6,-15),(-2,-15)]; 
        i = 0
        for (x,y) in posiciones : 
              self.vertices[i] = Circle((x,y),radius = 1,facecolor = 'white',edgecolor = 'black') 
              env.vars['ax'].add_patch(self.vertices[i])
              i = i + 1
        return 
    def poner_aristas(self): 
        return 

    def __init__(self):
        self.config_imagen()
        # poner un circulo 
        self.poner_vertices()  
        self.poner_aristas() 
        env.vars['ax'].relim()
        env.vars['ax'].autoscale_view()
        

env = Env() 
env.vars['fig'],env.vars['ax'] = plt.subplots()
maxim_x = 10
maxim_y = 10
r = run() 