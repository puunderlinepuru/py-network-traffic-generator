from scapy.all import *
import random

def send_icmp(dest_ip, tos=0, src_ip="192.168.1.1", id=random.randint(1, 65535)):
    # Create an ICMP packet with the required fields
    icmp = IP(dst=dest_ip, tos=tos, src=src_ip, id=id)/ICMP()/"Hello, World!"

    # Send the packet and get the response
    resp = sr1(icmp)

    if resp:
        print("Received ICMP reply from", dest_ip)
    else:
        print("No response received.")

# Test the function with a destination IP, ToS=8 (Minimize Delay), source IP and random packet ID
send_icmp(dest_ip="192.168.1.2", tos=8, src_ip="192.168.1.1")
