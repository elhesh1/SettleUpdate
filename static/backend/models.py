from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, func

#from static.backend.variableHelpers import initial_variables, initial_resources, initial_buildings, initial_countries
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
    def to_json(self):
        return {
            "name" : self.name,
            "id" : self.id
        }