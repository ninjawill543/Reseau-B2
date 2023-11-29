from scapy.all import *

def dns_sniff(packet):
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        print(domain_name[:-18])

sniff(filter='udp port 53', prn=dns_sniff)

