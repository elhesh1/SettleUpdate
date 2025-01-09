from config import app, db
from static.backend.models import  user
import static.backend.buildings as buildings
import static.backend.citizenActions as citizenActions
#import static.backend.country as country
def hoverString(typee,currUserName):
    print("STARTING RIGHT HERE FOR THE HOVERS")
    print('type   ', typee, '  ', currUserName)
    if typee == 'health':
        return healthString(currUserName)
    if str(typee)[0] == '.': 
        return buildingStringUpgrade(typee,currUserName)
    if typee in jobMap:
        return jobString(typee,currUserName)
    if typee == 'resourceSupply' or typee == 'peopleSupply' or typee == 'toolSupply':
        return country.supplyString(typee,currUserName)
    if typee == 'EnglandExplanation':
        return country.supplyToolTip(currUserName)
    if typee == 'PlantedGrid':
        return plantedString()
    return buildingToString(typee,currUserName)

jobMap = {'farmer': ['Farmer_value'], 
          'hunter': ['Hunter_value'], 
          'cook': ['Baker_value'], 
          'logger' : ['Logger_value'],
         'butcher' : ['Butcher_value'],
           'builder' : ['Builder_value']}

def jobString(typee,currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    JobValue = getattr(user_record, jobMap[typee][0])
    season = getattr(user_record,'season')
    baseEfficiency = citizenActions.jobEfficencies[jobMap[typee][0]]['e']
    seasonEfficiency = citizenActions.jobEfficencies[jobMap[typee][0]]['season'][season]
    strength = getattr(user_record,'Strength') * 0.01
    string = ''
    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Efficiency Factors</div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Base'
    string += '</div> <div style="text-align: right;">'
    string += str(baseEfficiency)
    string +=  '</div></div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Strength'
    string += '</div> <div style="text-align: right;">'
    string += str(round(strength,2))
    string +=  '</div></div>'
    string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Season'
    string += '</div> <div style="text-align: right;">'
    string += str(seasonEfficiency)
    string +=  '</div></div>'

    if typee == 'farmer':
        if int(season) == 1 or int(season) == 3:
            farmingPower, IronHoeEfficiency, UsingIronHoe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, seasonTool, verb = citizenActions.farmerEff(season,currUserName)
            string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
            string += seasonTool + ' ('  + str(UsingIronHoe) + ')'
            string += '</div> <div style="text-align: right;">'
            string += str(IronHoeEfficiency)
            string +=  '</div></div>'
        elif int(season) == 2:
            farmingPower, UsingNoTools, NoToolEfficiency, totalEfficiency, count, verb = citizenActions.farmerEff(season,currUserName)
        else:
            a = citizenActions.farmerEff(season,currUserName)
            farmingPower, UsingNoTools, NoToolEfficiency, totalEfficiency, count, verb = citizenActions.farmerEff(season,currUserName)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)
        string +=  '</div></div>'

        string += efficiencyAndCount(totalEfficiency,count)
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(farmingPower,2)) + ' ' + verb
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Farmers have different actions depending on the season. </div>'
        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Spring - Plant Crops</div>'
        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Summer - Gather Berries</div>'
        string += '<div class="flexitem" style="text-align: left; width: 100%">'
        string += 'Fall - Harvest Crops</div>'    
        # string += '<div class="flexitem" style="text-align: left; width: 100%">'
        # string += 'Winter - Nothing yet...</div>'           
    elif typee == 'logger':
        IronAxeEfficiency, UsingIronAxe, UsingNoTools, NoToolEfficiency, totalEfficiency, count, loggingPower = citizenActions.LoggerEff(currUserName)
        string  += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Iron Axe' + ' ('  + str(UsingIronAxe) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(IronAxeEfficiency)
        string +=  '</div></div>'

        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)
        string +=  '</div></div>'

        string += efficiencyAndCount(totalEfficiency,count)

        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(loggingPower,2)) + ' Wood'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'hunter':
        RifleEfficiency, UsingRifle, BowEfficiency, UsingBow, NoToolEfficiency, UsingNoTools, count, totalEfficiency, huntingpower = citizenActions.HunterEff(currUserName)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Rifle' + ' ('  + str(UsingRifle) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(RifleEfficiency)
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Bow' + ' ('  + str(UsingBow) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(BowEfficiency)
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'No Tools (' + str(UsingNoTools) + ')'
        string += '</div> <div style="text-align: right;">'
        string += str(NoToolEfficiency)  
        string +=  '</div></div>'
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(huntingpower,2)) + ' Raw Meat'
        string +=  '</div>'
        string += '</div> <div class="flexitem" style="text-align: right;">'
        string += str(round(huntingpower,2)) + ' Fur</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'cook':
        totalEfficiency, count , cookingpower = citizenActions.CooksEff(currUserName)
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Input: '
        string += '</div> <div style="text-align: right;">'
        string += '-' + str(round(cookingpower,2)) + ' Wheat'
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(cookingpower,2)) + ' Bread'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'butcher':
        totalEfficiency, count , butcherpower = citizenActions.ButcherEff(currUserName)
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Input: '
        string += '</div> <div style="text-align: right;">'
        string += '-' +  str(round(butcherpower,2)) + ' Raw Meat'
        string +=  '</div></div>'
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(butcherpower,2)) + ' Cooked Meat'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    elif typee == 'builder':
        totalEfficiency, count , builderpower = citizenActions.BuilderEff(currUserName)
        string += efficiencyAndCount(totalEfficiency,count)
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Output: '
        string += '</div> <div style="text-align: right;">'
        string += str(round(builderpower,2)) + ' Work'
        string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string

