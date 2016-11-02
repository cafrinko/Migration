"""Utility file to seed database from CSV data in seed-data"""

from sqlalchemy import func
from model import Species, Event, Animal

from model import connect_to_db, db
from server import app
from datetime import datetime


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

def load_animals():
    """Load animals from u.animal into database."""

    print "animals"

    Animal.query.delete()

    for row in open('seed_data/u.animal'):
        row = row.rstrip()
        animal_id, species_id = row.split('|')

        animal_id = int(animal_id)

        animal = Animal(animal_id=animal_id, species_id=species_id)

        db.session.add(animal)

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
        # row = row.split('|')
        # row = row[1:]

        animal_id, time, long_location, lat_location = row.split('|')

        timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        long_location = float(long_location)
        lat_location = float(lat_location)

        event = Event(animal_id=animal_id,
                      timestamp=timestamp,
                      long_location=long_location,
                      lat_location=lat_location)

        db.session.add(event)

    db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_species()
    load_animals()
    load_events()

