from flask import Flask, request, redirect, jsonify
from flask_login import LoginManager, UserMixin
from sqlalchemy import SQLAlchemy
import keys, requests
app = Flask(__name__)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

client_id = keys.get_spotify_id()
client_secret = keys.get_spotify_secret()
redirect_uri = "https://660646c0.ngrok.io/spotify-callback"

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.ColumN(db.String(64), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def home():
    return 'hello_world;'

@app.route("/authorize")
def authorize():
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    return redirect("https://accounts.spotify.com/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(client_id, redirect_uri))

@app.route("/spotify-callback")
def callback():
    error = request.args.get("error")
    code = request.args.get("code")
    state = request.args.get("state")
    if (not error):
        url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }
        response = requests.post(url=url, data=payload).json()
        access_token = response["access_token"]

        my_info_url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": "Bearer {0}".format(access_token)}
        response = requests.get(url=my_info_url, headers=headers).json()
        return jsonify(response)
    else:
        print(error)
        print(state)

