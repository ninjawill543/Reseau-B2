from scapy.all import IP, ICMP, send
import sys

packet = IP(dst=sys.argv[1])/ICMP()/str(sys.argv[2])

#packet.show()
send(packet)


