"""Server for National Parks app"""

from flask import Flask, render_template, request, flash, session, redirect

from pprint import pformat, pprint
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

API_KEY = os.environ['NPS_KEY']
base_url = 'developer.nps.gov/api/v1'


url = "https://developer.nps.gov/api/v1/parks"
# HEADERS = {"X-Api-Key": API_KEY}

payload = {"api_key": API_KEY}
payload['limit'] = "500"
# payload['start'] = "0"

# print("Headers = ", HEADERS)

# res = requests.get(url, headers=HEADERS, params=payload)
res = requests.get(url, params=payload)
data = res.json()
parks = data['data']
parks_count = len(parks)


parks_data = []
count = 0

def check_lat(park):
    if park['latitude'] == "":
        latitude = 0.0
    else:
        latitude = float((park['latitude'].strip()))
    
    return latitude

def check_long(park):
    if park['longitude'] == "":
        longitude = 0.0
    else:
        longitude = float((park['longitude'].strip()))
    
    return longitude


for park in parks:


    park_dict = {'park_name': park['fullName'],
                'park_code': park['parkCode'],
                'general_info': park['description'],
                'location_lat': check_lat(park),
                'location_long': check_long(park),
                'park_count': count + 1
                }
    count += 1
    # park_dict['history'] = 
    # park_dict['main_attractions'] = 
    # park_dict['trails'] = 
    parks_data.append(park_dict)

# print(parks_data[0])
# print("Length of parks_data = ", (len(parks_data)))

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

    return render_template("park_details.html", park=park)


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

    # name = request.args.get('search')
    # park = crud.get_park_by_name(name)

    # return render_template("park_details.html", park=park)

    return render_template("search.html", park_names=park_names)



@app.route("/search/result")
def search_result():
    """ Show the search results """

    # park_names = crud.get_park_names()

    park_name = request.args.get('park', "")
    park = crud.get_park_by_name(park_name)

    return render_template("park_details.html", park=park)
    

@app.route("/login")
def login_form():
    """ Show the log-in/ sign-up form """
    
    if 'user_email' in session:        
        flash("User already logged in")
        return redirect (request.referrer)
    else:
        return render_template("log-in.html")


@app.route("/login", methods=["POST"])
def login():
    """ Log in an existing user """

    email = request.form.get('email')
    password = request.form.get('password')

    user_emails = crud.get_user_emails()
    print("User emails = ", user_emails)

    if email in user_emails:
        user = crud.get_user_by_email(email)
        if user.password == password:
            session['user_email'] = user.email
            flash(f"Welcome, {user.fname}!")
            return redirect("/")
        else:
            flash("The password you entered is incorrect. Please try again")
            return redirect("/login")
    else:
        flash("Account with this email not found. Please sign-up using this email to create a new account.")
        return redirect("/login")
    


@app.route("/signup", methods=["POST"])
def sign_up():
    """ Sign up a new user/ Create a new account """

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user_emails = crud.get_user_emails()

    if email in user_emails:
        flash("An account with this email already exists. Try again.")
    else:
        new_user_email = crud.create_user(fname, lname, email, password)
        db.session.add(new_user_email)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")



@app.route("/logout")
def logout():
    """ Log out existing user """
    
    confirmation = request.args.get('confirmation')

    if confirmation == "Yes":
        if "user_email" in session:
            del session['user_email']
            return "You have been succesfully logged out!"
        else:
            return "User not logged in"
    # elif confirmation == "No":
    else:
        if "user_email" in session:
            return "You have not been logged out"
        else:
            return "User not logged in"



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



# @app.route("/users/<user_id>/<id>", methods=["POST"])
# # @app.route("/user/user_details/<favorite.park.id>", methods=["POST"])
# def remove_from_favorite(user_id, id):
#     """ Remove a park from user's favorites with the given arguments - user-id and park-id"""

#     # user_email = session["user_email"]
#     # user = crud.get_user_by_email
#     # user_id = user.user_id
#     park_remove = crud.get_user_favorite_to_be_removed(user_id, id)

#     db.session.delete(park_remove)
#     db.session.commit()

#     return redirect(request.referrer)



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
def add_to_wishlist(user_id, id):
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
        # print("User favorites ########## ", user_favorites)
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


    

    





    










    





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    