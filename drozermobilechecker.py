#!/usr/bin/env python

###############################################################################################################
## [Title]: drozermobilechecker.py -- an Information Gathering tool for mobile apps based on Drozer framework
## [Author]: Razvan-Costin Ionescu
##-------------------------------------------------------------------------------------------------------------
## [Details]:
## This script is intended to be executed locally on a Linux box to enumerate basic informations about a
## mobile application installed on a test device. The device should be connected to the Linux box, using
## adb and Drozer.
##-------------------------------------------------------------------------------------------------------------
## [Prerequisites]:
## You need a Drozer server running on the Linux box, a Drozer agent installed on the testing device, and adb
## connection working.
##-------------------------------------------------------------------------------------------------------------
## [Output]:
## The script is intended to offer you a short overview about a tested application, which are its PERMISSIONS,
## the possible attack surface (including content providers, intent filters etc).
###############################################################################################################

import sys
from commands import *


# title / formatting
bigline = "================================================================================================="
smlline = "-------------------------------------------------------------------------------------------------"
cmd_root = 'drozer console connect -c '


print bigline
print "DROZER MOBILE PENTEST CHECKER"
print bigline
print



# Setup checking
def check_setup():
    cmd_check = '\"run information.datetime\"'
    print cmd_root + cmd_check
    if (getstatusoutput(cmd_root + cmd_check)[0] != 0):
        print "Something went wrong! Check your drozer server - agent setup"
        print smlline
        print bigline
        sys.exit(0)
    else:
        print str(getstatusoutput(cmd_root + cmd_check)[1])+"\n"
        print "Setup is OK!"
        print smlline
        print

def exec_cmd(cmd):
    print cmd_root + cmd
    if (getstatusoutput(cmd_root + cmd)[0] != 0):
        print str(cmd_root + cmd)+" command failed"
        print smlline
    else:
        print str(getstatusoutput(cmd_root + cmd)[1])+"\n"
        print smlline
        print

PACK = sys.argv[1]
#Let the party started!
print "[*] CHECKING THE SETUP FIRST...\n"
print smlline
print
check_setup()

print "[*] TESTED PACKAGE: %s"%PACK
print smlline
print

print "[*] PACKAGE RELATED INFORMATION...\n"
print smlline
cmd = '\"run app.package.info -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.package.backup -f %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.package.debuggable -f %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.package.launchintent %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.package.manifest %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.package.native %s\"'%PACK
exec_cmd(cmd)
print smlline

print "[*] INFORMATION GATHERING MODULES...\n"
print smlline
cmd = '\"run app.activity.info -u -i -v -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.broadcast.info -u -v -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.provider.info -u -v -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run app.service.info -u -i -v -a %s\"'%PACK
exec_cmd(cmd)
print smlline

print "[*] ATTACK SURFACE...\n"
print smlline
cmd = '\"run app.package.attacksurface %s\"'%PACK
exec_cmd(cmd)
print smlline

print "[*] SCANNERS...\n"
print smlline
cmd = '\"run scanner.activity.browsable -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run scanner.misc.native -v -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run scanner.provider.finduris -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run scanner.provider.injection -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run scanner.provider.sqltables -a %s\"'%PACK
exec_cmd(cmd)
cmd = '\"run scanner.provider.traversal -a %s\"'%PACK
exec_cmd(cmd)
print smlline

print "[*] CONTENT PROVIDERS...\n"
print smlline
cmd = '\"run app.provider.finduri %s\"'%PACK
exec_cmd(cmd)
print smlline

print bigline
print "Done!"
