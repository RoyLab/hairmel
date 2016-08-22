
'''Globals'''
sampleRate = 1
stdFile = r"D:\Data\modelimport\code\std.mb"
outputFile = r"D:\Data\modelimport\code\test.mb"
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
        for i in xrange(20):
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

    # checking
    state = 2
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'"')

    # setup
    state = 3
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "' + fullPath(state) + '"')

    # rest state computing
    state = 4
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mcmd.playbackOptions(animationStartTime=0)
        mcmd.playbackOptions(animationEndTime=20)
        #mcmd.play(f=True)
        mcmd.bakeResults('pfxHair1', simulation=True, t=(0, 20), disableImplicitControl=True, sb=1, shape=True, cp=True)

        # use openMaya to set the frame - cmds.currentTime does not
        # stick in standalone:
        import maya.OpenMaya as om
        om.MGlobal.viewFrame(20)
        mel.eval('source "'+fullPath(state)+'"')


    # animation and rendering
    state = 5
    if begin <= state and end >= state:
        if begin == state:
            openFile()
        mel.eval('source "'+fullPath(state)+'"')