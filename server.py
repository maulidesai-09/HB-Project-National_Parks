"""Server for National Parks app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from pprint import pformat, pprint
from passlib.hash import argon2
import os
import requests
import json

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = 'SECRETSECRETSECRET'
app.jinja_env.undefined = StrictUndefined


#######################################################################################################

### Dictionary for state codes: state names

states_dict = {'AK': 'Alaska', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 
          'CO': 'Colorado', 'DC': 'Washington DC', 'FL': 'Florida', 'HI': 'Hawaii', 
          'ID': 'Idaho', 'IN': 'Indiana', 'KY': 'Kentucky', 'MD': 'Maryland', 
          'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 
          'MP': 'Northern Mariana Islands', 'MT': 'Montana', 'NC': 'North Carolina', 
          'ND': 'North Dakota', 'NM': 'New Mexico', 'NV': 'Nevada', 'OH': 'Ohio', 
          'OR': 'Oregon', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 
          'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 
          'WA': 'Washington', 'WY': 'Wyoming'}


#######################################################################################################


API_KEY = os.environ['NPS_KEY']
base_url = 'developer.nps.gov/api/v1'


url = "https://developer.nps.gov/api/v1/parks"
# HEADERS = {"X-Api-Key": API_KEY}

payload = {"api_key": API_KEY}
payload['limit'] = "500"

res = requests.get(url, params=payload)
data = res.json()
parks = data['data']
parks_count = len(parks)

categories = ["National and State Parks", "National Park", "Park", "National Parks"]
national_parks = []

for park in parks:
    if park['designation'] in categories:
        national_parks.append(park)

print(len(national_parks)) #includes total 64 national parks


parks_data = []
count = 0

def check_lat(park):
    """ Check for missing latitude information and assign its value as 0.0 """
    
    if park['latitude'] == "":
        latitude = 0.0
    else:
        latitude = float((park['latitude'].strip()))
    
    return latitude


def check_long(park):
    """ Check for missing latitude information and assign its value as 0.0 """

    if park['longitude'] == "":
        longitude = 0.0
    else:
        longitude = float((park['longitude'].strip()))
    
    return longitude


def get_activity_list(park):
    """ Get a list of topics for each park """

    activities = []
    for activity in park['activities']:
        activities.append(activity['name'])
    
    return activities


def get_topic_list(park):
    """ Get a list of topics for each park """

    topics = []
    for topic in park['topics']:
        topics.append(topic['name'])
    
    return topics


def get_state_name(state_code_list):
    """ Get state names based on state codes """
    state_names = []
    for state_code in state_code_list:
        state_names.append(states_dict[state_code])
    
    return state_names

def create_park_state_dict(state_code_list):
    """ Create a list of dictionaries based on list of state codes obtained """

    states = {}

    for state_code in state_code_list:
        states[state_code] = states_dict[state_code]
            
    return states
    


for park in national_parks:

    park_dict = {'park_name': park['fullName'],
                'park_code': park['parkCode'],
                'designation': park['designation'],
                'general_info': park['description'],
                'location_lat': check_lat(park),
                'location_long': check_long(park),
                'states': create_park_state_dict(park['states'].split(",")),
                'activities': get_activity_list(park),
                'topics': get_topic_list(park),
                'park_count': count + 1
                }
    count += 1

    parks_data.append(park_dict)



json.dump(parks_data, open('data/parks.json','w'), indent=2)


#######################################################################################################



@app.route("/")
def homepage():
    """ View homepage """

    return render_template('homepage.html')


@app.route("/parks")
def view_parks():
    """ View a list of all parks """

    parks = crud.get_parks()

    return render_template("all_parks.html", parks=parks)


@app.route("/parks/<id>")
def show_park_details(id):
    """ Show details of a particular park """

    park = crud.get_park_by_id(id)
    park_code = park.park_code

    ### Get Main Attractions/ Things To Do from API 
    
    url = "https://developer.nps.gov/api/v1/thingstodo"
    payload = {"api_key": API_KEY}
    payload['parkCode'] = park_code

    res = requests.get(url, params=payload)
    data = res.json()
    things_to_do = data['data']

    def get_activity_list(thing):
        """ Get a list of activities for each main attraction """

        activities = []
        for activity in thing['activities']:
            activities.append(activity['name'])
        
        return activities
    
    def get_topic_list(thing):
        """ Get a list of topics for each main attraction """

        topics = []
        for topic in thing['topics']:
            topics.append(topic['name'])
        
        return topics
    

    def get_images_list(thing):
        """ Get a list of images for each main attraction """

        images = []
        for image in thing['images']:
            images.append(image['url'])
        
        return images
    

    main_attractions = []
    
    for thing in things_to_do:
        attraction = {}
        attraction['id'] = thing['id']
        attraction['title'] = thing['title']
        attraction['short_description'] = thing['shortDescription']
        attraction['location'] = thing['location']
        attraction['long_description'] = thing['longDescription']
        attraction['activities'] = get_activity_list(thing)
        attraction['topics'] = get_topic_list(thing)
        attraction['images'] = get_images_list(thing)
        main_attractions.append(attraction)
    

    ### Get Alerts from API

    url = "https://developer.nps.gov/api/v1/alerts"
    payload = {"api_key": API_KEY}
    payload['parkCode'] = park_code

    res = requests.get(url, params=payload)
    data = res.json()
    alerts_api = data['data']

    alerts = []
    for item in alerts_api:
        alert = {}
        alert['id'] = item['id']
        alert['url'] = item['url']
        alert['title'] = item['title']
        alert['description'] = item['description']
        alert['lastIndexedDate'] = item['lastIndexedDate']
        alerts.append(alert)


    return render_template("park_details.html", 
                           park=park, 
                           main_attractions=main_attractions, 
                           alerts = alerts)



@app.route("/api/parks/<id>/main-attractions/ajax")
def get_details_of_main_attractions(id):
    """ Get details of main attractions to be sent via ajax response """

    park = crud.get_park_by_id(id)
    park_code = park.park_code

    attraction_title = request.args.get("title", "").strip()


    url = "https://developer.nps.gov/api/v1/thingstodo"
    payload = {"api_key": API_KEY}
    payload['parkCode'] = park_code

    res = requests.get(url, params=payload)
    data = res.json()
    things_to_do = data['data']

    def get_activity_list(thing):
        """ Get a list of activities for each main attraction """

        activities = []
        for activity in thing['activities']:
            activities.append(activity['name'])
        
        return activities
    
    def get_topic_list(thing):
        """ Get a list of topics for each main attraction """

        topics = []
        for topic in thing['topics']:
            topics.append(topic['name'])
        
        return topics
    

    def get_images_list(thing):
        """ Get a list of images for each main attraction """

        images = []
        for image in thing['images']:
            images.append(image['url'])
        
        return images
    

    main_attractions = []
    
    for thing in things_to_do:
        attraction = {}
        attraction['id'] = thing['id']
        attraction['title'] = thing['title']
        attraction['short_description'] = thing['shortDescription']
        attraction['location'] = thing['location']
        attraction['long_description'] = thing['longDescription']
        attraction['activities'] = get_activity_list(thing)
        attraction['topics'] = get_topic_list(thing)
        attraction['images'] = get_images_list(thing)
        main_attractions.append(attraction)

    
    for attraction in main_attractions:
        if attraction['title'] == attraction_title:
            result_attraction = attraction
    
    print("######### result attractions = ", result_attraction)
    
    return render_template("park_details-main_attractions.html", result = result_attraction)
    
    




@app.route("/users")
def view_users():
    """ View a list of all users """

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users/<user_id>")
def show_user_details(user_id):
    """ Show details of a particular user """

    user = crud.get_user_by_id(user_id)
    email = user.email

    if "user_email" in session:
        if session['user_email'] == email:
            user = crud.get_user_by_id(user_id)
            return render_template("user_details.html", user=user)
        else:
            flash("Please log in to view the profile details")
            return redirect(request.referrer)
    else:
        flash("Please log in to view the profile details")
        return redirect(request.referrer)


@app.route("/profile")
def view_profile():
    """ View user's profile """

    if "user_email" in session:
        email = session["user_email"]
        user = crud.get_user_by_email(email)
        id = user.user_id
        return redirect(f"/users/{id}")
    else:
        flash("Please log in to view profile")
        return redirect("/login")



