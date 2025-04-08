from flask import Flask
from flask_cors import CORS
from .app_bp import bp

app = Flask(__name__)
app.register_blueprint(bp)
CORS(app)
