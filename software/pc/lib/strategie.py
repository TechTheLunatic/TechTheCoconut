# -*- coding: utf-8 -*-

import outils_math.point as point

import carte
import robot
import timer, time
import math

import log
log = log.Log(__name__)

import __builtin__
import script


carte = carte.Carte()

class Strategie():
    """
    Classe permettant de construire une stratégie
    
    :param strategie: Type de stratégie à adopter :
                        - 1 : Stratégie en carton.
                        - 2 : Stratégie un peu mieux.
                        - 3 : Stratégie sopalin.
    :type strategie:  int

    """
    def __init__(self):

        
        self.strategie = constantes['Strategie']
        self.timerStrat = timer.Timer()
        self.actions = []
        
        # Remplir le tableau actions d'actions à faire (Thibaut)
        self.initialiserActionsAFaire()
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :
            log.logger.info("Lancement de la stratégie numéro " + str(self.strategie))
            
        #------------------------------#
        #-- Définition des instances --#
        #------------------------------#
            
        try :
            self.robotInstance = __builtin__.instance.robotInstance
        except :
            log.logger.error("stratégie : ne peut importer instance.robotInstance")
            
        try :
            self.scriptInstance = __builtin__.instance.scriptInstance
        except :
            log.logger.error("stratégie : ne peut importer instance.scriptInstance")
            
        try :
            self.baliseInstance = __builtin__.instance.baliseInstance  # NOTE Convention ? (Thibaut)            
        except :
            log.logger.error("stratégie : ne peut importer instance.baliseInstance")
            
    def lancer(self) :
            # Gestion de l'arrêt au bout de 90 secondes :
            Strategie.prendreDecisions = True
            
            # Lancement du timer.
            self.timerStrat.lancer()
        
            # Lancer la de prise de décision
            self.prendreDecision()
        
        
    def arreterPrendreDecisions(self) :
        """
        Appeller cette méthode lorsque l'on souhaite arrêter de prendre des décisions
        Cette méthode est appellée depuis le timer.        
        """
        
        Strategie.prendreDecisions = False
        self.Terminated = True
        log.logger.info("Arrêt de la prise de décisions")
        
    def prendreDecision(self): 
        """
        Retourne la décision prise par le robot. Pour les conventions, voir pc/lib/decision.py
        """
        
            
        #------------------------------------#
        #-- STRATEGIE NUMERO 1 : En carton --#
        #------------------------------------#
        
        if self.strategie == 1 :
            # Position de départ.
            #self.depart = self.robotInstance.position()     
            
            # Tant qu'on peut prendre des décisions
            while Strategie.prendreDecisions :
                
                # Si on arrive là, c'est que le script d'origine est terminé.
                # On appelle choisirAction tant que self.actions n'est pas vide
                while self.actions != [] :
                    self.choisirAction()
                
                if self.timerStrat.time() <= 70 :
                    # Prise de décision selon ce qui n'a pas été prise
                    pass
                
                else :
                    # Faire un "tour de piste"
                    pass

        #--------------------------------------#
        #-- STRATEGIE NUMERO 2: Un peu mieux --#
        #--------------------------------------#
        
        elif self.strategie == 2:
            while 42 :
                self.choisirAction()
        
        elif self.strategie == 3 :
            pass
        
        log.logger.info("ARRET DEFINITIF STRATEGIE")
        
        
    def initialiserActionsAFaire(self) :
        """
        TYPE D'ACTIONS : [NOM_DE_L_ACTION, +paramètresOptionnels, PRIORITÉ DE L'ACTION]
            NOM_DE_L_ACTION :   "FARMERTOTEM"   +param1 : ennemi, +param2: Nord
                                "ENFONCERPOUSSOIR"                +param : id poussoir
                                "FAIRECHIERENNEMI"
                                "TOURDETABLE"                     +param1 : brasOuverts
                                "DEFENDRE"
                                
                                
            PRIORITÉ DE L'ACTION : Nombre de points rapportés si l'action réussi.
        """
        
        # Nombre de paramètres par actions
        self.actions_nbrParametres = {"FARMERTOTEM":2, "ENFONCERPOUSSOIR":1, "FAIRECHIERENNEMI":0, "TOURDETABLE":1, "DEFENDRE":0}
        
        log.logger.debug("Initialisation des actions à faire")
        # Selon le profil de statégie choisi, on peut mettre des priorités différentes pour chaques actions.
        if self.strategie == 1 :
            self.actions.append(["FARMERTOTEM", 0, 0, 10])
            self.actions.append(["FARMERTOTEM", 0, 1, 10])
            self.actions.append(["FARMERTOTEM", 1, 0, 10])
            self.actions.append(["FARMERTOTEM", 1, 1, 10])
            
            self.actions.append(["ENFONCERPOUSSOIR", 0, 5])
            self.actions.append(["ENFONCERPOUSSOIR", 1, 5])
            
            #self.actions.append(["FAIRECHIERENNEMI", 1])    #
            
            self.actions.append(["TOURDETABLE", 0, 1  ])
            self.actions.append(["TOURDETABLE", 1, 0.1])
            self.actions.append(["DEFENDRE", 1])
            
            # Tableau de nouvelles priorités : Pour chaque actions, le premier argument est la nouvelle priorité si succès,
            # le deuxième argument est la nouvelle priorité si échec.
            self.nouvellesPriorites = { "FARMERTOTEM"       : [1, 5],
                                        "ENFONCERPOUSSOIR"  : [0, 5],
                                        "TOURDETABLE"       : [0.4, 0.4],
                                        "DEFENDRE"          : [0.1, 0.1]
                                      }
            
        elif self.strategie == 2 :
            self.actions.append(["FARMERTOTEM", 0, 0,   10  ])
            self.actions.append(["FARMERTOTEM", 0, 1,   10  ])
            self.actions.append(["FARMERTOTEM", 1, 0,   20  ])
            self.actions.append(["FARMERTOTEM", 1, 1,   20  ])
            
            self.actions.append(["ENFONCERPOUSSOIR", 0, 5])
            self.actions.append(["ENFONCERPOUSSOIR", 1, 5])
            
            #self.actions.append(["FAIRECHIERENNEMI", 1])    #
            
            self.actions.append(["TOURDETABLE", 0, 1  ])
            self.actions.append(["TOURDETABLE", 1, 0.1])
            self.actions.append(["DEFENDRE", 1])
            
            # Tableau de nouvelles priorités : Pour chaque actions, le premier argument est la nouvelle priorité si succès,
            # le deuxième argument est la nouvelle priorité si échec.
            self.nouvellesPriorites = { "FARMERTOTEM"       : [1, 5],
                                        "ENFONCERPOUSSOIR"  : [0, 5],
                                        "TOURDETABLE"       : [0.4, 0.4],
                                        "DEFENDRE"          : [0.1, 0.1]
                                      }
        
    
    def choisirAction(self) :
        """
        CETTE FONCTION PERMET A LA STRATEGIE DE CHOISIR QUELLE ACTION CHOISIR
        """
        
        # TODO associer la distance courante à celle de la balise.
        distance = 1
        
        # Poids du coefficient Nombre de Points / Durée
        k1 = 1
        
        # Poids du coefficient "Adversaire proche de l'objectif" :
        k2 = 1
        
        poids = []
        tempsScripts = []
        nomScripts = []
        nouvellesPriorites = []
        
        # Attribution des scores via les coefficients.   (k1*NbrPoints + k2*Prochitude de l'adv)
        for i in range(len(self.actions)) :
           # Ajout des nom de scripts.
            if self.actions[i][0] == "FARMERTOTEM" :
                nomScripts.append("self.scriptInstance.rafflerTotem"+str(self.actions[i][1])+str(self.actions[i][2]))

            elif self.actions[i][0] == "ENFONCERPOUSSOIR":
                nomScripts.append("self.scriptInstance.enfoncerPoussoir"+str(self.actions[i][1]))

            elif self.actions[i][0] == "FAIRECHIERENNEMI" :
                nomScripts.append("self.scriptInstance.fairechierEnnemi")

            elif self.actions[i][0] == "TOURDETABLE" :
                nomScripts.append("self.scriptInstance.tourDeTable"+ str(self.actions[i][1]))

            elif self.actions[i][0] == "DEFENDRE":
                nomScripts.append("self.scriptInstance.defendreBase")
                
            # On récupère le temps qu'un script fait pour s'accomplir.
            # Ce try...except... est utile si on n'a pas branché l'USB sur les ports.
            try :
                log.logger.debug("NOM DU SCRIPT : " + str(nomScripts[i]))
                exec("temps_script = self.scriptInstance.gestionScripts("+str(nomScripts[i])+", 1)")
            except :
                log.logger.error("Problème de script")
                # WARNING A ENLEVER POUR UN MATCH
                temps_script = 0
                
            # Temps de chaque scripts.
            tempsScripts.append(temps_script)
                
            # Ce try... except.. est utile si un script n'est pas fait en dur (pas scripté)
            # C'est souvent une ZeroDivisionError qui est lancée (script de temps nul)
            try :
                poids.append(k1*self.actions[i][-1]/temps_script + k2*distance)
            except :
                poids.append(k1*self.actions[i][-1]         + k2*distance)
                        
        # On cherche ceux qui font des points positifs (sinon, c'est qu'on est dans un cas
        # déjà fait. Ex : On a déjà farmé le totem.)
        max = 0
        maxID = -1
        deuxiemeMaxID = -1
        
        # On cherche l'action qui fait le meilleur score
        # Le deuxième max est utile pour arrêter le premier si celui ci met
        # trop de temps.
        for i in range(len(self.actions)) :
            if poids[i] > max :
                deuxiemeMaxID = maxID
                max = poids[i]
                maxID = i
        
        
        # Si maxID == -1 c'est que il ne reste rien à faire.
        # TODO Qu'est-ce qu'on fait dans ce cas là ?!
        if maxID < 0 :
            log.logger.critical("ZUT ALORS ! Plus d'actions à faire")
            return
        
            print "#######################" + str(nomScripts[maxID])

        # Sinon, on prend l'action
        try :
            # Ecris un timeout dans __builtin__.instance
            # CONVENTION : Si il n'y a pas de deuxième meilleure action à faire, on met
            # le timeout à -1
            if deuxiemeMaxID >= 0 :
                __builtin__.instance.timeout = tempsScripts[deuxiemeMaxID]
            else :
                __builtin__.instance.timeout = -1
            
            exec("success = self.scriptInstance.gestionScript("+nomScripts[maxID]+")")
            
        # Problème de script
        except :
            log.logger.critical("La stratégie ne peut pas lancer d'actions")
            success = True
            
        # Si l'action s'est  bien déroulée
        if success :
            # Puis on lui change sa priorité.
            self.changerPriorite_byID(maxID, self.nouvellesPriorites[self.actions[maxID][0]][0])
        # Si l'action a chié comme Deboc
        else :
            self.changerPriorite_byID(maxID, self.nouvellesPriorites[self.actions[maxID][0]][1])
    
            
        log.logger.debug("NOUVELLES ACTIONS : " + str(self.actions))
        time.sleep(5)
        
        
    # Changement de priorité d'une entrée du tableau self.actions
    def changerPriorite(self, nomAction, params, nouvellePriorite) :
        """
        
        Change la priorité d'une action dans le tableau self.actions
        
        
        :param nomAction: NOM_DE_L_ACTION
        :type nomAction: string
        
        :param params: Tableau contenant les paramètres optionels
        :type params: tableau de trucs
        
        :param nouvellePriorite: Nouvelle priorité pour l'action
        :type nouvellePriorite: int (entre 0 et 5)
        """
        for i in range(len(self.actions)) :
            if self.actions[i][0] == nomAction :
                found = 1
                for j in range(len(params)) :
                    if self.actions[i][j+1] != params[j] :
                        
                        found = 0
                        break
                if found :
                    self.actions[i][-1] = nouvellePriorite
                    return 1
                    
    def changerPriorite_byID(self, id, nouvellePriorite) :
        """
        Change la priorité d'une action dans le tableau self.actions, en fonction
        de l'ID de celui ci dans ce tableau
        """
        
        self.actions[id][-1] = nouvellePriorite
                    
    #TEST
    def strateg_scripts(self):
        if self.scriptInstance.scriptTestStruct0():
            self.scriptInstance.scriptTestStruct1()
        
def t() :
    s = Strategie()
    s.lancer()
