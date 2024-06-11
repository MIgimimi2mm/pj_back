from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json


app = Flask(__name__)
CORS(app)  # CORS設定を追加

click_count = 0

# Raspberry PiのURLを指定
RPI_SERVER_URL = "http://10.124.57.76:5001:5001/receive_message"


@app.route('/')

@app.route('/click-count', methods=['GET'])
def get_click_count():
    global click_count
    return jsonify({'count': click_count}), 200

@app.route('/increment-click', methods=['POST'])
def increment_click():
    global click_count
    click_count += 1
    return jsonify({'count': click_count}), 200


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

