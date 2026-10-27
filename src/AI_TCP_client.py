#!/usr/bin/env python3

from scapy.all import *
import time
import sys

def tcp_client():
    # Read payload from file
    try:
        with open('./file.txt', 'r') as f:
            payload = f.read()
    except FileNotFoundError:
        print("Error: ./file.txt not found")
        return
    
    # Client configuration
    client_ip = "192.168.1.64"   # Change to your client IP
    client_port = 54321
    server_ip = "192.168.1.64"  # Change to your server IP
    server_port = 12345
    
    interface="Беспроводная сеть"
    
    print(f"Starting TCP client connecting to {server_ip}:{server_port}")
    
    # Send SYN packet
    syn_packet = IP(dst=server_ip, src=client_ip) / \
                TCP(sport=client_port, dport=server_port, 
                    flags="S", seq=1000)
    print("Sending SYN packet...")
    syn_ack = sr1(syn_packet, iface=interface, timeout=5)
    
    if not syn_ack:
        print("No response received from server")
        return
    
    if syn_ack.haslayer(TCP):
        tcp_layer = syn_ack[TCP]
        if tcp_layer.flags == 18:  # SYN-ACK
            print(f"Received SYN-ACK from {server_ip}:{server_port}")
            
            # Send ACK packet
            ack_packet = IP(dst=server_ip, src=client_ip) / \
                        TCP(sport=client_port, dport=server_port,
                            flags="A", seq=1001, ack=tcp_layer.seq + 1)
            send(ack_packet, iface=interface)
            print("Sent ACK packet")
            
            # Wait for server data
            def handle_server_data(pkt):
                if pkt.haslayer(TCP) and pkt.haslayer(Raw):
                    tcp_layer = pkt[TCP]
                    if tcp_layer.flags == 16:  # ACK with payload
                        received_payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                        print(f"Received data from server: {received_payload}")
                        
            # Listen for data packet
            sniff(iface=interface, filter=f"tcp and host {server_ip} and port {client_port}", 
                  lfilter=lambda x: x.haslayer(TCP) and x.haslayer(Raw), 
                  timeout=10, prn=handle_server_data)
            
            # Send FIN packet
            fin_packet = IP(dst=server_ip, src=client_ip) / \
                        TCP(sport=client_port, dport=server_port,
                            flags="FA", seq=1001 + len(payload), ack=tcp_layer.seq + 1)
            send(fin_packet, iface=interface)
            print("Sent FIN packet")
            
            # Wait for FIN-ACK
            def handle_fin_ack(pkt):
                if pkt.haslayer(TCP) and pkt[TCP].flags == 17:  # FIN-ACK
                    print("Received FIN-ACK, connection closed")
                    
            sniff(iface=interface, filter=f"tcp and host {server_ip} and port {client_port}", 
                  lfilter=lambda x: x.haslayer(TCP) and x[TCP].flags == 17, 
                  timeout=5, prn=handle_fin_ack)
    
    print("TCP session completed")

if __name__ == "__main__":
    tcp_client()
