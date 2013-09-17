#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import MySQLdb

c = MySQLdb.connect(host="localhost", user="root", db="ads")
cursor = c.cursor()

cursor.execute("DROP TABLE affiliations")
cursor.execute("""CREATE TABLE IF NOT EXISTS affiliations (
    id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    affiliation TEXT,
    lat DECIMAL(10,7),
    lon DECIMAL(10,7),
    count INT UNSIGNED,
    FULLTEXT (affiliation)
) ENGINE=MyISAM;
""")

cursor.execute("""INSERT INTO affiliations (affiliation, lat, lon, count)
    SELECT affiliation, lat, lon, COUNT(affiliation)
    FROM authors
    WHERE lat IS NOT NULL AND lon IS NOT NULL
    GROUP BY affiliation
""")
