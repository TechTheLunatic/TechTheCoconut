# -*- coding: utf-8 -*-

import serie
import log
import __builtin__
import outils_math.point as point
import math
import time
import sys

sys.path.append('../')
import profils.develop.constantes

# Ajout de constantes de develop si on ne passe pas par la console INTech
if not hasattr(__builtin__, "constantes"):
    import profils.develop.constantes
    __builtin__.constantes = profils.develop.constantes.constantes

log = log.Log(__name__)


class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    
    :param ids: Dico contenant l'id de l'AX12 en fct° de sa position
    
    """
    # Le périphérique, le débit, le timeout et le nom sont les mêmes pour tous les actionneurs
    def __init__(self):
        self.ids        = {"hg":1, "hd":2, "bg":0, "bd":3}
        self.serie_sleep_time = 0.008
        self.demarrer()
        
        
    # Démarrage.
    def demarrer(self):
        
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("actionneur : ne peut importer instance.robotInstance")
        
        if not hasattr(Actionneur, 'initialise') or not Actionneur.initialise:
            Actionneur.initialise = True
            if hasattr(__builtin__.instance, 'serieCaptActionneurInstance'):
                self.serieCaptActionneurInstance = __builtin__.instance.serieCaptActionneurInstance
                self.deplacer(0)
            else:
                log.logger.error("actionneur : ne peut importer instance.serieCaptActionneurInstance")
                self.calculRayon(0)
                
            
        
        
    def deplacer(self, angle, position = ["hg", "hd", "bg", "bd"], couleur = __builtin__.constantes['couleur']):
        """
        Envoyer un ordre à l'actionneur
        
        :param angle: angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :type angle: int (entre 0 et ANGLEMAXI)
        
        :param position: Position de l'actionneur à tourner (OPTIONEL)
        :type position: string "hg" | "hd" | "bg" | "bd". Défaut : ALL

        """
        
        # Pas d'overflow, pas de trucs dégueux
        if angle >= constantes["Actionneurs"]["angleMax"] :
            angle = constantes["Actionneurs"]["angleMax"]
        elif angle <= constantes["Actionneurs"]["angleMin"] :
            angle = constantes["Actionneurs"]["angleMin"]
        
        #calcul du nouveau rayon du robot
        self.calculRayon(math.pi*angle/180)
               
        # Gestion de la symétrie
        if couleur == "v" :
            # Envoi des infos
            if "hg" in position:
                self.goto(self.ids["hg"], 180+3-angle)
            if "hd" in position:
                self.goto(self.ids["hd"], angle)
            if "bg" in position:
                self.goto(self.ids["bg"], angle+5)
            if "bd" in position:
                self.goto(self.ids["bd"], 180+9-angle)
        else :
            # Envoi des infos
            if "hg" in position:
                self.deplacer(angle, "hd", "v") 
            if "hd" in position:
                self.deplacer(angle, "hg", "v")
            if "bg" in position:
                self.deplacer(angle, "bd", "v")
            if "bd" in position:
                self.deplacer(angle, "bg", "v")
        

        
    def changerVitesse(self, nouvelleVitesse, position = ["hg", "hd", "bg", "bd"]) :
        """
        Changer la vitesse de rotation de TOUS les actionneurs branchés
        
        :param nouvelleVitesse: Nouvelle vitesse des actionneurs
        :type nouvelleVitesse: int (entre 0 et 1000)
        """
        
        if nouvelleVitesse >= 1000 :
            nouvelleVitesse = 1000
        elif nouvelleVitesse <= 0 :
            nouvelleVitesse = 0
        
        if "hd" in position :
            self.ecrireVitesse(self.ids["hd"], nouvelleVitesse)
        if "hg" in position :
            self.ecrireVitesse(self.ids["hg"], nouvelleVitesse)
        if "bd" in position :
            self.ecrireVitesse(self.ids["bd"], nouvelleVitesse)
        if "bg" in position :
            self.ecrireVitesse(self.ids["bg"], nouvelleVitesse)
        
    def test_demarrage(self, mode = "LONG") :
        """
        Test de démarrage des bras Ax12. Un paramètre optionnel est mis en place pour
        pouvoir régler la durée du test.
        
        :param mode: Type de test
        :type mode: String "LONG" | "SHORT". Défault : "LONG"
        
        """
        
        if mode == "LONG" :
            for i in range(4) :
                self.goto(i, 80)
                time.sleep(1)
            log.logger.debug("Test Actionneurs goto : Fait.")
            
            for i in ["hd", "hg", "bg", "bd"] :
                self.deplacer(50, i)
                time.sleep(1)
            log.logger.debug("Test Actionneurs déplacer : Fait")
            
            self.changerVitesse(100)
            self.deplacer(20)
            time.sleep(1)
            
            log.logger.debug("Test Actionneurs changerVitesse : Fait")
            self.changerVitesse(500)
            self.deplacer(0)
            
        elif mode == "SHORT" :
            self.deplacer(80)
            time.sleep(1)
            self.deplacer(0)
            time.sleep(1)
            log.logger.debug("Test des bras : Fait")

        
    def flash_id(self, nouvelID) :
        """
        Flashage de l'id
        """
        self.serieCaptActionneurInstance.ecrire("f")
        self.serieCaptActionneurInstance.ecrire(str(int(nouvelID)))
        
        
    def stop(self, position = ["hd", "hg", "bd", "bg"]):
        """
        Arrête l'actionneur en urgence
        """
        if "hd" in position :
            self.ecrireStop(self.ids["hd"])
        if "hg" in position :
            self.ecrireStop(self.ids["hg"])
        if "bd" in position :
            self.ecrireStop(self.ids["bd"])
        if "bg" in position :
            self.ecrireStop(self.ids["bg"])
        
    #------------------------------------------------#
    #       METHODES BAS NIVEAU                      #
    #------------------------------------------------#  
    
    def goto(self, id, angle) :
        # On considère que angle est dans les bonnes valeurs.
        
        self.serieCaptActionneurInstance.ecrire("GOTO")
        time.sleep(self.serie_sleep_time)
        self.serieCaptActionneurInstance.ecrire(str(int(id)))
        time.sleep(self.serie_sleep_time)
        self.serieCaptActionneurInstance.ecrire(str(int(angle)))
        time.sleep(self.serie_sleep_time)
    
    def ecrireVitesse(self, id, vitesse) :
        # On considère que  les valeurs données sont bonnes.
        self.serieCaptActionneurInstance.ecrire("CH_VIT")
        time.sleep(self.serie_sleep_time)
        self.serieCaptActionneurInstance.ecrire(str(int(id)))
        time.sleep(self.serie_sleep_time)
        self.serieCaptActionneurInstance.ecrire(str(int(vitesse)))
        time.sleep(self.serie_sleep_time)
        
    def ecrireStop(self, id) :
        self.serieCaptActionneurInstance.ecrire("U")
        time.sleep(self.serie_sleep_time)
        self.serieCaptActionneurInstance.ecrire(str(int(id)))
        time.sleep(self.serie_sleep_time)
        
    def envoyer(self, message) :
        # Envoi d'un message brut
        self.serieCaptActionneurInstance.ecrire(str(message))
        time.sleep(self.serie_sleep_time)
        
    def calculRayon(self, angle):
        """
        Modifie le rayon du cercle circonscrit au robot par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        :param angle: angle entre la face avant du robot et les bras en bas du robot. Unité :  radian
        :type angle: float
        """
        
        #récupération des constantes nécessaires:
        #log.logger.info('Calcul du rayon et du centre du robot')
        
        #[]la longueur est sur x, largeur sur y
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        
        rayon_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        
        #point à l'extremité du bras droit
        sommet_bras = point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + proj_y)
        rayon_avec_bras = math.sqrt((sommet_bras.x) ** 2 + (sommet_bras.y) ** 2)
        
        #mettre à jour l'attribut du robot
        #NOTE : on n'utilisera la recherche de chemin qu'avec des bras fermés. donc pas de recalculs intempestifs.
        #self.robotInstance.changeRayon(max(rayon_avec_bras,rayon_original))
        
    def test(self, temps = 0.3) :
        i = 0
        while 1 :
            self.deplacer((i%10)*10 + 90)
            time.sleep(temps)
            if i%10 == 0 :
                time.sleep(1)
            i += 1
        
    