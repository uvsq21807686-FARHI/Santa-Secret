from flask_restful import Resource
from models.tirage import TirageModel
from sqlalchemy import func
from db import db

class Tirage(Resource):
    def get(self, name):
        tirage = TirageModel.find_by_name(name)
        if tirage:
            return tirage.json()
        return {'messgae': 'Tirage not found'}, 404

    def post(self, name):
        if TirageModel.find_by_name(name):
            return {'message': "A tirage with a name '{}' already exists".format(name)}, 400

        tirage = TirageModel(name)
        try:
            tirage.save_to_db()
        except:
            return {"message": "An error occured creating the tirage."}, 500

        return {"message": "Tirage created successfully."}, 201

    def delete(self, name):
        tirage = TirageModel.find_by_name(name)
        if tirage:
            tirage.delete_from_db()

        return {"message": "tirage deleted"}

class historique(Resource):
    def get(self):
        liste=[]
        max = 0
        max_id = db.session.query(func.max(TirageModel.id)).scalar()
        if max_id >= 5:
            max=5
        else:
            max=max_id
        for i in range(1,max+1):
            liste.append(list(map(lambda x: x.json(), TirageModel.query.filter_by(id=max_id-max+i))))
        return  liste
class historique2(Resource):
    def get(self):
        return list(map(lambda x: x.json2(), TirageModel.query.all()))



class TirageList(Resource):
    def get(self,id_t):
        return  list(map(lambda x: x.json(), TirageModel.query.filter_by(id=id_t)))
