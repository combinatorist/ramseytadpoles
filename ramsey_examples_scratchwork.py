#This is a module from scratch to help with Ramsey numbers

def tadpole(chord1, chord2, modulus):
    """Find the first tadpole Ramsey number contradiction. Based on m-1, n-1"""

#Shouldn't I build something in to check that neither graph is a pan graph????
    generator = chord1 * chord2
    cntrd, chord1cntrd, chord2cntrd = False, False, False

    if coprime(generator, modulus):
        note = 'chord product is not relatively prime to p'
        return(cntrd, chord1cntrd, chord2cntrd, note)

    evenpows = modpows(generator, modulus)
    print(evenpows)
    if evenpows.count(chord1) > 0:
        chord2cntrd = True  #Yes, find chord1 to get contradiction for chord2
    if evenpows.count(chord2) > 0:
        chord1cntrd = True

    overlapcntrds = [chord1cntrd, chord2cntrd].count(True)
    if overlapcntrds == 2:
        cntrd = True
        note = 'overlap contradiction'
        return(cntrd, chord1cntrd, chord2cntrd, note)

    eveninverses = modinverses(evenpows, modulus)
    print(eveninverses)
    evenchords = evenpows + eveninverses
    if not chord1cntrd:
        print('chord1 odd powers')
        odd1pows = oddpows(evenpows, chord1, modulus, printlist=True)
        for pow in odd1pows:
            if evenchords.count(pow) > 0:
                chord1cntrd = True
    if not chord2cntrd:
        print('chord2 odd powers')
        odd2pows = oddpows(evenpows, chord2, modulus, printlist=True)
        for pow in odd2pows:
            if evenchords.count(pow) > 0:
                chord2cntrd = True

    undredgcntrds = [chord1cntrd, chord2cntrd].count(True) - overlapcntrds
    note1 = str(overlapcntrds) + ' overlap contradict\'s, '
    note2 = str(undredgcntrds) + ' undirected edge contradict\'s'
    cntrd = chord1cntrd and chord2cntrd

    return(cntrd, chord1cntrd, chord2cntrd, note1 + note2)


'''outline
0. should output the format:
        cntrd, chord1cntrd, chord2cntrd, note
1. check that both chords (i.e., their product) is relatively prime to p.
2. generate the even powers, watching for the chords to show up.
3. if either chord shows up, mark other chord as found in overlap contradiction
4. if both chords were found, return overlap contradiction
5. now run odd powers for every chord not found.
6. if chord generates an even power or its inverse, mark it found, undirected
7. if both chords are found, mark complete
8. return contradictions found
'''

#Optimize the contradiction finder and make a verbose explanation function.