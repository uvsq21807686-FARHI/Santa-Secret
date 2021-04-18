from flask_restful import Resource, reqparse
from models.participant import ParticipantModel


class Participant(Resource):
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
        participant = ParticipantModel.find_by_name(name,prenom)
        if participant:
            return participant.json()
        return {'message': 'participant not found'}, 404

    def post(self, name,prenom):
        if ParticipantModel.find_by_name(name,prenom):
            return {'message': "An participant with name '{}' already exists".format(name)}, 400

        data = Participant.parser.parse_args()
        participant = ParticipantModel(name, **data)

        try:
            participant.save_to_db()
        except:
            return {"message": "An error occured inserting the participant."}, 500

        return participant.json(), 201

    def delete(self, name):
        participant = ParticipantModel.find_by_name(name)
        if participant:
            participant.delete_from_db()
            return {'message': 'participant deleted'}

        return {'message': 'participant not found.'}, 404

    def put(self, name,prenom):
        data = Participant.parser.parse_args()
        participant = ParticipantModel.find_by_name(name,prenom)

        if participant:
            participant.prenom = data['prenom']
        else:
            participant = ParticipantModel(name, **data)

        try:
            participant.save_to_db()
        except:
            return {"message": "An error occured updating the participant."}, 500

        return participant.json()


class ParticipantList(Resource):
    def get(self):
        return list(map(lambda x: x.json(), ParticipantModel.query.all()))
