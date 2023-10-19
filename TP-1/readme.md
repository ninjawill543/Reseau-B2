# TP1 : Maîtrise réseau du poste


- [TP1 : Maîtrise réseau du poste](#tp1--maîtrise-réseau-du-poste)
- [I. Basics](#i-basics)
- [II. Go further](#ii-go-further)
- [III. Le requin](#iii-le-requin)

# I. Basics

☀️ **Carte réseau WiFi**


```bash
m4ul@thinkpad:~$ ip a

3: wlp0s20f3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000

    link/ether b0:3c:dc:ae:ab:6e brd ff:ff:ff:ff:ff:ff

    inet 172.20.10.2/28 brd 172.20.10.15 scope global dynamic noprefixroute wlp0s20f3

```
- l'adresse MAC de votre carte WiFi: `b0:3c:dc:ae:ab:6e`
- l'adresse IP de votre carte WiFi: `172.20.10.2`
- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
  - en notation CIDR: `/28`
  - ET en notation décimale:`255.255.255.240`

---

☀️ **Déso pas déso**


- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi: `172.20.0.0`
- l'adresse de broadcast: `172.20.255.255`
- le nombre d'adresses IP disponibles dans ce réseau:`65536 mais 65434 utilisables`

J'ai pas du tout utiliser un site: https://www.calculator.net/ip-subnet-calculator.html?cclass=any&csubnet=16&cip=172.20.10.2&ctype=ipv4&printit=0&x=84&y=31

---

☀️ **Hostname**

```bash
m4ul@thinkpad:~$ cat /etc/hostname
thinkpad
```

---

☀️ **Passerelle du réseau**

- l'adresse IP de la passerelle du réseau:
```bash
m4ul@thinkpad:~$ ip route
default via 172.20.10.1 dev wlp0s20f3 proto dhcp metric 600 
```

- l'adresse MAC de la passerelle du réseau:
```bash
m4ul@thinkpad:~$ ip neigh | grep 172.20.10.1
172.20.10.1 dev wlp0s20f3 lladdr 4a:b8:a3:88:38:64 REACHABLE
```
---

☀️ **Serveur DHCP et DNS**

- l'adresse IP du serveur DHCP qui vous a filé une IP: `172.20.10.1`
```bash
m4ul@thinkpad:~$ cat /var/log/syslog | grep -i 'dhcp' 
Oct 12 11:35:47 thinkpad dhclient[6213]: DHCPACK of 172.20.10.2 from 172.20.10.1 (xid=0xe2ac871b)
```
- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet: `172.20.10.1`
```bash
m4ul@thinkpad:~$ resolvectl status
Link 3 (wlp0s20f3)
    Current Scopes: DNS
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 172.20.10.1
       DNS Servers: 172.20.10.1
```

---

☀️ **Table de routage**


- dans votre table de routage, laquelle est la route par défaut:
```bash
m4ul@thinkpad:~$ ip route
default via 172.20.10.1 dev wlp0s20f3 proto dhcp metric 600 
```

---


# II. Go further

---

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`:
```bash
m4ul@thinkpad:~$ cat /etc/hosts
1.1.1.1		b2.hello.vous
```
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`:
```bash
m4ul@thinkpad:~$ ping b2.hello.vous -c 1
PING b2.hello.vous (1.1.1.1) 56(84) bytes of data.
64 bytes from b2.hello.vous (1.1.1.1): icmp_seq=1 ttl=53 time=47.3 ms
```


---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

```bash
m4ul@thinkpad:~$ ss -tnp
State          Recv-Q          Send-Q                                               Local Address:Port                         Peer Address:Port         Process                                            
ESTAB          0               0                                                      172.20.10.2:60198                      35.186.227.140:443           users:(("firefox",pid=2738,fd=183))               
ESTAB          0               0                                                      172.20.10.2:47132                        34.117.65.55:443           users:(("firefox",pid=2738,fd=182))               
ESTAB          0               0                                                      172.20.10.2:41740                      34.110.207.168:443           users:(("firefox",pid=2738,fd=100))     
```

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo: `35.186.227.140, 34.117.65.55, 34.110.207.168`

- le port du serveur auquel vous êtes connectés: `443`

- le port que votre PC a ouvert en local pour se connecter au port du serveur distant: `60198, 47132, 41740`


---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`:
```bash
m4ul@thinkpad:~$ dig www.ynov.com
www.ynov.com.		377	IN	A	104.26.11.233
www.ynov.com.		377	IN	A	172.67.74.226
www.ynov.com.		377	IN	A	104.26.10.233
```

- à quel nom de domaine correspond l'IP `174.43.238.89` :  
`89.sub-174-43-238.myvzw.com`
```bash
m4ul@thinkpad:~$ dig -x 174.43.238.89

; <<>> DiG 9.18.12-0ubuntu0.22.04.3-Ubuntu <<>> -x 174.43.238.89
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7752
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;89.238.43.174.in-addr.arpa.	IN	PTR

;; ANSWER SECTION:
89.238.43.174.in-addr.arpa. 4476 IN	PTR	89.sub-174-43-238.myvzw.com.
```
---

☀️ **Hop hop hop**



- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`:
```bash
m4ul@thinkpad:~$ traceroute www.ynov.com
traceroute to www.ynov.com (104.26.11.233), 64 hops max
  1   172.20.10.1  3,373ms  15,657ms  27,480ms 
  2   *  *  * 
  3   *  *  * 
  4   *  *  * 
  5   *  *  * 
  6   10.151.14.50  56,881ms  34,240ms  23,102ms 
  7   *  *  89.89.101.56  125,238ms 
  8   62.34.2.169  32,693ms  28,859ms  32,164ms 
  9   212.194.171.137  34,550ms  29,265ms  80,945ms 
 10   *  *  * 
 11   *  *  * 
 12   172.71.120.2  41,934ms  37,466ms  33,209ms 
 13   104.26.11.233  27,682ms  30,235ms  60,027ms 
```

---

☀️ **IP publique**


- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP):
```bash
m4ul@thinkpad:~$ curl https://ipinfo.io/ip ; echo
195.7.117.146
```

---

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

> Allez-y mollo, on va vite flood le réseau sinon. :)


# III. Le requin

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
[Lien vers capture ARP](./arp.pcap)

Filtre: arp

---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
[Lien vers capture DNS](./dns.pcap)


Filtre: eth.src == b0:3c:dc:ae:ab:6e && dns

---


☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
[Lien vers capture TCP](./tcp.pcap)


---

