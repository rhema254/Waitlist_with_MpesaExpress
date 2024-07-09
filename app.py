from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_restx import Resource, Api, fields
from config import DevConfig
from flask_session import Session
from exts import db
from models import user
from werkzeug.security import generate_password_hash 
from flask import jsonify
from flask_mail import Mail, Message
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime


app = Flask(__name__, template_folder='templates', static_folder='static')



app.config.from_object(DevConfig)
api = Api(app, doc='/docs') 

db.init_app(app)
 
mail = Mail(app)
Session(app)

consumer_key = app.config['CONSUMER_KEY']
consumer_secret = app.config['CONSUMER_SECRET']
myendpoint = "https://ecd3-102-0-3-110.ngrok-free.app" 

## Serializer model.
user_model = api.model(
    'user',
    {
        'email':fields.String(),
        'username': fields.String(),
        'password': fields.String(),
        'verified': fields.Boolean()
    }
)
token_model = api.model(
    'token',
    {
       'access_token': fields.String(),
        'expires_in': fields.Integer
    }
)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        current_user = user.query.filter_by(username=username).first()       

        if current_user is not None:
            flash(f"{current_user} already exists. Choose a different username", "danger")
            return redirect(url_for('register'))

        new_user = user(email=email, username=username, password=generate_password_hash(password))
        try:
            new_user.save()

            msg = Message(subject='Welcome to Waitlist!', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"Hello {username}, welcome to Waitlist!!<br/><br/><br/>. If you are seeing this email, it means that you have successfully created an account for our Upcoming App, MusiciansConnect and you will be the first to receive information on the date Launch and other community News! Viva!!"
            mail.send(msg)

            flash("Your account has been created successfully. Please check your email", "success")
            session['username'] = username
            session['email'] = email

            return redirect('payment')
        except Exception as e:
            print(f"Error saving the user:{e}")
            return "An error occurred while creating your account"
    
    return render_template('register.html')


def getAccessToken():
    """ Getting the access token from daraja endpoint """
    
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = response.json()
    return data["access_token"]


@app.route('/payment', methods=['GET', 'POST'])
    
def payment():
    username = session.get('username')
    email = session.get('email') 
    

    if request.method == 'POST':
        phone = request.form.get('phone')
        amount = request.form.get('amount')
        print(phone, amount)
        
        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        access_token = getAccessToken()
        headers = { "Authorization": "Bearer %s" % access_token }
        Timestamp = datetime.now()
        times = Timestamp.strftime("%Y%m%d%H%M%S")
        password = "174379" + app.config['PASSKEY'] + times
        password = base64.b64encode(password.encode('utf-8')).decode('utf-8') 

        data = {
            "BusinessShortCode": "174379",
            "Password": password,
            "Timestamp": times,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": myendpoint + "/callback",
            "AccountReference": "Test Payment",
            "TransactionDesc": "Waitlist4You",
            "amount": amount
        }

        response = requests.post(endpoint, json=data, headers = headers)
        return response.json()
        
    return render_template('pay.html', username=username, email=email)


@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    print(data)
    return "ok"




@api.route('/users')
class usersResource(Resource):
    
    @api.marshal_list_with(user_model)
    def get(self):
        """ Get list of users """
        users = user.query.all()
        return users
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

