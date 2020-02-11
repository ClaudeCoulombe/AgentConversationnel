# -*- coding: utf-8 -*-

import sys
import os
import random
from random import randint
import re
import unicodedata

class AgentConversationnel(object):
    
    def __init__(self, chemin_donnees=None, nom_agent=None ):
        """
        :param chemin_donnees: le chemin vers le fichier de données donnees.txt 
        :nom_agent: le nom de l'agent conversationnel
        """
        # paquet Python
        chemin_repertoire_courant = os.path.dirname(os.path.realpath(__file__))
        # chemin_repertoire_courant = os.getcwd()
        if chemin_donnees is None:
            chemin_donnees = chemin_repertoire_courant+"/DATA/donnees.txt"
        if nom_agent is None:
            nom_agent = "Nestor"

        self.CHEMIN_DONNEES = chemin_donnees
        self.NOM_AGENT = nom_agent
        
        self.TABLE_SUBSTITUTIONS = [ (" je suis "," vous êtes "), (" vous êtes "," je suis "), 
                                    (" j'ai "," vous avez "),(" vous avez "," j'ai "), 
                                    (" je dois "," vous devez "),(" vous devez "," je dois "),
                                    (" je peux "," vous pouvez "),(" vous pouvez "," je peux "),
                                    (" vous "," me "),(" toi "," moi "),(" votre "," mon "),
                                    (" mon "," votre "),(" ma "," la "),(" mes "," vos "),
                                    (" vos "," mes "),(" moi "," vous "),(" tu "," je "),
                                    (" te "," me "),(" ton "," mon "),(" me "," vous "),
                                    (" m'"," vous ")
                                   ]

        themes = []
        with open(self.CHEMIN_DONNEES,"r",encoding='utf-8"') as fichier_donnees:
            une_ligne = fichier_donnees.readline()[:-1]
            while len(une_ligne) > 0:
                if "THEME :" in une_ligne:
                    forme_trouvee = re.search(r"THEME\s*:\s*(\d*)\s([\w|\s|\?]*)\x2A", une_ligne)
                    if forme_trouvee:
                        numero_theme = forme_trouvee.group(1)
                        nom_theme = forme_trouvee.group(2)[:-1]
                        mots_declencheurs = []
                        une_ligne = fichier_donnees.readline()[:-1]
                        while une_ligne != "REPONSES":
                            mots_declencheurs.append(une_ligne)
                            une_ligne = fichier_donnees.readline()[:-1]
                        une_ligne = fichier_donnees.readline()[:-1]
                        les_reponses = []
                        while une_ligne != "PHRASE DE RELANCE":
                            les_reponses.append(une_ligne)
                            une_ligne = fichier_donnees.readline()[:-1]
                        une_ligne = fichier_donnees.readline()[:-1]
                        theme = {'numero' : numero_theme,
                                 'nom': nom_theme,
                                 'declencheurs' : mots_declencheurs,
                                 'reponses' : les_reponses,
                                 'relance' : une_ligne}
                    themes.append(theme)
                    une_ligne = fichier_donnees.readline()[:-1]

        self.THEMES = themes
        self.introduction(self.NOM_AGENT)
        self.dialoguer(self.NOM_AGENT,self.THEMES)
        
    def introduction(self,nom_agent):
        print("Bonjour, je m'appelle «" + nom_agent + "».")
        print("Vous pouvez bavarder avec moi en tapant des phrases simples.")
        print("Entrez quitter, arrêter ou terminer pour cesser le dialogue.")

    def dialoguer(self,nom_agent,themes):
        entree = ""
        invite =  "".join(["=" for _ in range(len(nom_agent))]) + "> "
        theme_courant = -1
        try: 
            entree = " " + input(invite).lower().strip() + " " 
        except EOFError:
            print(entree)
            print("Erreur")
        while entree not in [" quitter ", " arrêter ", " terminer ", " fin "]:
            if entree:
                theme_courant = self.repondre(invite,nom_agent,theme_courant,themes,entree)
            try: 
                entree = " " + input(invite).lower().strip() + " " 
            except EOFError:
                print(entree)
                print("Erreur")
        print(nom_agent+">",self.choix_aleatoire(
                ["Au revoir!",
                 "À bientôt!",
                 "Vous me manquez déjà...",
                 "Ce fut un plaisir de bavarder avec vous",
                 "Au plaisir de vous reparler"
                ]))

    def choix_aleatoire(self,liste):
        return random.choice(liste)

    def tester_entree_trop_courte(self,chaineDEntree):
        entree_trop_courte = False
        reponse = ""
        if (chaineDEntree == "") or  (len(chaineDEntree) <= 2):
            entree_trop_courte = True
            reponse = self.choix_aleatoire(
                ["Je vous trouve un peu bref! Élaborez davantage.",
                 "Ne soyez pas timide! Exprimez-vous.",
                 "Vous n'êtes pas très bavard! Allez, exprimez-vous.",
                 "Je ne peux pas vous aider, si vous refusez de communiquer.",
                 "Peut-être avez-vous accroché la touche retour? SVP, recommencez."
                ])                                  
        return(entree_trop_courte,reponse)

    def creerReponseMiroir(self,reponse):
    # Note: pas parfait, mais fonctionnel
        reponse_miroir = " " + reponse + " "
        position_max = len(reponse_miroir)
        nbre_substitutions_max = len(self.TABLE_SUBSTITUTIONS)-1
        index = 0
        while (index <= position_max):
            for couple_substitution in self.TABLE_SUBSTITUTIONS:
                position_sous_chaine = reponse_miroir.find(couple_substitution[0], index, position_max)
                if position_sous_chaine != -1 :
                    debut = reponse_miroir[0:index] + reponse_miroir[index:position_sous_chaine]
                    substitution = couple_substitution[1]
                    fin = reponse_miroir[position_sous_chaine+len(couple_substitution[0]):]
                    reponse_miroir = debut + substitution + fin
                    index += position_sous_chaine+len(couple_substitution[0])
                    reponse_miroir = " " + reponse_miroir.strip() + " " 
            index += 1
        return reponse_miroir;

    def retirer_accents(self,chaine_entree):
        nkfd_form = unicodedata.normalize('NFKD', str(chaine_entree))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def reconnaitre_foutaises(self,entree_brute):
        entree_sans_accent = self.retirer_accents(entree_brute)
        # test motifs  repetitifs
        if re.search('\s+(\w|\d){1,3}\s+(\w|\d){1,3}\s+(\w|\d){1,3}\s+(\w|\d){1,3}\s+(\w|\d){1,3}\s+', entree_sans_accent):
            return True
        # test 4 voyelles consecutives ou +
        if re.search('[aeiouyAEIOUY]{4,}', entree_sans_accent):
            return True
        # test 4 consonnes consecutives ou +
        if re.search('[bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ]{4,}', entree_sans_accent):
            return True
        # test 4 caractères spéciaux consecutifs
        if re.search('[|\^&+\-\$%*/=!>#@?]{4,}', entree_sans_accent):
            return True
        # Réponse probablement lisible
        return False

    def tester_entree_foutaises(self,chaineDEntree):
        foutaises = False
        reponse = ""
        if self.reconnaitre_foutaises(chaineDEntree):
            foutaises = True
            reponse = self.choix_aleatoire(
                ["Je suis incapable de vous comprendre. Exprimez-vous plus clairement.",
                 "Arrêtez de taper n'importe quoi!",
                 "Vous me semblez très confus. Recommencez.",
                 "Je ne peux pas vous aider, si vous refusez de communiquer clairement.",
                 "Cette langue m'est complètement étrangère. Répondez-moi en Français, SVP.",
                 "Il semble avoir de la friture sur la ligne. SVP, recommencez.",
                 "Avez-vous accroché des touches accidentellement? SVP, recommencez."
              ]) 
        return(foutaises,reponse)

    def repondre(self,invite,nom_agent,theme_courant,themes,chaineDEntree):
        # Vérifier si la réponse est vide ou trop courte
        entree_trop_courte, reponse = self.tester_entree_trop_courte(chaineDEntree)
        if entree_trop_courte:
            print(nom_agent+">",reponse) 
        else:
            # Uniformiser l'entrée
            chaineDEntree = " " + chaineDEntree.lower().strip() + " "
            # Identifier un thème
            theme_trouve = False
            for theme in themes:
                mots_declencheurs = theme['declencheurs']
                for mot_declencheur in mots_declencheurs:
                    mot_declencheur = mot_declencheur.replace('"','')
                    if mot_declencheur in chaineDEntree:
                        theme_trouve = True
                        theme_courant = int(theme['numero'])
                        une_reponse_au_hasard = random.choice(theme['reponses'])
                        if une_reponse_au_hasard.endswith('*'):
                            debut_reponse = une_reponse_au_hasard[0:len(une_reponse_au_hasard)-1]
                            fin_reponse = chaineDEntree[chaineDEntree.index(mot_declencheur)+len(mot_declencheur):]
                            fin_reponse = self.creerReponseMiroir(fin_reponse);
                            reponse = debut_reponse + fin_reponse
                        else:
                            reponse = une_reponse_au_hasard
                        break
                if theme_trouve:
                    print(nom_agent+">",reponse)
                    break
            if not theme_trouve:
                # Vérifier si l'usager écrit des foutaises
                foutaises, reponse = self.tester_entree_foutaises(chaineDEntree)
                if foutaises:
                    print(invite,reponse) 
                else:
                    # Relancer avec la phrase de rappel du dernier thème identifié
                    if theme_courant != -1:
                        reponse = themes[theme_courant]['relance']
                        print(invite,reponse)
                    else:
                    # Faire appel au thème fourre-tout situé en fin de liste
                        theme_fourretout = themes[theme_courant]
                        reponse = random.choice(theme_fourretout['reponses'])
                        print(invite,reponse)
            return theme_courant