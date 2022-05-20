#!/usr/bin/env python3

import os
import subprocess
import sys

# Sometimes shell skips fork() as an optimization.
# https://unix.stackexchange.com/questions/466496/
if os.environ.get('SHELL_SKIPS_FORK'):
  filename = '/tmp/sysctl_restore_%d.sh' % os.getppid()
else:
  pppid = int(os.popen("ps -p %d -oppid=" % os.getppid()).read().strip())
  filename = '/tmp/sysctl_restore_%d.sh' % pppid

restore_file = open(filename, 'w')
print('#!/bin/bash', file=restore_file)

for a in sys.argv[1:]:
  sysctl = a.split('=')

  # save current value
  cur_val = subprocess.check_output(['cat', sysctl[0]], universal_newlines=True)
  print('echo "%s" > %s' % (cur_val.strip(), sysctl[0]), file=restore_file)

  # set new value
  cmd = 'echo "%s" > %s' % (sysctl[1], sysctl[0])
  os.system(cmd)

os.system('chmod u+x %s' % filename)
