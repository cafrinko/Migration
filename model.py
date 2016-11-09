"""Models and database functions for Migration project."""

from flask_sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

#connection to postgresql database, where session object lives
db = SQLAlchemy()

####################################################################

# Model definitions


class Species(db.Model):
    """Species type among all tracked cohorts in this project."""

    __tablename__ = "species"

    species_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Species species_id=%s name=%s>"
        return s % (self.species_id, self.name)


class Animal(db.Model):
    """Individual animal in tracked cohort."""

    __tablename__ = "animals"

    animal_id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.String(50), db.ForeignKey('species.species_id'))

    species = db.relationship('Species', backref="animal")

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Animal animal_id=%s species_id=%s event_id=%s number=%s>"
        return s % (self.animal_id, self.species_id, self.event_id, self.number)


class Event(db.Model):
    """Time and location recording of an animal."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.animal_id'))
    timestamp = db.Column(db.DateTime, nullable=False)
    long_location = db.Column(db.Float(3), nullable=False)
    lat_location = db.Column(db.Float(3), nullable=False)

    animal = db.relationship('Animal', backref="animal")

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Event event_id=%s animal_id=%s timestamp_id=%s x_location=%s y_location=%s>"
        return s % (self.event_id, self.animal_id, self.timestamp, self.x_location, self.y_location)


##########################################################################################3###########

# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///migration'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    # If interactively run module, can work with database directly

    from server import app
    connect_to_db(app)
    print "Connected to DB."