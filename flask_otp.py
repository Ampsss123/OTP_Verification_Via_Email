from flask import Flask, render_template, request, jsonify
import smtplib
import random

app = Flask(__name__)

# Store OTP globally for verification (in a real app, you'd manage sessions or database)
otp = None

# Email setup
EMAIL = 'otp@gmail.com'
PASSWORD = '*********'

# SMTP setup
def send_otp_via_email(receiver_email):
    global otp
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])  # Generate a 4-digit OTP
    message = f'Hello, Your OTP is {otp}'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, receiver_email, message)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    
    if send_otp_via_email(email):
        return jsonify({'status': 'success', 'message': 'OTP sent successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send OTP'}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    entered_otp = data.get('otp')
    
    if entered_otp == otp:
        return jsonify({'status': 'success', 'message': 'OTP Verified Successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect OTP. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)
