""" Models for National Parks app """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Park(db.Model):
    """ Information about National Parks """

    __tablename__ = "parks"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    park_code = db.Column(db.String(4), nullable = False, unique = True)
    park_name = db.Column(db.String, nullable = False, unique = True)
    general_info = db.Column(db.Text)
    history = db.Column(db.Text)
    main_attractions = db.Column(db.Text)
    trails = db.Column(db.Text)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)

    favorites = db.relationship("User_Favorite", back_populates = "park")
    wishlists = db.relationship("User_Wishlist", back_populates = "park")


    def __repr__(self):
        """ Show info about park """

        return f'<Park_id = {self.id} Park_name = {self.park_name}>'



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



    


