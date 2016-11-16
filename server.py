"""Migration."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import and_, extract, cast, Date

from model import db, connect_to_db, Species, Event, Animal

from datetime import datetime

from itertools import chain

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

    #get all the animal ids
    # animal_ids = db.session.query(Animal.animal_id).all()
    # print animal_ids
    
    # coordinates = {}
    # for animal_id in animal_ids:
    #     animal = animal_id[0]
    #     events = db.session.query(Event.timestamp).filter(Event.animal_id==animal).limit(500).all()

    #     animal_positions = {}
    #     import pdb
    #     pdb.set_trace()
        # for event in events:
        #     month = event[0].month
        #     day = event[0].day
        #     year = event[0].year
            # date = str(month) + " " + str(day) + ", " + str(year)
            #query database for animal coordinate at this date
            # coordinate = db.session.query(Event.long_location, Event.lat_location).filter(month==extract('month', Event.timestamp), day==extract('day', Event.timestamp), Event.animal_id==animal).first()
            #put coordinate in its own list
            # animal_coordinate = [coordinate[0], coordinate[1]]  
            # if date not in animal_positions:
            #     animal_positions[date] = [[animal, animal_coordinate]]
            # else:
            #     animal_positions[date].append([animal, animal_coordinate])
            # event_dict[animal] = event_dict.get(animal, animal_coordinate)
            # date_list.append(date)

        # for date in date_list:
        # coordinates["coordinates"] = animal_positions
            #need to be able to append multiple animal coordinates to a date

    #get all events

    events = db.session.query(Event.timestamp).filter(extract('year', Event.timestamp)==2016, extract('month', Event.timestamp)==04, extract('day', Event.timestamp)==30).all()

    # import pdb
    # pdb.set_trace()

    animal_positions = {}
    #for each day get all distinct animals
    for event in events:
        month = event[0].month
        day = event[0].day
        year = event[0].year
        date = str(month) + "/" + str(day) + "/" + str(year)
        animal_ids = db.session.query(Event.animal_id).filter(month==extract('month', Event.timestamp), day==extract('day', Event.timestamp)).distinct()
        
        coordinates = {}
        #for each event's distinct animal get first coordinate
        for animal_id in animal_ids:
            animal = animal_id[0]
            coordinate = db.session.query(Event.long_location, Event.lat_location).filter(month==extract('month', Event.timestamp), day==extract('day', Event.timestamp), Event.animal_id==animal).first()
            animal_coordinate = [coordinate[0], coordinate[1]]
            # if animal not in coordinates:
            coordinates[animal] = [animal_coordinate]
            # else:
                # coordinates

        date_string = str(date)

        coordinates_update = {}
        for coordinate in coordinates:
            coordinates_update.update(coordinate)
        # coordinates = dict(chain(coordinates))
        # coordinate_set = set(coordinates)

        # coordinates = dict(coordinate_set)

        import pdb
        pdb.set_trace()

        # if date_string not in animal_positions:
        animal_positions[date_string] = coordinates_update
        # else:
        #     animal_positions[date_string].append(coordinates)
            # if event in animal:
                # print "hi",type(animal)
                #put the coordinates in an animal coordinates variable
    # print timestamp
    # datetime.datetime(2016, 11, 10, 16, 18, 56, 846206)
    # print 'hey', timestamps

    #make an empty dictionary

    # for animal_id in animal_ids:
    #get the first event in the event list for an animal
    #get the coordinates for that animal, only filtering by month and day, not smaller time units
        

    #put the coordinates in the animal positions array for with the animal as the key 
    #if the coordinate isn't already in the dictionary

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