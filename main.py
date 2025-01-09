# Request returns a Response. status:200 means success
from flask import request, jsonify, Flask, render_template
from static.backend.variableHelpers import DEFAULT_VALUES

from config import app, db
#from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, Country, user, contactOffset,resourceOffset,buildingOffset,countryOffset
import static.backend.citizenActions as citizenActions
from static.backend.models import user
from sqlalchemy import create_engine, Column, Integer, String, func
import static.backend.advance as advance
import static.backend.hover as hover
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
    data = request.json
    if 'value' not in data:
        return jsonify({"error": "Missing 'value' in request body"}), 400
    setattr(user_record, variableName, data['value'])
    try:
        db.session.commit()
        return jsonify({"message": f"{variableName} updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update {variableName}"}), 500

@app.route("/get/<string:currUserName>/<string:variableName>", methods=["GET"])
def get_resource(currUserName,variableName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    value = getattr(user_record, variableName)
    return jsonify({variableName: value}), 200

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
 

    value = checking
    value +=  toAdd

    if value < getattr(user_record, minimum):
        value = getattr(user_record, minimum)
        toAdd = checking - getattr(user_record, minimum)
    if value > getattr(user_record, maximum):
        value = getattr(user_record, maximum)
    actualChange = value - og

    if variableHelperTags[variableName][4] == 'job':
        addBack = 0
        second = getattr(user_record, 'Available_value')
        second -= actualChange
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
    data = request.json
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    for column, value in DEFAULT_VALUES.items():
        setattr(user_record, column, value)
    db.session.commit()
    return jsonify({"message": "Didn't break everything"}), 201


resources = [
    # name , shown (0s are always shown), integer (1s  only are integers), then type
    ['Wheat', 0, 0, 'raw'],
    ['Fur', 0, 0,'raw'],
    ['Raw_Meat', 0, 0,'raw'],
    ['Wood', 0, 0,'raw'],
    ['Bread', 0, 0, 'food'],
    ['Cooked_Meat', 0, 0,'food'],
    ['Wild_Berries', 0, 0,'food'],
    ['Vegtables', 0, 0,'food'],
    ['Iron_Hoe', 0, 1,'tool'],
    ['Iron_Sickle', 0, 1,'tool'],
    ['Iron_Axe', 0, 1,'tool'],
    ['Rifle', 0, 1,'tool'],
    ['Bow', 0, 1,'tool'],
    ['Iron_Shovel', 0, 1,'tool'],
    ['Iron_Pickaxe', 0, 1,'tool'],
    ['Clay', 1, 0,'raw'],
    ['Iron_Ore', 1, 0, 'raw'],
    ['People', 1, 0,'tool'],
    ['Bricks', 1, 0, 'adv'],
    ['Iron', 1, 0, 'adv'],
    ['Anvil', 1, 0, 'adv']
]

jobs = [
    ['Farmer','Farmer_value'],
    ['Hunter','Hunter_value'],
    ['Baker','Baker_value'],
    ['Butcher','Butcher_value'],
    ['Logger','Logger_value'],
    ['Builder','Builder_value']

]


buildings = [
    # name      typeofbuilding    , work
    ['Log_Cabin','Housing','a','a', 2],
    ['Town_Hall','Town_Hall','a','a', 50],
    ['Clay_Pit',"Raw Material Maker", 'Clay_Pit_Workers', 'Clay_Pit_Workers_Max',5],
    ['Mine',"Raw Material Maker", 'Mine_Workers', 'Mine_Workers_Max',15],
    ['Kiln',"Second Level", 'Kiln_Workers', 'Kiln_Workers_Max',3],
    ['Forge',"Second Level", 'Forge_Workers', 'Forge_Workers_Max',3],
    ['Tool_Shop','Tool_Shop','a','a',50],


]

@app.route("/resources/<string:currUserName>", methods=["GET"]) 
def get_resources(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404

    user_resources = {} 

    for resource in resources:
        resource_value = getattr(user_record, resource[0], 0)  
        user_resources[resource[0]] = {"name" : resource[0], "value": resource_value, "always": resource[1], "integer" : resource[2], 'type' : resource[3]}
    return jsonify({"resources": user_resources})

@app.route("/buildings/<string:currUserName>", methods=["GET"]) 
def get_buildings(currUserName):
    #round perhaps?
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404

    user_buildings = {}
    for building in buildings: 
        building_value = getattr(user_record, building[0], 0)  
        user_buildings[building[0]] = {"name" : building[0] , "value": building_value, "typeOfBuilding": building[1], "workers" : getattr(user_record,building[2], -1), 'max' : getattr(user_record,building[3],-1), 'work' : building[4]}
    return jsonify({"buildings": user_buildings})

@app.route("/<string:currUserName>/buildings/addQueue", methods=["PATCH"])
def create_building_queue(currUserName): # queue is in string form, which is not efficent....
    print("HERE PATCHING")
    data = request.json
    print(" this is the json  ", data)
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    queue = getattr(user_record, 'building_queue')
    queue = citizenActions.stringQueuetoArray(queue)

    for item in data['dataQ']:
       # print(item)
        numbertoAdd = str(data['dataQ'][item][0] )
        if len(queue) == 0:
            print('Queue is empty, adding new item')
            queue.append((0,item, numbertoAdd)) 
        else:
            last_item = queue[-1]
            print("LAST ITEM  ", last_item,  "  ", "item  ", item)
            if last_item[1] == item:
                print(f"Queue has item '{item}', adding {numbertoAdd} to the existing number")
                queue[-1] = (len(queue)-1, last_item[1], str(int(last_item[2]) + int(numbertoAdd))) 
            else:
                print(f"Queue has a different item, adding new entry for '{item}'")
                queue.append((len(queue), item, numbertoAdd)) 
    
    queue = citizenActions.arrayToStringQueue(queue)
    setattr(user_record, 'building_queue', queue)

    db.session.commit()
    return jsonify({"queue": queue})

@app.route("/currentContent/<string:currUserName>", methods=["GET"])
def returnCurrentBuildings(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    queue = getattr(user_record, 'building_queue')
    return jsonify({"queue": queue})


# def roundResources(currUserName):
#     user_record = db.session.query(user).filter_by(name=currUserName).first() 
#     if user_record is None:
#         return jsonify({"error": "User not found"}), 404
#     resources = Resource.query.filter(Resource.currUserName == currUserName).all()
#     for resource in resources:
#         setattr(user_record,resource,round(getattr(user_record,resource),3)) 
#     db.session.commit()


@app.route("/clearJobs/<string:currUserName>", methods = ["PATCH"]) 
def clearJobs(currUserName):

    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    addBack = 0

    for job in jobs:
        addBack += getattr(user_record,job[1])
        setattr(user_record,job[1],0)
    setattr(user_record, 'Available_value', getattr(user_record,'Available_value') + addBack)
    db.session.commit()

    return jsonify({"message": " Cleared :) "}), 201


@app.route("/hoverString/<string:type>/<string:currUserName>",methods=['GET'])
def returnHoverString(currUserName,type):
    return jsonify({"string" : hover.hoverString(type,currUserName)})




if __name__ == "__main__": ##### MUST BE AT BOTTOM
    with app.app_context():
        db.create_all() # creates all of the models
    app.run(debug=True)