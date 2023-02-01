""" CRUD operations """

from model import db, Park, User, User_Favorite, User_Wishlist, connect_to_db

def create_park(park_code, park_name, general_info, history, main_attractions,
                 trails, location_lat, location_long):
    """ Create and return a new park """

    park = Park(park_code = park_code,
                park_name = park_name, 
                general_info = general_info, 
                history = history, 
                main_attractions = main_attractions,
                trails = trails, 
                location_lat = location_lat, 
                location_long = location_long)

    return park



def get_parks():
    """ Return all parks """

    return Park.query.all()



def get_park_by_id(id):
    """ Returns a park with given id """

    return Park.query.get(id)

def get_park_by_name(name):
    """ Returns a park with given name """
    print("Name is ", name)
    return Park.query.filter_by(park_name = name).first()



def get_park_names():
    """ Return the names of all parks """

    parks = Park.query.all()

    park_names = []

    for park in parks:
        park_names.append(park.park_name)
    
    return park_names



def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname = fname, 
                lname = lname, 
                email = email, 
                password = password)

    return user



def get_users():
    """" Return all users """

    return User.query.all()



def get_user_by_id(id):
    """ Returns a user with given id """

    return User.query.get(id)



def get_user_emails():
    """ Return a list of all user emails """

    user_emails = []

    for user in User.query.all():
        user_email = user.email
        user_emails.append(user_email)
    

    return user_emails



def get_user_by_email(email):
    """ Returns a user with given email """

    return User.query.filter_by(email=email).one()




def create_user_favorite(user, park):
    """ Create and return a new park to be added to user's favorites """

    user_favorite = User_Favorite(user = user, 
                                  park = park)

    return user_favorite



def get_favorite_parks_by_user(user_id):
    """ Returns a list of favorite parks for given user """

    user_favs = User_Favorite.query.filter_by(user_id = user_id).all()
    # print(user_favs)

    user_favorites = []
    
    for fav in user_favs:
        user_favorites.append(fav.park)

    # print(user_favorites)
    return user_favorites



def get_user_favorites_by_user(user_id):
    """ Returns a list of user_favorites for a given user """

    user_favs = User_Favorite.query.filter_by(user_id = user_id).all()

    return user_favs



def get_user_favorite_to_be_removed(user_id, park_id):
    """ Returns a park with given park_id from User_Favorites of given user_id """

    park_id = int(park_id)
    user_favs = User_Favorite.query.filter_by(user_id = user_id).all()

    for fav in user_favs:
        if fav.park_id == park_id:
            fav_remove = fav
    
    return fav_remove    



def create_user_wishlist(user, park):
    """ Create and return a new park to be added to user's wishlist """

    user_wishlist = User_Wishlist(user = user,
                                  park = park)
    
    return user_wishlist
    


def get_wishlist_parks_by_user(user_id):
    """ Returns a list of parks in wishlist for given user"""

    user_wish = User_Wishlist.query.filter_by(user_id = user_id).all()

    user_wishlist = []
    
    for wish in user_wish:
        user_wishlist.append(wish.park)

    return user_wishlist



def get_user_wish_to_be_removed(user_id, park_id):
    """ Returns a park with given park_id from User_Wishlist of given user_id """

    park_id = int(park_id)
    user_wishlist = User_Wishlist.query.filter_by(user_id = user_id).all()

    for wish in user_wishlist:
        if wish.park_id == park_id:
            wish_remove = wish
    
    return wish_remove








if __name__ == '__main__':
    from server import app
    connect_to_db(app)