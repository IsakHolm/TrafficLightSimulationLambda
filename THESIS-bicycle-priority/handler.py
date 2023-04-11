import json
import time
from math import sin, cos, sqrt, atan2, radians

tl_1 = [57, 13]
tl_2 = [57, 10]

lights = [tl_1, tl_2]

def sim(event, context):

    event_body = json.loads(event["body"])
    
    user_pos = [event_body["lat"], event_body["lon"]]
    prev_user_pos = [event_body["prev_lat"], event_body["prev_lon"]]

    lightsList = sortTrafficLights(user_pos[0], user_pos[1])

    index = 0

    for i, tl in enumerate(lightsList):
        if calc_distance(user_pos[0], user_pos[1], tl[0], tl[1]) < calc_distance(prev_user_pos[0], prev_user_pos[1], tl[0], tl[1]):
            index = i
            break


    now = time.time() % 30

    res = {
        "status" : "green",
        "time_left" : int( 15 - ( now % 15 ) ),
        "light_lat": lightsList[index][0],
        "light_lon": lightsList[index][1],
        "distance": min
    }
    
    if now < 15:
        res["status"] = "red"

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

def searchTrafficLights(lat, lon, lightsCurrent):
    min = calc_distance(float(lat), float(lon), lightsCurrent[0][0], lightsCurrent[0][1])
    index = 0
    for i, tl in enumerate(lightsCurrent):
        tmp = calc_distance(float(lat), float(lon), tl[0], tl[1])
        if tmp < min:
            min = tmp
            index = i

    return (index, min)

def sortTrafficLights(lat, lon):
    resList = []
    lightsCopy = lights.copy
    for i in enumerate(lights):
        res = searchTrafficLights(lat, lon, lightsCopy)
        resList.append(lightsCopy.pop(res.index))

    return resList

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
