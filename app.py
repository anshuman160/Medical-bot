from flask import Flask, render_template, request, jsonify
import openai
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Fetch API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')



# Serve the HTML file at the root route
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle chat messages
@app.route('/api', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'message': 'No message received'}), 400

    # Interact with OpenAI's GPT-3.5 model to generate a response
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Dr. Sanjay Kumar Yadav, a helpful medical consultant."},
                {"role": "user", "content": user_message}
            ]
        )
        response_message = completion.choices[0].message['content']
        return jsonify({'message': response_message})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
