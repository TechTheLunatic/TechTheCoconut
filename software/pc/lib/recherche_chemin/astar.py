# -*- coding: utf-8 -*-

import os
import sys
# Ajout de ../../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import lib.log
log = lib.log.Log()

import lib.elements_jeu
from lib.outils_math.collisionRectangles import collision
try:
    from graph_tool.all import *
except:
    log.logger.error("Vous devez installer graph-tool, plus d'informations sur le README")
from lib.carte import Carte

"""
carte=Carte()
carte.reglettesEnBois.rectangle. #3
carte.totems.rectangle. #1
carte.palmiers.rectangle. #0
.x
.y
.t
.wx
.wy

carte = elements_jeu.carte
carte.totems[0] 
carte.palmiers[0]
carte.reglettesEnBois[0] 

.position.x
.position.y
.orientation
.longueur
.largeur


"""

class carteDiscrete():
    """
    Classe implémentant la carte du jeu discrétisée pour la recherche de chemin
    """
    def __init__(self):
        graph.Graph.__init__(self)
    #'pas' en mm pour la discrétisation de la carte en 'cases'
    self.pas=15
    self.nbCasesLarg=int (largeurCarte / self.pas)
    self.nbCasesHaut=int (hauteurCarte / self.pas)
    #on définie une matrice booléenne pour le caractère accessible des cases
    self.casesAccess=nbCasesHaut*[nbCasesLarg*[True]]
    for i in tableauElementInfranchissable:
        pass

class Astar(graph.Graph):
    """
    Classe implémentant l'algorithme A* pour la recherche de chemin
    """
    def __init__(self):
        graph.Graph.__init__(self)
        
