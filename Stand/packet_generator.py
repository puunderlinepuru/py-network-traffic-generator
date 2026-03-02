#  https://tl10k.dev/categories/networking/general/simple-tcp-scapy/#the-server-script

from scapy.all import IP, TCP, send

# Step 1: Creating a simple IP packet
packet = IP(dst="192.168.1.1")  # Setting the destination IP
print(packet.show())  # Display packet details

# packet = IP(dst="10.0.0.2") / TCP(dport=80, sport=12345, flags="S")
packet = IP(dst="10.0.0.2") / TCP(dport=80, sport=12345)
print(packet.show())

# for i in range(5):
send(packet)