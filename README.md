This repo contains a basic python script for checking your current IP address against your current Cloudflare load balancer IP.

If they differ, the load balancer IP is updated, else do nothing.

Simply specify your CF email, API key and load balancer info as environment variables like:
```python
origin_name = os.environ.get('ORIGIN_NAME')
pool_id = os.environ.get('POOL_ID')
email = os.environ.get('EMAIL')
api_key = os.environ.get('API_KEY')
```

The basic logic goes like this:

```python
#check your current WAN IP
new_ip = json.loads(requests.request("GET", "https://api.ipify.org?format=json").text)["ip"]
#Check if it equals the current CF load balancer IP
updated_origin, is_updated = get_updated_origins(new_ip)
print(is_updated)
if is_updated:
    #If they differ, update the IP 
    response = update_origins({"origins": updated_origin})
    print(response)
```

I've included a Dockerfile for a basic Alpine image and leave it to the user to determine how/when 
the script runs.


I check every 30 seconds with the following post argument to `docker run` and the `--restart=always` parameter:

```shell
/bin/sh -c ' while :; do python /scripts/update.py ; sleep 30; done'
```

        