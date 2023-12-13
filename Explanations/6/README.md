# TP6 : Un peu de root-me

P'tit sujet de TP autour de **plusieurs épreuves [root-me](https://www.root-me.org)**.

**But du TP** : vous pétez les épreuves, je vous accompagne pour le faire, et en rendu je veux un ptit write-up.

> *Un write-up c'est la démarche technique pour arriver à l'objectif avec un peu de blabla pour expliquer ladite démarche.*

Chaque partie correspond à un chall root-me. Je compléterai un peu le sujet de TP au fur et à mesure que vous avancez.

## Sommaire

- [TP6 : Un peu de root-me](#tp6--un-peu-de-root-me)
  - [Sommaire](#sommaire)
  - [I. DNS Rebinding](#i-dns-rebinding)
  - [II. Netfilter erreurs courantes](#ii-netfilter-erreurs-courantes)
  - [III. ARP Spoofing Ecoute active](#iii-arp-spoofing-ecoute-active)
  - [IV. Bonus : Trafic Global System for Mobile communications](#iv-bonus--trafic-global-system-for-mobile-communications)

## I. DNS Rebinding

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding)

- utilisez l'app web et comprendre à quoi elle sert
- lire le code ligne par ligne et comprendre chaque ligne
  - en particulier : comment/quand est récupéré la page qu'on demande
- se renseigner sur la technique DNS rebinding

🌞 **Write-up de l'épreuve**

🌞 **Proposer une version du code qui n'est pas vulnérable**

- les fonctionnalités doivent être maintenues
  - genre le site doit toujours marcher
  - dans sa qualité actuelle
    - on laisse donc le délire de `/admin` joignable qu'en `127.0.0.1`
    - c'est un choix effectué ça, on le remet pas en question
- mais l'app web ne doit plus être sensible à l'attaque

## II. Netfilter erreurs courantes

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Netfilter-erreurs-courantes)

- à chaque paquet reçu, un firewall parcourt les règles qui ont été configurées afin de savoir s'il accepte ou non le paquet
- une règle c'est genre "si un paquet vient de telle IP alors je drop"
- à chaque paquet reçu, il lit la liste des règles **de haut en bas** et dès qu'une règle match, il effectue l'action
- autrement dit, l'ordre des règles est important
- on cherche à match une règle qui est en ACCEPT

🌞 **Write-up de l'épreuve**

🌞 **Proposer un jeu de règles firewall**

- on doit là encore aboutir au même fonctionnalités : pas de régression
- mais la protection qui a été voulue est vraiment mise en place (limitation du bruteforce)

## III. ARP Spoofing Ecoute active

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/ARP-Spoofing-Ecoute-active)

🌞 **Write-up de l'épreuve**

🌞 **Proposer une configuration pour empêcher votre attaque**

- empêcher la première partie avec le Poisoning/MITM
- empêcher la seconde partie (empêcher de retrouver le password de base de données)
  - regarder du côté des plugins d'authentification de cette app précise
  - que pensez-vous du mot de passe choisi

## IV. Bonus : Trafic Global System for Mobile communications

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Trafic-Global-System-for-Mobile-communications)

⭐ **BONUS : Write-up de l'épreuve**
