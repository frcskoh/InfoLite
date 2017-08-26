from os import chdir, system
import sys
chdir(sys.argv[1])
system('python %s' % ('receive.py'))
