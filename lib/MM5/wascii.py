# ! file wascii.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for ASCII output "

import mm5_proj

def write(fieldname, input, timestep):

  "Transforms mm5 input to Ascii file"

  field = input.get_field(fieldname, timestep)
  if (field == -1):
    return -1

  outdat = fieldname + `timestep` + '.asc'

  dim_ns   = field['dim_ns']
  dim_ew   = field['dim_ew']
  dim_z    = field['dim_z']
  arrfield = field['values']

  if (field['cross']):
    offset = 1.00
  else:
    offset = 0.500

  levels = input.get_vertcoord()
  nlevs = levels['nlevs']
  levval = levels['values']

  proj = mm5_proj.projection(input)

  try:
    fout = open(outdat, "w")
  except Exception, e:
    print "Cannot open output file: ", e
    return -1

  header = 'MM5 file : ' + input.filename + '\n'
  header = header + "variable : " + field['name'] + '\n'
  header = header + "description : " + field['description'] + '\n'
  header = header + "units : " + field['units'] + '\n'
  header = header + "date : " + field['date'] + '\n'
  header = header + "dimensions : " + `nlevs` + ' '
  header = header + `dim_ns` + ' ' + `dim_ew` + '\n'
  fout.write(header)

  for k in xrange(dim_z):
    if (dim_z == 1):
      levstr = 'LEVEL ' + 'surface variable\n'
    else:
      levstr = 'LEVEL ' + `levval[k]` + ' ' + levels['unit'] + '\n'
    fout.write(levstr)
    for i in xrange(dim_ns):
      for j in xrange(dim_ew):
        (lat,lon) = proj.ij_to_latlon(i+offset,j+offset)
        valstr = 'LAT = ' + `lat` + ' '
        valstr = valstr + 'LON = ' + `lon` + ' '
        valstr = valstr + '(' + `i+1` + ',' + `j+1` + ') '
        valstr = valstr + fieldname + ' = ' + `arrfield[k][i][j]` + '\n'
        fout.write(valstr)

  fout.close()

  del field
  del levels
  del header
  del arrfield

  return 0

__path__ = ''

