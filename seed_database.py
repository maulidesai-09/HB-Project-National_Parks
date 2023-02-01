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


### Creating parks using CRUD function ###

with open('data/parks.json') as f:
    parks_data = json.loads(f.read())

parks_in_db = []

for park in parks_data:
    park_code = park['park_code']
    park_name = park['park_name']
    general_info = park['general_info']
    history = '*** history pending ***'
    main_attractions = '*** main_attractions pending ***'
    trails = '*** trails pending ***'
    location_lat = park['location_lat']
    location_long = park['location_long']

    # if park['location_lat'] == "":
    #     location_lat = 0.0
    # else:
    #     location_lat = float((park['location_lat']).strip())
    
    # if park['location_long'] == "":
    #     location_long = 0.0
    # else:
    #     location_long = float((park['location_long']).strip())

    db_park = crud.create_park(park_code, park_name, general_info, history, 
                               main_attractions, trails, location_lat, location_long)
    parks_in_db.append(db_park)

model.db.session.add_all(parks_in_db)
model.db.session.commit()



### Creating Users, User Favorites and User Wishlist using CRUD functions ###

users_in_db = []

for n in range(1,11):
    fname = f"Fname{n}"
    lname = f"Lname{n}"
    email = f"user{n}@test.com"
    password = f"test{n}"

    db_user = crud.create_user(fname, lname, email, password)
    # users_in_db.append(db_user)
    model.db.session.add(db_user)

    for _ in range(5):
        park_fav = random.choice(parks_in_db)
        park_wish = random.choice(parks_in_db)

        db_favorite = crud.create_user_favorite(db_user, park_fav)
        db_wishlist = crud.create_user_wishlist(db_user, park_wish)
        model.db.session.add(db_favorite)
        model.db.session.add(db_wishlist)


model.db.session.commit()




# model.db.session.add_all(users_in_db)
# model.db.session.commit()









