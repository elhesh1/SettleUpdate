import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
from static.backend.models import user
from flask import request, jsonify
import static.backend.advance
#import static.backend.hover as hover
import static.backend.buildings as buildings


#job efficencies
jobEfficencies = {
    'Farmer_value': { 'e': 0.1, 'season': {0: 1, 1: 1, 2: 1, 3: 1} },
    'Hunter_value': { 'e': 0.025, 'season': {0: 1, 1: 1, 2: 1, 3: 1} },
    'Butcher_value': { 'e': 0.1, 'season': {0: 1, 1: 1, 2: 1, 3: 1} },
    'Logger_value': { 'e': 0.1, 'season': {0: 0.6, 1: 0.95, 2: 1, 3: 1} },
    'Builder_value': { 'e': 0.1, 'season': {0: 0.6, 1: 1, 2: 1, 3: 1} },
    'Baker_value': { 'e': 0.1, 'season': {0: 1, 1: 1, 2: 1, 3: 1} }
}

nFoodTypes = 0 
# .filter(Contact.currUserName == currUserName)
def eat(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    

    global foodTypes

    rationingPval = getattr(user_record, 'RationP' ) 
    population = getattr(user_record, 'Population' ) 
    expectedFood = rationingPval * 0.01 * population * 0.02 
    eatHelper(expectedFood,currUserName, user_record)
    if  population != 0:
        housedRatio  = getattr(user_record, 'Log_Cabin') * buildings.LogCabinCapacity /  population # may want to change this one as well
        if housedRatio > 1:
            housedRatio = 1
    else:
        housedRatio = 0 
    season = getattr(user_record, 'season')
    if season == 1:
        housedValue = 0.85 + 0.15*housedRatio
    elif season == 2:
        housedValue = 0.9 + 0.1*housedRatio
    elif season == 3:
        housedValue = 0.85 + 0.15*housedRatio
    else:
        housedValue = 0.1 + 0.9*housedRatio
    if nFoodTypes == 0:         ### you are starving 
        rationingPval = 15 # basically the minimum if you can't eat
    HealthEquilibrium = rationingPval *0.01 * (68+nFoodTypes*8) * housedValue
    setattr(user_record, 'numberofFoods', nFoodTypes)
    setattr(user_record,'Health', round(HealthEquilibrium,0))
    db.session.commit()

    return jsonify({"message": " Values updated"}), 201

def eatHelper(expectedFood,currUserName,user_record):
    offset = user.query.get(currUserName).id
    global nFoodTypes
    FoodTypeValues = [0,0,0,0]
    nFoodTypes = 0
    # fruits, Vegetables, meat, grain        
    FoodTypeValues[0] = getattr(user_record,'Wild_Berries' ) 
    FoodTypeValues[1] = getattr(user_record, 'Vegetables') 
    FoodTypeValues[2] = getattr(user_record,'Cooked_Meat' ) 
    FoodTypeValues[3] = getattr(user_record,'Bread' ) 
                       # Only did one food for each value needs to be updated in the futrere/////////////////////
    foodmin = 9999999
    for FoodVal in FoodTypeValues:
        if FoodVal > 0:
            nFoodTypes += 1
            if FoodVal < foodmin:
                foodmin = FoodVal
    if nFoodTypes == 0:
        return 
    if foodmin >= expectedFood/nFoodTypes:
        change = expectedFood/nFoodTypes
        val8  = getattr(user_record,'Wild_Berries' )  
        val7 = getattr(user_record,'Cooked_Meat' ) 
        val6 = getattr(user_record,'Bread' ) 
        val9 = getattr(user_record, 'Vegetables') 
        val8 -= change
        val9 -= change
        val7 -= change
        val6 -= change
        if val8 < 0:
            val8 = 0
        if val9 < 0:
            val9 = 0
        if val7 < 0:
            val7 = 0
        if val6 < 0:
            val6 = 0
        setattr(user_record, 'Wild_Berries', val8)
        setattr(user_record, 'Cooked_Meat', val7)
        setattr(user_record, 'Bread', val6)
        setattr(user_record, 'Vegetables', val9)

         # put back in the vals 1/4/25


    else :
        change = foodmin
        foodleft = expectedFood - foodmin*4
        nFoodTypes -= 0.75 ##################### could change this if you are up for it some day
        val8  = getattr(user_record,'Wild_Berries' )  
        val7 = getattr(user_record,'Cooked_Meat' ) 
        val6 = getattr(user_record,'Bread' ) 
        val9 = getattr(user_record, 'Vegetables') 
        val8 -= change
        val9 -= change
        val7 -= change
        val6 -= change
        if val8 < 0:
            val8 = 0
            foodleft += foodmin 
        if val9 < 0:
            val9 = 0
            foodleft += foodmin
        if val7 < 0:
            val7 = 0
            foodleft += foodmin
        if val6 < 0:
            val6 = 0
            foodleft += foodmin
        setattr(user_record, 'Wild_Berries', val8)
        setattr(user_record, 'Cooked_Meat', val7)
        setattr(user_record, 'Bread', val6)
        setattr(user_record, 'Vegetables', val9)
       # put back in vals 1/4/25

        db.session.commit()
        eatHelper(foodleft,currUserName,user_record)

    db.session.commit()

# def build(currUserName): #16
#     offset = user.query.get(currUserName).id
#     global weeklyBuildPower
#     global buildingsBuiltThisWeek
#     buildingsBuiltThisWeek = {}
#     weeklyBuildPower = BuilderEff(currUserName)[2] 
#     index = Contact.query.get(16 + offset*contactOffset).value - 1
#     current = CurrentlyBuilding.query.filter(CurrentlyBuilding.currUserName == currUserName).all()
#     for i in range(index, len(current)):        # iterate through each building
#         c = current[i]
#         print("CURRENTLY BUILDING : " , current)
#         buildbuild(c,i,currUserName)
#     rows = CurrentlyBuilding.query.filter(Resource.currUserName == currUserName).all()
#     for row in rows:
#         if row.value == 0:
#             db.session.delete(row)  
#     db.session.commit()
#     buildings.reactToBuildings(buildingsBuiltThisWeek,currUserName)


# def buildbuild(c,i,currUserName):
#     offset = user.query.get(currUserName).id
#     global weeklyBuildPower
#     global buildingsBuiltThisWeek
#     temp = c.name

#     if temp == 2 or temp == 7:
#         print("update?")
#         temp += ( offset*buildingOffset)
    
#     ### IF the building in the queue is too low check the top. Maybe make it so each building can only "see" its type
#     if  CurrentlyBuildingNeedWork.query.filter_by(name=temp,  currUserName = currUserName).first() is None:
#         print(" c:  ", c, " ", temp)
#         if c.value > 0:             
#             print("C C C C C ", c )
#             building = Building.query.get(c.name)   ## dont add offset, its already been calculated
#             if c.name == 2 or c.name == 7:
#                 print("update?")
#                 building = Building.query.get(c.name + offset*buildingOffset)   ## this is for leveled buildings, its wierd ik

#             print("BUILDING COST  " , building.cost)
#             print("BUILDING COST  " , building.id)
#             cost = building.cost
#             work = building.work
#             print("BL ", building.value)
#             if (cost == -1):
#                 cost = hover.buildingLevels[building.value+1]['cost']     # make a call to the level table #######################################
#             if (work == -1):
#                 work = hover.buildingLevels[building.value+1]['work']  # make a call the correct table dufus
#             if c.name == 7:
#                 cost = hover.buildingLevelsT[building.value+1]['cost']  
#                 work = hover.buildingLevelsT[building.value+1]['work']
#             print(" COST ", type(cost), "  ", cost, "really doe")


#             good = 0
#             for key in cost:                       # iterate through each building requeremint
#                 resource = Resource.query.get(int(key) + offset*resourceOffset)  # '5'
#                 costA = cost[key]
#                 if  costA > resource.value:
#                     good = 1
#                     print("YOU DO NOT HAVE ENOUGH")
#                 else:
#                     print("you have enough ;)")
#             if good == 0:

#                 for key in cost:                       # iterate through each building requeremint
#                     resource = Resource.query.get(int(key) + offset*resourceOffset)  # '5'
#                     costA = cost[key]
#                     if  costA > resource.value:
#                         good = 1
#                         print("THIS IS SO BROKEN BROKEN BROKEN BROKEN BROKEN")
#                     else:
#                         print("you have enough ;)")
#                         resource.value -= costA
#                         db.session.add(resource)




#                 c.value -= 1
#                 c.value = round(c.value,0) ### this should be added to ACTIVE. then use up builders. Maybe have an active queue as
#                 print("HAVE RESOURCES TO BUILD ... ", c )
#                 db.session.commit()
#                 if work <= weeklyBuildPower: # we have enough power to build it this week 
#                     print("ENOUGH POWER TO BUILD ", work, " ", weeklyBuildPower)
#                     weeklyBuildPower -= work
#                     building.value += 1
#                     ###################################### built
#                     buildingsBuiltThisWeek[building.id] = 1
#                     db.session.commit()
#                     buildbuild(c,i,currUserName)
#                 else:
#                     c.value += 1
#                     c.value = round(c.value,0)
#                     print( "NOT ENOUGH POWER :(", work, " ", weeklyBuildPower)
#                     currentBuilding = CurrentlyBuildingNeedWork(name = building.id , value = work-weeklyBuildPower , currUserName = currUserName)
#                     weeklyBuildPower = 0
#                     db.session.add(currentBuilding)
#                     db.session.commit()
#         else:
#             db.session.rollback()
#     else:
#         CurrentlyBuildingNeedsMoreWork = CurrentlyBuildingNeedWork.query.filter_by(name=temp,  currUserName = currUserName).first()
#         print("YOU ALREADY GOT SOME SHIT IN THERE")
#         if CurrentlyBuildingNeedsMoreWork.value > weeklyBuildPower:
#             CurrentlyBuildingNeedsMoreWork.value -= weeklyBuildPower
#             weeklyBuildPower = 0 
#             db.session.add(CurrentlyBuildingNeedsMoreWork)
#             db.session.commit()
#         else:
#             weeklyBuildPower -= CurrentlyBuildingNeedsMoreWork.value
#             buildingType = Building.query.get(CurrentlyBuildingNeedsMoreWork.name) # no offset
#             buildingType.value += 1
#             print(buildingType.value)
#             print("BULIDNG TYPE FR ::::::: ", buildingType.name, " ")
#             cname = CurrentlyBuildingNeedsMoreWork.name
#             print(cname)
#             while cname > buildingOffset:
#                 cname -= buildingOffset
#             print("as god intended  ", cname)
#             newC = CurrentlyBuilding.query.filter_by(name=cname,  currUserName = currUserName).first()
#             newC.value -= 1
#             newC.value = round(newC.value,0)
#            # db.session.query(CurrentlyBuildingNeedWork).delete()
#             print(" FINISHED>>> ", CurrentlyBuildingNeedsMoreWork.name)
#             db.session.query(CurrentlyBuildingNeedWork).filter_by(name=CurrentlyBuildingNeedsMoreWork.name,  currUserName = currUserName).delete()
#             db.session.add(buildingType)
#             buildingsBuiltThisWeek[buildingType.id] = 1
#             #################################################
#             db.session.commit()
#             buildbuild(c,i,currUserName)

def farmerEff(season,currUserName):
        offset = user.query.get(currUserName).id

        user_record = db.session.query(user).filter_by(name=currUserName).first() 
        if user_record is None:
            return jsonify({"error": "User not found"}), 404
        
        baseEfficiency =  jobEfficencies['Farmer_value']['e']
        strength = getattr(user_record, 'Strength') * 0.01
        Season = int(getattr(user_record, 'season'))
        seasonEfficiency = jobEfficencies['Farmer_value']['season'][Season]
        count = int(getattr(user_record, 'Farmer_value'))
        if int(season) == 1:
            IronHoeMax = int(getattr(user_record, 'Iron_Hoe'))
            IronHoeEfficiency = 1
            NoToolEfficiency = 0.5 
            if IronHoeMax >= count:
                UsingIronHoe = count
            else:
                UsingIronHoe = IronHoeMax
            UsingNoTools = int(count - UsingIronHoe)
            if count != 0:
                totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronHoeEfficiency * UsingIronHoe)+(NoToolEfficiency*UsingNoTools)) / count )
            else:
                totalEfficiency = baseEfficiency * seasonEfficiency * IronHoeEfficiency * strength
            return count * totalEfficiency, IronHoeEfficiency, UsingIronHoe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Iron Hoe', 'Planted'
        elif int(season) == 3: 
            IronSickleMax = int(getattr(user_record, 'Iron_Sickle'))
            IronSickleEfficiency = 1
            NoToolEfficiency = 0.5 
            if IronSickleMax >= count:
                UsingIronSickle = count
            else:
                UsingIronSickle = IronSickleMax
            UsingNoTools = int(count - UsingIronSickle)
            if count != 0:
                totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronSickleEfficiency * UsingIronSickle)+(NoToolEfficiency*UsingNoTools)) / count )
            else:
                totalEfficiency = baseEfficiency * seasonEfficiency * IronSickleEfficiency * strength
            return  count * totalEfficiency, IronSickleEfficiency, UsingIronSickle, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Iron Sickle', 'Harvested'
        else:
            NoToolEfficiency = 0.18
            UsingNoTools = count
            totalEfficiency =  NoToolEfficiency * baseEfficiency
            return count*totalEfficiency, UsingNoTools, NoToolEfficiency, totalEfficiency, count, 'Berries Foraged' 


