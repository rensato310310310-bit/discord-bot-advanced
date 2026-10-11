from flask import Flask
from web.routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "change_this_secret_key"
app.register_blueprint(auth_bp)
