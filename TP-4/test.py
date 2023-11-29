from scapy.all import *

unique_strings = set()

def dns_sniff(packet):
    global unique_strings
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        if "~~end~~" in domain_name:
            print("Unique strings:", unique_strings)
            quit()
        elif "~" in domain_name and not "~~end~~" in domain_name:
            index = domain_name.find("~")
            substring = domain_name[index + 1:-18]
            
            # Add unique substring to the set
            unique_strings.add(substring)

sniff(filter='udp port 53', prn=dns_sniff)