def LoggerEff(currUserName):
    jobtitle = 'Logger_value'
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    strength = getattr(user_record, 'Strength') * 0.01
    Season = int(getattr(user_record, 'season'))
    baseEfficiency =  jobEfficencies[jobtitle]['e']
    seasonEfficiency = jobEfficencies[jobtitle]['season'][Season]
    count = int(getattr(user_record, jobtitle))

    IronAxeMax = int(getattr(user_record, 'Iron_Axe' ))
    IronAxeEfficiency = 1
    NoToolEfficiency = 0.5 
    if IronAxeMax >= count:
        UsingIronAxe = count
    else:
        UsingIronAxe = IronAxeMax
    UsingNoTools = int(count - UsingIronAxe)
    if count != 0:
        totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((IronAxeEfficiency * UsingIronAxe)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency * seasonEfficiency * IronAxeEfficiency * strength
    return IronAxeEfficiency, UsingIronAxe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, count * totalEfficiency

def HunterEff(currUserName):

    jobtitle = 'Hunter_value'

    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    strength = getattr(user_record, 'Strength') * 0.01
    Season = int(getattr(user_record, 'season'))
    baseEfficiency =  jobEfficencies[jobtitle]['e']
    seasonEfficiency = jobEfficencies[jobtitle]['season'][Season]
    count = int(getattr(user_record, jobtitle))

    RifleMax = int(getattr(user_record, 'Rifle'))
    BowMax = int(getattr(user_record, 'Bow'))
    RifleEfficiency = 1.5
    BowEfficiency = 1
    NoToolEfficiency = 0.5 
    UsingBow = 0
    if RifleMax >= count:
        UsingRifle = count
        UsingNoTools = int(count - UsingRifle)
    else:
        UsingRifle = RifleMax
        noRifle = int(count-UsingRifle)
        if BowMax >= noRifle:
            UsingBow = noRifle
            UsingNoTools = 0
        else:
            UsingBow = BowMax
            UsingNoTools = int(noRifle - BowMax)
    if count != 0:
        totalEfficiency = baseEfficiency * seasonEfficiency * strength * ( ((RifleEfficiency * UsingRifle)+(BowEfficiency * UsingBow)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency * seasonEfficiency * RifleEfficiency * strength
    return RifleEfficiency, UsingRifle, BowEfficiency, UsingBow, NoToolEfficiency, UsingNoTools, count, totalEfficiency, count*totalEfficiency

def CooksEff(currUserName):
    jobtitle = 'Baker_value'

    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    strength = getattr(user_record, 'Strength') * 0.01
    Season = int(getattr(user_record, 'season'))
    baseEfficiency =  jobEfficencies[jobtitle]['e']
    seasonEfficiency = jobEfficencies[jobtitle]['season'][Season]
    count = int(getattr(user_record, jobtitle))

    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def ButcherEff(currUserName):
    jobtitle = 'Butcher_value'

    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    strength = getattr(user_record, 'Strength') * 0.01
    Season = int(getattr(user_record, 'season'))
    baseEfficiency =  jobEfficencies[jobtitle]['e']
    seasonEfficiency = jobEfficencies[jobtitle]['season'][Season]
    count = int(getattr(user_record, jobtitle))

    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

def BuilderEff(currUserName):
    jobtitle = 'Builder_value'
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    strength = getattr(user_record, 'Strength') * 0.01
    Season = int(getattr(user_record, 'season'))
    baseEfficiency =  jobEfficencies[jobtitle]['e']
    seasonEfficiency = jobEfficencies[jobtitle]['season'][Season]
    count = int(getattr(user_record, jobtitle))

    totalEfficiency = baseEfficiency * seasonEfficiency * strength
    return totalEfficiency, count , count*totalEfficiency 

