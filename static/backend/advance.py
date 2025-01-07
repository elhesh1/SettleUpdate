import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
from flask import request, jsonify
from static.backend.models import user

#from static.backend.variableHelpers import initial_variables
import static.backend.citizenActions as citizenActions
# import static.backend.buildings as buildings
# import static.backend.country as country
import random




@app.route("/advance/<string:currUserName>", methods=["PATCH"])
def advance(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    
    

    offset = user.query.get(currUserName).id
    citizenActions.eat(currUserName)   ##### adjusts health as well #####
    healthFactor = getattr(user_record,'Health') * 0.01 
    season = getattr(user_record, 'season')
    strength  = round(40 + 0.6* 100*healthFactor,2)
    setattr(user_record, 'Strength', strength)
    # db.session.commit()
    # citizenActions.build(currUserName) ### including builders
    # country.advance(currUserName)


    # #cooks
    toAdd = 0
    cookingPower = citizenActions.CooksEff(currUserName)[2]
    wheat = getattr(user_record, 'Wheat')
    wheat -= cookingPower
    left = wheat  # wheat left after making the change
    if left < 0:
         toAdd = left
    wheat -= toAdd
    bread = getattr(user_record, 'Bread')
    bread += cookingPower + toAdd

    #Butchers
    toAdd = 0
    butcherPower = citizenActions.ButcherEff(currUserName)[2]
    rawMeat = getattr(user_record,'Raw_Meat' )
    rawMeat -= butcherPower
    left = rawMeat
    if left < 0:
        toAdd = left
    rawMeat -= toAdd
    cookedMeat = getattr(user_record,'Cooked_Meat')
    cookedMeat += butcherPower + toAdd
    
    #Hunters
    hunterPower = citizenActions.HunterEff(currUserName)[8]
    rawMeat += hunterPower
    fur = getattr(user_record, 'Fur')
    fur += hunterPower


    setattr(user_record,'Raw_Meat', rawMeat )
    setattr(user_record,'Cooked_Meat', cookedMeat)
    setattr(user_record, 'fur', fur)

    #Loggers
    wood = getattr(user_record,'Wood' )
    loggerPower = citizenActions.LoggerEff(currUserName)[6]
    setattr(user_record, 'Wood', wood + loggerPower)

    #Planters(Farmers)
    planted = getattr(user_record, 'Planted')
    farmerPower = citizenActions.farmerEff(season,currUserName)[0]
    if((season)%4 == 1): #Spring
        planted +=   farmerPower
    elif(season == 2):
        berries = getattr(user_record ,'Wild_Berries')
        setattr(user_record, 'Wild_Berries', berries + farmerPower)
    elif((season)%4 == 3):
        toAdd = 0
        planted -= farmerPower
        if planted < 0:
            toAdd = planted
            planted -= toAdd
        wheat += farmerPower + toAdd
    elif((season)%4 == 0):
        planted = 0
    
    setattr(user_record, 'Bread', bread)
    setattr(user_record,'Wheat',wheat)
    setattr(user_record,'Planted',planted)
    # buildings.advanceBuildings(currUserName)

    # population = Contact.query.get(5 + offset*contactOffset)

    # if healthFactor < 0.50:
    #     percentOff = 0
    #     diff = (0.6 - healthFactor) *0.6    
    #     if healthFactor < 0.25:
    #         diff += (0.3 - healthFactor)*4 # 
    #         if healthFactor < 0.1:
    #             diff += (0.1 - healthFactor)*5
    #     percentOff = diff  * random.randint(10,30) * 0.01 # 5-15,
    #     oldPop = population.value
    #     population.value = round(population.value * (1-percentOff),0)
    #     fallOff =  oldPop - population.value
    #     available = Contact.query.get(6 + offset*contactOffset)
    #     available.value -= fallOff
    #     print(" AVAILABILE VALUE ", available.value)
    #     if (available.value < 0):
    #         leftover = round(available.value * -1,0)
    #         index = 0
    #         for i in initial_variables:
    #             index += 1
                
    #             if i.get('type') == 'JOB':
    #                 toSubtract = Contact.query.get(index + offset*contactOffset)
    #                 toSubtract.value -= leftover
    #                 leftover = 0 
    #                 if (toSubtract.value < 0):
    #                     leftover -= toSubtract.value
    #                     toSubtract.value -= toSubtract.value
    #                     leftover = round(leftover,0)
    #                 db.session.add(toSubtract)
    #                 try:
    #                     db.session.commit()
    #                 except Exception as e:
    #                     db.session.rollback()
    #         if leftover > 0:
    #             print("leftover  ", )
    #             for j in Building.query.filter(Building.currUserName == currUserName).all():
    #                 print("j ", j)
    #                 if j.working != None:
    #                     print(j.working)
    #                     print("JWOKRVALUE " ,  j.working['value'])
    #                     j.working['value'] -= leftover
    #                     leftover = 0
    #                     if (j.working['value'] < 0):
    #                         leftover -= j.working['value'] 
    #                         j.working['value']  -= j.working['value'] 
    #                         leftover = round(leftover,0)
    #                     print("  JJJJ ", j.working)
    #                     newWork = {'value': j.working['value'], 'maximum': j.working['maximum'], 'minimum': j.working['minimum']}
    #                     print ("newWark", newWork)
    #                     j.working = {'value': int(j.working['value']), 'maximum': int(j.working['maximum']), 'minimum': int(j.working['minimum'])}
    #                     db.session.add(j)
    #                     try:
    #                         db.session.commit()
    #                     except Exception as e:
    #                         db.session.rollback()
    #                         return jsonify({"message": f"An error occurred: {str(e)}"}), 500




    #         available.value = 0

    week = getattr(user_record, 'week')
    week += 1
    week = round(week, 0)
    if week == 14:
        season = getattr(user_record, 'season')
        week = 1
        season += 1
        season = round(season, 0)
        if season == 4:
            season = 0
            year = getattr(user_record, 'year')
            year += 1
            year = round(year,0)
            setattr(user_record, 'year', year)
        setattr(user_record, 'season', season)
    setattr(user_record, 'week', week)
    db.session.commit()
    return jsonify({"message": "advanced...."}), 201

@app.route("/advancePackage/<string:currUserName>", methods=['GET'])
def advancePackage(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    
    week = getattr(user_record, 'week', None)  
    season = getattr(user_record, 'season', None) 
    year = getattr(user_record, 'year', None)  
    Health = getattr(user_record, 'Health', None)
    Population = getattr(user_record, 'Population', None)

    return jsonify({
        "week": week,
        "season": season,
        "year": year,
        'Health' : Health,
        'Population' : Population
    }), 200

