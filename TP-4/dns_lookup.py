from scapy.all import *

frame = Ether(src="b0:3c:dc:ae:ab:6e", dst="44:D4:54:7B:E1:4C")

packet = IP(src="192.168.1.71", dst="192.168.1.254")

UDP = UDP(sport=RandShort(), dport=53)

dns = DNS(rd=1, qd=DNSQR(qname="ynov.com", qtype="A"))


final_frame = frame/packet/UDP/dns

answers, unanswered_packets = srp(final_frame, timeout=10)

print(answers[0].answer[0].an.rdata)
