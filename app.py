from flask import Flask, request, jsonify
from inference import Translator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
translator = Translator(weight_dir='weights')  # Initialize translator

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    
    if 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'Missing or empty "text" parameter'}), 400
    
    try:
        translation = translator.translate(data['text'])

        return jsonify({
            'sinhala': data['text'],
            'english': translation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)