#!/bin/env python
from sys import argv
try:
    from subprocess import check_output
except ImportError:
    from subprocess import Popen
    from subprocess import PIPE
    def check_output(command):
        return Popen(command, stdout=PIPE).communicate()[0]

log = argv[1]
modules = set()
for line in file(log):
    if line.startswith('ERROR: Python module'):
        module = line.split()[3]
        modules.add(module.split('.')[0])
for module in modules:
    out_module = check_output(['yum', 'provides', '/usr/lib*/python*/site-packages/%s/__init__.py' % module])
    if 'Filename' in out_module:
        print "For %s:::\n%s" % (module, out_module)
        continue
    else:
        out_module = check_output(['yum', 'provides', '/usr/lib*/python*/site-packages/%s.py' % module])
        if 'Filename' in out_module:
            print "For %s:::\n%s" % (module, out_module)
        else:     
            print "For %s::: NOTHING" % module
