from scapy.all import sniff, ICMP

output = ""
def print_it_please(packet):
    global output
    if (packet['ICMP'].type == 8 and len(packet['Raw'].load) <= 7):
        if (packet['Raw'].load.decode("utf-8") == "000~000"):
            print(output)
            quit()
        elif (packet['Raw'].load.decode("utf-8") != "111~111"):
            output = output + packet['Raw'].load.decode("utf-8")    
        
sniff(filter="icmp", prn=print_it_please, count=0)

#iface if you want to change interface for the sniff

