# -*- coding: utf-8 -*-

import sys
from sys import argv
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

# Import d'un timer et du jumper
timer       = lib.timer.Timer()
jumper      = lib.jumper.Jumper()
strategie   = lib.strategie.Strategie()
asserv      = lib.asservissement.Asservissement()
robot       = lib.robot.Robot()
script      = lib.script.Script()

# On attend la mise en position du Jumper pour lancer le recalage
log.logger.info("Robot en attente du jumper pour recalage")
jumper.demarrerRecalage()
log.logger.info("Lancement du recalage...")

#Lancement du recalage
#TODO MONSIEUR DEBOC, FILE MOI LE PROTOCOLE
try :
    asserv.recalage()
except :
    log.logger.error("Impossible de lancer le recalage")
    
    
# On attends le réenlèvement du jumper
log.logger.info("Le recalage a été effectué")
jumper.scruterDepart()
log.logger.info("Le Jumper a été retiré. Lancement de la stratégie")

# On lance le script d'homologation
script.homologation()

# ET BIM !


