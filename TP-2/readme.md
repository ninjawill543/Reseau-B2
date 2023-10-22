# TP2 : Environnement virtuel

![](../images/hello.gif)



- [I. Topologie réseau](#i-topologie-réseau)
  - [Compte-rendu](#compte-rendu)
- [II. Interlude accès internet](#ii-interlude-accès-internet)
- [III. Services réseau](#iii-services-réseau)
  - [1. DHCP](#1-dhcp)
  - [2. Web web web](#2-web-web-web)


# I. Topologie réseau
## Compte-rendu

☀️ Sur **`node1.lan1.tp2`**


- afficher ses cartes réseau
```bash
[user1@node1-lan1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:3a:8e:aa brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe3a:8eaa/64 scope link 
       valid_lft forever preferred_lft forever
```
- afficher sa table de routage



```bash
[user1@node1-lan1 ~]$ ip r s
10.1.1.0/24 dev enp0s3 proto kernel scope link src 10.1.1.11 metric 100 
10.1.2.0/24 via 10.1.1.254 dev enp0s3 proto static metric 100 
```
- prouvez qu'il peut joindre `node2.lan2.tp2`

```bash
[user1@node1-lan1 ~]$ ping node2-lan2
PING node2-lan2 (10.1.2.12) 56(84) bytes of data.
64 bytes from node2-lan2 (10.1.2.12): icmp_seq=1 ttl=63 time=1.03 ms
64 bytes from node2-lan2 (10.1.2.12): icmp_seq=2 ttl=63 time=1.56 ms
64 bytes from node2-lan2 (10.1.2.12): icmp_seq=3 ttl=63 time=1.38 ms
^C
--- node2-lan2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 1.026/1.324/1.564/0.223 ms
```
- prouvez avec un `traceroute` que le paquet passe bien par `router.tp2`
```bash
[user1@node1-lan1 ~]$ traceroute node2-lan2
traceroute to node2-lan2 (10.1.2.12), 30 hops max, 60 byte packets
 1  router (10.1.1.254)  1.798 ms  1.754 ms  1.718 ms
 2  node2-lan2 (10.1.2.12)  1.686 ms !X  1.419 ms !X  1.359 ms !X
```

# II. Interlude accès internet

☀️ **Sur `router.tp2`**

- prouvez que vous avez un accès internet (ping d'une IP publique)
```bash
[user1@router ~]$ ping -c 1 216.58.214.174
PING 216.58.214.174 (216.58.214.174) 56(84) bytes of data.
64 bytes from 216.58.214.174: icmp_seq=1 ttl=63 time=27.1 ms

--- 216.58.214.174 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 27.141/27.141/27.141/0.000 ms
```

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

```bash
[user1@router ~]$ ping -c 1 amazon.com
PING amazon.com (54.239.28.85) 56(84) bytes of data.
64 bytes from 54.239.28.85 (54.239.28.85): icmp_seq=1 ttl=63 time=118 ms

--- amazon.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 117.506/117.506/117.506/0.000 ms
```

☀️ **Accès internet LAN1 et LAN2**

- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp2`
```bash
[user1@node2-lan1 ~]$ cat /etc/sysconfig/network-scripts/route-enp0s3 
10.1.2.0/24 via 10.1.1.254 dev enp0s3
default via 10.1.1.254 dev enp0s3
```
```bash
[user1@node2-lan1 ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 
NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.12
NETMASK=255.255.255.0

DNS1=1.1.1.1
```
- prouvez que `node2.lan1.tp2` a un accès internet :
  - il peut ping une IP publique
```bash
[user1@node2-lan1 ~]$ ping -c 1 216.58.214.174
PING 216.58.214.174 (216.58.214.174) 56(84) bytes of data.
64 bytes from 216.58.214.174: icmp_seq=1 ttl=61 time=35.2 ms

--- 216.58.214.174 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 35.201/35.201/35.201/0.000 ms
```
  - il peut ping un nom de domaine public
```bash
[user1@node2-lan1 ~]$ ping -c 1 google.com
PING google.com (142.250.75.238) 56(84) bytes of data.
64 bytes from par10s41-in-f14.1e100.net (142.250.75.238): icmp_seq=1 ttl=61 time=26.8 ms

--- google.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 26.750/26.750/26.750/0.000 ms
```


# III. Services réseau


## 1. DHCP

![](../images/get_one.gif)



☀️ **Sur `dhcp.lan1.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp2` devient `dhcp.lan1.tp2`)
- changez son adresse IP en `10.1.1.253`
```bash
[user1@dhcp-lan1 ~]$ ip a
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:27:b3:54 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe27:b354/64 scope link 
       valid_lft forever preferred_lft forever
```
- setup du serveur DHCP
  - commande d'installation du paquet
```bash
[user1@dhcp-lan1 ~]$ sudo dnf -y install dhcp-server 
```
  - fichier de conf
```bash
[user1@dhcp-lan1 ~]$ sudo cat /etc/dhcp/dhcpd.conf
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
range 10.1.1.100 10.1.1.200;
option routers 10.1.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
```
  - service actif
```bash
[user1@dhcp-lan1 ~]$ sudo firewall-cmd --add-service=dhcp 
[user1@dhcp-lan1 ~]$ sudo firewall-cmd --reload
```
```bash
[user1@dhcp-lan1 ~]$ sudo systemctl enable --now dhcpd
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.
[user1@dhcp-lan1 ~]$ sudo systemctl status dhcpd
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Sun 2023-10-22 11:02:30 CEST; 11s ago
       Docs: man:dhcpd(8)
             man:dhcpd.conf(5)
   Main PID: 1411 (dhcpd)
     Status: "Dispatching packets..."
      Tasks: 1 (limit: 4611)
     Memory: 7.1M
        CPU: 5ms
     CGroup: /system.slice/dhcpd.service
             └─1411 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid

Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Config file: /etc/dhcp/dhcpd.conf
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Database file: /var/lib/dhcpd/dhcpd.leases
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: PID file: /var/run/dhcpd.pid
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Source compiled to use binary-leases
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Wrote 0 leases to leases file.
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Listening on LPF/enp0s3/08:00:27:27:b3:54/10.1.1.0/24
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Sending on   LPF/enp0s3/08:00:27:27:b3:54/10.1.1.0/24
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Sending on   Socket/fallback/fallback-net
Oct 22 11:02:30 dhcp-lan1 dhcpd[1411]: Server starting service.
Oct 22 11:02:30 dhcp-lan1 systemd[1]: Started DHCPv4 Server Daemon.
```


☀️ **Sur `node1.lan1.tp2`**

- demandez une IP au serveur DHCP
- prouvez que vous avez bien récupéré une IP *via* le DHCP
```bash
[user1@node1-lan1 ~]$ sudo dhclient -v enp0s3
[sudo] password for user1: 
Internet Systems Consortium DHCP Client 4.4.2b1
Copyright 2004-2019 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/enp0s3/08:00:27:3a:8e:aa
Sending on   LPF/enp0s3/08:00:27:3a:8e:aa
Sending on   Socket/fallback
DHCPDISCOVER on enp0s3 to 255.255.255.255 port 67 interval 3 (xid=0x8a495905)
DHCPOFFER of 10.1.1.101 from 10.1.1.253
DHCPREQUEST for 10.1.1.101 on enp0s3 to 255.255.255.255 port 67 (xid=0x8a495905)
DHCPACK of 10.1.1.101 from 10.1.1.253 (xid=0x8a495905)
bound to 10.1.1.101 -- renewal in 391 seconds.
```
- prouvez que vous avez bien récupéré l'IP de la passerelle
```bash
[user1@node1-lan1 ~]$ ip r s
default via 10.1.1.254 dev enp0s3 proto dhcp src 10.1.1.100 metric 100 
```
- prouvez que vous pouvez `ping node1.lan2.tp2`
```bash
[user1@node1-lan1 ~]$ ping node1-lan2
PING node1-lan2 (10.1.2.11) 56(84) bytes of data.
64 bytes from node1-lan2 (10.1.2.11): icmp_seq=1 ttl=63 time=1.46 ms
64 bytes from node1-lan2 (10.1.2.11): icmp_seq=2 ttl=63 time=1.83 ms
64 bytes from node1-lan2 (10.1.2.11): icmp_seq=3 ttl=63 time=1.99 ms
^C
--- node1-lan2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 1.460/1.758/1.985/0.220 ms
```

## 2. Web web web


☀️ **Sur `web.lan2.tp2`**

  - installation de NGINX
```bash
[user1@web-lan2 ~]$ sudo dnf install nginx
```
  - gestion de la racine web `/var/www/site_nul/`
  - configuration NGINX
```bash
[user1@web-lan2 ~]$ cat /etc/nginx/nginx.conf
    server {
        listen       80;
        listen       [::]:80;
        server_name  site_nul.tp2;
        root         /var/www/site_nul/;
```
  - service actif
```bash
[user1@web-lan2 ~]$ sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: active (running) since Sun 2023-10-22 13:53:11 CEST; 3min 47s ago
    Process: 1572 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
    Process: 1573 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
    Process: 1574 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
   Main PID: 1575 (nginx)
      Tasks: 2 (limit: 4611)
     Memory: 2.0M
        CPU: 10ms
     CGroup: /system.slice/nginx.service
             ├─1575 "nginx: master process /usr/sbin/nginx"
             └─1576 "nginx: worker process"

Oct 22 13:53:11 web-lan2 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Oct 22 13:53:11 web-lan2 nginx[1573]: nginx: the configuration file /etc/nginx/nginx.conf syntax is >
Oct 22 13:53:11 web-lan2 nginx[1573]: nginx: configuration file /etc/nginx/nginx.conf test is succes>
Oct 22 13:53:11 web-lan2 systemd[1]: Started The nginx HTTP and reverse proxy server.

```
  - ouverture du port firewall
```bash
[user1@web-lan2 ~]$ sudo firewall-cmd --permanent --add-service=http
[user1@web-lan2 ~]$ sudo firewall-cmd --reload
```
- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)
```bash
[user1@web-lan2 ~]$ sudo ss -ltunp | grep nginx
tcp   LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=1576,fd=6),("nginx",pid=1575,fd=6))
tcp   LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=1576,fd=7),("nginx",pid=1575,fd=7))
```
- prouvez que le firewall est bien configuré
```bash
[user1@web-lan2 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources: 
  services: cockpit dhcpv6-client http ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

☀️ **Sur `node1.lan1.tp2`**

- éditez le fichier `hosts` pour que `site_nul.tp2` pointe vers l'IP de `web.lan2.tp2`
- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp2`
```bash
[user1@node1-lan1 ~]$ curl site_nul.tp2
<!DOCTYPE html>
<html>
<head>
<title>Hola !</title>
</head>
<body>

<h1>Hellooooo Leo</h1>
<p>Welcome sur mon site super bien :)</p>

</body>
</html>
```

![](../images/yes.gif)


