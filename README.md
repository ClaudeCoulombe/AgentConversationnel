# Agent conversationnel en français

### Introduction

Projet-jouet fortement inspiré du célèbre ELIZA de Joseph Weizenbaum conçu vers 1965.
Il s'agit d'une traduction rapide en Python d'un vieux programme Java que j'ai écrit aux environs de 2001. 
À l'époque, avec une interface inspirée de HAL et un module de synthèse  vocale, j'avais tenté d'intéresser des partenaires d'affaires aux agents conversationnels, sans grand succès...


### Référence

Weizenbaum, J. (1983). Eliza — a computer program for the study of natural language communication between man and machine. Communications of the ACM, 26(1), 23-28.

### Licence

Copyright (C) 2001-2020 Claude COULOMBE

Sous licence Apache, Version 2.0 (la "Licence");
vous ne pouvez pas utiliser ce fichier, sauf conformément avec la licence.
Vous pouvez obtenir une copie de la Licence sur
http://www.apache.org/licenses/LICENSE-2.0

Sauf si requis par la loi en vigueur ou par accord écrit, le logiciel distribué sous la licence est distribué "TEL QUEL", SANS GARANTIE NI CONDITION DE QUELQUE NATURE QUE CE SOIT, implicite ou explicite. Consultez la Licence pour connaître la terminologie spécifique régissant les autorisations et les limites prévues par la licence.

### Installation

1. Assurez-vous que pip est installé (https://packaging.python.org/tutorials/installing-packages/)<br/>
2. Vous pouvez alors installer AgentConversationnel :<br/>
`> pip install git+https://github.com/ClaudeCoulombe/AgentConversationnel`

*** Attention: S'exécute en Python 3.X mais peut être facilement adapté à Python 2.7X avec de petites modifications ***

### Usage


``` Python
>>>  from AgentConversationnel import AgentConversationnel
```

Paramètres du constructeur

On peut ajouter en paramètre un chemin différent pour les données ou un nom pour l'agent.
Sinon par défaut, il s'appellera «Nestor».

Exécution

``` Python
>>> agent = AgentConversationnel()
Bonjour, je m'appelle «Nestor».
Vous pouvez bavarder avec moi en tapant des phrases simples.
Entrez quitter, arrêter ou terminer pour cesser le dialogue.
======> je suis en amour avec mon thérapeute
Nestor> Pourquoi êtes-vous en amour avec votre thérapeute 
```

Autre exemple avec un agent qui s'appelle «Eliza»
``` Python
>>> agent = AgentConversationnel(nom_agent="Eliza")
Bonjour, je m'appelle «Eliza».
Vous pouvez bavarder avec moi en tapant des phrases simples.
Entrez quitter, arrêter ou terminer pour cesser le dialogue.
=====> je suis anxieux
Eliza> Etes-vous venu me voir parce que vous êtes anxieux  
```
