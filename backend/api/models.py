from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "Author"
    AuthorID = db.Column(db.Numeric, primary_key=True)
    Username = db.Column(db.Text, nullable=True)
    AvatarURL = db.Column(db.Text, nullable=True)

class PullRequest(db.Model):
    __tablename__ = "PullRequests"
    RequestID = db.Column(db.Numeric, primary_key=True)
    AuthorID = db.Column(db.Numeric, db.ForeignKey("Author.AuthorID"))
    Title = db.Column(db.Text)
    RequestURL = db.Column(db.Text)
    ProjectID = db.Column(db.Numeric, db.ForeignKey("Project.ProjectID"))

class Comment(db.Model):
    __tablename__ = "Comments"
    CommentID = db.Column(db.Numeric, primary_key=True)
    AuthorID = db.Column(db.Numeric, db.ForeignKey("Author.AuthorID"))
    Body = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime)
    RequestID = db.Column(db.Numeric, db.ForeignKey("PullRequests.RequestID"))
    CommentURL = db.Column(db.Text)
    SentimentScore = db.Column(db.Float)
    Association = db.Column(db.Text)
    StopWordRatio = db.Column(db.Float)
    ProjectID = db.Column(db.Numeric, db.ForeignKey("Project.ProjectID"))
    CodeSnippetCount = db.Column(db.Numeric)

class Project(db.Model):
    __tablename__ = "Project"
    ProjectID = db.Column(db.Integer, primary_key=True)
    ProjectURL = db.Column(db.Text)

class Sentiment(db.Model):
    __tablename__ = "Sentiment"
    SentimentID = db.Column(db.Numeric, primary_key=True)
