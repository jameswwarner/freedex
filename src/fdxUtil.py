#!/usr/bin/env python
def cleanupSectorIndustry(fields):
    for i in [2,3]:
        if not fields[i]: fields[i] = "Unknown"
    pass

def lines(fName, skipLines, cleanup=None):
    toSkip = skipLines
    for line in open(fName):
        fields = line.strip().split("\t")
        if cleanup: cleanup(fields)
        if toSkip:
            #print fields
            toSkip -= 1
            continue
        yield fields
    pass


