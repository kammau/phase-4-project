#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, session, jsonify, make_response
from flask_restful import Resource


# Local imports
from config import app, db, api
from models import db, User, Post, Plant, Forum, user_plant

app.secret_key = b'Q\xd9\x0c\xf0\xec\x1e!\xdb\xae6\x08\x0cuf\x95\xf9'


class CheckSession(Resource):
    def get(self):
        user_id = session["user_id"]
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200

        return {}, 401

class Login(Resource):
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id

            return user.to_dict(), 200
        
        return {"error": "401 Unauthorized"}, 401

class Signup(Resource):
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")

        if username and password:
            new_user = User(username=username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id

            return new_user.to_dict(), 201
        
        return {"error": "422 Unprocessable Entity"}, 422

class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {"message": "204: No Content"}, 204

class Plants(Resource):
    def get(self):
        plants = Plant.query.join(user_plant).join(User).filter((user_plant.c.user_id == session["user_id"]) & (user_plant.c.plant_id == Plant.id)).all()

        plants_serialized = [plant.to_dict() for plant in plants]
        
        if len(plants_serialized) > 0:
            return plants_serialized, 200

        else:
            return {"message": "404: No Content"}, 404

    def post(self):
        data = request.get_json()
        user = User.query.filter(User.id == session["user_id"]).first()

        new_plant = Plant(
            common_name=data["common_name"],
            scientific_name=data["scientific_name"],
            growing_level=data["growing_level"],
            img=data["img"],
        )

        db.session.add(new_plant)
        user.plants.append(new_plant)

        db.session.commit()

        return new_plant.to_dict(), 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        return plant.to_dict(), 200
    
    def post(self, id):
        pass
    
    def patch(self, id):
        data = request.get_json()

        plant = Plant.query.filter(Plant.id == id).first()

        for attr in data:
            setattr(plant, attr, data[attr])

        db.session.add(plant)
        db.session.commit()

        return plant.to_dict(), 202

    def delete(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        db.session.delete(plant)
        db.session.commit()

        return {}, 204
        

api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Plants, "/plants", endpoint="plants")
api.add_resource(PlantByID, "/plants/<int:id>", endpoint="plant_by_id")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")

if __name__ == '__main__':
    app.run(port=5555, debug=True)

