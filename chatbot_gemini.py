from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your Gemini API key and secret if required
BASE_URL = "https://api.gemini.com/v1"

# Helper function to call Gemini's public API
def gemini_public_api(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from Gemini"}

# Example: Get ticker price for a given cryptocurrency pair
def get_crypto_price(pair="btcusd"):
    data = gemini_public_api(f"pubticker/{pair}")
    if "error" not in data:
        return f"Price for {pair.upper()}:\nAsk: {data['ask']}, Bid: {data['bid']}, Last: {data['last']}"
    else:
        return "Error fetching price data."

# Serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Handle the chatbot response
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form.get('message').lower()

    # Check if the user is asking for a price of a crypto pair
    if 'price' in user_message:
        tokens = user_message.split()
        crypto_pair = "btcusd"  # Default pair
        for token in tokens:
            if len(token) == 6:  # Assuming the pair is valid
                crypto_pair = token
        response_message = get_crypto_price(crypto_pair)
    else:
        response_message = "I can provide cryptocurrency prices. Try asking 'price of btcusd'."

    return jsonify({"response": response_message})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
