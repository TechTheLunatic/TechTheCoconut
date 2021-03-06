# -*- coding: utf-8 -*-

from point import Point
from vecteur import Vecteur
from math import cos,sin,pi
    
def polygone(centre,rayon,nbCotes):
    #un polygone doit etre défini par une liste de sommets (points), dans le sens inverse des aiguilles d'une montre
    poly=[]
    for i in range(nbCotes):
        poly.append(Point(centre.x+rayon*cos(i*2*pi/nbCotes),centre.y+rayon*sin(i*2*pi/nbCotes)))
    return poly
    
def polygoneInscrit(poly):
    c_x=0.
    c_y=0.
    for sommet in poly:
        c_x+=sommet.x
        c_y+=sommet.y
    c_x/=len(poly)
    c_y/=len(poly)
    polyInscrit=[]
    for sommet in poly:
        polyInscrit.append(Point(0.999*sommet.x+0.001*c_x,0.999*sommet.y+0.001*c_y))
    return polyInscrit