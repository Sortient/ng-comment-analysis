from flask_restx import Namespace, Resource, fields
from models import db, PullRequest

pull_request_ns = Namespace("pull_requests", description="Operations related to pull requests")
pull_request_model = pull_request_ns.model(
    "PullRequest",
    {
        "RequestID": fields.Integer(readonly=True),
        "AuthorID": fields.Integer(required=True, description="ID of the author"),
        "Title": fields.String(required=True, description="Title of the pull request"),
        "RequestURL": fields.String(required=True, description="URL of the pull request"),
        "ProjectID": fields.Integer(required=True, description="ID of the associated project"),
    },
)

@pull_request_ns.route("/")
class PullRequestListResource(Resource):
    @pull_request_ns.marshal_list_with(pull_request_model)
    def get(self):
        """Get all pull requests"""
        return PullRequest.query.all()

    @pull_request_ns.expect(pull_request_model)
    @pull_request_ns.marshal_with(pull_request_model, code=201)
    def post(self):
        """Create a new pull request"""
        data = pull_request_ns.payload
        new_pull_request = PullRequest(
            AuthorID=data["AuthorID"],
            Title=data["Title"],
            RequestURL=data["RequestURL"],
            ProjectID=data["ProjectID"],
        )
        db.session.add(new_pull_request)
        db.session.commit()
        return new_pull_request, 201


@pull_request_ns.route("/<int:request_id>")
class PullRequestResource(Resource):
    @pull_request_ns.marshal_with(pull_request_model)
    def get(self, request_id):
        """Get a pull request by ID"""
        pr = PullRequest.query.get(request_id)
        if not pr:
            pull_request_ns.abort(404, f"PullRequest {request_id} not found")
        return pr

    @pull_request_ns.expect(pull_request_model)
    @pull_request_ns.marshal_with(pull_request_model)
    def put(self, request_id):
        """Update a pull request by ID"""
        pr = PullRequest.query.get(request_id)
        if not pr:
            pull_request_ns.abort(404, f"PullRequest {request_id} not found")

        data = pull_request_ns.payload
        pr.AuthorID = data["AuthorID"]
        pr.Title = data["Title"]
        pr.RequestURL = data["RequestURL"]
        pr.ProjectID = data["ProjectID"]
        db.session.commit()
        return pr

    def delete(self, request_id):
        """Delete a pull request by ID"""
        pr = PullRequest.query.get(request_id)
        if not pr:
            pull_request_ns.abort(404, f"PullRequest {request_id} not found")

        db.session.delete(pr)
        db.session.commit()
        return {"message": f"PullRequest {request_id} deleted"}, 200
