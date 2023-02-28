""" Script to seed database """

import os
import json
import random

import crud
import model
import server

os.system("dropdb parks")
os.system("createdb parks")
model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()

from datetime import datetime
from passlib.hash import argon2


### Creating parks, park states, park activities, park topics, using CRUD function ###

with open('data/parks.json') as f:
    parks_data = json.loads(f.read())

parks_in_db = []

for ind_park in parks_data:
    park_code = ind_park['park_code']
    park_name = ind_park['park_name']
    general_info = ind_park['general_info']
    history = '*** history pending ***'
    main_attractions = '*** main_attractions pending ***'
    trails = '*** trails pending ***'
    location_lat = ind_park['location_lat']
    location_long = ind_park['location_long']

    db_ind_park = crud.create_park(park_code, park_name, general_info, history, 
                               main_attractions, trails, location_lat, location_long)
    parks_in_db.append(db_ind_park)
    model.db.session.add(db_ind_park)


    for state in ind_park['states']:
        park = db_ind_park
        state_code = state
        state_name = ind_park['states'][state_code]
        db_park_state = crud.create_park_state(park, state_code, state_name)
        model.db.session.add(db_park_state)
    

    for ind_activity in ind_park['activities']:
        park = db_ind_park
        activity = ind_activity
        db_park_activity = crud.create_park_activity(park, activity)
        model.db.session.add(db_park_activity)
    

    for ind_topic in ind_park['topics']:
        park = db_ind_park
        topic = ind_topic
        db_park_topic = crud.create_park_topic(park, topic)
        model.db.session.add(db_park_topic)

model.db.session.commit()



### Creating Users, User Favorites and User Wishlist using CRUD functions ###

users_in_db = []

for n in range(1,11):
    fname = f"Fname{n}"
    lname = f"Lname{n}"
    email = f"user{n}@test.com"
    password = f"test{n}"
    hashed_password = argon2.hash(password)
    del password

    # print("hashed = ", hashed_password)


    db_user = crud.create_user(fname, lname, email, hashed_password)
    model.db.session.add(db_user)

    for _ in range(5):
        park_fav = random.choice(parks_in_db)
        park_wish = random.choice(parks_in_db)
        user_trip_park = random.choice(parks_in_db)
        user_trip_name = f"Sample Trip"
        user_trip_start_date = "02.10.2023"
        user_trip_end_date = "02.10.2023"
        notes = "Trip details go here.. "

        db_favorite = crud.create_user_favorite(db_user, park_fav)
        db_wishlist = crud.create_user_wishlist(db_user, park_wish)
        db_user_trip = crud.create_user_trip(user_trip_name, user_trip_start_date, user_trip_end_date, notes, db_user, user_trip_park)
        model.db.session.add(db_favorite)
        model.db.session.add(db_wishlist)
        model.db.session.add(db_user_trip)


model.db.session.commit()



# ### Sample comments for testing

# comments_in_db = []

# comment_user = crud.get_user_by_id(1)
# comment_park = crud.get_park_by_id(63)
# review_1 = "Sample review comment - 1"
# review_2 = "Sample review comment - 2"

# db_review_comment_1 = crud.create_review_comment(review_1, comment_user, comment_park)
# model.db.session.add(db_review_comment_1)

# db_review_comment_2 = crud.create_review_comment(review_2, comment_user, comment_park)
# model.db.session.add(db_review_comment_2)

# model.db.session.commit()









