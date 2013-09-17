#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["geocode"]

import requests

google_url = "https://maps.googleapis.com/maps/api/geocode/json"
mq_url = "http://open.mapquestapi.com/geocoding/v1/address"


def google_geocode(affiliation):
    params = {
        "sensor": "false",
        "address": affiliation,
    }
    r = requests.get(google_url, params=params)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    results = r.json().get("results", None)
    if results is None or not len(results):
        return None

    location = results[0]["geometry"]["location"]
    return (location["lat"], location["lng"])


def mapquest_geocode(location):
    params = {
        "location": location,
        "maxResults": 1,
        "thumbMaps": False
    }

    r = requests.get(mq_url, params=params)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    results = r.json().get("results", None)
    if results is None or not len(results):
        return None

    locs = results[0].get("locations", [])
    if not len(locs):
        return None

    latlng = locs[0].get("latLng", {})

    return (latlng["lat"], latlng["lng"])


if __name__ == "__main__":
    print(mapquest_geocode("Center for Cosmology and Particle Physics, Department of Physics, New York University, 4 Washington Place, New York, NY 10003, USA"))