@app.route("/search")
def search_form():
    """ Show the search form """

    park_names = crud.get_park_names()
    all_parks = crud.get_parks()
    all_states_names = crud.get_all_states_names()
    all_activities = crud.get_all_activities()
    all_topics = crud.get_all_topics()

    print("########", all_states_names)

    return render_template("search.html", 
                           all_parks = all_parks, 
                           all_states=all_states_names,
                           all_activities=all_activities,
                           all_topics=all_topics)



@app.route("/search/state_map_result")
def state_map_search_results():
    """ Show the result for state selected from clickable map """

    state_name = request.args.get("selected_map_state", "")

    all_parks = crud.get_parks()
    all_states_names = crud.get_all_states_names()
    all_activities = crud.get_all_activities()
    all_topics = crud.get_all_topics()

    activities = []
    topics = []
    response = True

    # print("######## state = ", state_name)
    # print("######## activities = ", activities)
    # print("######## topics = ", topics)

    if state_name == "" and len(activities) == 0 and len(topics) == 0:
       response = False
       result = "Please select a filter"
    else:
        parks = crud.get_matching_parks(state_name, activities, topics)
        if len(parks) == 0:
            response = False
            result = "No parks available"
        else:
            result = parks
    
    # print("######## result = ", result)
    

    return render_template("advance-search-result.html", 
                           response=response,
                           result=result,
                           all_parks = all_parks, 
                           all_states=all_states_names,
                           all_activities=all_activities,
                           all_topics=all_topics)



