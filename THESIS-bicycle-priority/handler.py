import json
import time
from math import sin, cos, sqrt, atan2, radians


def sim(event, context):
    
    tl_1 = (57.70556493250048, 11.99211749254271)
    tl_2 = (57.705567563648366, 11.992202034098431)

    now = time.time() % 30
    
    res = {
        "status" : "green",
        "time_left" : int( 15 - ( now % 15 ) ),
        "light_1_lat": tl_1[0],
        "light_1_lon": tl_1[1],
        "light_2_lat": tl_2[0],
        "light_2_lon": tl_2[1]
    }
    
    if now < 15:
        res["status"] = "red"

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

