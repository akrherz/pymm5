# ! file wraob.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for a raob sounding profile. "

import mm5_class
import mm5_proj
from math import log, exp, hypot, atan2, sin, cos, fmod
from string import split, atoi

def crh(t,q,prs):
  "Calculates rh given t, q, prs"
  if (t >= 273.15):
    es=6.112*exp(17.67*((t-273.15)/(t-29.65)))
  else:
    es=6.11*exp(22.514-(6150./t))
  es = es * 100.0
  qs=0.622*es/(prs-es)
  return(q/qs)

def tc(t):
  "Temperature in centigrades"
  return (t - 273.15)

def cprs(sigma,ptop,pp,ps):
  "Calculates pressure at given sigma"
  return((ps*sigma)+ptop+pp)

def hgt(sigma,ptop,bslp,bslt,blr,ter):
  "Calculates geopotential hgt"
  g = 9.81; r = 287.04;
  ps0 = bslp * exp((-1.*bslt/blr)+((((bslt/blr)**2.) - \
        (2.*g*(ter/(blr*r))))**0.5))
  ps0=ps0-ptop
  phydro=ps0*sigma+ptop
  z = -1.*(((r*blr/2./g)*((log(phydro/bslp)**2))) + \
      ((r*bslt/g)*log(phydro/bslp)))
  return z-ter

def write(input, start, nstep, lat, lon):

  "Transforms mm5 input to raob sound"

  levels = input.get_vertcoord()
  levval = levels['values']

  proj   = mm5_proj.projection(input)
  (i,j)  = proj.latlon_to_ij(lat,lon)

# interpol = proj.nearval
  interpol = proj.blinval
# interpol = proj.lwval
# interpol = proj.cubconval

  terrain = input.get_field('terrain', 0)
  if (terrain == -1):
    return -1
  terr = interpol(lat,lon,terrain['values'][0],1.0)

  mydat = split(terrain['date'], ':')
  hour = split(mydat[2], ' ')
  outdat = mydat[0] + mydat[1] + hour[0] + hour[1] + '.asc'
  del terrain

  try:
    fout = open(outdat, "w")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

  icount = 1
  for timestep in xrange(start,start+nstep):
    nlevs = levels['nlevs']

    t = input.get_field('t', timestep)
    if (t == -1):
      return -1
    rt = []
    for k in xrange(nlevs):
      rt.append(interpol(lat,lon,t['values'][k],1.0))

    mydat = split(t['date'], ':')
    hour = split(mydat[2], ' ')

    if (levels['name'] == 'sigma'):
      ptop = input.get_val('ptop')
      if (input.version == 2): ptop = ptop * 100.0
      bslp = input.get_val('basestateslp')
      bslt = input.get_val('basestateslt')
      blr  = input.get_val('basestatelapserate')

      ps = input.get_field('pstarcrs',timestep)
      if (ps == -1):
        return -1
      rps = interpol(lat,lon,ps['values'][0],1.0)
      if (input.version == 2): rps = rps * 1000.0
      pp = input.get_field('pp', timestep)
      if (pp == -1):
        return -1
      q = input.get_field('q',timestep)
      if (q == -1):
        return -1
      rprs = []
      rrh = []
      rhg = []
      for k in xrange(nlevs-1,-1,-1):
        rpp = interpol(lat,lon,pp['values'][k],1.0)
        rq  = interpol(lat,lon,q['values'][k],1.0)
        xp  = cprs(levval[k],ptop,rpp,rps)
        rprs.append(xp)
        rrh.append(crh(rt[k],rq,xp))
        rhg.append(hgt(levval[k],ptop,bslp,bslt,blr,terr) * 0.001)
      del pp
      del q
      rrt = []
      for k in xrange(nlevs-1,-1,-1):
        rrt.append(tc(rt[k]))
      for k in xrange(nlevs):
        rprs[k] = rprs[k] * 0.01
    else:
      rh = input.get_field('rh', timestep)
      if (rh == -1):
        return -1
      hg = input.get_field('h', timestep)
      if (hg == -1):
        return -1
      rprs = []
      rrh  = []
      rhg  = []
      rrt = []
      for k in xrange(nlevs):
        rprs.append(levval[k] * 0.01)
        rrh.append(interpol(lat,lon,rh['values'][k],1.0) * 0.01)
        rhg.append(interpol(lat,lon,hg['values'][k],1.0) * 0.001)
        rrt.append(tc(rt[k]))
      del rh
      del hg
      htp = rhg.pop(0); xx = rrh.pop(0);
      xx = rprs.pop(0); xx = rrt.pop(0);
      nlevs = nlevs - 1;
      while (rhg[0] < htp):
        xx = rhg.pop(0);  xx = rrh.pop(0);
        xx = rprs.pop(0); xx = rrt.pop(0);
        nlevs = nlevs - 1;

    icloud = 0
    for k in xrange(nlevs):
      if (rrh[k] > 0.9): icloud = 1

    year  = atoi(mydat[0]) - 1900
    if (year >= 100): year = year - 100
    month = atoi(mydat[1])
    day   = atoi(hour[0])
    hour  = atoi(hour[1])
    istat = 242
    irain = 0
    header = ('%2d%2d%2d%2d%3d %3d%2d%2d%7d%6.2f%6.2f\n' %
            (year,month,day,hour,nlevs,istat,icloud,irain,icount,lat,lon))
    icount = icount + 1
    fout.write(header)

    for k in xrange(nlevs):
      valstr = ('%6.1f %6.3f %6.1f %5.3f\n' % \
                 (rprs[k],rhg[k],rrt[k],rrh[k]))
      fout.write(valstr)

  fout.close()

  del levels
  del header

  return 0

__path__ = ''

