""" CRUD operations """

from model import db, Park, Park_State, Park_Activity, Park_Topic, User, User_Favorite, User_Wishlist, User_Trip, Trip_Attraction, Review_Comment, connect_to_db
from datetime import datetime

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

    id = int(id)

    return Park.query.get(id)

def get_park_by_name(name):
    """ Returns a park with given name """

    return Park.query.filter_by(park_name = name).first()



def get_park_names():
    """ Return the names of all parks """

    parks = Park.query.all()

    park_names = []

    for park in parks:
        park_names.append(park.park_name)
    
    return park_names



def get_park_code_by_id(id):
    """ Return a park code for the park with given park id """

    id = int(id)
    parks = Park.query.all()

    park_code = None

    for park in parks:
        if park.id == id:
            park_code = park.park_code

    return park_code


def create_park_state(park, state_code, state_name):
    """ Create the data for states for each park """

    park_state = Park_State(park = park, 
                            state_code = state_code,
                            state_name = state_name)
    
    return park_state



def get_all_park_states():
    """ Returns a list of all park_states objects """

    return Park_State.query.all()



def get_all_states_names():
    """ Returns a list of all states """

    park_states = Park_State.query.all()

    all_states = []

    for park in park_states:
        if not park.state_name in all_states:
            all_states.append(park.state_name)
    

    all_states = sorted(all_states)
    
    return all_states



def create_park_activity(park, activity):
    """ Create the data for activities for each park """

    park_activity = Park_Activity(park = park,
                                  activity = activity)
    
    return park_activity



def get_all_activities():
    """ Returns a list of all activities """

    parks_activities = Park_Activity.query.all()
    all_activities = []

    for park in parks_activities:
        if not park.activity in all_activities:
            all_activities.append(park.activity)
    
    all_activities = sorted(all_activities)
    
    return all_activities



def create_park_topic(park, topic):
    """ Create the data for topics for each park """

    park_topic = Park_Topic(park = park,
                            topic = topic)
    
    return park_topic



def get_all_topics():
    """ Returns a list of all topics """

    park_topics = Park_Topic.query.all()
    all_topics = []

    for park in park_topics:
        if not park.topic in all_topics:
            all_topics.append(park.topic)
    
    all_topics = sorted(all_topics)

    return all_topics



def get_matching_parks(state_name, activities, topics):
    """" Returns parks that match the given state, activities, topics """

    all_filters = []
    if state_name != "":
        all_filters.append(Park_State.state_name == state_name)
    if len(activities) > 0:
        all_filters.append(Park_Activity.activity.in_(activities))
    if len(topics) > 0:
        all_filters.append(Park_Topic.topic.in_(topics))
        

    all_parks = (db.session.query(Park)
                 .join(Park_State)
                 .join(Park_Activity)
                 .join(Park_Topic)
                 .filter(*all_filters) #'*' is used to unpack arrays
                 ).all()
    
    return all_parks


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

    user_favorites = []
    
    for fav in user_favs:
        user_favorites.append(fav.park)

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



def create_user_trip(trip_name, start_date, end_date, notes, user, park):
    """ Create and return a new trip to be added to user's trips """

    user_trip = User_Trip(trip_name=trip_name,
                          start_date = start_date,
                          end_date = end_date,
                          notes = notes,
                          user=user, 
                          park=park)
    
    return user_trip



def get_trip_by_id(trip_id):
    """ Returns a trip with given id """

    trip = User_Trip.query.filter_by(id = trip_id).one()

    return trip



def get_trips_by_user(user_id):
    """ Returns a list of trips saved in a user's list"""

    user_trips = User_Trip.query.filter_by(user_id = user_id).all()

    return user_trips



def get_user_trip_by_user_and_id(user_id, trip_id):
    """ Returns a trip to be removed from user's list """

    trip_id = int(trip_id)

    user_trips = User_Trip.query.filter_by(user_id = user_id).all()

    for trip in user_trips:
        if trip.user_id == user_id and trip.id == trip_id:
            trip_remove = trip
    
    return trip_remove



def create_trip_attraction(attraction_id_api, attraction_name, trip, user):
    """ Creates attraction for a trip """

    trip_attraction = Trip_Attraction(attraction_id_api = attraction_id_api,
                                      attraction_name = attraction_name,
                                      trip = trip,
                                      user = user)
    
    return trip_attraction



def get_attractions_for_trip(trip_id):
    """ Get all selected attractions for a given trip id """

    trip_attractions = Trip_Attraction.query.filter_by(trip_id = trip_id).all()

    return trip_attractions



def create_review_comment(review, user, park):
    """ Create review comment """

    review_comment = Review_Comment(review = review,
                                    user = user,
                                    park = park)
    
    return review_comment



def get_all_review_comments():
    """ Returns all review comments for all parks and all users """

    review_comments = Review_Comment.query.all()

    return review_comments



def get_review_comments_by_park(park_id):
    """ Returns all review comments for a particular park """

    review_comments = Review_Comment.query.filter_by(park_id = park_id).all()

    return review_comments



def get_review_comments_by_user(user_id):
    """ Returns all review comments made by a particular user """

    review_comments = Review_Comment.query.filter_by(user_id = user_id).all()

    return review_comments





if __name__ == '__main__':
    from server import app
    connect_to_db(app)