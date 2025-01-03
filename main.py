# Request returns a Response. status:200 means success
from flask import request, jsonify, Flask, render_template
from static.backend.variableHelpers import DEFAULT_VALUES

from config import app, db
#from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, Country, user, contactOffset,resourceOffset,buildingOffset,countryOffset
#import static.backend.citizenActions
from static.backend.models import user
from sqlalchemy import create_engine, Column, Integer, String, func
#import static.backend.advance as advance
#import static.backend.hover as hover
#import static.backend.buildings as buildings
from sqlalchemy.exc import IntegrityError
#from static.backend.variableHelpersDev import initial_variablesD, initial_buildingsD, initial_resourcesD, initial_countriesD
#import static.backend.country as country

@app.route("/user", methods=["GET"]) # gets all users
def get_contacts():  
    users = user.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    return jsonify({"users": json_users})

def set_user_defaults(user_record):
    for column, value in DEFAULT_VALUES.items():
        setattr(user_record, column, value)

@app.route("/set/<string:currUserName>/<string:variableName>", methods=["PATCH"])
def set_resource(currUserName,variableName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    print('data ', data['value'])
    print(variableName)
    data = request.json
    if 'value' not in data:
        return jsonify({"error": "Missing 'value' in request body"}), 400
    setattr(user_record, variableName, data['value'])
    try:
        db.session.commit()
        return jsonify({"message": f"{variableName} updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating {variableName}: {e}")
        return jsonify({"error": f"Failed to update {variableName}"}), 500


variableHelperTags = {
    'Farmer_value': ['Farmer_maximum', 'Farmer_minimum', 'Farmer_type', 'Farmer_efficiency','job'],
    'Hunter_value': ['Hunter_maximum', 'Hunter_minimum', 'Hunter_type', 'Hunter_efficiency','job'],
    'Baker_value': ['Baker_maximum', 'Baker_minimum', 'Baker_type', 'Baker_efficiency','job'],
    'Butcher_value': ['Butcher_maximum', 'Butcher_minimum', 'Butcher_type', 'Butcher_efficiency','job'],
    'Logger_value': ['Logger_maximum', 'Logger_minimum', 'Logger_type', 'Logger_efficiency','job'],
    'Builder_value': ['Builder_maximum', 'Builder_minimum', 'Builder_type', 'Builder_efficiency','job'],
    'Available_value': ['Available_maximum', 'Available_minimum', 'Available_type', 'Available_efficiency','job']
}

@app.route("/change/<string:currUserName>/<string:variableName>", methods=["PATCH"])
def change_resource(currUserName,variableName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    print('data ', data)
    print('vname = ' ,variableName)

    print('have we made it this far?   ')

    modifier = 1
    data = request.json

    maximum = variableHelperTags[variableName][0]
    minimum = variableHelperTags[variableName][1]
    if variableHelperTags[variableName][4] == 'job':
        modifier = getattr(user_record, 'job_modifier')

    og = getattr(user_record, variableName)
    toAdd = data.get("value", 0) * modifier
  
    # changing max and min if that is requested
    current_maximum = getattr(user_record, maximum, 0)
    setattr(user_record, maximum, current_maximum + data.get("maximum", 0))
    current_minimum = getattr(user_record, minimum, 0)
    setattr(user_record, minimum, current_minimum + data.get("minimum", 0))

    checking = getattr(user_record, variableName)
    print('STOP RIGHT HERE  ', og, ' ' , toAdd)
    print(variableHelperTags[variableName][0]," ", getattr(user_record, maximum, 0))
    print(variableHelperTags[variableName][1], " ", getattr(user_record, minimum, 0))
    print(variableName, " ", checking)

    value = checking
    value +=  toAdd

    if value < getattr(user_record, minimum):
        print("too low")
        value = getattr(user_record, minimum)
        toAdd = checking - getattr(user_record, minimum)
    if value > getattr(user_record, maximum):
        print("too high")
        value = getattr(user_record, maximum)
    actualChange = value - og

    print('actual change  ', actualChange)
    if variableHelperTags[variableName][4] == 'job':
        print('here we are')
        addBack = 0
        second = getattr(user_record, 'Available_value')
        print('second here ', second)
        second -= actualChange
        print('new second ', second)
        if second < getattr(user_record, 'Available_minimum'):
            addBack = second - getattr(user_record, 'Available_minimum')
            second = getattr(user_record, 'Available_minimum')
        setattr(user_record, 'Available_value',second)
        value += addBack
    
    setattr(user_record, variableName,value)
    db.session.commit()
    return jsonify({"message": " Values updated"}), 201  



@app.route("/add_user/<string:name>", methods=["POST"])
def add_user(name):
    try:
        print("Attempting to add user...")
        new_user = user(name=name)
        set_user_defaults(new_user)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "USER CREATED!"}), 201
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
        return jsonify({"message": "USER NOT CREATED, but still returning success."}), 201

@app.route('/reset/<string:currUserName>', methods=['PATCH'])
def reset(currUserName):
    print(" RESETTTING ", currUserName)
    data = request.json
    print("DATA   ", data)
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    for column, value in DEFAULT_VALUES.items():
        setattr(user_record, column, value)
    db.session.commit()
    return jsonify({"message": "Didn't break everything"}), 201

if __name__ == "__main__": ##### MUST BE AT BOTTOM
    with app.app_context():
        db.create_all() # creates all of the models
    app.run(debug=True)