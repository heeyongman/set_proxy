#!/usr/bin/python3
import os
import re
res = os.popen("ps -aux|grep brook").readlines()
pid_re = re.compile("(?<=\['he).*?(\d+)")
pid = re.search(pid_re, str(res)).group(1)
os.system("kill -9 %s" % pid)

cmd = "notify-send 'proxy stopped'"
os.system(cmd)
