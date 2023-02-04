from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class Generate(db.Model):
    __tablename__ = 'generate'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())