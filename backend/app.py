from flask import Flask, request, jsonify, Response
from models.openelm_connector import query_openelm
from models.azure_openai_connector import query_azure_openai
from utils.streaming import stream_response

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('question')
    model_choice = data.get('model')

    if model_choice == 'openelm':
        return stream_response(query_openelm(user_question))
    elif model_choice == 'azure_openai':
        return stream_response(query_azure_openai(user_question))
    else:
        return jsonify({'error': 'Invalid model choice'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)