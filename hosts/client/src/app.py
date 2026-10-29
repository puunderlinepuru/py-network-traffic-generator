from flask import Flask, request, jsonify, g
import TCP_client
import random
from lorem.text import TextLorem

app = Flask(__name__)

# Method to be called when the POST is received
def execute_method(message):
    print(f"Processing message: {message}")
    return f"Processed: {message}"

@app.route('/send', methods=['POST'])
def handle_execute():
    data = request.get_json() or {}
    
    if 'character' not in data or 'base_icn' not in data:
        return jsonify({'error': 'Missing parameter'}), 400
    
    character = data['character']
    base_icn = data['base_icn']
    base_icn = random.randint(1, 4294967295)
    new_icn = base_icn + int.from_bytes(character.encode())
    print("ICN: ", base_icn, " + ", int.from_bytes(character.encode()), " = ", new_icn)
    # result = execute_method(message)
    client.set_icn(new_icn)
    lorem = TextLorem(srange=(2,50))
    payload = lorem.sentence()
    result = client.send_message(payload)
    
    return jsonify({
        'status': 'success',
        'result': result,
        'message': character,
        'base_icn': base_icn,
        'new_icn': new_icn
    }), 200

if __name__ == '__main__':
    srv_address='192.168.1.68'
    srv_port=12345
    interface="Беспроводная сеть"
    client = TCP_client.TCPSession(server_ip=srv_address, server_port=srv_port, iface=interface)
    # client.send_file("file.txt")
    # client.send_message("Hello world!")
    app.run(host="0.0.0.0", debug=True, port=5000)