def healthString(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    nFoodTypes = getattr(user_record,'numberofFoods' )
    health =   getattr(user_record, 'Health' )
    rationP =   getattr(user_record, 'RationP')
    pop =  getattr(user_record, 'Population')
    housed = buildings.housingCapacity(currUserName)
    string = ""
    string += '<div class="flexitem" style="text-align: left; width: 100%">'
    string += 'The health of your colony is very important as it effects citizens ability to do jobs. If your health falls below 50, citizens will start to die off'
    string += '</div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: left; width: 100%">' 
    string += 'Your current health of ' + str(health) + ' is affected by your rationing percentage of ' + str(rationP) + ' and number of food groups : ' + str(nFoodTypes) + '. Providing all 4 food groups is good for health, but only 1 is needed.'
    string += '</div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: left; width: 100%">'
    string += 'Lack of housing effects health. While it has a small effect in summer, it can be detrimental in the winter'
    string += '</div>'
    string +='<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Housing Provided: </div> <div style="text-align: right;">'+ str(housed) + '/' + str(pop) + '</div></div>'
    return string

def efficiencyAndCount(totalEfficiency,count):
        string = '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Total</div> <div style="text-align: right;">'
        string += str(round(totalEfficiency,3))
        string +=  '</div></div><div class="flexitem ToolTipLine" width="80%" size="4"></div><div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Count: </div> <div style="text-align: right;">'
        string += str(count) + '</div></div>'
        return string

buildingMap = {'TownHall' : 2, 'ToolShop' : 7}

def TH2string():
    string = ''
    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Building a town hall will allow you to recieve supplies from England'+ '</div>'
    return string
def TH3string():
    string = ''
    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Upgrading the town hall will allow you to recieve larger supply ships</div>'
    return string
def TH4string():
    string = '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Upgrading your town hall to level three will set up your colony to be permanent. </div>'
    return string

def toolshopString(int):
    string = ''
    if int == 1:
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += 'Lets you make your own tools in the factory tab</div>'
    else:
        string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
        string += str(int) + '</div>'
    return string
buildingLevels = [
        {"capacity" : 0, "efficiency" : 1},
        { "capacity" : 10, "efficiency" : 1, "work" : 5, "cost" : {"5" : 5, "20" : 0}, "string" : TH2string()},
        { "capacity" : 30, "efficiency" : 1.02, "work" : 15,  "cost" : {"5" : 10, "20" : 4, "21" : 3}, "string" : TH3string()},
        { "capacity" : 30, "efficiency" : 1.02, "work" : 60,  "cost" : {"5" : 20, "20" : 20, "21" : 20}, "string" : TH4string()},
        { "capacity" : 30, "efficiency" : 1.02, "work" : 9999,  "cost" : {"5" : 9999, "20" : 9999, "21" : 9999}, "string" : TH3string()}

]
buildingLevelsT = [
        {"capacity" : 0, "efficiency" : 1},
        { "capacity" : 10, "efficiency" : 1, "work" : 8, "cost" : {"5" : 6, "20" : 5}, "string" : toolshopString(1)},
        { "capacity" : 30, "efficiency" : 1.02, "work" : 150,  "cost" : {"5" : 9999, "20" : 9999, "21" : 9999}, "string" : toolshopString(2)},
        { "capacity" : 30, "efficiency" : 1.02, "work" : 99099,  "cost" : {"5" : 9999, "20" : 9999, "21" : 9999}, "string" : toolshopString(3)}
]


value = buildingLevels[1]['capacity']

def buildingStringUpgrade(typee,currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    buildingString = typee.split(".")[1]
    print("BS ", buildingString)
    building = Building.query.get(buildingMap[buildingString] + offset*buildingOffset)
    if buildingMap[buildingString] == 2:
        bl = buildingLevels
    else:
        bl = buildingLevelsT
    builindgLevel = building.value
    string = ''

    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Current Level: ' + str(building.value)
    string += '</div>'

    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Upgrade Cost:'
    string += '</div>'
    if builindgLevel+1 < len(bl):
        costs = bl[builindgLevel+1]['cost']
        for key in costs:
            if  costs[key] != 0:
                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                string += str(Resource.query.get(str(int(key) + offset*resourceOffset)).name)+'</div><div style="text-align: right;">'
                string +=  str(costs[key]) if builindgLevel+1 < len(bl) else 'Max'
                string +=  '</div></div>'

    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
    string += 'Work</div><div style="text-align: right;">'
    string +=   str(bl[builindgLevel+1]['work']) if builindgLevel+1 < len(bl) else 'Max'
    string +=  '</div></div>'
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    string += '<div class="flexitem" style="text-align: center; width: 100%">'
    string += 'Upgrade Effects:'
    string += '</div>'


    next_level = bl[builindgLevel + 1]
    
    if next_level is not None:
        if 'string' in next_level:
            string += str(next_level['string'])

    return string  

def buildingToString(typee,currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    string = ''

    if typee in buildings.namesToIDs:
        currBuilding = buildings.namesToIDs[typee][0]
        costList = buildings.building_prices[currBuilding]['Cost']
        print("COST LIST ", costList)
        print('Work   ', (user_record,buildings.building_prices[currBuilding]['Work'])) 
        if costList != None:
            string += '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + '</div>'
            for val in costList:
                print("VALLL   ", val)
                string  +=' <div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">' + str(val)
                string += '</div> <div style="text-align: right;">' + str(costList[val]) + '</div></div>'
        string +=    '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Work</div> <div style="text-align: right;">' + str(buildings.building_prices[currBuilding]['Work']) +'</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
    
    
    
    
        if  buildings.building_prices[currBuilding]['Work'] is not None and currBuilding != 'Log_Cabin':
                toolEfficiency, UsingTool, UsingNoTools, NoToolEfficiency, totalEfficiency, count, baseEfficiency, otherFactors, toolName, strength  = buildings.buildingsEff(currBuilding,currUserName) 
                string += '<div class="flexitem" style="text-align: center; width: 100%">'
                string += 'Efficiency Factors</div>'

                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                string += 'Base'
                string += '</div> <div style="text-align: right;">'
                string += str(baseEfficiency)
                string +=  '</div></div>'
                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                string += 'Strength: '
                string += '</div> <div style="text-align: right;">'
                string += str(strength)
                string +=  '</div></div>'
                if toolEfficiency != 0:
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += str(toolName) + '(' + str(UsingTool) +')'
                    string += '</div> <div style="text-align: right;">'
                    string += str(toolEfficiency)
                    string +=  '</div></div>'
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += 'No Tools' + '(' + str(UsingNoTools) +')'
                    string += '</div> <div style="text-align: right;">'
                    string += str(NoToolEfficiency)
                    string +=  '</div></div>'
                string += efficiencyAndCount(totalEfficiency,count)
                print("BREAKING HERE   ",  buildings.building_prices[currBuilding]['Work'] )
                if  buildings.building_prices[currBuilding]['Inputs']:
                    Inputs = buildings.building_prices[currBuilding]['Inputs']
                    first = 0
                    for key in Inputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Input: '
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key] * totalEfficiency * count,2))+ ' '  + str(key)+ ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key]* totalEfficiency * count,2)) + ' '  + str(key) + ' ' 
                            string +=  '</div></div>'
                if  buildings.building_prices[currBuilding]['Outputs']:
                    Outputs = buildings.building_prices[currBuilding]['Outputs']
                    first = 0
                    for key in Outputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Outputs: '
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(key) + ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(key) + ' ' 
                            string +=  '</div></div>'
                string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
            #  if currBuilding.Inputs == {}
        print("BREAKING RIGHT HERE  ", buildings.building_prices[currBuilding])
        print("BREAKING RIGHT HERE  ", buildings.building_prices[currBuilding]['capacity'])

        if buildings.building_prices[currBuilding]['capacity'] != 0:
                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Building Capacity:'
                string += '</div> <div style="text-align: right;">'
                string +=  str(round(buildings.building_prices[currBuilding]['capacity'])) 
                string +=  '</div></div>'   



        string += description(typee,currUserName)


    return string


def description(typee,currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    if typee == 'Log_Cabin':
        string = ''
        sum = round(getattr(user_record, 'Log_Cabin') * buildings.building_prices['Log_Cabin']['capacity'] )
        string +=  '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">' + 'Each '+ 'log cabin' + ' can house ' +  str(buildings.building_prices['Log_Cabin']['capacity']) +  ' people. The ' +  str(getattr(user_record, 'Log_Cabin')) + " " + 'log cabin' + 's currently built house ' + str(sum) + ' citizens' +  '</div>'
        return string
    return ""
def plantedString():
    string = '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">Each 1 crop planted in the spring can be harvested for 1 wheat in the fall. </div>'

    return string