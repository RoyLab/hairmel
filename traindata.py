
'''Globals'''
sampleRate = 1
stdFile = r"D:\Data\modelimport\code\std.mb"
outputFile = r"D:\Data\modelimport\code\test50k2.mb"
hairModelFile = r"D:\hair project\models\curly.hair"
scriptPath = r"D:\Data\modelimport\code"
scriptSource = ["genHair","checking","setupAttr","rest","anim"]

import os
import pymel.core as pmc
import maya.mel as mel
import maya.cmds as mcmd

import pyhair

'''Class Defs'''
class HairGeometry:
    def __init__(self, hair):
        self.hairCount = hair[2]
        self.pointCount = hair[3]
        self.position = hair[0].reshape((-1, 3))
        self.segment = hair[1]

def unixPath(str):
    return str.replace('\\', '/')

def openFile():
    src = 'file -f -options "v=0;"  -ignoreVersion  -typ "mayaBinary" -o "' + unixPath(outputFile) + '";'
    mel.eval(src)

def newFile():
    src = 'file -f -new;'
    mel.eval(src)

def saveFile():
    src = 'file -save;'
    mel.eval(src)

def fullPath(i):
    return unixPath(scriptPath)+'/'+scriptSource[i-1] # -1 is offset relative to state

def runMain(begin, end=None):

    if end == None:
        end = begin

    state = 0
    # import hair curve
    if begin <=state and end >=state:
        copyCmd = "copy " + stdFile + ' ' + outputFile;
        os.system(copyCmd)
        openFile()
        hair = HairGeometry(pyhair.loadHairZhou(hairModelFile))
        posPtr = 0
        for i in xrange(hair.hairCount):
            segLength = hair.segment[i]
            if i % sampleRate == 0:
                pmc.curve(p=hair.position[posPtr:posPtr+segLength].tolist())
            posPtr += segLength
        saveFile()

    # convert curve to hair
    state = 1
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'"')
        print "Convert curve to hair...done!"

    # checking
    state = 2
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'"')
        print "Checking...done!"

    # setup
    state = 3
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "' + fullPath(state) + '"')
        print "Setup parameters...done!"

    # rest state computing
    state = 4
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'"')
        print "Rest state computing...done!"

    # animation and rendering
    state = 5
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'";')
        for i in range(2):
            mel.eval('cacheAndRender('+str(i+1)+')')
        print "Animation and rendering...done!"
