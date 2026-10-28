from scapy.all import sniff, sendp, IP, TCP

CLIENT = "192.168.1.68"
RELAY  = "192.168.1.64"
SERVER = "192.168.1.2"
PORT   = 12345


def handle(pkt):
    print("packet", pkt)
    if pkt.haslayer(IP) and pkt.haslayer(TCP):
        src = pkt[IP].src
        dst = pkt[IP].dst
        if src == CLIENT and dst == RELAY:
            # client -> server: change source to relay
            pkt[IP].src = RELAY
            pkt[IP].dst = SERVER
            sendp(pkt, iface="Беспроводная сеть")
        elif src == SERVER and dst == RELAY:
            # server -> relay: change dest to client
            pkt[IP].src = RELAY
            pkt[IP].dst = CLIENT
            sendp(pkt, iface="Беспроводная сеть")


sniff(iface="Беспроводная сеть", filter="tcp and port 12345", prn=handle, store=0)
