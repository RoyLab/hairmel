import maya.mel as mmel
import pymel.core as pmc
import ipdb

fileName = 'D:/Data/modelimport/head_dev_no_red_50000_b.mb'
#fileName = 'D:/Data/modelimport/head_smalltest_for_animation_script.mb'


cmds = [r'file -f -options "v=0;"  -ignoreVersion  -typ "mayaBinary" -o "'+fileName+'";',\
	r'select -r head1',\
	r'select -add curve',\
	r'makeCurvesDynamic 2 { "1", "1", "0", "0", "1"};',\
	r'file -save']

# ipdb.set_trace()

mmel.eval(cmds[0])
mmel.eval(cmds[1])

for i in xrange(50000):
	mmel.eval(cmds[2]+str(i+1))

print "selection complete!\n"
	
for cmd in cmds[3:]:
	mmel.eval(cmd)
