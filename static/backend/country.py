from static.backend.models import user
import static.backend.buildings as buildings
import re
#from static.backend.variableHelpers import factoryTrades
import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
def countryInnerString(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()
    string = '<div class="country-flex-container" id="country-flex-England"><div class="countryTitleRow" id="countryGridEngland">'
    townHall = getattr(user_record, 'Town_Hall')
    townHallLevel =  getattr(user_record, 'Town_Hall') if townHall else 0
    string +=  '<div class="TopLine"></div><h5 class="countryTitle" id="England">England - our overlord </h5>'
    if townHallLevel == 0:
       string += '<h3 class="countryExplanation" id="EnglandExplanation">Since our settlement does not have a town hall, the English are refusing to send us any people or funds</h3>'
    elif townHallLevel > 0:
        supplyTime = getattr(user_record, 'SupplyTime')
        if supplyTime < 1:
            string +='<h3 class="countryExplanation" id="EnglandExplanation">Request supply ship:  </h3>'
            string += '<button class="requestSupply" id="peopleSupply">People</button>'
            string += '<button class="requestSupply" id="toolSupply">Tools</button>'  
            string += '<button class="requestSupply" id="resourceSupply">Resources</button>'

        else: 
            string +='<h3 class="countryExplanation HoverSupply" id="EnglandExplanation">Time until supply ship arrives: '+ str(getattr(user_record, 'SupplyTime')) + ' weeks </h3>'
    else:
        string +='<h3 class="countryExplanation" id="EnglandExplanation">Broken or not implemented yet: </h3>'
    string += '</div></div>'
    return string


initial_countries = [ 
{
    "type" : 'Native',
    "pop": 16000,
    "name": "Pequot",
    "opinion": 5,
    "trades": [['Rifle', 3, 'Bread', 2], ['Rifle',1,'Bow',2], ['Iron_Axe', 1, 'Fur', 1], ['Iron_Sickle', 1, 'Bread', 1]]  # List of lists
}
]


def countryInnerStringNative(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()
    natives = initial_countries
    string = ""
    for native in natives:
        if native['type'] == 'Native':
            cName = native['name']
            string +=  '<div class="country-flex-container" id="country-flex-'+ cName + '"><div class="countryTitleRow" id="countryGrid'+ cName + '">'
            townHall =  getattr(user_record, 'Town_Hall')
            townHallLevel = townHall if townHall else 0
            string +=  '<div class="TopLine"></div><h5 class="countryTitle" id="'+ cName + '">'+ cName + ' - native tribe </h5>'
            if native['trades']:
                string += '<div class="TradeBox">'
                string += '<div class="InnerTradeGrid">' 
                string +='<h3 class="giveTrade" style="text-decoration: underline;">Give</h3>'
                string += '<span class=arrowTrade>&#8594;</span>'
                string +='<h3 class="getTrade"   style="text-decoration: underline;">Receive</h3>' 
                string +=  '</div>'
                number = 0
                for trade in native['trades']:
                    number += 1
                    string += '<div class="InnerTradeGrid">'        
                    string +='<h3 class="giveTrade"">' +  str(trade[1]) + ' ' + str(trade[0])  + '</h3>'
                    string += '<span class=arrowTrade>&#8594;</span>'
                    string +='<h3 class="getTrade"">' + str(trade[3])  + ' ' +  str(trade[2]) +   '</h3>'
                    string += '<button class="TradeButton" id="TradeButton' + cName + str(number) + '" >Trade</button>'
                    string +=  '</div>'
                string += '</div></div>'
            string +=  '</div>'
            
        string += '</div>'

    return string

def advance(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()
    if getattr(user_record, "Town_Hall")> 0:
        supplyTime = getattr(user_record, 'SupplyTime')
        supplyTime -= 1
        setattr(user_record,'SupplyTime', supplyTime)
        if supplyTime == 0:        ####### gives you the supply stuff
            typeeNumber = getattr(user_record,'SupplyShipType')
            if typeeNumber == 3:
                typee = 'resourceSupply'
            elif typeeNumber == 2:
                typee = 'toolSupply' 
            else:
                typee = 'peopleSupply'
            supplyShipsGiven = getattr(user_record,'SupplyShipsGiven')
            gives = supplyShipIns[supplyShipsGiven][typee]
            for key in gives:
                setattr(user_record, key, getattr(user_record,key) + gives[key] )

            people = getattr(user_record, 'Population')
            setattr(user_record,'Population', people + supplyShipIns[supplyShipsGiven][typee]['People'] )
            avaliable = getattr(user_record, 'Available_value')
            setattr(user_record,'Available_value', avaliable + supplyShipIns[supplyShipsGiven][typee]['People'] )
            setattr(user_record, 'People' , 0)


            if getattr(user_record, 'Town_Hall') > 1:
                setattr(user_record,'SupplyShipsGiven',1)
    db.session.commit()
            



supplyShipIns = {0 :   { 'time' : 4, 'resourceSupply' : {'People' : 20, 'Bread' : 5, 'Cooked_Meat' : 5, 'Vegetables' : 5, 'Clay':2, 'Iron_Ore':2, 'Iron_Hoe' : 2, 'Iron_Sickle' : 2, 'Iron_Axe' : 2, 'Rifle':1,'Bow':2,'Iron_Shovel':3,'Iron_Pickaxe':4},  'peopleSupply' : {'People' : 50, 'Bread' : 1, 'Cooked_Meat' : 1, 'Vegetables' : 1, 'Iron_Hoe' : 1, 'Iron_Sickle' : 1, 'Iron_Axe' : 1, 'Bow':2,'Iron_Shovel':2,'Iron_Pickaxe':2}, 'toolSupply': {'People' : 20, 'Bread' : 1, 'Cooked_Meat' : 1, 'Vegetables' : 2, 'Iron_Hoe' : 4, 'Iron_Sickle' : 4, 'Iron_Axe' : 4, 'Rifle':6,'Bow':4,'Iron_Shovel':5,'Iron_Pickaxe':5}},
                 1 : { 'time' : 6 , 'resourceSupply' : {'People' : 40, 'Bread' : 8, 'Cooked_Meat' : 8, 'Vegetables' : 8, 'Clay':4, 'Iron_Ore':4, 'Iron_Hoe' : 4, 'Iron_Sickle' : 4, 'Iron_Axe' : 4, 'Rifle':2,'Bow':4,'Iron_Shovel':5,'Iron_Pickaxe':6},  'peopleSupply' : {'People' : 100, 'Bread' : 2, 'Cooked_Meat' : 2, 'Vegetables' : 2, 'Iron_Hoe' : 2, 'Iron_Sickle' : 2, 'Iron_Axe' : 3, 'Bow':3,'Iron_Shovel':3,'Iron_Pickaxe':3}, 'toolSupply': {'People' : 40, 'Bread' : 2, 'Cooked_Meat' : 2, 'Vegetables' : 4, 'Iron_Hoe' : 8, 'Iron_Sickle' : 6, 'Iron_Axe' : 8, 'Rifle':10,'Bow':8,'Iron_Shovel':10,'Iron_Pickaxe':12}}}

def supplyString(typee,currUserName):
    string = ''
    string += supplyStringFlesh(typee,currUserName)
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line

    return string
def supplyStringFlesh(typee,currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()

    offset = user.query.get(currUserName).id
    supplyShipsGiven = getattr(user_record,'SupplyShipsGiven') 
    string = ''
    if supplyShipsGiven in supplyShipIns:
        gives = supplyShipIns[supplyShipsGiven][typee]
        for key in gives:
                    string += '<div class="flexitem" style="display: flex; justify-content: space-between; width: 100%;"><div style="text-align: left; ">'
                    string += str(key)
                    string += '</div> <div style="text-align: right;">'
                    string += str(gives[key])
                    string +=  '</div></div>'
        string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' # line
    return string



def supplyToolTip(currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()

    offset = user.query.get(currUserName).id
    typeeNumber = getattr(user_record, 'SupplyShipType')
    if typeeNumber == 3:
         typee = 'resourceSupply'
    elif typeeNumber == 2:
         typee = 'toolSupply'
    else:
         typee = 'peopleSupply'
    string = ''
    string += supplyStringFlesh(typee)
    
    return string
def split_string(data):
    letters = ''.join(re.findall(r'[a-zA-Z]', data))
    numbers = ''.join(re.findall(r'[0-9]', data))
    return letters, int(numbers)


def trade(data, currUserName):
    user_record = db.session.query(user).filter_by(name=currUserName).first()
    name, number = split_string(data['buttonName'])
    print(" TRADEING ", name, "  ", number)

    if name == 'FactoryButton':
        input = getattr(user_record,buildings.factoryTrades[number][0] )
        output = getattr(user_record,buildings.factoryTrades[number][2] )
        if input >= float(buildings.factoryTrades[number][1]):
            setattr(user_record,buildings.factoryTrades[number][0], input - buildings.factoryTrades[number][1])
            setattr(user_record,buildings.factoryTrades[number][2] , output +  buildings.factoryTrades[number][3])
            db.session.commit()
    else:
        if name == 'Pequot':
            country = initial_countries[0]
        trade = country['trades'][int(number-1)]
        input = getattr(user_record,  trade[0] )
        output = getattr(user_record,  trade[2] )
        if input >= float(trade[1]):
            input -= trade[1]
            setattr( user_record,trade[0], input )
            output += trade[3]
            setattr( user_record,trade[2], output )

            db.session.commit()

