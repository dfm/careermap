#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["compare_addresses"]

from math import sqrt
from collections import defaultdict


def compare_addresses(ad1, ad2):
    d1 = defaultdict(int)
    for word in ad1.split():
        d1[word] += 1
    norm1 = sqrt(sum([w*w for w in d1.values()]))

    d2 = defaultdict(int)
    for word in ad2.split():
        d2[word] += 1
    norm2 = sqrt(sum([w*w for w in d2.values()]))

    score = sum([d1[k] * d2[k] for k in set(d1.keys() + d2.keys())])

    return score / norm1 / norm2


if __name__ == "__main__":
    print(compare_addresses("Center for Cosmology and Particle Physics, Department of Physics, New York University, 4 Washington Place, New York, NY 10003, USA",
                            "Department of Computer Science, University of Toronto, 6 King's College Road, Toronto, Ontario, M5S 3G4 Canada"))
