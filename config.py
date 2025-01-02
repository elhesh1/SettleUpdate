from flask import Flask,  render_template
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
import logging

# app = Flask(__name__)
# app.url_map.strict_slashes = False
# CORS(app) 


app = Flask(__name__, template_folder='templates') 
app.url_map.strict_slashes = False
CORS(app)



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  


db = SQLAlchemy(app) 

@app.route('/')
def index():
    return render_template('index.html')
