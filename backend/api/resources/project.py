from flask_restx import Namespace, Resource, fields
from models import db, Project

project_ns = Namespace("projects", description="Operations related to projects")
project_model = project_ns.model(
    "Project",
    {
        "ProjectID": fields.Integer(readonly=True),
        "ProjectURL": fields.String(required=True, description="URL of the project"),
    },
)

@project_ns.route("/")
class ProjectListResource(Resource):
    @project_ns.marshal_list_with(project_model)
    def get(self):
        """Get all projects"""
        return Project.query.all()

    @project_ns.expect(project_model)
    @project_ns.marshal_with(project_model, code=201)
    def post(self):
        """Create a new project"""
        data = project_ns.payload
        new_project = Project(ProjectURL=data["ProjectURL"])
        db.session.add(new_project)
        db.session.commit()
        return new_project, 201


@project_ns.route("/<int:project_id>")
class ProjectResource(Resource):
    @project_ns.marshal_with(project_model)
    def get(self, project_id):
        """Get a project by ID"""
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f"Project {project_id} not found")
        return project

    @project_ns.expect(project_model)
    @project_ns.marshal_with(project_model)
    def put(self, project_id):
        """Update a project by ID"""
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f"Project {project_id} not found")

        data = project_ns.payload
        project.ProjectURL = data["ProjectURL"]
        db.session.commit()
        return project

    def delete(self, project_id):
        """Delete a project by ID"""
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f"Project {project_id} not found")

        db.session.delete(project)
        db.session.commit()
        return {"message": f"Project {project_id} deleted"}, 200
