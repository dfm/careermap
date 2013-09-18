import json
from careermap.get_locations import get_locations

for user in open("data/authors.txt"):
    locations = get_locations(user.strip())
    json.dump(locations, open(user.replace(" ", "_").lower() + "json"),
              indent=2, separators=(",", ": "))
