from flask_app import db

#TestDB
class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    hoge = db.Column(db.String(255))