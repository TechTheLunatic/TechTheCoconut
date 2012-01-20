# -*- coding: utf-8 -*-

from graph_tool.all import *
import os,sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from outils_math.collisionRectangleCase import collisionRectangleCase
from outils_math.point import Point
from outils_math.rectangle import Rectangle

#TODO lien avec constantes dans profil
tableLargeur = 200.
tableLongueur = 300.
coteRobot = 50.

#TODO lien avec éléments de jeu
#listeObjets=[Rectangle(120.,120.,0.52,19.,100.),Rectangle(50.,150.,0.,50.,40.),Rectangle(150.,150.,-0.3,90.,20.)]
listeObjets=[Rectangle(50,50,0.,10.,10.)]

#déclaration du graphe, avec tables de propriétés : structure de données optimale pour les noeuds
g = Graph(directed=False)
posX = g.new_vertex_property("int")
posY = g.new_vertex_property("int")
poids = g.new_edge_property("double")

Nstruct = 10 #nb de noeuds de structure placés à la racine. il servent à pointer d'autres noeuds
"""
g.vertex(0) pointe sur le noeud de départ
g.vertex(1) pointe sur le noeud d'arrivé
"""

#poids des arêtes, tenant compte du déplacement en diagonale avec sqrt(2)
poidsDirect = 1.
poidsDiag = 1.41

pas = 10 # pas en mm
longueur = int(tableLongueur/pas)
largeur = int(tableLargeur/pas)
#centrage de l'axe des abscisses
axeX=-(tableLongueur-pas)/2
axeY=0#-(0-pas)/2

#élargissement des objets : les noeuds concernent les zones accessibles par le centre du robot
largeurRobot=coteRobot*1.414#sqrt(2)
for o in listeObjets:
    o.wx += largeurRobot
    o.wy += largeurRobot


def rechercheChemin(depart,arrive):
    """
    fonction de recherche de chemin, utilisant le meilleur algorithme codé
    """
    
    print "discretiseTable -->"
    #g=load_graph("map_vierge.xml")

    #noeuds de structures, servant de pointeurs
    for k in range(Nstruct):
        g.add_vertex()
    discretiseTable()

    #g.save("map_vierge.xml")
    
    #masque les pointeurs
    posX[g.vertex(0)]=int((depart.x)/pas)*pas-pas/2
    posY[g.vertex(0)]=int((depart.y)/pas)*pas
    posX[g.vertex(1)]=int((arrive.x)/pas)*pas-pas/2
    posY[g.vertex(1)]=int((arrive.y)/pas)*pas
    
    #calcul l'index initial des noeuds de départ et d'arrivée 
    Ndepart=( int((depart.x-axeX)/pas)*pas + int((depart.y-axeY)/pas)*pas*longueur )/pas
    Narrive=( int((arrive.x-axeX)/pas)*pas + int((arrive.y-axeY)/pas)*pas*longueur )/pas

    #définit les noeuds correspondant aux points de départ et d'arrivée
    Ndepart=g.vertex(Nstruct+Ndepart)
    Narrive=g.vertex(Nstruct+Narrive)
    
    #pointeurs sur départ et arrivé
    g.add_edge(g.vertex(0),Ndepart)
    g.add_edge(g.vertex(1),Narrive)
    
    supprimerInaccessibles()
    
    for n in g.vertex(0).out_neighbours():
        Ndepart=n
    for n in g.vertex(1).out_neighbours():
        Narrive=n
    return AStar(Ndepart,Narrive)

def AStar(Ndepart,Narrive):
    """
    algorithme A*, sur une table de jeu discrétisée "par cases"
    """
    
    #TODO : algorithme A* sur le graphe obtenu
    #dist, pred = gt.astar_search(g, g.vertex(Nstruct+0), weight, VisitorExample(touch_v, touch_e, target), heuristic=lambda v: h(v, target, pos))
    #TODO : retour de la structure cheminObtenu
    print "tracePDF -->"
    tracePDF()
    
def supprimerInaccessibles():
    """
    retire du graphe les noeuds entrant en collision avec les objets inaccessibles de la table de jeu
    """
    
    print "supprimerNoeuds -->"
    listeNoeuds=[]
    #itération sur les objets
    for objet in listeObjets:
        #trouve directement un noeud en collision avec l'objet en arrondissant les coordonnées de ce dernier
        n=( int((objet.x-axeX)/pas)*pas + int((objet.y-axeY)/pas)*pas*longueur )/pas
        if(n > longueur*largeur):
            n -= longueur
        elif(n<0):
            n += longueur
        n=g.vertex(Nstruct+n)
        #n=g.vertex(Nstruct+(int((objet.x-axeX)/pas)*pas+int((objet.y-axeY)/pas)*pas*longueur)/pas)
        #recherche les autres noeuds en collision par récurrence sur les noeuds voisins. complexité proportionnelle à l'aire de l'objet.
        listeNoeuds.extend(listerNoeuds(objet,[n],[n],[]))
    listeNoeuds=sorted(list(set(listeNoeuds)),reverse=True)
    supprimerNoeuds(listeNoeuds)

    
