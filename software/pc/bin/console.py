# -*- coding: utf-8 -*-

import sys
from sys import argv
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.chargement_lib
log = lib.log.Log(__name__)

try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell()
except:
    try:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed()
        ipshell()
    except:
        log.logger.error("La dépendance Ipython n'est pas installée. Taper sudo apt-get install ipython")

