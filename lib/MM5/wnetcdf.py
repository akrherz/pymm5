# ! file wnetcdf.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output Routine for NetCDF output. "

import string
import mm5_proj
import nc
from math import fabs

def write(fieldname, input, timestep):

  "Transforms mm5 input to NetCDF file"

  field = input.get_field(fieldname, timestep)
  if (field == -1):
    return -1
  date = field['date']
  dlen = len(field['date'])

  proj = mm5_proj.projection(input)
# interpol = proj.nearval
# interpol = proj.blinval
  interpol = proj.lwval
# interpol = proj.cubconval

  outdat = fieldname + `timestep` + '.nc'

  levels = input.get_vertcoord()
  nlevs = levels['nlevs']
  levval = levels['values']
  if (levels['unit'] == 'sigma'):
    for k in xrange(nlevs):
      levval[k] = levval[k] * 1000.0
      levels['unit'] = 'sigma_level'
  else:
    for k in xrange(nlevs):
      levval[k] = levval[k] * 0.01
      levels['unit'] = 'mb'

  dim_ns = field['dim_ns']
  dim_ew = field['dim_ew']
  dim_z  = field['dim_z']
  if (field['cross']):
    offset = 1.000
  else:
    offset = 0.500

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

  xlat = []
  xlon = []
  for i in xrange(nbins_ns):
    xlat.append(minlat + i * reslat)
  for j in xrange(nbins_ew):
    xlon.append(minlon + j * reslon)

  fld = []
  for k in xrange(dim_z):
    for i in xrange(nbins_ns):
      for j in xrange(nbins_ew):
        fld.append(interpol(xlat[i],xlon[j],field['values'][k],offset))

  a = nc.create(outdat,nc.CLOBBER)

  a.def_dim('timelen', dlen)
  a.def_dim('level', dim_z)
  a.def_dim('latitude', nbins_ns)
  a.def_dim('longitude', nbins_ew)
  a.def_att('Title','',nc.CHAR,'MM5 output file')
  a.def_var('level',nc.FLOAT,('level'))
  a.def_att('_units','level',nc.CHAR,levels['unit'])
  a.def_att('units','level',nc.CHAR,levels['unit'])
  a.def_var('latitude',nc.FLOAT,('latitude'))
  a.def_att('_units','latitude',nc.CHAR,'degree_north')
  a.def_att('units','latitude',nc.CHAR,'degree_north')
  a.def_var('longitude',nc.FLOAT,('longitude'))
  a.def_att('_units','longitude',nc.CHAR,'degree_east')
  a.def_att('units','longitude',nc.CHAR,'degree_east')
  a.def_var('time',nc.CHAR,('timelen'))
  a.def_att('_units','time',nc.CHAR,'formatted')
  a.def_att('units','time',nc.CHAR,'formatted')
  a.def_var(fieldname,nc.FLOAT,('level','latitude','longitude'))
  a.def_att('_units',fieldname,nc.CHAR,field['units'])
  a.def_att('units',fieldname,nc.CHAR,field['units'])
  a.def_att('missing_value',fieldname,nc.FLOAT,1e20)
  a.def_att('long_name',fieldname,nc.CHAR,field['description'])
  a.endef()

  time = a.var('time')
  hgt = a.var('level')
  lat = a.var('latitude')
  lon = a.var('longitude')
  xfld = a.var(fieldname)

  time[0:dlen] = date
  lat[0:nbins_ns] = xlat
  lon[0:nbins_ew] = xlon
  if (dim_z > 1):
    hgt[0:dim_z] = levval[0:dim_z]
  else:
    hgt[0] = 0.0
  xfld[0:dim_z] = fld

  a.close()

  del field
  del fld
  del levels

  return 0

__path__ = ''

