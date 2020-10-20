import requests
import sys
import os
import json
import time

email = 'caspar.data@uwaterloo.ca'
login_url = "http://206.167.181.226/login"
post_url = "http://206.167.181.226/fetchResult"


def post_request(url, token, jsondata):
    # sends JSON processing request to frontend

    tic = time.perf_counter()

    jsondata['auth_token'] = token
    r = requests.post(url=url, json=jsondata)
    print(r.text)
    toc = time.perf_counter()
    print("completed request posting in  {} seconds".format(toc - tic))

if __name__ == '__main__':
    password = sys.argv[1]

    # get login token
    r = requests.post(url=login_url, json={'email': email, 'password': password})
    result = r.json()
    token = result["response"]["user"]["authentication_token"]

    now = time.time()
    json_request = '{{"variables": ["CaPA_coarse_A_PR_SFC"], "fcst_window": [], "issues": ["00:00"], "product": "CaPA_coarse", "backend": "slurm", "bounding_geom": [{{"type": "Feature", "properties": {{}}, "geometry": {{"type": "Polygon", "coordinates": [[[-94.956207, 34.03872], [-94.956207, 34.039858], [-94.954491, 34.039858], [-94.954491, 34.03872], [-94.956207, 34.03872]]]}}}}], "start_time": "2012-09-17", "end_time": "2012-09-17", "request_id": "{}_{}", "user_email": "{}", "user_firstname": "Caspar", "user_lastname": "Dummy", "globus_id": "julemai@computecanada.ca"}}'.format(email, now, email)

    post_request(post_url, token, json.loads(json_request))
