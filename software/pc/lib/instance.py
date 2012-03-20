# -*- coding: utf-8 -*-

import sys
import os
import lib.log
import robot
import peripherique
import asservissement
import serial


log =lib.log.Log(__name__)

class Instance:
    """
    Classe pour créer des instances des classes importantes
    :param robotInstance: Instance de la classe robot
    :param capteurInstance: Instance de la classe capteur
    :param asserInstance: Instance de la classe asservissement
    :param serieAsserInstance: Instance de la classe serie pour l'asservissement
    :param serieCaptInstance: Instance de la classe  serie pour les capteurs/actionneurs
    :param actionInstance: Instance de la classe actionneurs
    """
    
    def __init__(self):
        log.logger.info("Instanciation de la classe Instance")

    def instanciation(self):
        self.instanciationRobot()
        self.instanciationSerie()
        self.instanciationAsservissement()
        self.instanciationCapteur()
        self.instanciationActionneur()
    
    def instanciationCapteur(self):
        try : self.capteurInstance = lib.capteur.Capteur()
        except : log.logger.error("Impossible d'instancier capteur")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()
        
    def instanciationAsservissement(self):
        try : self.asserInstance = asservissement.Asservissement()
        except : log.logger.error("Impossible d'instancier asservissement")

    def instanciationActionneur(self):
        try: self.actionInstance = actionneur.Actionneur()
        except: log.logger.error("Impossible d'instancier actionneur")
        
    def instanciationSerie(self):
        #Instance serie asservissement
        cheminAsser = lib.peripherique.chemin_de_peripherique("asservissement")
        if cheminAsser:
            self.serieAsserInstance = serial.Serial(cheminAsser, 9600, timeout=0)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
            
        
        cheminCapt = peripherique.chemin_de_peripherique("capteur")
        if cheminCapt:
            self.serieCaptInstance = serial.Serial(cheminCapt, 57600, timeout=3)
        else:
            log.logger.error("Le capteur n'est pas chargé")
        
        

        