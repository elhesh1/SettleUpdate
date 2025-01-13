
# important building variables ig
LogCabinCapacity = 4

#building prices
building_prices = {
    "Log_Cabin" : {"Work" : 4, "Cost" : {"Wood" : 2}  , "capacity" :  LogCabinCapacity         } ,
    'Town_Hall' : {"Work" : 10000, "Cost" : -1  , "capacity" : 0        },
    'Clay_Pit' : {"Work" : 5, "Cost" : {"Wood" : 1}, "working" : {"value" : 0, "maximum" : 0, "minimum" : 0}  , 
            "tools" : {"None" : 0.5, "With" : ['Iron_Shovel',1], "Base" : 0.1},
            "Inputs" : {}, 
            "Outputs" : {"Clay" : 1} ,
            "capacity" : 5},
    "Mine" : {"Work" : 15, "Cost" : {"Wood" : 4},    "working" : {"value" : 0,  "maximum" : 0, "minimum" : 0},     
            "tools" : {"None" : 0.3, "With" : ['Iron_Pickaxe',1.1], "Base" : 0.1}, 
            "Inputs" : {}, 
            "Outputs" : {"Iron_Ore" : 1}  ,
            "capacity" : 4}, 
    'Kiln' : {"Work" : 3, "Cost" : {"Clay" : 2} ,     "working" : {"value" : 0,  "maximum" : 0, "minimum" : 0},   
            "tools" : {"None" : 1, "Base" : 0.1}, 
            "Inputs" : {"Clay" : 1, "Wood" : 0.2}, 
            "Outputs" : {"Bricks" : 1} ,
            "capacity" : 4}, 
    'Forge' : {"Work" : 2, "Cost" :{"Wood" : 4} ,        "working" : {"value" : 0, "maximum" : 0, "minimum" : 0},  
            "tools" : {"None" : 0.4, "With" : ['Anvil',2],"Base" : 0.1}, 
            "Inputs" : {"Iron_Ore" : 1, "Wood" : 0.3}, 
            "Outputs" : {"Iron" : 1} ,
            "capacity" : 6},
    'Tool_Shop' : {"Work" : 10001, "Cost" : -2 , "capacity" : 0   }
}

#lol this is kind of useless
namesToIDs = {'Log_Cabin' : ['Log_Cabin'], 'Town_Hall' : ['Town_Hall'], 'Clay_Pit' : ['Clay_Pit'], 'Mine' : ['Mine'], 'Kiln' : ['Kiln'], 'Forge' : ['Forge'], 'Tool_Shop' : ['Tool_Shop']}


from static.backend.models import user
from flask import request, jsonify
#from static.backend.variableHelpers import factoryTrades
import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db


