import scapy.all as scapy
from flask import Flask, request, jsonify, g

interfaces = scapy.get_if_list()
counter = 0
for interface in interfaces:
    print("interface ", counter, ": ", interface)
    counter+=1
    
app = Flask(__name__)

# Method to be called when the POST is received
def execute_method(message):
    print(f"Processing message: {message}")
    return f"Processed: {message}"

@app.route('/execute', methods=['POST'])
def handle_execute():
    data = request.get_json() or {}
    
    if 'message' not in data:
        return jsonify({'error': 'Missing "message" parameter'}), 400
    
    message = data['message']
    result = execute_method(message)
    
    return jsonify({
        'status': 'success',
        'result': result,
        'message': message
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)