from flask import Flask, render_template, request, jsonify
import stripe
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Hardcoded Stripe keys
STRIPE_SECRET_KEY = 'sk_test_51KCnvuJshHAfrxBU7q7avpoI585IA95UdKOOkAIMi85GCw4lgxvAuu1Ut3tvqizlCpBZZZH7d67yPIDp8S84qOhK00A5tZgrTx'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51KCnvuJshHAfrxBUDHSlfrQefwZSC7vWTSDndZyNIvDROQC1rPzJUCDf5AjL7ycZ6yztCs8FNV4Hh4yqMsauGRGM0006vgbSBz'

# Set your Stripe secret key
stripe.api_key = STRIPE_SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html', publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/receive_token', methods=['POST'])
def receive_token():
    token = request.json.get('token')
    print(f"Received token: {token}")
    return jsonify({'status': 'success', 'token': token}), 200

@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    try:
        token = request.json.get('token')
        amount = request.json.get('amount')

        # Create a PaymentIntent with the given token
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_data={
                'type': 'card',
                'card': {
                    'token': token,
                },
            },
            confirmation_method='manual',
            confirm=True,
        )
        return jsonify({'status': 'success', 'client_secret': intent.client_secret})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 403

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
