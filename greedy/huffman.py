from cmath import atan
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
out1 = widgets.Output()
display(out1)
#--------------------------------------
def frequencies(s): 
    freq = dict()
    for c in s: 
        if c in freq: 
            freq[c] = freq[c] + 1
        else: 
            freq[c] = 1
    its = freq.items() 
    ans = []
    for (c,i) in its: 
        ans.append((c,i/len(s)))
    return ans 
class get_text: 
    
    def ready_button_handler(self,event):  
        global texto
        texto = self.text.value
        clear_output()
        estado = run()
    
    def __init__(self): 
        self.ready_button = widgets.Button(description='Listo')
        self.ready_button.on_click(self.ready_button_handler)
        self.text = widgets.Text(description='texto:',disabled=False,value= "",placeholder='',)
        self.out = widgets.Output()
        self.box = widgets.VBox([self.text,self.ready_button,self.out])
        display(self.box)
#-------------------------------------
class nodo: 
    def __init__(self,val,freq): 
        self.val = val 
        self.freq = freq
        self.char = ''
        self.padre = None
        self.children = [] 
        
class arbol:
    def __init__(self): 
        self.root = nodo(0,0)
        self.val_node = dict() 
        self.val_coord = dict()
        self.val_node[0] = self.root
    def agregar(self,padre,val,freq,simb):
        nuevo = nodo(val,freq)
        nuevo.char = simb
        self.val_node[val] = nuevo
        self.val_node[padre].children.append(nuevo)
        nuevo.padre = padre 
    def aplastar_rec(self,node,ans,dpt): 
        for i in range(0,math.ceil(len(node.children)/2)): 
            self.aplastar_rec(node.children[i],ans,dpt+1)
        ans.append((node.val,dpt))
        for i in range(math.ceil(len(node.children)/2),len(node.children)):
            self.aplastar_rec(node.children[i],ans,dpt+1)
            
    def aplastar(self):
        ans = []
        self.aplastar_rec(self.root,ans,0)
        largest_d = -1
        for (v,d) in ans: 
            largest_d = max(largest_d,d)
        return (ans,largest_d)
    def obtener_coord(self): 
        rad = 1.0 
        (l,largest_d) = self.aplastar()
        largest_x = [2 for i in range(0,largest_d+1)] 
        dy = 3
        #el radio del circulo 
        r = 2 
        tree_rep = dict()
        for (v,d) in l: 
            if(self.val_node[v].children): 
                ch_ind = math.ceil(len(self.val_node[v].children)/2) -1 
                child = self.val_node[v].children[ch_ind].val
                (cx,cy) = self.val_coord[child]
                x = max(cx + r,largest_x[d]) 
            else: 
                x = largest_x[d] 
            largest_x[d] = x + 2*r 
            y = largest_d*dy - d*dy + 1 
            self.val_coord[v] = (x,y)
    
    def coord_hijos(self,u,maxx_depth): 
        rad = 1
        nh  = len(self.val_node[u].children)
        lc = (2*nh -1)*(2*rad)
        x,y = self.val_coord[u]
        x1 = max(float('-inf') if (y -3*rad) not in maxx_depth else maxx_depth[y-3*rad], x - lc/2 + rad)
        for i in range(0,nh): 
            self.val_coord[self.val_node[u].children[i].val] = (x1,y - 3*rad)
            x1 = x1 + 4*rad
            maxx_depth[y-3*rad] = x1 
            
    def obtener_coord2(self,x,y): 
        rad = 1
        queue = [0]
        self.val_coord[0] = (x,y)
        maxx_depth = dict()
        while(queue): 
            u = queue[0]
            queue.pop(0)
            self.coord_hijos(u,maxx_depth)
            for n in self.val_node[u].children: 
                queue.append(n.val)
        
def inter_points(rad,x1,y1,x2,y2): 
    phi = math.atan2(y2-y1, x2-x1)
    x = x1 + rad * math.cos(phi)
    y = y1 + rad * math.sin(phi)
    return (x,y)
