#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, print_function
import re

# Country codes.
codes = dict([line.decode("utf-8").split("\t")[:2]
              for line in open("data/admin1CodesASCII.txt")])
# zipcodes = dict([(line.split(",")[0].strip(), map(float, line.split(",")[3:4]))
#                  for line in open("data/zipcode.csv") if "zip" not in line])


def load_locations():
    locations = []
    with open("data/cities15000.txt") as f:
        for line in f:
            cols = line.decode("utf-8").split("\t")
            names = [cols[1], cols[2]] + cols[3].split(",")
            names = [n for n in names if len(n)]
            latlng = [float(cols[4]), float(cols[5])]
            country_codes = [cols[8]] + cols[9].split(",")
            country_codes = [c for c in country_codes if len(c)]
            code = cols[10]
            population = int(cols[14])
            state = codes.get(country_codes[0] + "." + code, None)
            locations.append({
                "city": names[0],
                "alternatives": names[1:],
                "state": state,
                "country_codes": country_codes,
                "population": population,
                "latlng": latlng,
            })
    return locations


def location_score(affiliation, location):
    srch = location["city"]
    score = len(re.findall(r"(\b{0}\b)".format(re.escape(srch)), affiliation,
                           re.I))
    if score == 0:
        return 0

    state = location["state"]
    if state is not None:
        score += len(re.findall(r"(\b{0}\b)".format(re.escape(state)),
                                affiliation, re.I))

    return score


if __name__ == "__main__":
    locations = load_locations()
    for l in locations:
        score = location_score("Department of Astronomy and Astrophysics, University of California, Santa Cruz, Santa Cruz, CA 95064", l)
        if score:
            print(score, l["city"], l["state"])
