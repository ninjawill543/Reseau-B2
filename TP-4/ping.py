from scapy.all import *


ping = ICMP(type=8)

packet = IP(src="192.168.1.71", dst="192.168.1.254")

frame = Ether(src="b0:3c:dc:ae:ab:6e", dst="44:D4:54:7B:E1:4C")

final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")