def housingCapacity(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()
    logCabinCount = getattr(user_record,'Log_Cabin')
    print('this is important ngl ', logCabinCount , "   ", building_prices['Log_Cabin']['capacity'])
    return logCabinCount * building_prices['Log_Cabin']['capacity']

def reactToBuildings(currUserName):
    print("going to add buildings to my total")
    user_record = db.session.query(user).filter_by(name=currUserName).first()

    setattr(user_record, 'Clay_Pit_Workers_Max', getattr(user_record, 'Clay_Pit') * building_prices['Clay_Pit']['capacity'])
    setattr(user_record, 'Mine_Workers_Max',getattr(user_record, 'Mine')* building_prices['Mine']['capacity'])
    setattr(user_record, 'Kiln_Workers_Max',getattr(user_record,'Kiln' )* building_prices['Kiln']['capacity'])
    setattr(user_record, 'Forge_Workers_Max',getattr(user_record, 'Forge' )* building_prices['Forge']['capacity'])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def buildingsEff(building, currUserName,outputPower=0):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    building_prices[building]

    currentBuilding = building_prices[building]
    strength = round(getattr(user_record, 'Strength')* 0.01,2)
    NoToolEfficiency = currentBuilding['tools']['None']
    count = currentBuilding['working']['value']
    count = getattr(user_record,  building + '_Workers')
    toolEfficiency = 0
    toolMax = 0
    toolName = "THIS SHOULD BE HIDDEN"
    if 'With' in currentBuilding['tools']:

        toolOfNote = currentBuilding['tools']['With']
        toolName = toolOfNote[0]
        toolMax = int(getattr(user_record, toolOfNote[0]))
        toolEfficiency = toolOfNote[1]
    baseEfficiency = currentBuilding['tools']['Base']
    otherFactors = []
    if toolMax >= count:
        UsingTool = count
    else:
        UsingTool = toolMax
    UsingNoTools = int(count - UsingTool)
    if count != 0:
        totalEfficiency = baseEfficiency  * strength * ( ((toolEfficiency * UsingTool)+(NoToolEfficiency*UsingNoTools)) / count )
    else:
        totalEfficiency = baseEfficiency  * toolEfficiency * strength
        if totalEfficiency == 0:
            totalEfficiency = baseEfficiency * NoToolEfficiency * strength
    if outputPower != 0:
        return totalEfficiency * count
    return toolEfficiency, UsingTool, UsingNoTools, NoToolEfficiency, totalEfficiency, count, baseEfficiency, otherFactors, toolName, strength

def advanceBuildings(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 

    buildings = ['Mine', 'Kiln', 'Forge', 'Clay_Pit']

    for buildingCurr in buildings:
        if   building_prices[buildingCurr]['working'] is not None:  ####### Action involving workers
            if  building_prices[buildingCurr]['Inputs']:
                input = building_prices[buildingCurr]['Inputs']
                output = building_prices[buildingCurr]['Outputs']
                buildingPower = buildingsEff(buildingCurr,currUserName, 1)
                for key in input:
                    resource = getattr(user_record, key)
                    ratio = 1
                    if resource  < buildingPower *  input[key]:
                        ratio = resource / (buildingPower*input[key])
                    buildingPower  *=  ratio
                for key in input:
                    resource = getattr(user_record, key)
                    setattr(user_record, key ,resource - buildingPower * input[key])
                for key in output:
                    resource = getattr(user_record, key)
                    setattr(user_record, key ,resource + buildingPower * output[key])
            else:
                if building_prices[buildingCurr]['Outputs']:
                    output = building_prices[buildingCurr]['Outputs']
                    buildingPower = buildingsEff(buildingCurr, currUserName,1)
                    for key in output:
                        resource = getattr(user_record, key)
                        setattr(user_record, key ,resource + buildingPower * output[key])
    db.session.commit()


factoryTrades = [
    
        ['Iron', 1, 'Iron_Hoe', 1],
        ['Iron', 1, 'Iron_Sickle', 1],
        ['Iron', 1, 'Iron_Axe', 1],
        ['Iron', 1, 'Iron_Shovel', 1],
        ['Iron', 1, 'Iron_Pickaxe', 1],
        ['Iron', 4, 'Anvil', 1],
]

def factoryString(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    string = ''
    string = '<div class="country-flex-container" id="factoryFlex"><div class="factoryGrid" id="factoryGrid">'
    factoryLevel = getattr(user_record, 'Tool_Shop')
    string += '<div class="TradeBox">'
    print("factoryLevel", factoryLevel)
    if factoryLevel > 0:

        string += "<table  style='border-collapse: collapse;   font-size: 2vh;>"
        for tradeN in range(len(factoryTrades)):

            string += "<tr style='height: 3vh;'>"
            print("trade", factoryTrades[tradeN])
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][0]).replace("_", " ") +  "</td>"
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][1]) +  "</td>"
            string += "<td style='width: 6vh;'>&#8594;</td>"
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][2]).replace("_", " ") +  "</td>"
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][3]) +  "</td>"
            string += '<td  style="width: 6vh;"><button class="TradeButton" style="width: 80%;" id="FactoryButton' + str(tradeN) + '" >Make</button></td>'
            string += "</tr>"; 
        string += '</table'
    else:
        string += 'You havent built a tool shop yet. You can build one in the buildings (B) tab.</h3>'
    string += '</div>'
    string += '</div></div>'

    return string