def dibujar_arbol(tree,tree_rep,ax,edg_rep):
    #son los nodos invisibles 
    inv = [0]
    tree.obtener_coord2(15,20)
    rad = 1
    for v,(x,y) in tree.val_coord.items():
        if(v in tree_rep): 
            [c,frq_anot,char_anot,vis] = tree_rep[v]
            c.set(center = (tree.val_coord[v])) 
            frq_anot.set(x = tree.val_coord[v][0])
            frq_anot.set(y = tree.val_coord[v][1])
            char_anot.set(x = tree.val_coord[v][0])
            char_anot.set(y = tree.val_coord[v][1]-rad/2)
        else: 
            c = Circle((x,y),radius = rad,facecolor = 'white',edgecolor = 'black')
            freq_anot = ax.annotate(str(round(tree.val_node[v].freq,2)), (x, y),color='black', weight='bold', fontsize=7, ha='center', va='center')
            char_anot = ax.annotate(str(tree.val_node[v].char), (x, y-rad/2),color='black', weight='bold', fontsize=7, ha='center', va='center')
            vis = False if v in inv else True
            ax.add_patch(c)
            tree_rep[v] = [c,freq_anot,char_anot,vis]
        if(not tree_rep[v][3]): 
            tree_rep[v][0].set(visible = False)
            tree_rep[v][1].set(visible = False)
            tree_rep[v][2].set(visible = False)
    queue = []
    queue.append(0) 
    #limpiar el diccionario de aristas 
    for _,l in edg_rep.items(): 
        l[0].set(visible = False)
    edg_rep.clear()
    while(queue): 
        u = queue[0]
        queue.pop(0)
        for n in tree.val_node[u].children: 
            v = n.val 
            xu,yu = tree_rep[u][0].get_center()
            xv,yv = tree_rep[v][0].get_center()
            linea = PathPatch(Path([inter_points(rad,xu,yu,xv,yv),inter_points(rad,xv,yv,xu,yu)]), facecolor='none', edgecolor='black')
            ax.add_patch(linea)
            if(u in inv):
                linea.set(visible = False) 
            queue.append(v)  
            #necesito que u y v esten en orden por eso creo este temporal 
            temp = [u,v]
            temp.sort()
            edg_rep[(temp[0],temp[1])] = [linea]
                    
class run:  
    #tree 
    #ordenados los simbolos 
    #ax,tree,tree_rep,edg_rep
    def onclick(self,event):
        st = "nada"
        os.write(1, st.encode())
    def poner_nodos_iniciales(self,freq): 
        #al cero le agregamos todos
        i = 1
        for (s,f) in freq: 
            self.tree.agregar(0,i,f,s)

            i = i + 1
        #hacemos invisible al 0
        
    def next_button_handler(self,event):
        global cid
        #cuando los hijos de la raiz sea uno 
        if(len(self.tree.val_node[0].children) <= 1): 
            clear_output()
            estado = codification(self.tree)
            return
        #tomar los dos nodos hijos del 0 que tienen la frecuencia mas chica 
        lista = []
        for n in self.tree.val_node[0].children: 
            if(n.val != 0): 
                lista.append((n.freq,n))
        lista.sort(key = (lambda elem : elem[0]))
        #tomas los dos primeros n1 n2 
        n1 = lista[0][1]
        lista.pop(0)
        n2 = lista[0][1]
        lista.pop(0)
        n_node = nodo(len(self.tree.val_node),n1.freq + n2.freq)
        self.tree.val_node[len(self.tree.val_node)] = n_node
        n1.padre = n_node.val 
        n2.padre = n_node.val
        n_node.children = [n1,n2]
        #eliminar hijos del 0
        self.tree.val_node[0].children.remove(n1)
        self.tree.val_node[0].children.remove(n2)
        self.tree.val_node[0].children.append(n_node)
        n_node.padre = 0 
        dibujar_arbol(self.tree,self.tree_rep,self.ax,self.edg_rep) 
    def plt_config(self): 
        global cid
        self.fig, self.ax = plt.subplots()
        self.maxim_x = 40
        self.maxim_y = 25
        plt.xticks(range(1,self.maxim_x))
        plt.yticks(range(1,self.maxim_y))   
        plt.gca().set_aspect('equal', adjustable='box')
    def button_config(self): 
        self.next_button = widgets.Button(description='Listo')
        self.next_button.on_click(self.next_button_handler)
        self.out = widgets.Output()
        self.box = widgets.VBox([self.next_button,self.out])
        display(self.box)
    def __init__(self,freq): 
        print(freq)
        rad = 1.0 
        self.edg_rep = dict()
        global texto
        self.plt_config()
        self.tree_rep = dict()
        self.tree = arbol()
        self.poner_nodos_iniciales(freq)
        dibujar_arbol(self.tree,self.tree_rep,self.ax,self.edg_rep)
        self.button_config()
    

