from flask_restx import Namespace, Resource, fields
from sqlalchemy.sql import func, cast
from sqlalchemy.types import Integer
from models import db, Author, Comment

author_ns = Namespace("authors", description="Operations related to authors")
author_model = author_ns.model(
    "Author",
    {
        "AuthorID": fields.Integer(readonly=True),
        "Username": fields.String(required=True, description="Author's username"),
        "AvatarURL": fields.String(description="URL of the author's avatar"),
    },
)

@author_ns.route("/ranked")
class RankedAuthorsResource(Resource):
    def get(self):
        """Get authors ranked by their number of comments"""
        results = (
            db.session.query(
                Author.AuthorID,
                Author.Username,
                cast(func.count(Comment.CommentID), Integer).label("comment_count")
            )
            .join(Comment, Author.AuthorID == Comment.AuthorID)
            .group_by(Author.AuthorID, Author.Username)
            .order_by(func.count(Comment.CommentID).desc())
            .all()
        )

        ranked_authors = [
            {
                "AuthorID": int(r.AuthorID),
                "Username": r.Username,
                "CommentCount": r.comment_count
            }
            for r in results
        ]

        return ranked_authors, 200

@author_ns.route("/")
class AuthorListResource(Resource):
    @author_ns.marshal_list_with(author_model)
    def get(self):
        """Get all authors"""
        return Author.query.all()

    @author_ns.expect(author_model)
    @author_ns.marshal_with(author_model, code=201)
    def post(self):
        """Create a new author"""
        data = author_ns.payload
        new_author = Author(Username=data["Username"], AvatarURL=data.get("AvatarURL"))
        db.session.add(new_author)
        db.session.commit()
        return new_author, 201


@author_ns.route("/<int:author_id>")
class AuthorResource(Resource):
    @author_ns.marshal_with(author_model)
    def get(self, author_id):
        """Get an author by ID"""
        author = Author.query.get(author_id)
        if not author:
            author_ns.abort(404, f"Author {author_id} not found")
        return author

    @author_ns.expect(author_model)
    @author_ns.marshal_with(author_model)
    def put(self, author_id):
        """Update an author by ID"""
        author = Author.query.get(author_id)
        if not author:
            author_ns.abort(404, f"Author {author_id} not found")

        data = author_ns.payload
        author.Username = data["Username"]
        author.AvatarURL = data.get("AvatarURL")
        db.session.commit()
        return author

    def delete(self, author_id):
        """Delete an author by ID"""
        author = Author.query.get(author_id)
        if not author:
            author_ns.abort(404, f"Author {author_id} not found")

        db.session.delete(author)
        db.session.commit()
        return {"message": f"Author {author_id} deleted"}, 200
