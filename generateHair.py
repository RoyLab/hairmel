import numpy
import pymel.core as pmc
import pyhair
'''Globals'''
sampleRate = 1

'''Class Defs'''
class HairGeometry:
    def __init__(self, hair):
        self.hairCount = hair[2]
        self.pointCount = hair[3]
        self.position = hair[0].reshape((-1, 3))
        self.segment = hair[1]

'''Scripts'''
#hair = HairGeometry(pyhair.loadHair(r"D:\Data\modelimport\wWavyThin.hair"))
hair = HairGeometry(pyhair.loadHairZhou(r"D:\hair project\models\curly.hair"))
posPtr = 0
for i in xrange(hair.hairCount):
    segLength = hair.segment[i]
    if i % sampleRate == 0:
        pmc.curve(p=hair.position[posPtr:posPtr+segLength].tolist())
    posPtr += segLength