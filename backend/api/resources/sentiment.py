from flask_restx import Namespace, Resource, fields
from models import db, Sentiment
sentiment_ns = Namespace("sentiments", description="Operations related to sentiments")

sentiment_model = sentiment_ns.model(
    "Sentiment",
    {
        "SentimentID": fields.Integer(readonly=True, description="Unique ID of the sentiment"),
    },
)

@sentiment_ns.route("/")
class SentimentListResource(Resource):
    @sentiment_ns.marshal_list_with(sentiment_model)
    def get(self):
        """Get all sentiments"""
        return Sentiment.query.all()