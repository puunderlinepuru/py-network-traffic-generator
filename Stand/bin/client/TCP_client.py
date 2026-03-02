from scapy.all import *
import random

from scapy.layers.inet import IP, TCP

class TCPClient:
    def __init__(self, server_ip, server_port, chunk_size=512):
        self.server_ip = server_ip
        self.server_port = server_port
        self.local_port = random.randint(1024, 65535)
        self.client_seq_num = 1000
        self.client_ack_num = None
        self.server_seq_num = None
        self.chunk_size = 1400

    def initiate_connection(self):
        print(f"SENDING SYN PACKET")

        syn_packet = IP(dst=self.server_ip) / TCP(sport=self.local_port, dport=self.server_port, flags='S', seq=self.client_seq_num)
        syn_ack_response = sr1(syn_packet, verbose=False)

        self.client_seq_num += 1

        print(f"RECEIVING SYN ACK")

        if syn_ack_response and syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags == 'SA':  # SYN-ACK flags
            print(f"SENDING ACK TO SYN-ACK")

            self.server_seq_num = syn_ack_response[TCP].seq
            self.client_ack_num = self.server_seq_num + 1

            ack_packet = IP(dst=self.server_ip) / TCP(sport=self.local_port, dport=self.server_port, flags='A', seq=self.client_seq_num, ack=self.server_seq_num + 1)
            send(ack_packet, verbose=False)

            print(f"THREE-WAY HANDSHAKE COMPLETE")

            return True
        return False

    def send_payload(self, payload):
        if not self.initiate_connection():
            print("FAILED TO ESTABLISH A CONNECTION WITH THE SERVER")
            return

        bytes_sent = 0
        current_packet_index = 0
        total_packets = int(len(payload)/self.chunk_size)

        while bytes_sent < len(payload):

            print(f"SENDING PACKET {current_packet_index + 1} OF {total_packets}")
            print(f"TOTAL BYTES SENT: {bytes_sent} PAYLOAD {len(payload)}")

            chunk = payload[bytes_sent:bytes_sent + self.chunk_size]
            psh_ack_packet = IP(dst=self.server_ip) / TCP(sport=self.local_port, dport=self.server_port, flags='PA', seq=self.client_seq_num, ack=self.client_ack_num) / Raw(load=chunk)
            ack_response = sr1(psh_ack_packet, verbose=False)

            print(f"UPDATING MY SEQUENCE NUMBER")

            self.client_seq_num += len(chunk)

            print(f"RECEIVING AN ACK FOR THIS CHUNK OF DATA")

            if ack_response and ack_response.haslayer(TCP) and ack_response[TCP].flags == 'A':  # ACK flag
                bytes_sent += len(chunk)
                current_packet_index += 1
            else:
                print("FAILED TO SEND PAYLOAD")
                return

        print("PAYLOAD SENT SUCCESSFULLY")

    def terminate_connection(self):
        # AsyncSniffer(iface="ens224",filter=f"tcp and dst port {self.local_port}", prn=self.handle_packet, store=0)

        print(f"SENDING CLIENT FIN")

        fin_packet = IP(dst=self.server_ip) / TCP(sport=self.local_port, dport=self.server_port, flags='FA', seq=self.client_seq_num, ack=self.client_ack_num)
        fin_ack_response = sr1(fin_packet, verbose=False)

        if fin_ack_response and fin_ack_response.haslayer(TCP) and fin_ack_response[TCP].flags == 'A':
            print(f"RECEIVED AN ACK FOR CLIENT FIN: MY CONNECTION IS CLOSED")

        print("STILL LISTENING FOR A SERVER FIN")

        sniff(iface="eth0",filter=f"tcp and dst port {self.local_port}", prn=self.handle_packet, store=0)

    def handle_packet(self, packet):

        if packet.haslayer(IP) and packet.haslayer(TCP) and packet[TCP].flags == 'FA':

            print(f"RECEIVED A FIN FROM SERVER")
            print(f"SENDING ACK TO FIN-ACK ")

            self.server_seq_num = packet[TCP].seq
            fin_packet = IP(dst=packet[IP].src) / TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, flags='A', seq=self.client_seq_num + 1, ack=self.server_seq_num + 1)
            send(fin_packet, verbose=0)

            print(f"EXITING")

            exit()

    def send_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        self.send_payload(file_data)
        self.terminate_connection()

if __name__ == "__main__":
    client = TCPClient(server_ip="10.0.0.1", server_port=12345)
    client.send_file("file.txt")