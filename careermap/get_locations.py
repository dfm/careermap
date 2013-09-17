#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["get_locations"]

from geocode import geocode
from ads import get_author_locations


def get_locations(name):
    affils = get_author_locations(name)
    if not len(affils):
        return []
    print(affils)
    locations = map(geocode, affils.values())
    return locations


if __name__ == "__main__":
    print(get_locations("Foreman-Mackey"))
