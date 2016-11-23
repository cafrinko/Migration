"""Migration."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import extract, cast, Date

from model import db, connect_to_db, Species, Event, Animal

from datetime import datetime

from collections import defaultdict

app = Flask(__name__)

# Required to use Flask sessions and the debug DebugToolbarExtension

app.secret_key = "ABC"


# Raises an error if undefined variable used in Jinja2, instead of silently failing

app.jinja_env.undefined = StrictUndefined

@app.before_request
def make_session_permanent():
    """Keep a session open past when user closes browser aka session lasts forever."""

    session.permanent = True

# @app.route('/markermap-form', methods=["POST"])
# def markermap_form_submit():
#     """Submit markermap form."""

#     years = request.form.getlist("year")
#     months = request.form.getlist("month")

#     return redirect('/time_data.json', years=years, months=months)

@app.route('/')
def animals_menu_display():
    """Displays whale id's in a dropdown menu."""

    animal_ids = db.session.query(Animal.animal_id).all()

    return render_template("index.html", animal_ids=animal_ids)

@app.route('/animals_info')
def animals_info_display():
    """Displays whale id's that are links for more info about each whale."""

    animal_ids = db.session.query(Animal.animal_id).all()

    return render_template("animal_ids_display.html", animal_ids=animal_ids)

# @app.route('/animal_path/<animal_id>')
# def 


@app.route('/animal_id/<animal_id>')
def ind_animal_info(animal_id):
    """Displays individual animal info."""

    num_events = db.session.query(Event.timestamp).filter(Event.animal_id==animal_id).count()

    coordinates = db.session.query(Event.long_location, Event.lat_location, Event.timestamp).filter(Event.animal_id==animal_id).all()

    # timestamps = db.session.query(Event.timestamp).filter(Event.animal_id==animal_id).all()

    return render_template("ind_animal_info.html", 
                            animal_id=str(animal_id), 
                            num_events=str(int(num_events)), coordinates=coordinates)

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

    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))

    events = db.session.query(Event.timestamp).filter(extract('year', Event.timestamp)==year,
                                                      extract('month', Event.timestamp)==month,
                                                      extract('day', Event.timestamp)==day).all()

    # animal_positions = {}
    #for each day get all distinct animals
    for event in events:
        month = event[0].month
        day = event[0].day
        year = event[0].year
        date = str(month) + "/" + str(day) + "/" + str(year)
        animal_ids = db.session.query(Event.animal_id).filter(year==extract('year', Event.timestamp),
                                                              month==extract('month', Event.timestamp),
                                                              day==extract('day', Event.timestamp)).distinct().all()
        
        # print animal_ids

        # import pdb
        # pdb.set_trace()
        coordinates = {}
        #for each event's distinct animal get first coordinate
        for animal_id in animal_ids:
            animal = animal_id[0]
            lat_long = db.session.query(Event.long_location, Event.lat_location).filter(year==extract('year', Event.timestamp),
                                                                                        month==extract('month', Event.timestamp),
                                                                                        day==extract('day', Event.timestamp),
                                                                                        Event.animal_id==animal).first()
            coord_pair = [lat_long[0], lat_long[1]]

            if animal not in coordinates:
                coordinates[animal] = coord_pair
            else:
                coordinates[animal].append(coord_pair)

    return jsonify({"coordinates": coordinates.values()})


##Querying by user inputted animal##
    #get all events filtering by year and month

    # year = request.form.get("year")
    # month = request.form.get("month")

    # events = db.session.query(Event.timestamp).filter(extract('year', Event.timestamp)==year,
    #                                                   extract('month', Event.timestamp)==month).all()

    # # import pdb
    # # pdb.set_trace()
                                                
    # # animal_positions = {}
    # #for each month get all distinct animals
    # for event in events:
    #     month = event[0].month
    #     # day = event[0].day
    #     year = event[0].year
    #     date = str(month) + "/" + str(day) + "/" + str(year)
    #     animal_ids = db.session.query(Event.animal_id).filter(year==extract('year', Event.timestamp),
    #                                                           month==extract('month', Event.timestamp)).distinct().all()
        
    #     # print animal_ids

    #     # for each event's distinct animal get all coordinates
    #     for animal_id in animal_ids:
    #         animal = animal_id[0]
    #         lat_longs = db.session.query(Event.long_location, Event.lat_location).filter(year==extract('year', Event.timestamp),
    #                                                                                     month==extract('month', Event.timestamp),
    #                                                                                     Event.animal_id==animal).all()
            
            
    #         coordinates = {}
    #         for lat_long in lat_longs:
    #             coord_pair = [lat_long[0], lat_long[1]]

    #             if animal not in coordinates:
    #                 coordinates[animal] = coord_pair
    #             else:
    #                 coordinates[animal].append(coord_pair)

    # return jsonify({"coordinates": coordinates.values()})
##Querying by user inputted animal##


        # date_string = str(date)

        # coordinates_update = {}
        # for coordinate in coordinates:
        #     coordinates_update.update(coordinate)
        # coordinates = dict(chain(coordinates))
        # coordinate_set = set(coordinates)

        # coordinates = dict(coordinate_set)

        # import pdb
        # pdb.set_trace()

        # animal_update = {}
        # if date_string not in animal_positions:
        #     animal_positions[date_string] = [coordinates]
        # else:
            # make a set of previous and current coordinates
            # animal_positions[date_string].append(coordinates)

    # map(dict, set(map(lambda animal_po: tuple(x.items()), animal_positions)))

            # old_keys = animal_positions[date_string].keys()
            # new_keys = coordinates.keys()
            # list(set().union(old_keys, new_keys))
            # key = date_string
            # value = animal_positions[date_string]
            # set(animal_positions[date_string])
            
        # temp_dict = defaultdict(set)
        # for item in animal_positions[date_string]:
        #     for key, value in item.items():
        #         temp_dict[key].add()
            # import pdb
            # pdb.set_trace()
            # for item in animal_positions[date_string]:
            #     animal_update.update(item)
            #     for key, value in item.iteritems():
            #         animal_defaultdict[key].add[value]

        # for coordinate in animal_positions[date_string]:
        #     for key, value in coordinate.iteritems():
        #         coordinate[key].add[value]

        # animal_positions = defaultdict(set)

        # for animal_position in animal_positions:
        #     for key, value in animal_position.iteritems():
        #         animal
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
    # import pdb
    # pdb.set_trace()



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