#!/usr/bin/env python

import sys
import os
import re
import py_compile

def getpath(msg, expect):
  " Manage user input defaults "
  ok = 0
  while (not ok):
    try:
      s = raw_input(mesg)
    except KeyboardInterrupt:
      print "\nSuspended as requested."
      sys.exit(-1)
    if (s != ""): expect = s
    print "You entered: ", expect
    try:
      s = raw_input("Are you sure? [N/y]: ")
    except KeyboardInterrupt:
      print "\nSuspended as requested."
      sys.exit(-1)
    if (s == 'y' or s == 'Y' or s == 'YES' or s == 'yes'):
      ok = 1
  return expect

def xmkdir(pth):
  if (not os.path.isdir(pth)):
    if (os.path.isfile(pth)):
      print "Sorry, this is a regular file !"
      print "Installing NOT OK"
      sys.exit(-1)
    try:
      os.makedirs(pth)
    except:
      print "Sorry, cannot create ", pth, " directory !"
      print "Installing NOT OK"
      sys.exit (-1)
  return

##############################################################

print " "
print "Installing MM5 I/O Library."
print " "

# Try to find default python site-packages directory

rex = re.compile(r'/[/\S]+site-packages')
libpth = `sys.path`
libpth = re.findall(rex,libpth)
libpth = libpth[0]
mesg = "Library directory [" + libpth + "] is: "
libpth = getpath(mesg, libpth)

binpth = '/usr/local/bin'
mesg = "Binary directory [/usr/local/bin] is: "
binpth = getpath(mesg, binpth)

etcpth = '/usr/local/etc/pymm5'
mesg = "Conf files directory [/usr/local/etc/pymm5] is: "
etcpth = getpath(mesg, etcpth)

docpth = '/usr/local/doc/pymm5'
mesg = "Documentation files directory [/usr/local/doc/pymm5] is: "
docpth = getpath(mesg, docpth)

libpth = os.path.abspath(os.path.expanduser(libpth))
binpth = os.path.abspath(os.path.expanduser(binpth))
etcpth = os.path.abspath(os.path.expanduser(etcpth))
docpth = os.path.abspath(os.path.expanduser(docpth))

xmkdir(libpth)
xmkdir(binpth)
xmkdir(etcpth)
xmkdir(docpth)

# Adjust path in source files

rex = re.compile(r'/usr/atmo/etc/rgb.txt')
txt = open('lib/MM5/wgif.py').read()
extr = rex.sub(os.path.normpath(etcpth)+'/rgb.txt',txt)
x = open('lib/MM5/wgif.py', 'w').write(extr)
rex = re.compile(r'/usr/atmo/etc')
txt = open('bin/mm5_ground').read()
extr = rex.sub(os.path.normpath(etcpth)+'/Station.txt',txt)
x = open('bin/mm5_ground', 'w').write(extr)

command = "cp -R ./lib/* " + libpth + " 2> /dev/null"
print "Copying library files ..."
res = os.system(command)
if (res != 0):
  print "Sorry, check permission on directory ", libpth
  print "Installing NOT OK"
  sys.exit(-1)

print "Compiling them ..."
libpth = libpth + "/MM5"
print 'Listing', libpth
names = os.listdir(libpth)
names.sort()
for name in names:
  fullname = os.path.join(libpth, name)
  if os.path.isfile(fullname):
    head, tail = name[:-3], name[-3:]
    if tail == '.py':
      print "Compiling ", name
      try:
        py_compile.compile(fullname, None, None)
      except KeyboardInterrupt:
        raise KeyboardInterrupt
      except:
        if type(sys.exc_type) == type(''):
          exc_type_name = sys.exc_type
        else: exc_type_name = sys.exc_type.__name__
        print 'Sorry:', exc_type_name + ':',
        print sys.exc_value
        sys.exit(-1)

print " "
print "Installing Binaries."
print " "

print "Copying Binaries..."

print "Listing ./bin"
names = os.listdir("./bin")
names.sort()
for name in names:
  command = "cp ./bin/" + name + " " + binpth
  ret = os.system(command)
  if (res != 0):
    print "Sorry, check permission on directory ", binpth
    print "Installing NOT OK"
    sys.exit(-1)
  try:
    os.chmod(binpth + '/' + name, 0755)
  except:
    print "Sorry, cannot chmod file ", binpth + name, " !"
    print "Installing NOT OK"
    sys.exit(-1)

print "Listing ./etc"
names = os.listdir("./etc")
names.sort()
for name in names:
  command = "cp ./etc/" + name + " " + etcpth
  ret = os.system(command)
  if (res != 0):
    print "Sorry, check permission on directory ", etcpth
    print "Installing NOT OK"
    sys.exit(-1)

print "Listing ./doc"
names = os.listdir("./doc")
names.sort()
for name in names:
  command = "cp ./doc/" + name + " " + docpth
  ret = os.system(command)
  if (res != 0):
    print "Sorry, check permission on directory ", docpth
    print "Installing NOT OK"
    sys.exit(-1)

print " "
print "MM5 I/O Software successfully installed on your system."
print "Remember to add to your path environment variable the directory:"
print " "
print "    ", binpth
print " "
print "Good Luck !"
print " "

sys.exit(0)