@app.route("/search/advance_search_result")
def advance_search_result():
    """ Show the result for advance search on a new page """

    park_names = crud.get_park_names()
    all_parks = crud.get_parks()
    all_states_names = crud.get_all_states_names()
    all_activities = crud.get_all_activities()
    all_topics = crud.get_all_topics()

    state_name = request.args.get("state", "")
    activities = request.args.getlist("activity")
    topics = request.args.getlist("topic")
    response = True

    # print("######## state = ", state_name)
    # print("######## activities = ", activities)
    # print("######## topics = ", topics)

    if state_name == "" and len(activities) == 0 and len(topics) == 0:
       response = False
       result = "Please select a filter"
    else:
        parks = crud.get_matching_parks(state_name, activities, topics)
        if len(parks) == 0:
            response = False
            result = "No parks available"
        else:
            result = parks
    
    # print("######## result = ", result)
    

    return render_template("advance-search-result.html", 
                           response=response,
                           result=result,
                           all_parks = all_parks, 
                           all_states=all_states_names,
                           all_activities=all_activities,
                           all_topics=all_topics)



@app.route("/api/search/advance_search_result/ajax", methods=["POST"])
def advance_search_result_ajax():
    """ Show the result for advance search """

    state = request.json.get("state")
    activities = request.json.get("activities")
    topics = request.json.get("topics")
    response = True

    # print("######## state = ", state)
    # print("######## activities = ", activities)
    # print("######## topics = ", topics)

    if state == "" and len(activities) == 0 and len(topics) == 0:
       response = False
       result = "Please select a filter" 
    else:
        parks = crud.get_matching_parks(state, activities, topics)

        if len(parks) == 0:
            response = False
            result = "No parks available"
        else:
            result_object = parks

            result = []
            for park in result_object:
                park_dict = {}
                park_dict['park_id'] = park.id
                park_dict['park_name'] = park.park_name
                park_dict['park_lat'] = park.location_lat
                park_dict['park_long'] = park.location_long
                park_dict['park_code'] = park.park_code
                result.append(park_dict)


    return jsonify({'response': response,
                    'result': result})



@app.route("/login")
def login_form():
    """ Show the log-in/ sign-up form """
    
    if 'user_email' in session:        
        flash("User already logged in")
        return redirect (request.referrer)
    else:
        return render_template("log-in.html", request_url = request.referrer)



