# import pywhatkit as kit
# from flask import Flask, request, jsonify
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def mukul():
#     return jsonify({
#         "username": "mukul"
#     })


# @app.route('/send_message', methods=['POST'])
# def send_message():
#     # Parse JSON request
#     data = request.get_json()

#     # Extract phone number and message
#     phone_number = data.get('phone_number')
#     message = data.get('message')

#     if not phone_number or not message:
#         return jsonify({'error': 'Phone number and message are required'}), 400

#     try:
#         # Use pywhatkit to send the WhatsApp message instantly
#         kit.sendwhatmsg_instantly(f"+{phone_number}", message, 10, True, 10)
#         return jsonify({'status': 'Message sent successfully', 'phone_number': phone_number}), 200

#     except Exception as e:
#         return jsonify({'status': 'Failed to send message', 'error': str(e)}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080,debug=True)
    
from flask import Flask, request, jsonify
import pandas as pd
import pywhatkit as kit
import time
import io

app = Flask(__name__)
CORS(app)

@app.route("/")
def mukul():
    return jsonify({
        "username": "mukul"
    })

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    # Check if the CSV file is present in the request
    if 'csv_file' not in request.files:
         return jsonify({'error': 'No file part'}), 400

    file = request.files['csv_file']
    # return jsonify({'error': file.filename})
    
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
    except Exception as e:
        return jsonify({'error': f'Error reading CSV file: {str(e)}'}), 400

    # Define the required columns (assuming these columns exist in the CSV)
    phone_column = 'phone_number'  # Replace with your column name
    message_column = 'message'  # Replace with your column name

    # Check if the expected columns are in the CSV
    if phone_column not in df.columns or message_column not in df.columns:
        return jsonify({'error': 'CSV must contain Phone and Message columns'}), 400

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        phone_number = row[phone_column]
        message_text = row[message_column]
        print(phone_number)

        # Send the WhatsApp message using pywhatkit
        try:
            kit.sendwhatmsg_instantly(f"+{phone_number}", message_text, 10, True, 10)
            print(f'Message sent to {phone_number}: {message_text}')
        except Exception as e:
            print(f'Failed to send message to {phone_number}: {e}')

        # Wait for 5 seconds before sending the next message to avoid being blocked
        time.sleep(5)

    return jsonify({'status': 'success', 'message': 'All messages sent!'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

