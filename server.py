"""Migration."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from stock_scraper import get_data
from flask_debugtoolbar import DebugToolbarExtension

from model import Species, Event, Animal, connect_to_db, connect_to_db

app = Flask(__name__)

# Required to use Flask sessions and the debug DebugToolbarExtension

app.secret_key = "ABC"


# Raises an error if undefined variable used in Jinja2, instead of silently failing

app.jinja_env.undefined = StrictUndefined


@app.before_request
def make_session_permanent():
    """Keep a session open past when user closes browser aka session lasts forever."""
    
    session.permanent = True

@app.route('/data.json')
def get_data():
    """Query database for data to plot in d3."""
    events = db.session.query(Event.long_location, Event.lat_location).all()

    coordinates = {}
    i = 1
    for event in events:
        values = [event.long_location, even.lat_location]
        coordinate = {}
        coordinate[i] = values
        coordinates[coordinate] = coordinate
        i += 1

    return jsonify(coordinates)

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

    app.debug = true

    connect_to_db(app)

    # Use DebugToolbar
    DebugToolbarExtension(app)

    app.run()