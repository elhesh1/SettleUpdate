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
 
def build(currUserName): #16
    print("FUCKING GOT HERE")
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if user_record is None:
        return jsonify({"error": "User not found"}), 404
    global buildingsBuiltThisWeek
    buildingsBuiltThisWeek = {}
    weeklyBuildPower = BuilderEff(currUserName)[2] 
    setattr(user_record, 'weekly_build_power', weeklyBuildPower)
    print("BUILD POWER  ", weeklyBuildPower)
    current = (getattr(user_record, 'building_queue') )
    print("CURRENT      ", current)
    current = stringQueuetoArray(current)
    print("CURRENT      ", current)

    for i in range( len(current)):        # iterate through each building
        c = current[i]
        print("CURRENTLY BUILDING : " , c)
        buildbuild(c,i,currUserName)
  
    
    buildings.reactToBuildings(buildingsBuiltThisWeek,currUserName)
    setattr(user_record,'weekly_build_power', 0)

    buildings_to_add = getattr(user_record, 'buildings_to_add')
    buildings_to_add = stringQueuetoArray(buildings_to_add)
    print("BUILDLINGS TO ADD  ", buildings_to_add)
    for building in buildings_to_add:
        print(" THIS BUILDING 2ah    ", building[1])
        setattr(user_record, building[1], int((getattr(user_record,building[1])) + 1))
    setattr(user_record, "buildings_to_add", "")
    db.session.commit()


def buildbuild(c,i,currUserName):
    print('start buildbuild    ', c, i ," "  )
    user_record = db.session.query(user).filter_by(name=currUserName).first() 

#     offset = user.query.get(currUserName).id
    weeklyBuildPower = getattr(user_record, 'weekly_build_power')
    currently_building_queue = getattr(user_record,'currently_building_queue')
    currently_building_queue = stringQueuetoArray(currently_building_queue,0)
    buildings_to_add = getattr(user_record, 'buildings_to_add')
    buildings_to_add = stringQueuetoArray(buildings_to_add)
  #  print(" THIS IS THE  curbuiq  ", currently_building_queue)
