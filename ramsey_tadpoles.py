# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 08:12:08 2014

@author: combinatorist
"""

# outline
# 0. should output the format:
#         cntrd, chord1cntrd, chord2cntrd, note
# 1. check that both chords (i.e., their product) are relatively prime to p.
# 2. generate the even powers, watching for the chords to show up.
# 3. if either chord shows up, mark other chord found (by overlap contradiction)
# 4. if both chords were found, return overlap contradiction
# 5. now run odd powers for every chord not found.
# 6. if chord generates an even power or its inverse, mark it found, undirected
# 7. if both chords are found, mark complete
# 8. return contradictions found

# todo:
# * Optimize the contradiction finder and make a verbose explanation function.

from math import sqrt

def proof(chord1, chord2, modulus):
    """Find the first tadpole Ramsey number contradiction. Based on m-1, n-1"""

    #NB: Should I check that neither graph is a pan graph????
    generator = chord1 * chord2
    cntrd, chord1cntrd, chord2cntrd = False, False, False

    if not coprime(generator, modulus):
        note = 'chord product is not relatively prime to p'
        return cntrd, chord1cntrd, chord2cntrd, note

    evenpows = modpows(generator, modulus)
    # Find chord1 in evenpows to get contradiction for chord2 and vice versa
    chord2cntrd = evenpows.count(chord1) > 0
    chord1cntrd = evenpows.count(chord2) > 0

    overlapcntrds = [chord1cntrd, chord2cntrd].count(True)
    if overlapcntrds == 2:
        cntrd = True
        note = 'overlap contradiction'
        return cntrd, chord1cntrd, chord2cntrd, note

    eveninverses = modinverses(evenpows, modulus)
    evenchords = evenpows + eveninverses
    if not chord1cntrd:
        odd1pows = oddpows(evenpows, chord1, modulus)
        for power in odd1pows:
            if evenchords.count(power) > 0:
                chord1cntrd = True
    if not chord2cntrd:
        odd2pows = oddpows(evenpows, chord2, modulus)
        for power in odd2pows:
            if evenchords.count(power) > 0:
                chord2cntrd = True

    undredgcntrds = [chord1cntrd, chord2cntrd].count(True) - overlapcntrds
    note1 = str(overlapcntrds) + ' overlap contradict\'s, '
    note2 = str(undredgcntrds) + ' undirected edge contradict\'s'
    cntrd = chord1cntrd and chord2cntrd

    return cntrd, chord1cntrd, chord2cntrd, note1 + note2


def coprime(x, y):
    """checks that two integers are relatively prime"""

    small, big = min(x, y), max(x, y)
    iscoprime = True
    if big % small == 0:
        iscoprime = False
    else:
        for z in range(2, int(sqrt(small)) + 1):
            if small % z == 0:
                if big % z == 0 or big % (small / z) == 0:
                    iscoprime = False
                    break

    return iscoprime


def modpows(generator, modulus):
    """"Finds all powers of a generator in a given mod"""
    powers = []
    current = 1

    for _ in range(modulus):
        current = generator * current % modulus
        powers.append(current)
        if current in (1, 0):
            break

    return powers


def oddpows(evenpows, chord, modulus):
    """Finds odd powers for a chord in a given mod. Enter evenpows as list"""
    return [evenpow * chord % modulus for evenpow in evenpows]


def modinverses(values, modulus):
    """Finds the inverses in the modulus. Only takes normalized values."""
    return [modulus - value for value in values]