@app.route("/login", methods=["POST"])
def login():
    """ Log in an existing user """

    email = request.form.get('email')
    password = request.form.get('password')
    request_url = request.form.get('request_url')

    user_emails = crud.get_user_emails()
    # print("User emails = ", user_emails)
    # print("################### request", request_url)

    if email in user_emails:
        user = crud.get_user_by_email(email)
        if argon2.verify(password, user.password):
            session['user_email'] = user.email
            flash(f"Welcome, {user.fname}!")
            return redirect(request_url)
        else:
            flash("The password you entered is incorrect. Please try again")
            return redirect("/login")
    else:
        flash("Account with this email not found. Please sign-up using this email to create a new account.")
        return redirect("/login")
    


@app.route("/signup", methods=["POST"])
def sign_up():
    """ Sign up a new user/ Create a new account """

    request_url = request.form.get('request_url')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = argon2.hash(password)
    del password

    user_emails = crud.get_user_emails()

    if email in user_emails:
        flash("An account with this email already exists. Try again.")
    else:
        new_user_email = crud.create_user(fname, lname, email, hashed_password)
        db.session.add(new_user_email)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect(request_url)



@app.route("/logout")
def logout():
    """ Log out existing user """
    
    confirmation = request.args.get('confirmation')
    # print("############", confirmation)
    previous_path = request.referrer
    # print("###################", previous_path)

    if confirmation == "Yes":
        if "user_email" in session:
            user = crud.get_user_by_email(session["user_email"])
            user_id = user.user_id
            print("#######################", f"/users/{user_id}")
            del session['user_email']
            if previous_path == f"http://localhost:5000/users/{user_id}" or previous_path.__contains__("/trip"):
                return redirect("/")
            else:
                flash("You have been succesfully logged out!")
                return redirect(request.referrer)
        else:
            flash("User not logged in")
            return redirect(request.referrer)
    else:
        if "user_email" in session:
            flash("You have not been logged out")
            return redirect(request.referrer)
        else:
            flash("User not logged in")
            return redirect(request.referrer)



@app.route("/parks/<id>/favorite", methods=["POST"])
def add_to_favorite(id):
    """ Add a park to user's favorites list"""

    logged_in_email = session.get("user_email")
    # print("logged in email is ########################## ", logged_in_email)

    if logged_in_email is None:
        flash("Please log in to add park to favorites")
    else:
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        park = crud.get_park_by_id(id)
        user_favorites = crud.get_favorite_parks_by_user(user_id)
        print("User favorites ########## ", user_favorites)
        if park in user_favorites:
            flash("Park already exists in your favorites")
        else:
            add_favorite = crud.create_user_favorite(user, park)
            db.session.add(add_favorite)
            db.session.commit()
            flash("Added to favorites!")
    
    return redirect(f"/parks/{id}")


@app.route("/parks/<id>/remove_favorite")
def remove_from_favorite(id):
    """ Remove a park with given id from logged in user's favorites """

    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_id = user.user_id
        park_to_be_removed = crud.get_user_favorite_to_be_removed(user_id, id)
        park_name = park_to_be_removed.park.park_name
        
        db.session.delete(park_to_be_removed)
        db.session.commit()
        
        flash(f"{park_name} has been removed from your favorites")

    else:
        flash("Please log in to remove park from favorites")
    
    return redirect(request.referrer)
    


@app.route("/parks/<id>/wishlist", methods=["POST"])
def add_to_wishlist(id):
    """ Add a park to user's wishlist """

    logged_in_email = session.get("user_email")
    # print("logged in email is ########################## ", logged_in_email)

    if logged_in_email is None:
        flash("Please log in to add park to wishlist")
    else:
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        park = crud.get_park_by_id(id)
        user_wishlist = crud.get_wishlist_parks_by_user(user_id)
        if park in user_wishlist:
            flash("Park already exists in your wishlist")
        else:
            add_wishlist = crud.create_user_wishlist(user, park)
            db.session.add(add_wishlist)
            db.session.commit()
            flash("Added to wishlist!")
    
    return redirect(f"/parks/{id}")



@app.route("/parks/<id>/remove_wish")
def remove_from_wishlist(id):
    """ Remove a park with given id from logged in user's favorites """

    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_id = user.user_id
        park_to_be_removed = crud.get_user_wish_to_be_removed(user_id, id)
        park_name = park_to_be_removed.park.park_name
        
        db.session.delete(park_to_be_removed)
        db.session.commit()
        
        flash(f"{park_name} has been removed from your wishlist")

    else:
        flash("Please log in to remove park from favorites")
    
    return redirect(request.referrer)