def supprimerNoeuds(listeNoeuds):
    listeNoeuds = map(lambda v: g.vertex(Nstruct+v),listeNoeuds)
    for n in listeNoeuds:
        g.remove_vertex(n)
    
def NoeudsVoisins(noeud,registreVoisins):
    nouveaux=[]
    for v in noeud.out_neighbours():
        if not (v in registreVoisins):
            nouveaux.append(v)
    return nouveaux   
    
def listerNoeuds(objet,registreVoisins,aParcourir,listeNoeuds):
    while aParcourir!=[]:
        noeud=aParcourir.pop()
        if collisionRectangleCase(objet,Point(posX[noeud],posY[noeud]),pas):
            listeNoeuds.append((posX[noeud]-axeX+(posY[noeud]-axeY)*longueur)/pas)
            nouveaux = NoeudsVoisins(noeud,registreVoisins)
            registreVoisins.extend(nouveaux)
            aParcourir.extend(nouveaux)
            
    return listeNoeuds
        
def discretiseTable():    
    """
    génération des noeuds, avec positions
    et des arêtes, avec poids
    """
    #premier noeud
    g.add_vertex()
    posX[g.vertex(Nstruct+0)] = 0+axeX
    posY[g.vertex(Nstruct+0)] = 0+axeY
    #première ligne
    for j in range(1,longueur):
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*0+j)] = j*pas+axeX
        posY[g.vertex(Nstruct+longueur*0+j)] = 0*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(Nstruct+longueur*0+j-1),g.vertex(Nstruct+longueur*0+j))
        poids[g.edge(g.vertex(Nstruct+longueur*0+j-1),g.vertex(Nstruct+longueur*0+j))]=poidsDirect
    #autres lignes
    for i in range(1,largeur):
        #premier de la ligne
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*i)] = 0+axeX
        posY[g.vertex(Nstruct+longueur*i)] = i*pas+axeY
        #2 noeuds dessus
        g.add_edge(g.vertex(Nstruct+longueur*(i-1)),g.vertex(Nstruct+longueur*i))
        poids[g.edge(g.vertex(Nstruct+longueur*(i-1)),g.vertex(Nstruct+longueur*i))]=poidsDirect
        g.add_edge(g.vertex(Nstruct+longueur*(i-1)+1),g.vertex(Nstruct+longueur*i))
        poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+1),g.vertex(Nstruct+longueur*i))]=poidsDiag
        #corps de la ligne
        for j in range(1,longueur-1):
            g.add_vertex()
            posX[g.vertex(Nstruct+longueur*i+j)] = j*pas+axeX
            posY[g.vertex(Nstruct+longueur*i+j)] = i*pas+axeY
            #noeud à gauche
            g.add_edge(g.vertex(Nstruct+longueur*i+j-1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*i+j-1),g.vertex(Nstruct+longueur*i+j))]=poidsDirect
            #3 noeuds dessus
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j-1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j-1),g.vertex(Nstruct+longueur*i+j))]=poidsDiag
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j),g.vertex(Nstruct+longueur*i+j))]=poidsDirect
            g.add_edge(g.vertex(Nstruct+longueur*(i-1)+j+1),g.vertex(Nstruct+longueur*i+j))
            poids[g.edge(g.vertex(Nstruct+longueur*(i-1)+j+1),g.vertex(Nstruct+longueur*i+j))]=poidsDiag
        #dernier de la ligne
        g.add_vertex()
        posX[g.vertex(Nstruct+longueur*(i+1)-1)] = (longueur-1)*pas+axeX
        posY[g.vertex(Nstruct+longueur*(i+1)-1)] = i*pas+axeY
        #noeud à gauche
        g.add_edge(g.vertex(Nstruct+longueur*(i+1)-2),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*(i+1)-2),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDirect
        #2 noeuds dessus
        g.add_edge(g.vertex(Nstruct+longueur*i-1),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*i-1),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDirect
        g.add_edge(g.vertex(Nstruct+longueur*i-2),g.vertex(Nstruct+longueur*(i+1)-1))
        poids[g.edge(g.vertex(Nstruct+longueur*i-2),g.vertex(Nstruct+longueur*(i+1)-1))]=poidsDiag
        
    
def tracePDF():
    #tracé pdf
    #graph_draw(g, vprops={"label": g.vertex_index}, output="map_suppr.pdf", splines='false',vsize=0.11, elen=1)
    etiq = g.new_vertex_property("int")
    for v in g.vertices() :
        etiq[v]=(posX[v]-axeX+(posY[v]-axeY)*longueur)/pas
    graph_draw(g, vprops={"label": etiq}, output="map_objetsAprès.pdf", pos=(posX,posY),vsize=5, pin=True,penwidth=20.,ecolor="#000000")

rechercheChemin(Point(-20,0),Point(50,190))