from flask import Flask
from flask_restful import Api
from resources.participant import ParticipantList, Participant
from resources.liste_noire import  Liste_noire, ParticipantList_noire
from resources.tirage import TirageList, Tirage,historique,historique2
from db import db
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()



api.add_resource(Tirage, '/tirage/<string:name>')
api.add_resource(TirageList, '/tirages/<int:id_t>')
api.add_resource(Participant, '/participant/<string:name>/<string:prenom>')
api.add_resource(Liste_noire, '/liste_noire/<string:name>')
api.add_resource(ParticipantList_noire, '/participant_noire')
api.add_resource(ParticipantList, '/participants')
api.add_resource(historique, '/historiques')
api.add_resource(historique2, '/historiques2')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
