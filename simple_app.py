from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running"

@app.route('/api/send-template', methods=['POST'])
def send_template():
    return jsonify({'success': True, 'message': 'Template route works!'})

@app.route('/test')
def test():
    return "Test route works"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)