import maya.standalone
maya.standalone.initialize()

import maya.mel as mmel
import pymel.core as pmc

fileName = 'D:/Data/modelimport/head_dev_no_red_50000_2.mb'
fileName = 'D:/Data/modelimport/head_smalltest_for_animation_script.mb'
# ipdb.set_trace()

openCode = r'file -f -options "v=0;"  -ignoreVersion  -typ "mayaBinary" -o "'+fileName+'";';
mmel.eval(openCode)

a1 = ['select -r head1;',
'makeCollideNCloth;',
'file -save;',
'file -f -new;']
a1.append(openCode)

for c in a1:
	print c
	mmel.eval(c)

src = r"D:\Data\modelimport\code\setattr.mel"
srcFile = open(src)
mmel.eval(srcFile.read())


mmel.eval('file -save')