@app.route("/plan-trip")
def plan_a_trip():
    """ Display a form for planning a trip """
    
    parks = crud.get_parks()

    return render_template("plan_trip.html", 
                           parks = parks)



@app.route("/app/plan-trip/ajax")
def get_main_attractions_for_trip():
    """ Get main attractions to be displayed based on park selected """
    
    park_id = request.args.get("park_id", "")

    park_code = crud.get_park_code_by_id(park_id)

    url = "https://developer.nps.gov/api/v1/thingstodo"
    payload = {"api_key": API_KEY}
    payload['parkCode'] = park_code

    res = requests.get(url, params=payload)
    data = res.json()
    things_to_do = data['data']

    main_attractions = []
    
    for thing in things_to_do:
        attraction = {}
        attraction['id'] = thing['id']
        attraction['title'] = thing['title']
        main_attractions.append(attraction)


    return render_template("plan_trip-main_attractions.html", 
                           main_attractions = main_attractions)


@app.route("/trip")
def create_a_trip():
    """ Create a trip with the details entered in trip plan """

    trip_name = request.args.get("trip-name")
    park_id = request.args.get("park")
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    trip_attractions_id = request.args.getlist("attraction")
    notes = request.args.get("notes")


    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("Please log in to create a trip")

        return redirect(request.referrer)
    
    else:
        user = crud.get_user_by_email(logged_in_email)
        park = crud.get_park_by_id(park_id)
        add_user_trip = crud.create_user_trip(trip_name, start_date, end_date, notes, user, park)
        db.session.add(add_user_trip)
        db.session.commit()

        url = "https://developer.nps.gov/api/v1/thingstodo"
        payload = {"api_key": API_KEY}
        park_code = park.park_code
        payload['parkCode'] = park_code

        res = requests.get(url, params=payload)
        data = res.json()
        things_to_do = data['data']

        trip_attractions = []
        for id in trip_attractions_id:
            attraction = {}
            for thing in things_to_do:
                if thing['id'] == id:
                    attraction['id'] = id
                    attraction['title'] = thing['title']
                    trip_attractions.append(attraction)
        

        trip_attractions_objects = []
        for attraction in trip_attractions:
            add_trip_attraction = crud.create_trip_attraction(attraction['id'], attraction['title'], add_user_trip, user)
            db.session.add(add_trip_attraction)
            db.session.commit()
            trip_attractions_objects.append(add_trip_attraction)


        flash("Trip has been added to your profile")         

    return render_template("trip-details.html",
                        trip = add_user_trip,
                        trip_attractions_objects = trip_attractions_objects
                        )



@app.route("/trip/<id>")
def display_trip_details(id):
    """ Display details of trip with given id """

    trip = crud.get_trip_by_id(id)
    # print(f"############### trip = {trip}")

    trip_attractions_objects = crud.get_attractions_for_trip(id)

    return render_template("trip-details.html",
                           trip = trip,
                           trip_attractions_objects = trip_attractions_objects)



@app.route("/trip/<id>/remove_trip")
def remove_trip(id):
    """ Remove trip from user's list of trips """
    
    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_id = user.user_id

        trip_to_be_removed = crud.get_user_trip_by_user_and_id(user_id, id)

        # print("########################## trip to be removed = ", trip_to_be_removed)

        trip_name = trip_to_be_removed.trip_name
        
        db.session.delete(trip_to_be_removed)
        db.session.commit()
        
        flash(f"{trip_name} has been removed from your wishlist")

    else:
        flash("Please log in to remove park from favorites")
    
    return redirect(request.referrer)



