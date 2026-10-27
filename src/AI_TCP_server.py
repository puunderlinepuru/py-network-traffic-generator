#!/usr/bin/env python3

from scapy.all import *
import time
import sys

def tcp_server():
    # Read payload from file
    try:
        with open('./file.txt', 'r') as f:
            payload = f.read()
    except FileNotFoundError:
        print("Error: ./file.txt not found")
        return
    
    # Server configuration
    client_ip = "192.168.1.68"   # Change to your client IP
    client_port = 54321
    server_ip = "192.168.1.64"  # Change to your server IP
    server_port = 12345
    
    interface="Беспроводная сеть"
    
    print(f"Starting TCP server on {server_ip}:{server_port}")
    print(f"Waiting for connection from {client_ip}:{client_port}")
    
    def handle_connection(packet):
        if packet.haslayer(TCP) and packet.haslayer(IP):
            tcp_layer = packet[TCP]
            ip_layer = packet[IP]
            
            # Check if it's a SYN packet
            if tcp_layer.flags == 2:  # SYN
                print(f"Received SYN from {ip_layer.src}:{tcp_layer.sport}")
                
                # Send SYN-ACK
                syn_ack = IP(dst=ip_layer.src, src=server_ip) / \
                         TCP(sport=server_port, dport=tcp_layer.sport, 
                             flags="SA", seq=1000, ack=tcp_layer.seq + 1)
                send(syn_ack, iface=interface)
                print("Sent SYN-ACK")
                
            # Check if it's an ACK packet (connection established)
            elif tcp_layer.flags == 16:  # ACK
                print(f"Received ACK from {ip_layer.src}:{tcp_layer.sport}")
                
                # Send payload data
                data_packet = IP(dst=ip_layer.src, src=server_ip) / \
                             TCP(sport=server_port, dport=tcp_layer.sport,
                                 flags="PA", seq=1001, ack=tcp_layer.seq + 1) / \
                             Raw(load=payload)
                send(data_packet, iface=interface)
                print("Sent payload data")
                
                # Send FIN packet
                fin_packet = IP(dst=ip_layer.src, src=server_ip) / \
                            TCP(sport=server_port, dport=tcp_layer.sport,
                                flags="FA", seq=1001 + len(payload), ack=tcp_layer.seq + 1)
                send(fin_packet, iface=interface)
                print("Sent FIN packet")
                
                # Wait for FIN-ACK
                def handle_fin_ack(pkt):
                    if pkt.haslayer(TCP) and pkt[TCP].flags == 17:  # FIN-ACK
                        print("Received FIN-ACK, connection closed")
                        
                # Listen for FIN-ACK for a short time
                sniff(iface=interface, filter=f"tcp and host {client_ip} and port {client_port}", 
                      lfilter=lambda x: x.haslayer(TCP) and x[TCP].flags == 17, 
                      timeout=5, prn=handle_fin_ack)
                
    # Start sniffing for TCP packets
    try:
        print("Listening for TCP connection...")
        sniff(iface=interface, filter=f"tcp and host {client_ip} and port {server_port}", 
              lfilter=lambda x: x.haslayer(TCP), 
              prn=handle_connection, timeout=30)
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    tcp_server()
