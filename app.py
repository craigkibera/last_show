from flask import Flask,jsonify,request
from flask_migrate import Migrate
from models import db,Episode,Guest,Appearance
from flask_restful import Api, Resource
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///episodes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
api=Api(app)

class EpisodeResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        episode_list = [
            {
                "id":episode.id,
                "date":episode.date,
                "number":episode.number
            } 
            for episode in episodes
            
        ] 

        return jsonify(episode_list)



class SingleEpisodeResource(Resource):
    def get(self, episode_id):
        episode = Episode.query.get(episode_id)
        if not episode:
            return jsonify({"message": "Episode not found"}), 404
        episode_data = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": [
                {
                    "episode_id": appearance.episode_id,
                    "guest":{
                        "id": appearance.guest.id,
                        "name": appearance.guest.name,
                        "occupation": appearance.guest.occupation
                    },
                    "guest_id": appearance.guest_id,
                    "id": appearance.id,
                    "rating": appearance.rating
                }
                for appearance in episode.appearances
            ]
        }
        return jsonify(episode_data)

class GuestResource(Resource): # endpoint for getting all guests
    def get(self): # get all guests
        guests = Guest.query.all() # query all guests
        guest_list = [ # create a list of dictionaries for each guest
            {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
            for guest in guests # iterate through each guest
        ]
        return jsonify(guest_list) # return the list of guests


class AppearanceResource(Resource): # endpoint for creating new appearances
    def post(self):  #registering a new appearance
        data = request.get_json() # get the json data from the request
        if not data:
            return {"error": "Missing JSON Data"}, 400
        # Extracting data from the request
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        if not all([rating, episode_id, guest_id]):
            return {"message": "Missing required fields"}, 400
        # querying the database to check if the episode and guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode:
            return {"message": "Episode not found"}, 404
        if not guest:
            return {"message": "Guest not found"}, 404
        # Creating a new Appearance object
        try:
            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )
            db.session.add(new_appearance)
            db.session.commit()
            # Return the newly created appearance
            return {
                "id": new_appearance.id,
                "rating": new_appearance.rating,
                "episode_id": new_appearance.episode_id,
                "guest_id": new_appearance.guest_id,
                "episode": {
                    "id": episode.id,
                    "date": episode.date,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }, 201

        except ValueError as e:
            db.session.rollback()
            return {"message": str(e)}, 400


api.add_resource(EpisodeResource, '/episodes')
api.add_resource(SingleEpisodeResource, '/episodes/<int:episode_id>')
api.add_resource(GuestResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')

if __name__ == '__main__':
    app.run()