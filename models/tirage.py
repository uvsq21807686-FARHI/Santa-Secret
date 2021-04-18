from db import db
import random

class TirageModel(db.Model):

    __tablename__ = 'tirages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    participant = db.relationship('ParticipantModel', lazy='dynamic')
    liste_noire = db.relationship('ListenoireModel', lazy='dynamic')
    def __init__(self, name):
        self.name = name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def affiche(self,list1,list2):
        la_list = []
        for i in range(0,len(list1)):
            x = {'donner' : list1[i], 'recu' : list2[i]}
            la_list.append(x)
        return la_list



    def appartient_a_la_liste(self, list, elt):
        for i in list:
            if i == elt:
                return True
        return False

    def aleatoire_paire(self, list):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        while len(list) > 0:
            x = random.choice(list)
            list1.append(x)
            list.remove(x)
            y = random.choice(list)
            if not self.appartient_a_la_liste(list5, x):
                list2.append(y)
                list.remove(y)
            else:
                while self.appartient_a_la_liste(list5, y):
                    y = random.choice(list)
                list2.append(y)
                list.remove(y)
        a = self.affiche(list1, list2)
        while len(list1) > 0:
            x = random.choice(list2)
            list3.append(x)
            list2.remove(x)
            y = random.choice(list1)
            if not self.appartient_a_la_liste(list5, x):
                list4.append(y)
                list1.remove(y)
            else:
                while self.appartient_a_la_liste(list5, y):
                    y = random.choice(list1)
                list4.append(y)
                list1.remove(y)

        return a + self.affiche(list3, list4)

    def aleatoire(self):
        list = []
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        for i in self.participant.all():
            list.append(i.json().get('name'))
        for i in self.liste_noire.all():
            list5.append(i.json().get('name'))
        list += list5
        if len(list) % 2 == 0 and len(list) != 0:
            return self.aleatoire_paire(list)
        else:
            x = random.choice(list)
            list.remove(x)
            z = random.choice(list)
            while self.appartient_a_la_liste(list5, z):
                z = random.choice(list)

            y = [{'donner': z, 'recu': x}]
            return self.aleatoire_paire(list) + y




    def json(self):
        return self.aleatoire()
    def json2(self):
        return {'name': self.name,'id': self.id, 'participants':[participant.json() for participant in self.participant.all()], 'participant_liste_noire' : [participant_n.json() for participant_n in self.liste_noire.all()]}






