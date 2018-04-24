##
## Author: Randy Burrell
##
## Date: [DATE HERE]
##
## Description:
##
##
##

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class KittyName(db.Model):
    __tablename__ = 'kitty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    used = db.Column(db.Boolean, nullable=True)
    gender = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=True)
    #gender = db.relationship("Gender", backref="kitty", lazy=True)

    def save(self):
        print('saving data')
        print(db.session.commit())

class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)

def mani():
    print("Welcome to main")

if __name__ == '__main__':
    main()

