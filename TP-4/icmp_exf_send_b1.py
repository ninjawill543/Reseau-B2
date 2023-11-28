from scapy.all import IP, ICMP, send
import sys

start_value = "~~~"
start = (IP(dst=sys.argv[1])/ICMP()/start_value)
send(start)

to_send = str(sys.argv[2])
    
list = ([to_send[i:i + 3] for i in range(0, len(to_send), 3)])

for i in list:
    packet = (IP(dst=sys.argv[1])/ICMP()/i)
    send(packet)


end_value = "end"
end = (IP(dst=sys.argv[1])/ICMP()/end_value)
send(end)
