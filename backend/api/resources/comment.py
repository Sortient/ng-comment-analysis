from flask_restx import Namespace, Resource, fields
from sqlalchemy.sql import func
from models import db, Comment

comment_ns = Namespace("comments", description="Operations related to comments")
comment_model = comment_ns.model(
    "Comment",
    {
        "CommentID": fields.Integer(readonly=True),
        "AuthorID": fields.Integer(required=True, description="ID of the author"),
        "Body": fields.String(required=True, description="Content of the comment"),
        "Timestamp": fields.String(required=True, description="Timestamp of the comment"),
        "RequestID": fields.Integer(required=True, description="ID of the associated pull request"),
        "CommentURL": fields.String(required=True, description="URL of the comment"),
        "SentimentScore": fields.Float(description="Sentiment score of the comment"),
        "Association": fields.String(description="Association of the comment"),
        "StopWordRatio": fields.Float(description="Ratio of stop words in the comment"),
        "ProjectID": fields.Integer(description="ID of the associated project"),
        "CodeSnippetCount": fields.Integer(description="Number of code snippets in the comment"),
    },
)

@comment_ns.route("/top")
class TopCommentsResource(Resource):
    def get(self):
        """Get top 5 positive and negative comments"""
        top_positive = (
            db.session.query(Comment)
            .filter(Comment.SentimentScore > 0)
            .order_by(Comment.SentimentScore.desc())
            .limit(5)
            .all()
        )

        top_negative = (
            db.session.query(Comment)
            .filter(Comment.SentimentScore < 0)
            .order_by(Comment.SentimentScore)
            .limit(5)
            .all()
        )

        def serialize_comment(comment):
            return {
                "CommentID": float(comment.CommentID),
                "Body": comment.Body,
                "SentimentScore": float(comment.SentimentScore),  # Convert Decimal to float
                "AuthorID": float(comment.AuthorID),
                "Timestamp": comment.Timestamp.isoformat() if comment.Timestamp else None,
            }


        return {
            "top_positive": [serialize_comment(c) for c in top_positive],
            "top_negative": [serialize_comment(c) for c in top_negative],
        }, 200

@comment_ns.route("/")
class CommentListResource(Resource):
    @comment_ns.marshal_list_with(comment_model)
    def get(self):
        """Get all comments"""
        return Comment.query.all()

    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model, code=201)
    def post(self):
        """Create a new comment"""
        data = comment_ns.payload
        new_comment = Comment(
            AuthorID=data["AuthorID"],
            Body=data["Body"],
            Timestamp=data["Timestamp"],
            RequestID=data["RequestID"],
            CommentURL=data["CommentURL"],
            SentimentScore=data.get("SentimentScore"),
            Association=data.get("Association"),
            StopWordRatio=data.get("StopWordRatio"),
            ProjectID=data.get("ProjectID"),
            CodeSnippetCount=data.get("CodeSnippetCount"),
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment, 201

@comment_ns.route("/<int:comment_id>")
class CommentResource(Resource):
    @comment_ns.marshal_with(comment_model)
    def get(self, comment_id):
        """Get a comment by ID"""
        comment = Comment.query.get(comment_id)
        if not comment:
            comment_ns.abort(404, f"Comment {comment_id} not found")
        return comment

    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model)
    def put(self, comment_id):
        """Update a comment by ID"""
        comment = Comment.query.get(comment_id)
        if not comment:
            comment_ns.abort(404, f"Comment {comment_id} not found")

        data = comment_ns.payload
        comment.AuthorID = data["AuthorID"]
        comment.Body = data["Body"]
        comment.Timestamp = data["Timestamp"]
        comment.RequestID = data["RequestID"]
        comment.CommentURL = data["CommentURL"]
        comment.SentimentScore = data.get("SentimentScore")
        comment.Association = data.get("Association")
        comment.StopWordRatio = data.get("StopWordRatio")
        comment.ProjectID = data.get("ProjectID")
        comment.CodeSnippetCount = data.get("CodeSnippetCount")
        db.session.commit()
        return comment

    def delete(self, comment_id):
        """Delete a comment by ID"""
        comment = Comment.query.get(comment_id)
        if not comment:
            comment_ns.abort(404, f"Comment {comment_id} not found")

        db.session.delete(comment)
        db.session.commit()
        return {"message": f"Comment {comment_id} deleted"}, 200

@comment_ns.route("/stats")
class CommentStatsResource(Resource):
    def get(self):
        """Get overall statistics for PR comments which have been analysed"""
        total_comments = db.session.query(func.count(Comment.CommentID)).scalar()
        positive_comments = db.session.query(func.count(Comment.CommentID)) \
            .filter(Comment.SentimentScore > 0).scalar()
        negative_comments = db.session.query(func.count(Comment.CommentID)) \
            .filter(Comment.SentimentScore < 0).scalar()
        return {
            "total_comments": total_comments,
            "positive_comments": positive_comments,
            "negative_comments": negative_comments
        }, 200