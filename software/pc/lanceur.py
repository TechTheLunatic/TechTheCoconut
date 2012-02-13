# -*- coding: utf-8 -*-

import os
import shutil
import glob
import lib.log
import lib.conf
import __builtin__

first = True
while first or not profil.importation:
	first = False
	conf = raw_input('Indiquer la configuration a importer (prod, develop, developSimulUc) : \n')
	profil = lib.conf.Conf(conf)

# Chargement des constantes en variable globale
exec('import profils.'+conf+'.constantes')
exec('__builtin__.constantes = profils.'+conf+'.constantes.constantes')

# Initialisatoin des logs
log = lib.log.Log(constantes['Logs']['logs'], constantes['Logs']['logs_level'], constantes['Logs']['logs_format'], constantes['Logs']['stderr'], constantes['Logs']['stderr_level'], constantes['Logs']['stderr_format'], constantes['Logs']['dossier'])

log.logger.info('Profil de configuration chargé : ' + conf)

log.logger.info('Injection des données de la carte')
exec('import profils.'+conf+'.injection.elements_jeu')

first = True
erreur = False
while first or erreur:
    mode = raw_input('Indiquer le mode de lancement (autonome, console, visualisation_table) : \n')
    first = False
    try:
        log.logger.info("Chargement du fichier de lancement " + mode)
        exec('import bin.'+ mode)
        if mode == "visualisation_table":
            first = True
    except:
        log.logger.warning("Le mode '" + mode + "' n'a pas pu etre charge")
        erreur = True
