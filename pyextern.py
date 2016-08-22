import sys
sys.path.append(r'C:\Program Files\Autodesk\Maya2015\Python\Lib\site-packages')

import maya.standalone
maya.standalone.initialize()

import maya.mel as mel
mel.eval('source "namedCommandSetup.mel";')

print "Try to import pymel:"
import pymel.core as pm

def func(b, e=None):
	from traindata import runMain
	runMain(b,e)