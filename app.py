from flask import Flask, request, jsonify
from inference import Translator
from simpletransformers.t5 import T5Model

app = Flask(__name__)
translator = Translator(weight_dir='weights')  # Initialize translator


model = T5Model("mt5", "thilina/mt5-sinhalese-english")
print(model.predict(["Let's translate!"]))

@app.route('/translate/<model_name>', methods=['POST'])
def translate(model_name=="default"):
    data = request.get_json()
    
    if 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'Missing or empty "text" parameter'}), 400
    
    try:
        if model_name=="default":
            translation = translator.translate(data['text'])
        elif model_name=="T5":
            translation = model.predict(["When will this happen?"])[0]

        return jsonify({
            'sinhala': data['text'],
            'english': translation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)