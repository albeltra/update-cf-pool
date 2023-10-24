import requests
import json
import os

origin_name = os.environ.get('ORIGIN_NAME')
pool_id = os.environ.get('POOL_ID')
email = os.environ.get('EMAIL')
api_key = os.environ.get('API_KEY')

parameters = [origin_name, pool_id, email, api_key]

headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": f"{email}",
    "X-Auth-Key": f"{api_key}"
}

url = f"https://api.cloudflare.com/client/v4/user/load_balancers/pools/{pool_id}"


def get_updated_origins(updated_address, updated=False):
    resp = requests.request("GET", url, headers=headers)
    origins = json.loads(resp.text)['result']['origins']

    updated_origins = []
    for origin in origins:
        cur_origin = {}
        for k, v in origin.items():
            if k not in ['healthy', 'failure_reason']:
                cur_origin[k] = v
        if origin['name'] == origin_name:
            if origin["address"] != updated_address:
                updated = True
            cur_origin['address'] = updated_address
        updated_origins.append(cur_origin)
    print(updated_origins)
    return updated_origins, updated


def update_origins(payload):
    return requests.request("PATCH", url, json=payload, headers=headers).text


if all(parameters):
    new_ip = json.loads(requests.request("GET", "https://api.ipify.org?format=json").text)["ip"]
    updated_origin, is_updated = get_updated_origins(new_ip)
    print(is_updated)
    if is_updated:
        response = update_origins({"origins": updated_origin})
        print(response)
else:
    print('One or more required parameters has not been specified!')