#------------------------------------------------ 
"""
tree val_node, val_coord 
tree_rep  [c el circulo ,freq_anot la anotacion de frecuencia ,char_anot : la anotacion de caracter,vis si es visible o no]
edg_rep es un diccionario donde las llaves son parejas y el contenido es una linea 
"""
class codification: 
    codif = None
    def plt_config(self): 
        global cid
        self.fig, self.ax = plt.subplots()
        plt.figure(self.fig.number)
        self.maxim_x = 40
        self.maxim_y = 25
        plt.xticks(range(1,self.maxim_x))
        plt.yticks(range(1,self.maxim_y))
        plt.gca().set_aspect('equal', adjustable='box')

    def handler_char_button(self,event): 
        self.pintar_camino(self.char_node[event.description])

    def buttons_config(self): 
        children = [] 
        for (c,v) in self.char_node.items(): 
            button = widgets.Button(description=str(c))
            button.on_click(self.handler_char_button)
            children.append(button)
        self.box = widgets.VBox(children)
        display(self.box)
    #s es la separacion 
    def punto_medio(self,x1,y1,x2,y2,s): 
        dx = x1 - x2 
        dy = y1 - y2 
        ang = (math.pi/2 if dy > 0 else (3*math.pi)/2) if dx == 0 else math.atan(dy/dx)
        ang = ang + 2* math.pi if ang < 0 else ang
        x = (math.sqrt((x1- x2)**2 + (y1 - y2)**2))/2
        y = s 
        xp = x*math.cos(ang) - y*math.sin(ang)
        yp = x*math.sin(ang) + y*math.cos(ang)
        xp = xp + x1 if dx*dy > 0 else xp + x2 
        yp = yp + y1 if dx*dy > 0 else yp + y2 
        return (xp,yp)
    def anotar_aristas(self): 
        inv = [0]
        for (u,v) in self.edg_rep.keys(): 
            x1,y1 = self.tree.val_coord[u]
            x2,y2 = self.tree.val_coord[v]
            xp,yp = self.punto_medio(x1,y1,x2,y2,0.5)
            an = self.ax.annotate('',(xp,yp),color='black', weight='bold', fontsize=7, ha='center', va='center')
            self.edg_rep[(u,v)].append(an)
        for v,n in self.tree.val_node.items():
            if(v == 0): 
                continue
            p = n.padre
            if(v in inv or p in inv): 
                continue 
            if(v == self.tree.val_node[p].children[0].val):
                temp = [v,p]
                temp.sort() 
                self.edg_rep[(temp[0],temp[1])][1].set(text = '0')
            else: 
                temp = [v,p]
                temp.sort() 
                self.edg_rep[(temp[0],temp[1])][1].set(text = '1')

    def __init__(self,tree):
        self.painted_edgs = []
        self.tree = tree
        self.tree_rep = dict()
        self.edg_rep = dict()
        self.plt_config()
        dibujar_arbol(self.tree,self.tree_rep,self.ax,self.edg_rep)
        self.anotar_aristas()
        self.map_char_node()
        self.buttons_config()
    def map_char_node(self): 
        self.char_node = dict()
        for (v,n) in self.tree.val_node.items():
            if(n.char != ''): 
                self.char_node[n.char] = v 
    #esta función pinta el camino pero también halla la codificación 
    def pintar_camino(self,n): 
        current = n; 
        #mientras current es distinto de la raiz 
        #limpiarlos 
        codif = ""
        for e in self.painted_edgs: 
            e.set(color = 'black')
            e.set(linewidth = 1)
        self.painted_edgs = [] 
        while(current != 0): 
            temp = [current,self.tree.val_node[current].padre]
            temp.sort()
            self.edg_rep[(temp[0],temp[1])][0].set(color = 'blue')
            self.edg_rep[(temp[0],temp[1])][0].set(linewidth = 3)
            codif = codif + self.edg_rep[(temp[0],temp[1])][1].get_text()
            self.painted_edgs.append(self.edg_rep[(temp[0],temp[1])][0])
            current = self.tree.val_node[current].padre

        #pone la letra y la codificacion
        #cod_str = codif[::-1][1:]
        cod_str = self.tree.val_node[n].char + " : " + codif[::-1]
        if (self.codif == None): 
            self.codif = self.ax.annotate(cod_str, (20, 19),color='black', weight='bold', fontsize=7, ha='center', va='center')
        else: 
            self.codif.set(text = cod_str )
 #   boton siguiente
  #  toma una letra 
   # dibuja el camino 
    #pon la codificacion 
cid = None
texto = ""
estado = run(frequencies("lkadjfjadljfldkfaidfajldihfaiwueyriewyroiyueowryuuirywidfkjadl"))