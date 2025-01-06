
# important building variables ig
LogCabinCapacity = 4

from static.backend.models import user
from flask import request, jsonify
#from static.backend.variableHelpers import factoryTrades
import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
namesToIDs = {'LogCabin' : 1, 'TownHall' : 2, 'ClayPit' : 3, 'Mine' : 4, 'Kiln' : 5, 'Forge' : 6, 'ToolShop' : 7}





def housingCapacity(currUserName):
    offset = user.query.get(currUserName).id
    logCabin = Building.query.get(1 + offset*buildingOffset)
    return logCabin.value * logCabin.capacity

def reactToBuildings(buildingsBuiltThisWeek,currUserName):
    offset = user.query.get(currUserName).id
    for key in buildingsBuiltThisWeek:
        CurrentlyBuilding = Building.query.get(key)
        if CurrentlyBuilding.working is not None:
            cpw = CurrentlyBuilding.working
            maximum = CurrentlyBuilding.value * CurrentlyBuilding.capacity
            CurrentlyBuilding.working =  {'value': int(cpw['value']), 'maximum': int(maximum), 'minimum': int(cpw['minimum'])}
            db.session.add(CurrentlyBuilding)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def buildingsEff(building, currUserName,outputPower=0):
    offset = user.query.get(currUserName).id
    strength = round(Contact.query.get(18 + offset*contactOffset).value * 0.01,2)
    NoToolEfficiency = building.tools['None']
    count = building.working['value']
    toolEfficiency = 0
    toolMax = 0
    toolName = "THIS SHOULD BE HIDDEN"
    if 'With' in building.tools:

        toolOfNote = building.tools['With']
        tool = (Resource.query.get(toolOfNote[0] + offset*resourceOffset)) 
        toolName = tool.name
        toolMax = int(tool.value)
        toolEfficiency = toolOfNote[1]
    baseEfficiency = building.tools['Base']
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