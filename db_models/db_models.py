from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class Generate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())