#     global buildingsBuiltThisWeek
#     temp = c.name
 ##   print("BUILD BUILD Enter   ", c,  i, "  ", currently_building_queue)
    found_building = False
    print(" THIS IS ACTUALLY KIND OF VERY                  Important   ", currently_building_queue)
    print (   type(currently_building_queue))
    if currently_building_queue not in ("", None) and currently_building_queue != [] and currently_building_queue: # THERE IS SOMETHING ALREADY IN THE CURRENTLY BUILDING
        found_building = False
        j = 0
        loopOver = False
        print(" WE WE WE HAVE HAVE HAVE SOMETHING IN THE SHITTER AND IT LOOKS LIKE THIS     ",  currently_building_queue)
        while currently_building_queue and not found_building and not loopOver:
            if j in range(len(currently_building_queue)):
                currently_building = currently_building_queue[j]
                print("RIGHT HERE   MISTAKE  ", currently_building_queue, "   ", currently_building)

                if currently_building[1].split('Current')[0] == c[1].split('Current')[0]:
             #       print("THIS JOHN is NOT empty lmao take a look inside", currently_building)
                    #currently_building[2]  # this is the work left
             #       print(currently_building[2]  , "   and   ", weeklyBuildPower, "    and ", currently_building_queue[i])
                    if weeklyBuildPower >= currently_building[2]:  # We can build the building
                        weeklyBuildPower -= currently_building[2]  
                        currently_building = (currently_building[0], currently_building[1], 0)
                      #  print(" RIGH HERE DOING SOME SUBTRACTING   ", weeklyBuildPower, currently_building, "    and   ", currently_building[2])
                        
                        found_building = True  



                        buildings_to_add.append((0,currently_building[1] ,0))
                  ##      print("                                                               Adding a building woohoo")
                        current = (getattr(user_record, 'building_queue') ) # show that we have lone less in the Q
                        current = stringQueuetoArray(current)
                        print("Current i b4  " , current[i])
                        updatingbuildingqueue = (current[i][0], current[i][1], int(current[i][2] - 1))
                        print('current i after' , updatingbuildingqueue)
                        current[i] = updatingbuildingqueue
                        oneMoreQ = True
                        if updatingbuildingqueue[2] == 0:
                            print("its over")
                            oneMoreQ = False
                        # array = current
                        # get array and remove all rows that are (x,x, 0)
                        current = [row for row in current if not( row[2] == 0)]

                        setattr(user_record, 'building_queue' ,arrayToStringQueue(current))



                        if oneMoreQ:
                            print("keep going   -----------------------                 ------- this much work   ",weeklyBuildPower )
                            print("This    " , currently_building_queue)
                            currently_building_queue[j] = currently_building
                            buildings_to_add = arrayToStringQueue(buildings_to_add)
                            currently_building_queue = [item for item in currently_building_queue if item[2] != 0]
                            currently_building_queue = arrayToStringQueue(currently_building_queue)
                            print("THIS   " ,currently_building_queue)

                            setattr(user_record,'currently_building_queue',currently_building_queue)
                            setattr(user_record, 'weekly_build_power', weeklyBuildPower)
                            setattr(user_record, 'buildings_to_add', buildings_to_add)
                            db.session.commit()
                            if c[2] - 1 != 0:
                                buildbuild((c[0],c[1],c[2]-1),i, currUserName)
                                return
                        #### WE CAN STILL BUILD DO SOMETHING ABOUT THAT
                    else:
                        # we can't build shit but we can start
                     ##   print("   we can try ", weeklyBuildPower)
                        currently_building = (currently_building[0], currently_building[1], currently_building[2] - weeklyBuildPower)
                        weeklyBuildPower = 0
                        found_building = True  # Exit the loop 
                print("RIGHT HERE   MISTAKE  ", j, " ", currently_building_queue, " next  ", currently_building)

                if isinstance(currently_building_queue, str):
                    currently_building_queue = stringQueuetoArray(currently_building_queue, intt = 0)

                currently_building_queue[j] = currently_building
                currently_building_queue = [item for item in currently_building_queue if item[2] != 0]
                j += 1
            else:
                loopOver = True

    if found_building == False:                         # NOTHING IS BEING BUILT - if found building = false we did not find it
        building = c[1].split('Current')[0]
        print(" THIS SHOUDL BE HAPPENINING THE SECOND SECOND SECOND TIMEEEE")
     ##   print("       this is empty  ", building)
        costs = buildings.building_prices[building]['Cost']

        buildable = 1
        for cost in costs:  #
     ##       print("COST :   ", cost)
            valueWeHave = getattr(user_record, cost)
            
            if costs[cost] <= valueWeHave:
                print("WE HAVE enough: " , valueWeHave, "  and we need  ", costs[cost])
            else:
               print("WE DONT HAVE enough: " , valueWeHave, "  and we need  ", costs[cost]) 
               buildable = 0
        
        if buildable == 1:
            # we can start construction on this boy
         ##   print('we can build')
            for cost in costs:
                setattr(user_record, cost , getattr(user_record, cost) - costs[cost])
            currently_building_queue.append((1, building, int(buildings.building_prices[building]['Work'])))  
        


  ##  print("BUILD BUILD Exit   ", c,  i, "  ", currently_building_queue)
    if isinstance(buildings_to_add, list):
        print(" BUILDINGS TO ADDDD " , buildings_to_add)
        buildings_to_add = arrayToStringQueue(buildings_to_add)
    currently_building_queue = arrayToStringQueue(currently_building_queue)
    setattr(user_record,'currently_building_queue',currently_building_queue)
    setattr(user_record, 'weekly_build_power', weeklyBuildPower)
    setattr(user_record, 'buildings_to_add', buildings_to_add)
    db.session.commit()

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

def stringQueuetoArray(queueString, intt=1):
    print("Q STRING  :   ", queueString)
    items = queueString.split('-')
    queue = []
    if (intt == 1):
        for item in items:
            if item.strip():  
                order, name, number = item.split()  
                queue.append((order, name, int(number) ))  
    else:
         for item in items:
            if item.strip():  
                order, name, number = item.split()  
                queue.append((order, name, float(number)))  
    return queue

def arrayToStringQueue(queue):
    queueString = ""
    print("QUEUEING ", queue)
    for item in queue:
        order, name, number = item 
        queueString += f"{order} {name} {number}-"  
    if queueString.endswith('-'):
        queueString = queueString[:-1]

    return queueString