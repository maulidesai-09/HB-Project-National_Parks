""" Models for National Parks app """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Park(db.Model):
    """ Information about National Parks """

    __tablename__ = "parks"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    park_code = db.Column(db.String, nullable = False, unique = True)
    park_name = db.Column(db.String, nullable = False, unique = True)
    general_info = db.Column(db.Text)
    history = db.Column(db.Text)
    main_attractions = db.Column(db.Text)
    trails = db.Column(db.Text)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)

    favorites = db.relationship("User_Favorite", back_populates = "park")
    wishlists = db.relationship("User_Wishlist", back_populates = "park")
    states = db.relationship("Park_State", back_populates = "park")
    activities = db.relationship("Park_Activity", back_populates = "park")
    topics = db.relationship("Park_Topic", back_populates = "park")


    def __repr__(self):
        """ Show info about park """

        return f'<Park_id = {self.id} Park_name = {self.park_name}>'



class Park_State(db.Model):
    """ Information about states for each park """

    __tablename__ = "park_states"

    park_state_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))
    # park_name = db.Column(db.String, db.ForeignKey("parks.park_name"))
    state_code = db.Column(db.String, nullable = False)
    state_name = db.Column(db.String, nullable = False)

    park = db.relationship("Park", back_populates = "states")

    def __repr__(self):
        """ Show info about park_state"""

        return f'<park_state_id = {self.park_state_id} park_id = {self.park_id} state_code = {self.state_code}>'



class Park_Activity(db.Model):
    """Information about activities in each park """

    __tablename__ = "park_activities"

    park_activity_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))
    activity = db.Column(db.String, nullable = False)

    park = db.relationship("Park", back_populates = "activities")

    def __repr__(self):
        """ Show info about park_activity """

        return f'<park_activity_id = {self.park_activity_id} park_id = {self.park_id} activity = {self.activity}>'



class Park_Topic(db.Model):
    """ Information about topics for each park """

    __tablename__ = "park_topics"

    park_topic_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))
    topic = db.Column(db.String, nullable = False)

    park = db.relationship("Park", back_populates = "topics")

    def __repr__(self):
        """ Show info about park_topic """

        return f'<park_topic_id = {self.park_topic_id} park_id = {self.park_id} activity = {self.topic}>'



class User(db.Model):
    """ Infofrmation about Users """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    favorites = db.relationship("User_Favorite", back_populates = "user")
    wishlists = db.relationship("User_Wishlist", back_populates = "user")


    def __repr__(self):
        """ Show info about a user"""

        return f'<User_id = {self.user_id} User_Name = {self.fname} {self.lname}>'



class User_Favorite(db.Model):
    """ Information about parks added to user's favorites """

    __tablename__ = "user_favorites"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))

    user = db.relationship("User", back_populates="favorites")
    park = db.relationship("Park", back_populates="favorites")

    def __repr__(self):
        """ Show info about park added to user's favorites """

        return f'<User_favorite id = {self.id} User_id = {self.user_id} Park_id = {self.park.id}>'



class User_Wishlist(db.Model):
    """ Information about parks added to user's wishlist """

    __tablename__ = "user_wishlist"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))

    user = db.relationship("User", back_populates = "wishlists")
    park = db.relationship("Park", back_populates = "wishlists")

    def __repr__(self):
        """ Show info about park added to user's wishlist """

        return f'<User_wishlist id = {self.id} User_id = {self.user_id} Park_id = {self.park_id}>'
    

    
def connect_to_db(flask_app, db_uri="postgresql:///parks", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)



    


