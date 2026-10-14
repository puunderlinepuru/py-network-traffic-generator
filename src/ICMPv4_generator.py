from scapy.all import *
import random

from scapy.modules.nmap import ICMP
from scapy.modules.nmap import IP

# ip_src_normal = "127.0.0.1"
# ip_src_sus = "127.0.0.1"
# ip_dst = "127.0.0.1"
# tos_normal = 8
# tos_sus = 7

if len(sys.argv) < 3:
    count = 30
    sus_packets_amount = 0
else:
    count = int(sys.argv[1])
    sus_packets_amount = int(sys.argv[2])
print(f'sending {count} packets')


def send_icmp(dest_ip, tos=0, src_ip="192.168.1.1", time_to_live=64, id=random.randint(1, 65535)):
    # Create an ICMP packet with the required fields
    icmp = IP(dst=dest_ip, ttl=time_to_live, tos=tos, src=src_ip, id=id)/ICMP()/"Hello, World!"

    # Send the packet and get the response
    resp = sr1(icmp)

    if resp:
        print("Received ICMP reply from", dest_ip)
    else:
        print("No response received.")




def ICMP_generate_traffic_src_ip(count, stego_amount, normal_src, stego_src, dst, normal_tos):

    sus_packets_index_start = random.randint(1,count-sus_packets_amount)
    print("injecting at ", sus_packets_index_start)

    if (count-stego_amount - sus_packets_index_start == 0):
        for _ in range(sus_packets_index_start):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)
        print("\n\n [INJECTION] \n\n")
        for _ in range(sus_packets_amount):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=stego_src)

    else:
        for _ in range(sus_packets_index_start):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)
        print("\n\n [INJECTION] \n\n")
        for _ in range(sus_packets_amount):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=stego_src)
        print("\n\n [INJECTION OVER] \n\n")
        for _ in range(count - (sus_packets_index_start + stego_amount)):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)

# TODO TOS -> ECN + DSCP
def ICMP_generate_traffic_tos(count, stego_amount, normal_src, dst, normal_tos, stego_tos):
    """
    Generates
    """
    sus_packets_index_start = random.randint(1,count-sus_packets_amount)
    print("injecting at ", sus_packets_index_start)

    if (count-stego_amount - sus_packets_index_start == 0):
        for _ in range(sus_packets_index_start):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)
        print("\n\n [INJECTION] \n\n")
        for _ in range(stego_amount):
            send_icmp(dest_ip=dst, tos=stego_tos, src_ip=normal_src)

    else:
        for _ in range(sus_packets_index_start):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)
        print("\n\n [INJECTION] \n\n")
        for _ in range(stego_amount):
            send_icmp(dest_ip=dst, tos=stego_tos, src_ip=normal_src)
        print("\n\n [INJECTION OVER] \n\n")
        for _ in range(count - (sus_packets_index_start + stego_amount)):
            send_icmp(dest_ip=dst, tos=normal_tos, src_ip=normal_src)