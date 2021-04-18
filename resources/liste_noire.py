from flask_restful import Resource, reqparse
from models.liste_noire import ListenoireModel


class Liste_noire(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('prenom',
                        type=str,
                        required=True,
                        help='This field cannot be blank!'
                        )
    parser.add_argument('tirage_id',
                        type=int,
                        required=True,
                        help='Every participant needs a tirage_id'
                        )

    #@jwt_required()
    def get(self, name,prenom):
        participant_n = ListenoireModel.find_by_name(name,prenom)
        if participant_n:
            return participant_n.json()
        return {'message': 'Participant not found'}, 404

    def post(self, name,prenom):
        if ListenoireModel.find_by_name(name,prenom):
            return {'message': "ce participant '{}' exciste deja dans la liste noire ".format(name)}, 400

        data = Liste_noire.parser.parse_args()
        participant_n = ListenoireModel(name, **data)

        try:
            participant_n.save_to_db()
        except:
            return {"message": "probleme d'insertion de ce participant dans la liste noire."}, 500

        return participant_n.json(), 201

    def delete(self, name):
        participant_n = ListenoireModel.find_by_name(name)
        if participant_n:
            participant_n.delete_from_db()
            return {'message': 'participant supprimé dans la liste noire '}

        return {'message': 'participant not found.'}, 404



class ParticipantList_noire(Resource):
    def get(self):
        return {'participants_liste_noire': list(map(lambda x: x.json(), ListenoireModel.query.all()))}
