from scapy.all import *
import time

from scapy.layers.inet import IP, TCP

class TCPServer:
    def __init__(self, host='192.168.0.12', port=12345):
        self.host = host
        self.port = port
        self.server_seq_num = 5000
        self.client_seq_num = None
        self.client_ack_num = None

    def start(self):
        print(f"STARTING TCP SERVER ON {self.host}:{self.port}")
        sniff(iface="Outer Ethernet",filter=f"tcp and dst port {self.port}", prn=self.handle_packet, store=0)

    def handle_packet(self, packet):

        if packet.haslayer(IP) and packet.haslayer(TCP):

            self.client_seq_num = packet[TCP].seq
            self.client_ack_num = packet[TCP].ack

            if packet[TCP].flags == 'S':  # SYN flag
                print(f"RECEIVED A SYN")
                print(f"SENDING A SYN-ACK")

                syn_ack_packet = IP(dst=packet[IP].src) / TCP(sport=self.port, dport=packet[TCP].sport, flags='SA', seq=self.server_seq_num, ack=self.client_seq_num + 1)
                send(syn_ack_packet, verbose=0)

                print(f"UPDATING MY SEQUENCE NUMBER")

                self.server_seq_num += 1

            elif packet[TCP].flags == 'A':  # ACK flag
                print(f"RECEIVED AN ACK FOR SYN-ACK")
                print(f"THREE-WAY HANDSHAKE COMPLETE")

            elif packet[TCP].flags == 'PA':  # PSH and ACK flags
                print(f"RECEIVED SOME DATA: {packet[TCP].payload.load.decode()}")
                print(f"SENDING AN ACK FOR THIS CHUNK OF DATA")

                ack_packet = IP(dst=packet[IP].src) / TCP(sport=self.port, dport=packet[TCP].sport, flags='A', seq=self.server_seq_num, ack=self.client_seq_num + len(packet[TCP].payload.load))
                send(ack_packet, verbose=0)

            elif packet[TCP].flags == 'FA':  # FIN flag
                print(f"RECEIVED A FIN FROM CLIENT")
                print(f"SENDING ACK TO FIN-ACK ")

                fin_packet = IP(dst=packet[IP].src) / TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, flags='A', seq=self.server_seq_num, ack=self.client_seq_num + 1)
                send(fin_packet, verbose=0)

                # print(f"UPDATING MY SEQUENCE NUMBER")

                # self.server_seq_num += 1

                print(f"SENDING SERVER FIN")

                time.sleep(1)

                fin_packet = IP(dst=packet[IP].src) / TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, flags='FA', seq=self.server_seq_num, ack=self.client_seq_num + 1 )
                fin_ack_response = sr1(fin_packet, verbose=False)

                if fin_ack_response and fin_ack_response.haslayer(TCP) and fin_ack_response[TCP].flags == 'A':  # FIN-ACK flags
                    print(f"RECEIVED AN ACK FOR SERVER FIN: MY CONNECTION IS CLOSED")
                    print(f"EXITING")
                    exit()

if __name__ == "__main__":
    server = TCPServer()
    server.start()