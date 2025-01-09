from static.backend.models import Contact, Resource, Building, CurrentlyBuilding, CurrentlyBuildingNeedWork, user,contactOffset,resourceOffset,buildingOffset,countryOffset
import static.backend.buildings as buildings
import static.backend.citizenActions as citizenActions
import static.backend.country as country
def hoverString(typee,currUserName):
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

jobMap = {'farmer': 1, 'hunter': 2, 'cook': 3, 'logger' : 4, 'butcher' : 11, 'builder' : 15}

def jobString(typee,currUserName):
    offset = user.query.get(currUserName).id
    JobValue = Contact.query.get(jobMap[typee] + offset*contactOffset)
    season = str(Contact.query.get(8 + offset*contactOffset).value)
    baseEfficiency = JobValue.efficiency['e']
    seasonEfficiency = JobValue.efficiency['season'][season]
    strength = Contact.query.get(18 + offset*contactOffset).value * 0.01
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
    offset = user.query.get(currUserName).id
    nFoodTypes = Contact.query.get(17 + offset*contactOffset).value
    health = Contact.query.get(13 + offset*contactOffset).value 
    rationP = Contact.query.get(12 + offset*contactOffset).value
    pop = Contact.query.get(5 + offset*contactOffset).value
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
    offset = user.query.get(currUserName).id
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
    offset = user.query.get(currUserName).id
    string = ''
    print("Offsets    ", resourceOffset, "   ")
    print("Offsets    ", buildings.namesToIDs[typee], "   ", buildingOffset, "  ", offset, " ",buildings.namesToIDs[typee] + buildingOffset*offset )

    if typee in buildings.namesToIDs:
        currBuilding = Building.query.get(buildings.namesToIDs[typee] + buildingOffset*offset)
        costList = currBuilding.cost
        if costList != None:
            string += '<div class="flexitem" id="Cost" style="text-align: center">' + 'Cost:' + '</div>'
            for val in costList:
                string  +=' <div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">' + str(Resource.query.get(int(val) + offset*resourceOffset).name)
                string += '</div> <div style="text-align: right;">' + str(costList[val]) + '</div></div>'
        string +=    '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Work</div> <div style="text-align: right;">' + str(currBuilding.work) +'</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
        if currBuilding.working is not None:
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
                if  currBuilding.Inputs:
                    Inputs = currBuilding.Inputs
                    first = 0
                    for key in Inputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Input: '
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key] * totalEfficiency * count,2))+ ' '  + str(Resource.query.get(int(key) + offset*resourceOffset).name)+ ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string += '-' + str(round(Inputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(int(key) + offset*resourceOffset).name) + ' ' 
                            string +=  '</div></div>'
                if  currBuilding.Outputs:
                    Outputs = currBuilding.Outputs
                    first = 0
                    for key in Outputs:
                        if first == 0:
                            first = 1
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += 'Outputs: '
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(int(key) + offset*resourceOffset).name) + ' ' 
                            string +=  '</div></div>'
                        else:
                            string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                            string += '</div> <div style="text-align: right;">'
                            string +=  str(round(Outputs[key]* totalEfficiency * count,2)) + ' '  + str(Resource.query.get(int(key) + offset*resourceOffset).name) + ' ' 
                            string +=  '</div></div>'
                string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                                # line
            #  if currBuilding.Inputs == {}
        if currBuilding.capacity != 0:
                string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">Building Capacity:'
                string += '</div> <div style="text-align: right;">'
                string +=  str(round(currBuilding.capacity)) 
                string +=  '</div></div>'   



        string += description(typee,currUserName)


    return string


def description(typee,currUserName):
    offset = user.query.get(currUserName).id
    print("This offset:   ", int(buildings.namesToIDs[typee]), "  ", offset, " ", buildingOffset, " ", int(buildings.namesToIDs[typee]) + offset*buildingOffset )
    currBuilding = Building.query.get(int(buildings.namesToIDs[typee]) + offset*buildingOffset)
    if typee == 'LogCabin':
        string = ''
        sum = round(currBuilding.value * currBuilding.capacity)
        string +=  '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">' + 'Each '+ 'log cabin' + ' can house ' +  str(currBuilding.capacity) +  ' people. The ' +  str(currBuilding.value) + " " + 'log cabin' + 's currently built house ' + str(sum) + ' citizens' +  '</div>'
        return string
    return ""
def plantedString():
    string = '<div class="flexitem" id="Cost" style="text-align: left; width: 100%">Each 1 crop planted in the spring can be harvested for 1 wheat in the fall. </div>'

    return string