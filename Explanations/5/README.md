# TP5 SECU : Exploit, pwn, fix

> *[Un "write-up" + bilan de l'exercice complet est désormais dispo ici.](./mitigate.md)*

Encore un TP de dév, mais où vous ne développez pas ! Pas mal nan ?

Le but : **exploiter un code vulnérable et proposer des remédiations** pour qu'il ne le soit plus.

La mise en situation est assez proche d'un cas réel, en restant dans des conditions de TP.

> **Pour maximiser le fun, ne discutez de rien de tout ça ni avec les dévs, ni avec les infras**, restez dans votre secte de sécu :D Si tu joues le jeu c'est un exercice cool, moins tu le jeu, plus il est nul !

![Gunna be hax](./img/gunna_be_hacker.png)

## Sommaire

- [TP5 SECU : Exploit, pwn, fix](#tp5-secu--exploit-pwn-fix)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
  - [1. Reconnaissance](#1-reconnaissance)
  - [2. Exploit](#2-exploit)
  - [3. Reverse shell](#3-reverse-shell)
  - [4. Bonus : DOS](#4-bonus--dos)
  - [II. Remédiation](#ii-remédiation)

## 0. Setup

➜ **Je vous filerai un lien en cours pour télécharger le client d'une application**

- pas possible de commencer le TP tant que j'ai rien donné donc, attendez le feu vert !

➜ Votre but : 🏴‍☠️ **prendre le contrôle du serveur** 🏴‍☠️

## 1. Reconnaissance

> ***Cette section est en grande partie uniquement réalisable en cours. Perdez pas de temps.***

➜ On a de la chance dis donc ! Du Python pas compilé !

- prenez le temps de lire le code
- essayez de le lancer et de capter à quoi il sert

🌞 **Déterminer**

- à quelle IP ce client essaie de se co quand on le lance
- à quel port il essaie de se co sur cette IP
- vous **DEVEZ** trouver une autre méthode que la lecture du code pour obtenir ces infos

> Disons que si le code est compilé, t'auras pas la possibilité de le lire. Je vous laisse le code pour l'aspect pédagogique de l'exercice. Il existe au moins deux façons très directes qui permettraient de trouver ces infos. Trouvez-en une au moins.

➜ **On me dit à l'oreillette que cette app est actuellement hébergée au sein de l'école.**

🌞 **Scanner le réseau**

- trouvez une ou plusieurs machines qui héberge une app sur ce port
- votre scan `nmap` doit être le plus discret possible : il ne teste que ce port là, rien d'autres
- testez d'abord dans un réseau avec des VMs

🦈 **tp5_nmap.pcapng**

- capture Wireshark de votre `nmap`
- je ne veux voir que les trames envoyées/reçues par `nmap` dans la capture

🌞 **Connectez-vous au serveur**

- éditer le code du client pour qu'il se connecte à la bonne IP et au bon port
- utilisez l'application !
- vous devez déterminer, si c'est pas déjà fait, à quoi sert l'application

## 2. Exploit

➜ **On est face à une application qui, d'une façon ou d'une autre, prend ce que le user saisit, et l'évalue.**

Ca doit lever un giga red flag dans votre esprit de hacker ça. Tu saisis ce que tu veux, et le serveur le lit et l'interprète.

🌞 **Injecter du code serveur**

- démerdez-vous pour arriver à faire exécuter du code arbitraire au serveur
- tu sais comment te co au serveur, et tu sais que ce que tu lui envoies, il l'évalue
- vous pouvez normalement avoir une injection de code :
  - exécuter du code Python
  - et normalement, exécuter des commandes shell depuis cette injection Python

## 3. Reverse shell

➜ **Injecter du code c'est bien mais...**

- souvent c'est ***chiant*** si on veut vraiment prendre le contrôle du serveur
- genre ici, à chaque commande, faut lancer une connexion au serveur étou, relou
- on pourrait lancer un serveur à nous sur la machine, et s'y connecter, mais s'il y a un firewall, c'est niquéd
- ***reverse shell* à la rescousse** : l'idée c'est de lancer un shell sur le serveur victime

> C'est *comme* une session SSH, mais c'est à la main, et c'est le serveur qui se connecte à toi pour que toi tu aies le shell. Genre c'est l'inverse de d'habitude. D'où le nom : *reverse* shell.

➜ **Pour pop un reverse shell**

- **en premier**
  - sur une machine que tu contrôles
  - tu lances un programme en écoute sur un port donné
  - un ptit `nc -lvp 9999` par exemple
- **en deuxième**
  - sur la machine où tu veux un shell, là où t'as de l'injection de code
  - tu demandes à l'OS d'ouvrir un port, et de se connecter à ton port ouvert sur la machine que tu contrôles
  - tu lances un shell (`bash` par exemple)
  - ce `bash` va "s'accrocher" à la session TCP
- **enfin**
  - tu retournes sur la machine que tu contrôles
  - et normalement, dans ta session `nc -lvp 9999`, t'as un shell qui a pop

➜ **Long story short**

- une commande sur une machine que tu contrôles
- une commande injectée sur le serveur victime
- t'as un shell sur le serveur victime depuis la machine que tu contrôles

> Quand tu commences à être bon en bash/réseau étou tu peux pondre ça tout seul. Mais sinon, on se contente de copier des commandes trouvées sur internet c'est très bien.

🌞 **Obtenez un reverse shell sur le serveur**

- si t'as injection de code, t'as sûrement possibilité de pop un reverse shell
- y'a plein d'exemple sur [le très bon hacktricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/linux)

🌞 **Pwn**

- voler les fichiers `/etc/shadow` et `/etc/passwd`
- voler le code serveur de l'application
- déterminer si d'autres services sont disponibles sur la machine

## 4. Bonus : DOS

Le DOS dans l'esprit, souvent c'est :

- d'abord t'es un moldu et tu trouves ça incroyable
- tu deviens un tech, tu te rends compte que c'est pas forcément si compliqué, ptet tu essaies
- tu deviens meilleur et tu te dis que c'est super lame, c'est nul techniquement, ça mène à rien, exploit c'est mieux
- tu deviens conscient, et ptet que parfois, des situations t'amèneront à trouver finalement le principe pas si inutile (politique ? militantisme ?)

⭐ **BONUS : DOS l'application**

- faut que le service soit indispo, d'une façon ou d'une autre
- fais le crash, fais le sleep, fais le s'arrêter, peu importe

## II. Remédiation

🌞 **Proposer une remédiation dév**

- le code serveur ne doit pas exécuter n'importe quoi
- il faut préserver la fonctionnalité de l'outil
- **vous devez donc proposer une version mise à jour du code**
  - code serveur ? code client ? les deux
  - les fonctionnalités doivent être préservées
  - les vulnérabilités doivent être fixed

🌞 **Proposer une remédiation système**

- l'environnement dans lequel tourne le service est foireux (le user utilisé ?)
- la machine devrait bloquer les connexions sortantes (pas de reverse shell possible)
- **vous devez donc proposer une suite d'étapes pour empêcher l'exploitation**
  - l'app vulnérable doit fonctionner
  - mais l'exploitation que vous avez utilisé doit être impossible
  - c'est un des jobs de l'admin (et du mec de sécu qui fait des recommandations aux admins) : héberger des apps vulnérables, mais empêcher l'exploitation
