### Extract from files 'server.py' and 'crud.py' in this repository ###

from flask import Flask, jsonify, request
from model import db, Park, Park_State, Park_Activity, Park_Topic
import crud

app = Flask(__name__)

### Extract from server.py ###

@app.route("/api/search/advance_search_result/ajax", methods=["POST"])
def advance_search_result_ajax():
    """ Show the result for advanced search """

    # Extract POST params from  browser AJAX request
    state = request.json.get("state")
    activities = request.json.get("activities")
    topics = request.json.get("topics")
    
    response = True

    # Get results from database based on search filters and return
    # the jsonified results as the response to AJAX request
    if state == "" and len(activities) == 0 and len(topics) == 0:
       response = False
       result = "Please select a filter" 
    else:
        # see line 51 for extract of crud function
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
                result.append(park_dict)

    return jsonify({'response': response,
                    'result': result})



### Extract from crud.py ###

def get_matching_parks(state_name, activities, topics):
    """" Returns parks from database that match the given state, 
    activities, topics """

    all_filters = []
    if state_name != "":
        all_filters.append(Park_State.state_name == state_name)
    if len(activities) > 0:
        all_filters.append(Park_Activity.activity.in_(activities))
    if len(topics) > 0:
        all_filters.append(Park_Topic.topic.in_(topics))

    # Join the 4 tables based on input attributes and search for matching records(rows)
    all_parks = (db.session.query(Park)
                 .join(Park_State)
                 .join(Park_Activity)
                 .join(Park_Topic)
                 .filter(*all_filters) #'*' is used to unpack arrays
                 ).all()
    
    return all_parks

