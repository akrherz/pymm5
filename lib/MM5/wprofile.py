# ! file wprofile.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for wind profile. "

import mm5_class
import mm5_proj
from math import log, exp, hypot, atan2, sin, cos, fmod
from string import split

def write(input, timestep, lat, lon):

  "Transforms mm5 input to Ascii file"

  u = input.get_field('u', timestep)
  if (u == -1):
    return -1
  v = input.get_field('v', timestep)
  if (v == -1):
    return -1
  w = input.get_field('w', timestep)
  if (w == -1):
    return -1

  mydat = split(u['date'], ':')
  hour = split(mydat[2], ' ')
  outdat = mydat[0] + mydat[1] + hour[0] + '_' + hour[1] + '.asc'

  dim_ns = u['dim_ns']
  dim_ew = u['dim_ew']
  dim_z  = u['dim_z']

  levels = input.get_vertcoord()
  nlevs  = levels['nlevs']
  levval = levels['values']

  proj   = mm5_proj.projection(input)
  (i,j)  = proj.latlon_to_ij(lat,lon)
  ufield = u['values']
  vfield = v['values']
  wfield = w['values']

  try:
    fout = open(outdat, "w")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

# interpol = proj.nearval
  interpol = proj.blinval
# interpol = proj.lwval
# interpol = proj.cubconval

  terrain = input.get_field('terrain', 0)
  if (terrain == -1):
    return -1
  myterr = mm5_class.c2d(terrain['values'])
  terr = interpol(lat,lon,myterr[0],0.5)

  header = '% MM5 file : ' + input.filename + '\n'
  header = header + "% date : " + u['date'] + '\n'
  header = header + "% dimensions : " + `nlevs` + ' '
  header = header + `dim_ns` + ' ' + `dim_ew` + '\n'
  header = header + '% terrain elevation : ' + `terr` + '\n'
  header = header + '% latitude,longitude : '+repr(proj.ij_to_latlon(i,j))+'\n'
  header = header + '% i,j : '+repr((i,j))+'\n'

  for k in xrange(nlevs):
    wfield[k] = (wfield[k] + wfield[k+1]) * 0.50

  if (levels['name'] == 'sigma'):
    header = header + '%     LEVEL ELEVATION INTENSITY DIRECTION    NORMAL\n'
    fout.write(header)
    g = 9.81
    r = 287.04
    ptop = input.get_val('ptop')
    if (input.version == 2): ptop = ptop * 100.0
    base_state_slp = input.get_val('basestateslp')
    base_state_slt = input.get_val('basestateslt')
    base_state_lapse_rate = input.get_val('basestatelapserate')

    for k in xrange(nlevs):
      ps0 = base_state_slp * exp( (-1.*base_state_slt/base_state_lapse_rate)+ \
            (( ((base_state_slt/base_state_lapse_rate)**2.)- \
            (2.*g*(terr/(base_state_lapse_rate*r))))**0.5))
      ps0=ps0-ptop
      phydro=ps0*levval[k]+ptop
      z = -1.*(  ((r*base_state_lapse_rate/2./g)* \
          ((log(phydro/base_state_slp)**2))) +
          ((r*base_state_slt/g)*log(phydro/base_state_slp)))
      uval = interpol(lat,lon,ufield[k],0.5)
      vval = interpol(lat,lon,vfield[k],0.5)
      xlonc = input.get_val('coarse_cenlon')
      xlatc = input.get_val('coarse_cenlat')
      xlonr = xlonc - lon
      if (xlonr > 180.0): xlonr=xlonr-360.0
      if (xlonr < -180.0): xlonr=xlonr+360.0
      angle = xlonr*input.get_val('conefac')*0.017453292519943
      if (xlatc < 0.0): angle=-angle
      uval = vval*sin(angle)+uval*cos(angle)
      vval = vval*cos(angle)-uval*sin(angle)
      intensity = hypot(uval,vval)
      direction = fmod(270.0-(atan2(vval,uval)*57.2957795130823208852),360.0)
      normal = interpol(lat,lon,wfield[k],0.5)
      height = z-terr
      valstr = ('  %9.4f %9.2f %9.2f %9.2f %9.4f\n' % \
               (levval[k],height,intensity,direction,normal))
      fout.write(valstr)
  else:
    header = header + '%     LEVEL INTENSITY DIRECTION    NORMAL\n'
    fout.write(header)
    for k in xrange(nlevs):
      uval = interpol(lat,lon,ufield[k],0.5)
      vval = interpol(lat,lon,vfield[k],0.5)
      xlonc = input.get_val('coarse_cenlon')
      xlatc = input.get_val('coarse_cenlat')
      xlonr = xlonc - lon
      if (xlonr > 180.0): xlonr=xlonr-360.0
      if (xlonr < -180.0): xlonr=xlonr+360.0
      angle = xlonr*input.get_val('conefac')*0.017453292519943
      if (xlatc < 0.0): angle=-angle
      uval = vval*sin(angle)+uval*cos(angle)
      vval = vval*cos(angle)-uval*sin(angle)
      intensity = hypot(uval,vval)
      direction = fmod(270.0-(atan2(vval,uval)*57.2957795130823208852),360.0)
      normal = interpol(lat,lon,wfield[k],0.5)
      valstr = ('  %9.4f %9.2f %9.2f %9.4f\n' % \
               (levval[k],intensity,direction,normal))
      fout.write(valstr)

  fout.close()

  del u
  del v
  del ufield
  del vfield
  del levels
  del header

  return 0

__path__ = ''

