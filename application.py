from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json


app = Flask(__name__)
CORS(app)  # CORS設定を追加


# Raspberry PiのURLを指定
RPI_SERVER_URL = "http://10.124.57.76:5001:5001/receive_message"


@app.route('/')

@app.route('/message', methods=['POST'])
def process_message():
    data = request.get_json()
    input_text = data['inputText']
    modified_message = input_text + 'だみょ～ん'


    # Raspberry Piにメッセージを送信
    try:
        response = requests.post(RPI_SERVER_URL, json={'message': modified_message})
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Message sent to Raspberry Pi'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send message to Raspberry Pi'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

