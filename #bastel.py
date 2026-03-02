import requests
import json

# Base URL for the service
base_url = "https://maps.infas-lt.de/default/"

print(f"Fetching landing page: {base_url}")
response = requests.get(base_url)
response.raise_for_status()

pretty_json = json.loads(response.content.decode("utf-8"))
print(json.dumps(pretty_json, indent=2))

#Find all links that end with "styles"
links = (link for link in pretty_json["links"] if link["rel"].endswith("styles"))


