# Request returns a Response. status:200 means success
from flask import request, jsonify, Flask, render_template

from config import app, db
#from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, Country, user, contactOffset,resourceOffset,buildingOffset,countryOffset
#import static.backend.citizenActions
from static.backend.models import user
from sqlalchemy import create_engine, Column, Integer, String, func
#import static.backend.advance as advance
#import static.backend.hover as hover
#import static.backend.buildings as buildings
#from static.backend.variableHelpers import initial_variables, initial_resources, initial_buildings, initial_countries
from sqlalchemy.exc import IntegrityError
#from static.backend.variableHelpersDev import initial_variablesD, initial_buildingsD, initial_resourcesD, initial_countriesD
#import static.backend.country as country

@app.route("/user", methods=["GET"])
def get_contacts():  
    users = user.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    return jsonify({"users": json_users})

@app.route("/add_user/<string:name>", methods=["POST"])
def add_user(name):
    try:
        print("Attempting to add user...")
        new_user = user(name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "USER CREATED!"}), 201
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
        return jsonify({"message": "USER NOT CREATED, but still returning success."}), 201


if __name__ == "__main__": ##### MUST BE AT BOTTOM
    with app.app_context():
        db.create_all() # creates all of the models
    app.run(debug=True)