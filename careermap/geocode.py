#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["geocode"]

import MySQLdb


def geocode(aff, min_affils=10):
    with MySQLdb.connect(host="localhost", user="root", db="ads") as c:
        c.execute("""SELECT affiliation, lat, lon, count,
            MATCH (affiliation) AGAINST (%s) AS score
            FROM affiliations
            WHERE count > %s AND MATCH (affiliation) AGAINST (%s)
            ORDER BY score DESC
            LIMIT 1
        """, (aff, min_affils, aff))

        result = c.fetchone()

    if result is None:
        return None

    return {
        "affiliation": result[0],
        "latlng": (float(result[1]), float(result[2])),
        "count": int(result[3]),
        "score": float(result[4]),
    }
