from scapy.all import *

list = ""
def dns_sniff(packet):
    global list
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        if ("~~end~~" in domain_name):
            print(list)
            quit()
        elif ("~" in domain_name and "~~end~~" !in domain_name):
            index = domain_name.find("~")
            list = list + domain_name[index + 1:-18]

sniff(filter='udp port 53', prn=dns_sniff)

