# TP7 SECU : Accès réseau sécurisé

On passe blue team cette fois ! On va voir un peu comment sécuriser l'accès à un parc de machines à distance, de façon assez robuste.

L'objectif :

- tout est loggé
- **l'accès à distance** est "sécurisé"
  - on prouve l'identité du serveur au user
  - le user est authentifié (password ou clé en plus de son username)
- **l'accès est centralisé** : une seule machine accueille tout le trafic
- quelques mesures de sécurité supplémentaires

Concrètement, au menu :

- **serveur VPN**
  - toutes les machines du TP, votre PC compris, sont des clients du VPN
  - le réseau VPN est un réseau privé au sein duquel seront hébergés des services
  - la connexion VPN est un prérequis obligatoire pour accéder aux autres machines du parc
- **bastion SSH**
  - une machine dédiée à accueillir uniquement des connexions SSH
  - les autres machines du parc n'acceptent les connexions SSH que si elles viennent de cette IP
  - si on veut se co à une machine en SSH, on est obligés de passer par le bastion
  - tous les serveurs SSH ne sont accessibles qu'au sein du réseau VPN
- **HTTPS** trusted
  - on va gérer une CA maison pour signer des certificats nous-mêmes
  - on ajoutera le certificat de la CA à votre navigateur, pour avoir un beau cadenas vert avec votre propre cert
  - le serveur HTTP n'est disponible qu'au sein du réseau VPN

![No one can use it](./img/no_one.png)

## Sommaire

