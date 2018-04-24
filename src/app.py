##
## Author: Randy Burrell
##
## Date: [DATE HERE]
##
## Description: Application with endpoints to get kitty names
##

from flask import Flask, jsonify, request
from models import *
from scraper import *
import os

## Define env var for app
APP_PORT = os.getenv('APP_PORT')
APP_DATA = os.getenv("DATABASE_URL")
IS_APP_DATA = os.getenv('IS_APP_DATA')

## Set the port for app if none has been set
if APP_PORT is None:
    APP_PORT = 3000

## Use locat sqlite db engine if no db env var has been set
if APP_DATA is None:
    APP_DATA = 'sqlite:///kitty_db.sqlite3'

## Init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = APP_DATA
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def create_db():
    '''Creates all database tables'''
    db.create_all()

def load_data():
    '''
        Loads data into database
        TODO: load data from rest of sources
    '''
    data = main()
    for i in data:
        for j in i.find_all('li'):
            name = j.find('span', attrs={'class', 'result-name'})
            if name is None:
                continue
            description = j.find('span', attrs={'class', 'result-desc'}).text.strip()
            kitty = KittyName(name=name.text.strip(), description=description,
                    used=False)
            db.session.add(kitty)
        db.session.commit()
    os.environ['IS_APP_DATA'] = 'True'

# End point to get kitty name
@app.route('/kitty', methods=['get', 'post'])
def kitty_name():
    '''
        Desc: API endpoint for getting a kitty name.
        Accepts: {
            name: required,
            description: optional
        }
        Return: {
            id: kitty_name_id,
            name: kitty_name,
            description: kitty_name_description
        }
        TODO: Stress test endpoint and do other request tests
    '''
    ## Respond according to request method
    if request.method == "GET":
        # Get the first available unused kitty name
        kitty = KittyName.query.filter_by(used=False).first()
        # Send message if none is available
        if kitty is None:
            return jsonify(message='No kitty name found'), 404
        # Send available kitty name object
        return jsonify(name=kitty.name, id=kitty.id,
                       description=kitty.description), 200
    elif request.method == 'POST':
        # Parse request
        json_obj = request.get_json(silent=True)
        # If no kitty name was sent then return message to sender
        if json_obj["name"] is None:
            return jsonify(message='Bad Request'), 400
        # Get kitty name and desc from json object
        name, description = json_obj['name'], json_obj['description']
        # Set description if none has been given
        if description is None:
            description = ''

        # Create a new kitty
        kitty = KittyName(name=name,
                      description=description,
                      used=False)
        # Persist kitty in database
        db.session.add(kitty)
        db.session.commit()
        kitty.save()
        # Retrun message to sender
        return jsonify(message='Saved kitty name'), 201

@app.route('/use_kitty/<int:id>', methods=['POST'])
def use_kitty_name(id):
    # Query db for kitty assigned to id
    kitty = KittyName.query.get(id)
    # Return 404 message if kitty is not found
    if kitty is None:
        return jsonify(message="kitty was not found"), 404
    # Return not acceptable when kitty has already been used
    # note: I'm not sure if this status code is correct
    if kitty.used:
        return jsonify(message="Kitty name has already been used"), 406
    # Make kitty used
    kitty.used = True
    # Save kitty
    db.session.add(kitty)
    db.session.commit()
    # Respond to sender
    return jsonify(message="Completed successfully"), 200

if __name__ == '__main__':
    '''Call database function and exports data to db'''
    with app.app_context():
        create_db()
        # If DATA environment variable has not been set
        # then load data into database from websites
        if IS_APP_DATA is None:
            load_data()
    app.run(port=APP_PORT)

