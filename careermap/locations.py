#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, print_function
import re

codes = dict([line.decode("utf-8").split("\t")[:2]
              for line in open("data/admin1CodesASCII.txt")])


def load_locations():
    results = []
    with open("data/cities1000.txt") as f:
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
            results.append({
                "city_names": names,
                "state": state,
                "country_codes": country_codes,
                "population": population,
                "latlng": latlng,
            })

    return results


def location_score(affiliation, location):
    cities = location["city_names"][:50]
    city_re = re.compile("|".join([r"(\b{0}\b)".format(re.escape(city))
                                   for city in cities]),
                         re.I)
    score = len(city_re.findall(affiliation))

    countries = location["country_codes"][:50]
    country_re = re.compile("|".join([r"(\b{0}\b)".format(re.escape(c))
                                      for c in countries]),
                            re.I)
    score += len(country_re.findall(affiliation))

    state = location["state"]
    if state is not None:
        score += len(re.findall(r"(\b{0}\b)".format(re.escape(state)),
                                affiliation, re.I))

    return score


if __name__ == "__main__":
    locations = load_locations()
    for l in locations:
        score = location_score("New York", l)
        if score > 0:
            print(score, l["city_names"][0] + ", " + l["country_codes"][0])
