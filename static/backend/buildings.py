
# important building variables ig
LogCabinCapacity = 4

#building prices
building_prices = {
    "Log_Cabin" : {"Work" : 2, "Cost" : {"Wood" : 2}  , "capacity" :  LogCabinCapacity         } ,
    'Town_Hall' : {"Work" : 0, "Cost" : -1  , "capacity" : 0        },
    'Clay_Pit' : {"Work" : 5, "Cost" : {"Wood" : 1}, "working" : {"value" : 0, "maximum" : 0, "minimum" : 0}  , 
            "tools" : {"None" : 0.5, "With" : ['Iron_Shovel',1], "Base" : 0.1},
            "Inputs" : {}, 
            "Outputs" : {"17" : 1} ,
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
    'Tool_Shop' : {"Work" : 0, "Cost" : -1 , "capacity" : 0   }
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
    return logCabinCount * LogCabinCapacity

def reactToBuildings(buildingsBuiltThisWeek,currUserName):
    print("going to add buildings to my total")
    # for key in buildingsBuiltThisWeek:
    #     CurrentlyBuilding = Building.query.get(key)
    #     if CurrentlyBuilding.working is not None:
    #         cpw = CurrentlyBuilding.working
    #         maximum = CurrentlyBuilding.value * CurrentlyBuilding.capacity
    #         CurrentlyBuilding.working =  {'value': int(cpw['value']), 'maximum': int(maximum), 'minimum': int(cpw['minimum'])}
    #         db.session.add(CurrentlyBuilding)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def buildingsEff(building, currUserName,outputPower=0):
    user_record = db.session.query(user).filter_by(name=currUserName).first() 
    building_prices[building]

    print("IS THIS THE MAP BRO  ", building_prices[building])
    currentBuilding = building_prices[building]
    strength = round(getattr(user_record, 'Strength')* 0.01,2)
    NoToolEfficiency = currentBuilding['tools']['None']
    count = currentBuilding['working']['value']
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
    offset = user.query.get(currUserName).id
    buildings = Building.query.filter_by(currUserName=currUserName).all()
    print("CURRENT BUILDINGS : ", buildings)
    for buildingCurr in buildings:
        if buildingCurr.working is not None:  ####### Action involving workers
            print(" THIS BUIDLING HAS WORKERS FR?  ", buildingCurr)
            if  buildingCurr.Inputs:
                input = buildingCurr.Inputs
                output = buildingCurr.Outputs
                buildingPower = buildingsEff(buildingCurr,currUserName, 1)
                for key in input:
                    print("BUDILNGIN DUBULINDIN BUDILING INPUTS   ;  ", input, "  ", output, "  ", buildingPower)
                    print("rescourse key : ", int(key), " ", offset, " ", resourceOffset, " ", int(key) + offset*resourceOffset)

                    resource = Resource.query.get(int(key) + offset*resourceOffset)
                    ratio = 1
                    if resource.value  < buildingPower *  input[key]:
                        ratio = resource.value / (buildingPower*input[key])
                    buildingPower  *=  ratio
                for key in input:
                    resource = Resource.query.get(int(key)+ offset*resourceOffset)
                    resource.value -= buildingPower * input[key]

                for key in output:
                    resource = Resource.query.get(int(key)+ offset*resourceOffset)
                    resource.value += buildingPower * output[key]

            else:
                if buildingCurr.Outputs:
                    output = buildingCurr.Outputs
                    buildingPower = buildingsEff(buildingCurr, currUserName,1)
                    for key in output:
                        resource = Resource.query.get(int(key) + offset*resourceOffset)
                        resource.value += buildingPower * output[key]
def factoryString(currUserName):
    offset = user.query.get(currUserName).id
    string = ''
    string = '<div class="country-flex-container" id="factoryFlex"><div class="factoryGrid" id="factoryGrid">'
    factoryLevel = Building.query.get(7 + offset*buildingOffset).value
    string += '<div class="TradeBox">'
    print("factoryLevel", factoryLevel)
    if factoryLevel > 0:

        string += "<table  style='border-collapse: collapse;   font-size: 2vh;>"
        for tradeN in range(len(factoryTrades)):
            string += "<tr style='height: 3vh;'>"
            print("trade", factoryTrades[tradeN])
            string += "<td style='width: 6vh;'>" + Resource.query.get(factoryTrades[tradeN][0] + offset*resourceOffset).name +  "</td>"
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][1]) +  "</td>"
            string += "<td style='width: 6vh;'>&#8594;</td>"
            string += "<td style='width: 6vh;'>" + Resource.query.get(factoryTrades[tradeN][2] + offset*resourceOffset).name +  "</td>"
            string += "<td style='width: 6vh;'>" + str(factoryTrades[tradeN][3]) +  "</td>"
            string += '<td  style="width: 6vh;"><button class="TradeButton" style="width: 80%;" id="FactoryButton' + str(tradeN) + '" >Make</button></td>'
            string += "</tr>"; 
        string += '</table'
    else:
        string += 'You havent built a factory yet</h3>'
    string += '</div>'
    string += '</div></div>'

    return string