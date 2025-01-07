from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY,JSON

from static.backend.variableHelpers import DEFAULT_VALUES
import sys
import os
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, two_levels_up)
from config import app, db
# contactOffset = len(initial_variables) 
# resourceOffset = len(initial_resources) 
# buildingOffset = len(initial_buildings) 
# countryOffset = len(initial_countries) 



class user(db.Model):
    name = db.Column(db.String, primary_key=True)
    id = db.Column(db.Integer, unique=True)

    Farmer_value = db.Column(db.Integer, nullable=False) 
    Farmer_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Farmer_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Farmer_type = db.Column(db.String, nullable=True)
    Farmer_efficiency = db.Column(db.JSON, nullable=True)

    # Hunter Fields
    Hunter_value = db.Column(db.Integer, nullable=False)
    Hunter_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Hunter_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Hunter_type = db.Column(db.String, nullable=True)
    Hunter_efficiency = db.Column(db.JSON, nullable=True)

    # Baker Fields
    Baker_value = db.Column(db.Integer, nullable=False)
    Baker_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Baker_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Baker_type = db.Column(db.String, nullable=True)
    Baker_efficiency = db.Column(db.JSON, nullable=True)

    # Butcher Fields
    Butcher_value = db.Column(db.Integer, nullable=False)
    Butcher_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Butcher_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Butcher_type = db.Column(db.String, nullable=True)
    Butcher_efficiency = db.Column(db.JSON, nullable=True)

    # Logger Fields
    Logger_value = db.Column(db.Integer, nullable=False)
    Logger_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Logger_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Logger_type = db.Column(db.String, nullable=True)
    Logger_efficiency = db.Column(db.JSON, nullable=True)

    # Builder Fields
    Builder_value = db.Column(db.Integer, nullable=False)
    Builder_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Builder_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Builder_type = db.Column(db.String, nullable=True)
    Builder_efficiency = db.Column(db.JSON, nullable=True)

    # Available Fields
    Available_value = db.Column(db.Integer, nullable=False)
    Available_maximum = db.Column(db.Integer, nullable=False, default=2147483646)
    Available_minimum = db.Column(db.Integer, nullable=False, default=-2147483646)
    Available_type = db.Column(db.String, nullable=True)
    Available_efficiency = db.Column(db.JSON, nullable=True)

    job_modifier = db.Column(db.Integer,nullable=False, default = 1)

    week = db.Column(db.Integer, nullable =False, default = 1)
    season = db.Column(db.Integer, nullable =False, default = 1)
    year = db.Column(db.Integer, nullable =False, default = 1620)

    Wheat = db.Column(db.Integer, nullable = False, default = 0)
    Fur = db.Column(db.Integer, nullable=False, default=0)
    Raw_Meat = db.Column(db.Integer, nullable=False, default=0)
    Wood = db.Column(db.Integer, nullable=False, default=0)
    Bread = db.Column(db.Integer, nullable=False, default=0)
    Cooked_Meat = db.Column(db.Integer, nullable=False, default=0)
    Wild_Berries = db.Column(db.Integer, nullable=False, default=0)
    Vegetables = db.Column(db.Integer, nullable=False, default=0)
    Iron_Hoe = db.Column(db.Integer, nullable=False, default=0)
    Iron_Sickle = db.Column(db.Integer, nullable=False, default=0)
    Iron_Axe = db.Column(db.Integer, nullable=False, default=0)
    Rifle = db.Column(db.Integer, nullable=False, default=0)
    Bow = db.Column(db.Integer, nullable=False, default=0)
    Iron_Shovel = db.Column(db.Integer, nullable=False, default=0)
    Iron_Pickaxe = db.Column(db.Integer, nullable=False, default=0)
    Clay = db.Column(db.Integer, nullable=False, default=0)
    Iron_Ore = db.Column(db.Integer, nullable=False, default=0)
    People = db.Column(db.Integer, nullable=False, default=0)
    Bricks = db.Column(db.Integer, nullable=False, default=0)
    Iron = db.Column(db.Integer, nullable=False, default=0)
    Anvil = db.Column(db.Integer, nullable=False, default=0)
    
    Planted = db.Column(db.Integer, nullable=False, default=0)
    RationP = db.Column(db.Integer, nullable=False, default=0)
    Health = db.Column(db.Integer, nullable=False, default=0)
    Strength = db.Column(db.Integer, nullable=False, default=0)
    SupplyTime = db.Column(db.Integer, nullable=False, default=0)
    SupplyShipsGiven = db.Column(db.Integer, nullable=False, default=0)
    SupplyShipType = db.Column(db.Integer, nullable=False, default=0)
    Population = db.Column(db.Integer, nullable=False, default=0)
    numberofFoods = db.Column(db.Integer, nullable=False, default=0)


    Log_Cabin = db.Column(db.Integer, nullable=False, default=0)
    Town_Hall = db.Column(db.Integer, nullable=False, default=0)
    Clay_Pit = db.Column(db.Integer, nullable=False, default=0)
    Mine = db.Column(db.Integer, nullable=False, default=0)
    Kiln = db.Column(db.Integer, nullable=False, default=0)
    Forge = db.Column(db.Integer, nullable=False, default=0)
    Tool_Shop = db.Column(db.Integer, nullable=False, default=0)

    Clay_Pit_Workers = db.Column(db.Integer, nullable=False, default=0)
    Clay_Pit_Workers_Max = db.Column(db.Integer, nullable=False, default=0)
    Mine_Workers = db.Column(db.Integer, nullable=False, default=0)
    Mine_Workers_Max = db.Column(db.Integer, nullable=False, default=0)
    Kiln_Workers = db.Column(db.Integer, nullable=False, default=0)
    Kiln_Workers_Max = db.Column(db.Integer, nullable=False, default=0)
    Forge_Workers = db.Column(db.Integer, nullable=False, default=0)
    Forge_Workers_Max = db.Column(db.Integer, nullable=False, default=0)

    building_queue =  Column(db.String, nullable=True)
    currently_building_queue =  Column(db.String, nullable=True)

    def to_json(self):
        return {
            "name" : self.name,
            "id" : self.id,
            "Planted" : self.Planted,
            "RationP" : self.RationP,
            "Health" : self.Health,
            "Strength" : self.Strength,
            "SupplyTime" : self.SupplyTime,
            "SupplyShipsGiven" : self.SupplyShipsGiven,
            "SupplyShipsType" : self.SupplyShipType,
            "Population" : self.Population,
            "numberofFoods" : self.numberofFoods ,



            "Time" : {
            "week" : self.week,
            "season" : self.season,
            "year" : self.year,
            },
            

            "Resources": {
                "Wheat": self.Wheat,
                "Fur": self.Fur,
                "Raw_Meat": self.Raw_Meat,
                "Wood": self.Wood,
                "Bread": self.Bread,
                "Cooked_Meat": self.Cooked_Meat,
                "Wild_Berries": self.Wild_Berries,
                "Vegetables": self.Vegetables,
                "Iron_Hoe": self.Iron_Hoe,
                "Iron_Sickle": self.Iron_Sickle,
                "Iron_Axe": self.Iron_Axe,
                "Rifle": self.Rifle,
                "Bow": self.Bow,
                "Iron_Shovel": self.Iron_Shovel,
                "Iron_Pickaxe": self.Iron_Pickaxe,
                "Clay": self.Clay,
                "Iron_Ore": self.Iron_Ore,
                "People": self.People,
                "Bricks": self.Bricks,
                "Iron": self.Iron,
                "Anvil": self.Anvil
            },

            "Farmer": {
                "Farmer_value": self.Farmer_value,
                "Farmer_maximum": self.Farmer_maximum,
                "Farmer_minimum": self.Farmer_minimum,
                "Farmer_type": self.Farmer_type,
                "Farmer_efficiency": self.Farmer_efficiency
            },
            "Hunter": {
                "Hunter_value": self.Hunter_value,
                "Hunter_maximum": self.Hunter_maximum,
                "Hunter_minimum": self.Hunter_minimum,
                "Hunter_type": self.Hunter_type,
                "Hunter_efficiency": self.Hunter_efficiency
            },
            "Baker": {
                "Baker_value": self.Baker_value,
                "Baker_maximum": self.Baker_maximum,
                "Baker_minimum": self.Baker_minimum,
                "Baker_type": self.Baker_type,
                "Baker_efficiency": self.Baker_efficiency
            },
            "Butcher": {
                "Butcher_value": self.Butcher_value,
                "Butcher_maximum": self.Butcher_maximum,
                "Butcher_minimum": self.Butcher_minimum,
                "Butcher_type": self.Butcher_type,
                "Butcher_efficiency": self.Butcher_efficiency
            },
            "Logger": {
                "Logger_value": self.Logger_value,
                "Logger_maximum": self.Logger_maximum,
                "Logger_minimum": self.Logger_minimum,
                "Logger_type": self.Logger_type,
                "Logger_efficiency": self.Logger_efficiency
            },
            "Builder": {
                "Builder_value": self.Builder_value,
                "Builder_maximum": self.Builder_maximum,
                "Builder_minimum": self.Builder_minimum,
                "Builder_type": self.Builder_type,
                "Builder_efficiency": self.Builder_efficiency
            },
            "Available": {
                "Available_value": self.Available_value,
                "Available_maximum": self.Available_maximum,
                "Available_minimum": self.Available_minimum,
                "Available_type": self.Available_type,
                "Available_efficiency": self.Available_efficiency
            },
            'job_modifier' : self.job_modifier,

            "Buildings" : {
                "Log_Cabin" : self.Log_Cabin,
                "Town_Hall" : self.Town_Hall,
                "Clay_Pit" : self.Clay_Pit,
                "Mine" : self.Mine,
                "Kiln" : self.Kiln,
                "Forge" : self.Forge,
                "Tool_Shop" : self.Tool_Shop,
                "Clay_Pit_Workers" : self.Clay_Pit_Workers,
                "Clay_Pit_Workers_Max" : self.Clay_Pit_Workers_Max,
                "Mine_Workers" : self.Mine_Workers,
                "Mine_Workers_Max" : self.Mine_Workers_Max,
                "Kiln_Workers" : self.Kiln_Workers,
                "Kiln_Workers_Max" : self.Kiln_Workers_Max,
                "Forge_Workers" : self.Forge_Workers,
                "Forge_Workers_Max" : self.Forge_Workers_Max
            },
            "building_queue" : self.building_queue,
            "currently_building_queue" : self.currently_building_queue
        }
    


