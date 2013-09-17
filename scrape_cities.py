#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup


def parse_coords(coords, nw):
    """
    Example: 79°59′N	85°56′W
    """
    try:
        pre, suff = coords.split(u"°")
        am, d = suff.split(u"′")
        return [1.0, -1.0][nw.index(d)] * float(pre) + float(am) / 60.
    except ValueError:
        return None


def scrape_cities():
    r = requests.get("http://en.wikipedia.org/wiki/List_of_cities_by_latitude")
    # do you need this if statement?  I thought "raise_for_status" makes this "if" redundant
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    results = []
    tree = BeautifulSoup(r.text)
    for table in tree.find_all("table"):
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 4:
                city = cols[2].text.split(",")
                country = cols[3].text[1:]
            elif len(cols) == 5:
                city = [cols[2].text, cols[3].text[1:]]
                country = cols[4].text[1:]
            else:
                continue

            lat = parse_coords(cols[0].text, nw="NS")
            lng = parse_coords(cols[1].text, nw="EW")
            results.append({
                "city": city[0],
                "state": None,
                "country": country,
                "latlng": [lat, lng]
            })
            if len(city) > 1:
                results[-1]["state"] = city[1]
    return results


if __name__ == "__main__":
    json.dump(scrape_cities(), open("coordinates.json", "w"),
              indent=2, separators=(",", ": "))
