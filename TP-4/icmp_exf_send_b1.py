from scapy.all import IP, ICMP, send
import sys

start_value = "°°°1°°°"
start = (IP(dst=sys.argv[1])/ICMP()/start_value)
send(start)

to_send = str(sys.argv[2])
    
list = ([to_send[i:i + 7] for i in range(0, len(to_send), 7)])

for i in list:
    packet = (IP(dst=sys.argv[1])/ICMP()/i)
    send(packet)


end_value = "°°°0°°°"
end = (IP(dst=sys.argv[1])/ICMP()/end_value)
send(end)
