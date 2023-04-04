import json
import time
from math import sin, cos, sqrt, atan2, radians


def sim(event, context):
    
    tl_1 = [57, 13]
    tl_2 = [57, 10]

    lights = [tl_1, tl_2]

    event_body = json.loads(event["body"])
    
    user_pos = [event_body["lat"], event_body["lon"]]

    min = calc_distance(float(user_pos[0]), float(user_pos[1]), lights[0][0], lights[0][1])
    index = 0

    for i, tl in enumerate(lights):
        tmp = calc_distance(float(user_pos[0]), float(user_pos[1]), tl[0], tl[1])
        if tmp < min: 
            min = tmp
            index = i

    now = time.time() % 30
    
    res = {
        "status" : "green",
        "time_left" : int( 15 - ( now % 15 ) ),
        "light_lat": lights[index][0],
        "light_lon": lights[index][1],
        "distance": min
    }
    
    if now < 15:
        res["status"] = "red"

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }


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
