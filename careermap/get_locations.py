#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["get_locations"]

from geocode import geocode
from ads import get_author_locations


def get_locations(name):
    affils = get_author_locations(name)
    print(affils)
    if not len(affils):
        return []
    locations = []
    for year, affiliation in affils:
        if year is None:
            continue

        loc = geocode(affiliation)
        if loc is None:
            continue

        locations.append({
            "year": year,
            "affiliation": loc["affiliation"],
            "latlng": loc["latlng"],
        })
    return sorted(locations, key=lambda l: int(l["year"]))


if __name__ == "__main__":
    print(get_locations("Angus, R"))
