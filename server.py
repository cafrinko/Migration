"""Migration."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import and_, extract, cast, Date

from model import db, connect_to_db, Species, Event, Animal

from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug DebugToolbarExtension

app.secret_key = "ABC"


# Raises an error if undefined variable used in Jinja2, instead of silently failing

app.jinja_env.undefined = StrictUndefined


@app.before_request
def make_session_permanent():
    """Keep a session open past when user closes browser aka session lasts forever."""

    session.permanent = True

@app.route('/animal_data.json')
def get_animal_data():
    """Query database for data to plot in d3."""
    # coordinates = { "type": "Point", "coordinates": [100.0, 0.0]

    # humpbacks = {
    #     humpback.animal_id: {
    #         "id": humpback.animal_id,
    #         "timestamp": humpback.timestamp,
    #         "lng": humpback.long_location,
    #         "lat": humpback.lat_location,
    #     }
    #     for humpback in db.session.query(Event).all()
    # }

    animal_ids = db.session.query(Animal.animal_id).all()

    animals = { "animals": [] }

    for animal_id in animal_ids:
        animal_values = { "animal": [] }
        animal_values["animal"].append(animal_id)
        events = db.session.query(Event.long_location, Event.lat_location).filter(Event.animal_id==animal_id).all()
        positions = []

        for event in events:
            value1 = event.long_location
            value2 = event.lat_location
            values = [value1, value2]
            positions.append(values)

        animal_values["positions"] = positions
        animals["animals"].append(animal_values)

    return jsonify(animals)

    # animal_ids = db.session.query(Animal.animal_id).all()

    # animal_pos_dict = {}

    # for animal_id in animal_ids:
    #     animal_pos_dict["animal_id"] = animal_id
    #     events = db.session.query(Event.long_location, Event.lat_location).filter(Event.animal_id==animal_id).all()
    #     coordinates = []

    #     for event in events:
    #         value1 = event.long_location
    #         value2 = event.lat_location
    #         values = [value1, value2]
    #         coordinates.append(values)

    #     animal_pos_dict["coordinates"] = coordinates

    # return jsonify(animal_pos_dict)

@app.route('/time_data.json')
def get_time_data():

    animal_ids = db.session.query(Animal.animal_id).first()
    animal = animal_ids
    
    # start_time = datetime(2016, 05, 19)
    # end_time = datetime(2016, 05, 20)
    event_list = db.session.query(Event.timestamp).filter(Event.animal_id==animal).all()
    # print timestamp
    # datetime.datetime(2016, 11, 10, 16, 18, 56, 846206)
    # print 'hey', timestamps

    animal_positions = {}

    # for animal_id in animal_ids:
    date = event_list[0].timestamp
    event = db.session.query(Event.long_location, 
                             Event.lat_location).filter(date.month==extract('month', Event.timestamp),
                                                        date.day==extract('day', Event.timestamp),
                                                        Event.animal_id==animal).all()
        
    # if event:
        # print "hi",type(animal)
    animal_coordinate = [event[0].long_location, event[0].lat_location]

    animal_positions[animal] = animal_positions.get(animal, animal_coordinate)

    return jsonify(animal_positions)


@app.route('/')
def index():
    """Homepage, where most of the action happens."""

    return render_template("index.html")

# Page that displays study author credits

@app.route('/credits')
def display_credits():
    """Displays study author credits page."""

    return render_template("credits.html")





if __name__ == "__main__":

    # At point that DebugToolbarExtension invoked, debug has to be set to true

    app.debug = True

    connect_to_db(app)

    # Use DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")