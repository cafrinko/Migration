"""Utility file to seed database from CSV data in seed-data"""

from sqlalchemy import func
from model import Species, Event, Animal

from model import connect_to_db, connect_to_db
from server import app
import datetime


def load_species():
    """Load species from u.species into database."""

    print "Species"

    Species.query.delete()

    for row in open('seed_data/u.species'):
        row = row.rstrip()
        species_id, name = row.split('|')

        species = Species(species_id=species_id, name=name)

        db.session.add(species)

    db.session.commit()


def load_events():
    """Load events from u.event into database."""

    print "Events"

    # Delete all rows in table, so if we need to run seed.py multiple times,
    # won't add duplicate events
    Event.query.delete()

    # Read u.event file and insert data
    for row in open("seed_data/u.event"):
        row = row.rstrip()
        row = row.split('|')
        row = row[1:]
        timestamp, long_location, lat_location = row.split('|')

        event = Event(timestamp=timestamp,
                      long_location=long_location,
                      lat_location=lat_location)

        db.session.add(event)

    db.session.commit()


def load_animals():
    """Load animals from u.animal into database."""

    print "animals"

    Animals.query.delete()

    for row in open('seed_data/u.animal'):
        row = row.rstrip()
        species_id, number = row.split('|')

        animal = Animal(species_id=species_id, number=number)

        db.session.add(animal)

    db.session.commit()    


if __name__ == "__main__"
    connect_to_db(app)

    db.create_all()

    load_species()
    load_events()
    load_animals()

