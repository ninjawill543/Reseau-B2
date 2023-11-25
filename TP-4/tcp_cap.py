from scapy.all import sniff

def print_it_please(packet):
    print("TCP SYN ACK reçu !")
    print(f"- Adresse IP src : {packet['IP'].src}")
    print(f"- Adresse IP dst : {packet['IP'].dst}")
    print(f"- Port TCP src : {packet['TCP'].sport}")
    print(f"- Port TCP dst : {packet['TCP'].dport}")

sniff(filter="tcp[tcpflags] == tcp-syn|tcp-ack", prn=print_it_please, count=1)

