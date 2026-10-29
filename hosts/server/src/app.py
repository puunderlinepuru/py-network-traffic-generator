import TCP_server

if __name__ == "__main__":
    srv_address='0.0.0.0'
    srv_port=12345
    interface = "eth0"
    server = TCP_server.TCPServer(host=srv_address, port=srv_port, iface=interface)
    server.start()