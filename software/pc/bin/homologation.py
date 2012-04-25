# -*- coding: utf-8 -*-

import sys
from sys import argv
import os
import __builtin__
import lib.instance

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


import lib.chargement_lib
log = lib.log.Log(__name__)

# Import d'un timer et du jumper
timer       = lib.timer.Timer()
jumper      = lib.jumper.Jumper()
strategie   = lib.strategie.Strategie()
asserInstance      = __builtin__.instance.asserInstance
robot       = lib.robot.Robot()
script      = __builtin__.instance.scriptInstance

# On attend la mise en position du Jumper pour lancer le recalage
log.logger.warning("Robot en attente du jumper pour recalage")
jumper.demarrerRecalage()
log.logger.info("Lancement du recalage...")

#Lancement du recalage

try :
    asserInstance.recalage()
except :
    log.logger.error("Impossible de lancer le recalage")
    
    
# On attends le réenlèvement du jumper
log.logger.warning("Le recalage a été effectué")
jumper.scruterDepart()
log.logger.warning("Le Jumper a été retiré. Lancement de la stratégie")

# On lance le script d'homologation
asserInstance.setUnsetAsser("translation",1)
asserInstance.setUnsetAsser("rotation",1)
script.homologation()

# ET BIM !

