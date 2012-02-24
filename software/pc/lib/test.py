# -*- coding: utf-8 -*-

from asservissement import *

#Tests fait en binome entre recherche de chemin et asservissement.


"""x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)
x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""
x = 50
y = 80
depart = outils_math.point.Point(x,y)
arrivee = outils_math.point.Point(x,y)

angle = raw_input("Donner l'angle des bras\n")

robot.orientation = 50
asser = Asservissement()
asser.centrePython(angle)

#Ici le centre et le rayon du robot sont initialisés, tu y accèdes avec robot.centre et robot.rayon
#J'ai mis la suite du code, à modifier de ton côté certainement. Ma fonction centreAvr() n'est pas testée, je l'utilise pas ici du coup ! (et je vais en SH maintenant)

theta = recherche_chemin.thetastar.Thetastar([])
print "Appel de la recherche de chemin pour le point de départ : ("+str(depart.x)+","+str(depart.y)+") et d'arrivée : ("+str(arrivee.x)+","+str(arrivee.y)+")"
chemin = theta.rechercheChemin(depart,arrivee)

i = 0
while i+1 < len(chemin):
    centre_avr[i] = centreAVR(chemin[i],chemin[i+1])
        
i = 0
for i in chemin:
    print "goto " + str(centre_avr[i].x) + ' ' + str(centre_avr[i].y) + '\n'