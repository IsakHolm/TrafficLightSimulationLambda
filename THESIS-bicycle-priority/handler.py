import json
import time
from math import sin, cos, sqrt, atan2, radians

def sim(event, context):

    now = time.time() % 30

    tl_1 = [57.706361, 11.989455]
    tl_2 = [57.705112, 11.990036]
    tl_3 = [57.702246, 11.991057]

    lightsList = [tl_1, tl_2, tl_3]

    event_body = json.loads(event["body"])
    
    user_pos = [event_body["lat"], event_body["lon"]]
    prev_user_pos = [event_body["prev_lat"], event_body["prev_lon"]]

    # Send status and time left if request requested debug info
    if user_pos[0] == "Debug":
        res = {
            "status" : "green",
            "time_left" : int( 15 - ( now % 15 ) ),
            "light_lat": "0",
            "light_lon": "0",
            "distance": "0"
        }
    
        if now < 15:
            res["status"] = "red"

        return {
            'statusCode': 200,
            'body': json.dumps(res)
        }

    lightsListAscendingDistance = sortTrafficLightsList(user_pos[0], user_pos[1], lightsList)

    index = -1
    min = 0

    # This for-loop loops through a list of traffic lights that are sorted with ascending distance to the biker. 
    # The loop checks to see if the biker i moving away from the traffic light. If not, that index is chosen and the loop ends.  
    for i, tl in enumerate(lightsListAscendingDistance):
        min = calc_distance(float(user_pos[0]), float(user_pos[1]), tl[0], tl[1])
        if min < calc_distance(float(prev_user_pos[0]), float(prev_user_pos[1]), tl[0], tl[1]):
            index = i
            break

    # If index == -1, then no traffic light was found that the biker is getting closer to. Then this "non-data" is sent and can be interpreted as "nothing to process"
    if index == -1:
        res = {
            "status" : "None",
            "time_left" : "0",
            "light_lat": "0",
            "light_lon": "0",
            "distance": "0"
        }
        return {
            'statusCode': 200,
            'body': json.dumps(res)
        }

    res = {
        "status" : "green",
        "time_left" : int( 15 - ( now % 15 ) ),
        "light_lat": lightsListAscendingDistance[index][0],
        "light_lon": lightsListAscendingDistance[index][1],
        "distance": min
    }
    
    if now < 15:
        res["status"] = "red"

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

# Searches a list (lightsCurrent) for the traffic light that is closest to the point (lat, lon)
def findMinDistanceTrafficLights(lat, lon, lightsCurrent):
    min = calc_distance(float(lat), float(lon), lightsCurrent[0][0], lightsCurrent[0][1])
    index = 0
    for i, tl in enumerate(list(lightsCurrent)):
        tmp = calc_distance(float(lat), float(lon), tl[0], tl[1])
        if tmp < min:
            min = tmp
            index = i

    return (index, min)

# Sorts a list of traffic lights where the order is ascending in distance between the point (lat, lon) and the traffic lights
def sortTrafficLightsList(lat, lon, lights):
    resList = []
    lightsCopy = lights.copy()
    for i in enumerate(lights):
        res = findMinDistanceTrafficLights(lat, lon, lightsCopy)
        resList.append(lightsCopy.pop(res[0]))

    return resList

# Function to calculate the distance in meters between two coordinates
def calc_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    
    R_lat1 = radians(lat1)
    R_lon1 = radians(lon1)
    R_lat2 = radians(lat2)
    R_lon2 = radians(lon2)
    dlon = R_lon2 - R_lon1
    dlat = R_lat2 - R_lat1
    a = (sin(dlat/2))**2 + cos(R_lat1) * cos(R_lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c * 1000
    return distance
