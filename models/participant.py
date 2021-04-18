from db import db


class ParticipantModel(db.Model):
    __tablename__ = 'participant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    prenom = db.Column(db.String(80))

    tirage_id = db.Column(db.Integer, db.ForeignKey('tirages.id'))
    tirage  = db.relationship('TirageModel')

    def __init__(self, name, prenom, tirage_id):
        self.name = name
        self.prenom = prenom
        self.tirage_id = tirage_id

    def json(self):
        return {'name': self.name, 'prenom': self.prenom}

    @classmethod
    def find_by_name(cls, name,prenom):
        return cls.query.filter_by(prenom=prenom).filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()