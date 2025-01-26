import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api
from models import db
from resources.author import author_ns
from resources.pull_request import pull_request_ns
from resources.comment import comment_ns
from resources.project import project_ns
from resources.sentiment import sentiment_ns

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api = Api(app, title="PR Comment Analysis API", version="1.0", description="API for managing PR comments and data related to the sentiment analysis of these comments.")

api.add_namespace(author_ns)
api.add_namespace(pull_request_ns)
api.add_namespace(comment_ns)
api.add_namespace(project_ns)
api.add_namespace(sentiment_ns)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
