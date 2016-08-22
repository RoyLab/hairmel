import maya.standalone
maya.standalone.initialize()

import maya.mel as mel
mel.eval('source "namedCommandSetup.mel";')

import pymel.core as pm

def func(b, e=None):
	from traindata import runMain
	runMain(b,e)