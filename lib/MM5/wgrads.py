# ! file wgrads.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for GrADS output "

import string
import mm5_proj
from math import fabs

def gradsdate(adate):

  "Formats date for grads ctl file"

  months = ( 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
             'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC' )

  gdate = string.split(adate, ':')
  gdate[2] = string.split(gdate[2])
  imon = int(gdate[1]) - 1

  fdate = "%2s:%2sZ%2s%3s%4s" % (gdate[2][1], gdate[3], 
           gdate[2][0], months[imon], gdate[0])

  return fdate

def write(fieldname, input, timestep):

  "Transforms mm5 input to Grads file"

  field = input.get_field(fieldname, timestep)
  if (field == -1):
    return -1

  proj = mm5_proj.projection(input)

  outdat = fieldname + `timestep` + '.dat'
  outctl = fieldname + `timestep` + '.ctl'

  dim_ns = field['dim_ns']
  dim_ew = field['dim_ew']

  griddist = input.get_val('grid_distance')
  if (input.version == 2): griddist = griddist * 1000.0

  cenind_ns = (float(dim_ns) * 0.50)
  cenind_ew = (float(dim_ew) * 0.50)

  (clat,clon) = proj.ij_to_latlon(cenind_ns, cenind_ew)


  if (field['cross']):
    offset = 1.000
  else:
    offset = 0.500
    cenind_ns = cenind_ns + 0.500
    cenind_ew = cenind_ew + 0.500

  levels = input.get_vertcoord()
  nlevs = levels['nlevs']
  levval = levels['values']

  (minlat, minlon) = proj.ij_to_latlon(offset, offset)
  (maxlat, maxlon) = proj.ij_to_latlon(dim_ns, dim_ew)

  maxew = float(dim_ew - 1) + offset
  maxns = float(dim_ns - 1) + offset
  for i in xrange(dim_ns):
    (lat,lon) = proj.ij_to_latlon(i+offset,offset)
    if (lon < minlon): minlon = lon
    (lat,lon) = proj.ij_to_latlon(i+offset,maxew)
    if (lon > maxlon): maxlon = lon
  for j in xrange(dim_ew):
    (lat,lon) = proj.ij_to_latlon(offset,j+offset)
    if (lat < minlat): minlat = lat
    (lat,lon) = proj.ij_to_latlon(maxns,j+offset)
    if (lat > maxlat): maxlat = lat

  if (maxlon < 0.0 and minlon > 0.0): maxlon = maxlon + 360.0
  reslat = (maxlat - minlat) / (2.0 * float(dim_ns))
  reslon = (maxlon - minlon) / (2.0 * float(dim_ew))
  nbins_ns = 2 * dim_ns + 1
  nbins_ew = 2 * dim_ew + 1

  griddist = "%9.2f" % griddist
  mlat  = `minlat`
  rlat  = `reslat`
  mlon  = `minlon`
  rlon  = `reslon`
  glevs = `nlevs`

  ctl = 'dset ' + outdat + '\n'
  ctl = ctl + 'title ' + fieldname + '\n'
  ctl = ctl + 'undef -9999.0\n'
  ctl = ctl + 'pdef ' + `dim_ew` + ' ' + `dim_ns`
  ctl = ctl + ' lcc ' + `clat` + ' ' + `clon` + ' '
  ctl = ctl + `cenind_ew` + ' ' + `cenind_ns` + ' '
  ctl = ctl + `input.get_val('stdlat1')` + ' '
  ctl = ctl + `input.get_val('stdlat2')` + ' '
  ctl = ctl + `input.get_val('coarse_cenlon')` + ' '
  ctl = ctl + griddist + ' ' + griddist + '\n'
  ctl = ctl + 'xdef ' + `nbins_ew` + ' linear ' + mlon + ' ' + rlon + '\n'
  ctl = ctl + 'ydef ' + `nbins_ns` + ' linear ' + mlat + ' ' + rlat + '\n'
  if (nlevs == 1):
    ctl = ctl + 'zdef 1 levels 1013.0\n'
  else:
    ctl = ctl + 'zdef ' + glevs + ' levels\n'
    for i in xrange(nlevs):
      ctl = ctl + '      ' + ("%9.4f" % (levval[i] * 0.01)) + '\n'
  if (input.timeincrement == 0):
    ctl = ctl + 'tdef 1 linear 00Z00JAN2000 1MN\n'
  else:
    mydat = gradsdate(field['date'])
    ctl = ctl + 'tdef 1 linear ' + mydat + '     '
    ctl = ctl + `(input.timeincrement / 60)` + 'MN\n'
  ctl = ctl + 'vars 1\n'
  ctl = ctl + fieldname + ' ' + glevs + ' 99 '
  ctl = ctl + field['description'] + ' ' + field['units'] + '\n'
  ctl = ctl + 'endvars\n'

  try:
    fout = open(outdat, "wb")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

  field['values'] = field['values'].astype('f')
  fout.write(field['values'].tostring())
  fout.close()

  try:
    fout = open(outctl, "w")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

  fout.write(ctl)
  fout.close()

  del field
  del levels
  del ctl

  return 0

__path__ = ''

