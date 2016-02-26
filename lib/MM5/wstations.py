# ! file wstations.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for rain data. "

import mm5_class
import mm5_proj
from math import log, exp, hypot, atan2
from string import split

def write(input, timestep, stzcode, lat, lon):

  "Transforms mm5 input to file with rain data. "

  if (len(lat) != len(lon)):
    print "Inconsistent lat-lon pairs !"
    return -1;

  terrain = input.get_field('terrain', timestep)
  if (terrain == -1):
    return -1
  terr = terrain['values']

  rain_tot = input.get_field('rain_tot', timestep)
  if (rain_tot == -1):
    print "Warning: Summing rain_con and rain_non"
    rain_con = input.get_field('rain_con', timestep)
    if (rain_con == -1):
      print "Sorry, no precipitation data in file !"
      return -1
    rain_non = input.get_field('rain_non', timestep)
    if (rain_non == -1):
      print "Sorry, no precipitation data in file !"
      return -1
    rain_tot = rain_con
    rain_tot['values'] = rain_tot['values'] + rain_non['values']
    rain_tot['name'] = 'rain_tot'
    rain_tot['description'] = 'Accumulated Total Rain'

  ground_t = input.get_field('ground_t', timestep)
  if (ground_t == -1):
    return -1

  mydat = split(rain_tot['date'], ':')
  hour = split(mydat[2], ' ')
  outdat = mydat[0] + mydat[1] + hour[0] + '_' + hour[1] + '.asc'

  dim_ns = rain_tot['dim_ns']
  dim_ew = rain_tot['dim_ew']
  dim_z = rain_tot['dim_z']

  levels = input.get_vertcoord()
  nlevs = levels['nlevs']
  levval = levels['values']

  proj = mm5_proj.projection(input)
  rain = rain_tot['values']
  temp = ground_t['values']

  try:
    fout = open(outdat, "w")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

# interpol = proj.nearval
  interpol = proj.blinval
# interpol = proj.lwval
# interpol = proj.cubconval

  header = '% MM5 file : ' + input.filename + '\n'
  header = header + "% date : " + rain_tot['date'] + '\n'
  header = header + "% dimensions : " + `nlevs` + ' '
  header = header + `dim_ns` + ' ' + `dim_ew` + '\n'
  header = header + '% CODE  LAT   LON    HGT       RAIN   TEMP\n'
  fout.write(header)

  for i in xrange(len(lat)):
    rval = interpol(lat[i],lon[i],rain[0],1.0)
    rter = interpol(lat[i],lon[i],terr[0],1.0)
    rtem = interpol(lat[i],lon[i],temp[0],1.0)
    fout.write(" %s %5.2f %5.2f %7.2f %9.4f %7.2f\n" % \
               (stzcode[i],lat[i],lon[i],rter,rval,rtem))

  fout.close()

  del rain
  del terr
  del temp
  del levels
  del header

  return 0

__path__ = ''