- [TP7 SECU : Accès réseau sécurisé](#tp7-secu--accès-réseau-sécurisé)
  - [Sommaire](#sommaire)
- [0. Setup](#0-setup)
- [I. VPN](#i-vpn)
- [II. SSH](#ii-ssh)
  - [1. Setup](#1-setup)
  - [2. Bastion](#2-bastion)
  - [3. Connexion par clé](#3-connexion-par-clé)
  - [4. Conf serveur SSH](#4-conf-serveur-ssh)
- [III. HTTP](#iii-http)
  - [1. Initial setup](#1-initial-setup)
  - [2. Génération de certificat et HTTPS](#2-génération-de-certificat-et-https)
    - [A. Préparation de la CA](#a-préparation-de-la-ca)
    - [B. Génération du certificat pour le serveur web](#b-génération-du-certificat-pour-le-serveur-web)
    - [C. Bonnes pratiques RedHat](#c-bonnes-pratiques-redhat)
    - [D. Config serveur Web](#d-config-serveur-web)
    - [E. Bonus renforcement TLS](#e-bonus-renforcement-tls)

# 0. Setup


# I. VPN

Dans cette section, vous allez monter un serveur VPN. Le but : avoir un réseau LAN privé, accessible qu'après connexion au serveur VPN. On continuera à se servir de ce réseau VPN dans le reste du TP.

![VPN](./img/vpn.jpg)

| Machine            | LAN `10.7.1.0/24` | VPN `10.7.2.0/24` |
| ------------------ | ----------------- | ----------------- |
| `vpn.tp7.secu`     | `10.7.1.100/24`   |                   |
| `martine.tp7.secu` | `10.7.1.11/24`    | `10.7.2.11/24`    |
| ton PC             | X                 | `10.7.2.100/24`   |

🌞 **Monter un serveur VPN Wireguard sur `vpn.tp7.secu`**

```
$ sudo modprobe wireguard

$ lsmod | grep wireguard

$ sudo echo wireguard > /etc/modules-load.d/wireguard.conf

$ sudo dnf install wireguard-tools
```
```
$ wg genkey | sudo tee /etc/wireguard/server.key

$ sudo chmod 0400 /etc/wireguard/server.key

$ sudo cat /etc/wireguard/server.key | wg pubkey | sudo tee /etc/wireguard/server.pub
```
```
$ sudo cat /etc/wireguard/wg0.conf

[Interface]
PrivateKey = GHsfZF+6MwpxFED0Va7JLKpD4Qf4VBvoS2Av5eo0dnU= 

Address = 10.7.2.0/24

ListenPort = 51820

SaveConfig = true

PostUp = firewall-cmd --zone=public --add-masquerade
PostUp = firewall-cmd --direct --add-rule ipv4 filter FORWARD 0 -i wg -o eth0 -j ACCEPT
PostUp = firewall-cmd --direct --add-rule ipv4 nat POSTROUTING 0 -o eth0 -j MASQUERADE

PostDown = firewall-cmd --zone=public --remove-masquerade
PostDown = firewall-cmd --direct --remove-rule ipv4 filter FORWARD 0 -i wg -o eth0 -j ACCEPT
PostDown = firewall-cmd --direct --remove-rule ipv4 nat POSTROUTING 0 -o eth0 -j MASQUERADE

[Peer]
PublicKey = lkJZNYwGK226dGnjx2DYlb6lTlW/ifJ8UqPs8Gi2ji4=

AllowedIPs = 10.7.2.11/24
```
```
$ sudo cat /etc/sysctl.conf

net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1


$ sudo sysctl -p
```
```
$ sudo firewall-cmd --add-port=51820/udp --permanent
$ sudo firewall-cmd --reload
```
```
$ sudo systemctl start wg-quick@wg0.service
$ sudo systemctl enable wg-quick@wg0.service
```

🌞 **Client Wireguard sur `martine.tp7.secu`**

Vous pouvez lancer le script [vpn](VPN.sh) avec comme argument l'ip du client souhaité.

🌞 **Client Wireguard sur votre PC**

- configurez un client Wireguard sur votre PC
- vous devriez pouvoir conserver votre accès internet (sans passer par le VPN) ET ping `martine.tp7.secu` en utilisant le VPN

➜ **A partir de ce moment dans le TP**

- toutes les machines doivent être connectées au VPN
- toutes les machines récupèrent un accès internet en passant par le réseau VPN (à part votre PC bien sûr)

# II. SSH

## 1. Setup

| Machine            | LAN `10.7.1.0/24` | VPN `10.7.2.0/24` |
| ------------------ | ----------------- | ----------------- |
| `vpn.tp7.secu`     | `10.7.1.100/24`   |                   |
| `martine.tp7.secu` | `10.7.1.11/24`    | `10.7.2.11/24`    |
| `bastion.tp7.secu` | `10.7.1.12/24`    | `10.7.2.12/24`    |
| `web.tp7.secu`     | `10.7.1.13/24`    | `10.7.2.13/24`    |
| ton PC             | X                 | `10.7.2.100/24`   |

🌞 **Générez des confs Wireguard pour tout le monde**

- tout le monde doit pouvoir se ping en utilisant les IPs du VPN
- il serait ptet malin de faire un script non ? J'propose hein.

> *Notez que dans un cas réel, la clé privée et la clé publique de chaque client doivent être générés par les client eux-mêmes. Sinon ce serait comme choisir un password pour quelqu'un d'autre : il est compromis dès sa création ! Dans notre cas, le client génère sa clé privée et sa clé publique, et il file sa clé publique au serveur (seule info nécessaire pour la conf serveur).*

## 2. Bastion

On va décider que la machine `bastion.tp7.secu` est notre bastion SSH : si on veut se connecter à n'importe quel serveur en SSH, on doit passer par lui.

Par exemple, si on essaie de se connecter à `web.tp7.secu` en direct sur l'IP `10.7.2.13/24`, il dois nous jeter.

En revanche, si on se connecte d'abord à `bastion.tp7.secu`, puis on se connecte à `web.tp7.secu`, alors là ça fonctionne.

On peut faire ça en une seule commande SSH en utilisant la feature de jump SSH. Littéralement : on rebondit sur une machine avant d'arriver sur une autre. Comme ça :

```bash
# on remplace
ssh bastion.tp7.secu
# puis, une fois connecté :
ssh web.tp7.secu

# paaaar une seule commande directe :

# avec les noms
ssh -j bastion.tp7.secu web.tp7.secu
# avec les IPs
ssh -j 10.7.2.12 10.7.2.13
```

🌞 **Empêcher la connexion SSH directe sur `web.tp7.secu`**

- on autorise la connexion SSH que si elle vient de `bastion.tp7.secu`
- avec le firewall : on bloque le trafic à destination du port 22 s'il ne vient pas de `10.7.2.12`
- prouvez que ça fonctionne
  - que le trafic est bien bloqué en direct
  - mais qu'on peut y accéder depuis `bastion.tp7.secu`

🌞 **Connectez-vous avec un jump SSH**

- en une seule commande, vous avez un shell sur `web.tp7.secu`

> Désormais, le bastion centralise toutes les connexions SSH. Il devient un noeud très important dans la gestion du parc, et permet à lui seul de tracer toutes les connexions SSH effectuées.

## 3. Connexion par clé

🌞 **Générez une nouvelle paire de clés pour ce TP**

- vous les utiliserez pour vous connecter aux machines
- vous n'utiliserez **PAS** l'algorithme RSA
- faites des recherches pour avoir l'avis de gens qualifiés sur l'algo à choisir en 2023 pour avoir la "meilleure" clé (sécurité et perfs)

## 4. Conf serveur SSH

🌞 **Changez l'adresse IP d'écoute**

- sur toutes les machines
- vos serveurs SSH ne doivent être disponibles qu'au sein du réseau VPN
- prouvez que vous ne pouvez plus accéder à une sesion SSH en utilisant l'IP host-only (obligé de passer par le VPN)

🌞 **Améliorer le niveau de sécurité du serveur**

- sur toutes les machines
- mettre en oeuvre au moins 3 configurations additionnelles pour améliorer le niveau de sécurité
- 3 lignes (au moins) à changer quoi
- le doc est vieux, mais en dehors des recommendations pour le chiffrement le reste reste très cool : [l'ANSSI avait édité des recommendations pour une conf OpenSSH](https://cyber.gouv.fr/publications/openssh-secure-use-recommendations)

# III. HTTP

## 1. Initial setup

🌞 **Monter un bête serveur HTTP sur `web.tp7.secu`**

- avec NGINX
- une page d'accueil HTML avec écrit "toto" ça ira
- **il ne doit écouter que sur l'IP du VPN**
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.1.1.1:80;

    # vous collez un ptit index.html dans ce dossier et zou !
    root /var/www/site_nul;
}
```

🌞 **Site web joignable qu'au sein du réseau VPN**

- le site web ne doit écouter que sur l'IP du réseau VPN
- le trafic à destination du port 80 n'est autorisé que si la requête vient du réseau VPN (firewall)
- prouvez qu'il n'est pas possible de joindre le site sur son IP host-only

🌞 **Accéder au site web**

- depuis votre PC, avec un `curl`
- vous êtes normalement obligés d'être co au VPN pour accéder au site

## 2. Génération de certificat et HTTPS

### A. Préparation de la CA

On va commencer par générer la clé et le certificat de notre Autorité de Certification (CA). Une fois fait, on pourra s'en servir pour signer d'autres certificats, comme celui de notre serveur web.

Pour que la connexion soit trusted, il suffira alors d'ajouter le certificat de notre CA au magasin de certificats de votre navigateur sur votre PC.

🌞 **Générer une clé et un certificat de CA**

```bash
# mettez des infos dans le prompt, peu importe si c'est fake
# on va vous demander un mot de passe pour chiffrer la clé aussi
$ openssl genrsa -des3 -out CA.key 4096
$ openssl req -x509 -new -nodes -key CA.key -sha256 -days 1024  -out CA.pem
$ ls
# le pem c'est le certificat (clé publique)
# le key c'est la clé privée
```

### B. Génération du certificat pour le serveur web

Il est temps de générer une clé et un certificat que notre serveur web pourra utiliser afin de proposer une connexion HTTPS.

🌞 **Générer une clé et une demande de signature de certificat pour notre serveur web**

```bash
$ openssl req -new -nodes -out web.tp7.secu.csr -newkey rsa:4096 -keyout web.tp7.secu.key
$ ls
# web.tp7.secu.csr c'est la demande de signature
# web.tp7.secu.key c'est la clé qu'utilisera le serveur web
```

🌞 **Faire signer notre certificat par la clé de la CA**

- préparez un fichier `v3.ext` qui contient :

```ext
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = web.tp7.secu
DNS.2 = www.tp7.secu
```

- effectuer la demande de signature pour récup un certificat signé par votre CA :

```bash
$ openssl x509 -req -in web.tp7.secu.csr -CA CA.pem -CAkey CA.key -CAcreateserial -out web.tp7.secu.crt -days 500 -sha256 -extfile v3.ext
$ ls
# web.tp7.secu.crt c'est le certificat qu'utilisera le serveur web
```

### C. Bonnes pratiques RedHat

Sur RedHat, il existe un emplacement réservé aux clés et certificats :

- `/etc/pki/tls/certs/` pour les certificats
  - pas choquant de voir du droit de lecture se balader
- `/etc/pki/tls/private/` pour les clés
  - ici, seul le propriétaire du fichier a le droit de lecture

🌞 **Déplacer les clés et les certificats dans l'emplacement réservé**

- gérez correctement les permissions de ces fichiers

### D. Config serveur Web

🌞 **Ajustez la configuration NGINX**

- le site web doit être disponible en HTTPS en utilisant votre clé et votre certificat
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.7.1.103:443 ssl;

    ssl_certificate /etc/pki/tls/certs/web.tp7.secu.crt;
    ssl_certificate_key /etc/pki/tls/private/web.tp7.secu.key;
    
    root /var/www/site_nul;
}
```

🌞 **Prouvez avec un `curl` que vous accédez au site web**

- depuis votre PC
- avec un `curl -k` car il ne reconnaît pas le certificat là

🌞 **Ajouter le certificat de la CA dans votre navigateur**

- vous pourrez ensuite visitez `https://web.tp7.b2` sans alerte de sécurité, et avec un cadenas vert
- il faut aussi ajouter l'IP de la machine à votre fichier `hosts` pour qu'elle corresponde au nom `web.tp7.b2`

> *En entreprise, c'est comme ça qu'on fait pour qu'un certificat de CA non-public soit trusted par tout le monde : on dépose le certificat de CA dans le navigateur (et l'OS) de tous les PCs. Evidemment, on utilise une technique de déploiement automatisé aussi dans la vraie vie, on l'ajoute pas à la main partout hehe.*

### E. Bonus renforcement TLS

⭐ **Bonus : renforcer la conf TLS**

- faites quelques recherches pour forcer votre serveur à n'utiliser que des méthodes de chiffrement fortes
- ça implique de refuser les connexions SSL, ou TLS 1.0, on essaie de forcer TLS 1.3

![Do you even](img/do_you_even.jpg)