@app.route("/trip/<id>/edit_trip")
def edit_trip(id):
    """ Edit trip with given id """

    parks = crud.get_parks()

    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_id = user.user_id

        trip_to_be_edited = crud.get_user_trip_by_user_and_id(user_id, id)

    else:
        flash("Please log in to remove park from favorites")

    saved_attractions = trip_to_be_edited.trip_attractions
    list_of_saved_attraction_names = []
    for attraction in saved_attractions:
        list_of_saved_attraction_names.append(attraction.attraction_name)


    ### API call and code to get all main attractions (things to do) for the park that is being edited
    
    park_id = trip_to_be_edited.park.id
    park_code = crud.get_park_code_by_id(park_id)

    url = "https://developer.nps.gov/api/v1/thingstodo"
    payload = {"api_key": API_KEY}
    payload['parkCode'] = park_code

    res = requests.get(url, params=payload)
    data = res.json()
    things_to_do = data['data']

    main_attractions = []
    
    for thing in things_to_do:
        attraction = {}
        attraction['id'] = thing['id']
        attraction['title'] = thing['title']
        main_attractions.append(attraction)




    
    return render_template("edit_trip.html", 
                           trip = trip_to_be_edited,
                           parks = parks,
                           main_attractions = main_attractions,
                           list_of_saved_attraction_names = list_of_saved_attraction_names)
        



@app.route("/trip/<id>/trip-details-edited")
def saved_edited_trip(id):
    """ Edit the details of trip with given trip id """

    trip_name = request.args.get("trip-name")
    park_id = request.args.get("park")
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    trip_attractions_id = request.args.getlist("attraction")
    notes = request.args.get("notes")

    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_id = user.user_id

        trip_to_be_updated = crud.get_user_trip_by_user_and_id(user_id, id)
        updated_park = crud.get_park_by_id(park_id)

        trip_to_be_updated.trip_name = trip_name
        trip_to_be_updated.start_date = start_date
        trip_to_be_updated.end_date = end_date
        trip_to_be_updated.notes = notes
        trip_to_be_updated.park = updated_park
        db.session.commit()

        ### delete pre-edit trip attractions/ things to do
        trip_attractions_to_be_updated = crud.get_attractions_for_trip(id)
        for attraction in trip_attractions_to_be_updated:
            db.session.delete(attraction)
            db.session.commit
        

        ### create and add new attractions for trip based on edited information

        url = "https://developer.nps.gov/api/v1/thingstodo"
        payload = {"api_key": API_KEY}
        park_code = updated_park.park_code
        payload['parkCode'] = park_code

        res = requests.get(url, params=payload)
        data = res.json()
        things_to_do = data['data']

        trip_attractions = []
        for id in trip_attractions_id:
            attraction = {}
            for thing in things_to_do:
                if thing['id'] == id:
                    attraction['id'] = id
                    attraction['title'] = thing['title']
                    trip_attractions.append(attraction)
        

        trip_attractions_objects = []
        for attraction in trip_attractions:
            add_trip_attraction = crud.create_trip_attraction(attraction['id'], attraction['title'], trip_to_be_updated, user)
            db.session.add(add_trip_attraction)
            db.session.commit()
            trip_attractions_objects.append(add_trip_attraction)
    

    return render_template("trip-details.html",
                        trip = trip_to_be_updated,
                        trip_attractions_objects = trip_attractions_objects
                        )



@app.route("/parks/<id>/review-comments")
def get_review_comments_for_park(id):
    """ Get review comments for a park with given id """

    park_comments = crud.get_review_comments_by_park(id)

    review_comments = []
    for comment in park_comments:
        review_comment = {}
        review_comment['id'] = comment.id
        review_comment['review'] = comment.review
        review_comment['user'] = comment.user.fname + "  " + comment.user.lname
        review_comments.append(review_comment)

    return jsonify({"review_comments": review_comments})



@app.route("/add-review-comment", methods=["POST"])
def add_review_comment():
    """ Add review comment to the database """

    review = request.get_json().get("review")
    park_id = request.get_json().get("park_id")
    park = crud.get_park_by_id(park_id)
    
    if "user_email" in session:
        logged_in_user_email = session["user_email"]
        user = crud.get_user_by_email(logged_in_user_email)
        user_name = user.fname + user.lname
        
        new_review_comment = crud.create_review_comment(review, user, park)
        db.session.add(new_review_comment)
        db.session.commit()
        
        response = {"id": new_review_comment.id,
                    "review": review,
                    "user": user_name}

    else:
        response = flash("Please log in to add review")
       

    return jsonify({"response": response})







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    