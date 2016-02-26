# ! file wgif.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Output routine for ascii output. "

import Image
import ImagePalette
import ImageFilter
from Numeric import ravel, Int32

def write(fieldname, input, timestep):

  "Transforms mm5 input to GIF file"

  field = input.get_field(fieldname, timestep)
  if (field == -1):
    return -1

  outdat = fieldname + `timestep`

  dim_ns = field['dim_ns']
  dim_ew = field['dim_ew']
  dim_z = field['dim_z']

  dim_k = dim_z

  arrfield = field['values']
  for k in xrange(dim_k):
    maxval = max(ravel(arrfield[k]))
    minval = min(ravel(arrfield[k]))
    rprec  = (maxval - minval) / 255.0
    arrfield[k] = (arrfield[k] - minval) / rprec

  arrfield = arrfield.astype(Int32)

  try:
    palette = ImagePalette.load('rgb.txt')
  except:
    print "Using System color palette."
    print "To use your own color palette, copy the file /disk1/utenti/giuliani/python_mm5/pillo/etc/rgb.txt"
    print "in this directory and modify as needed."
    palette = ImagePalette.load('/disk1/utenti/giuliani/python_mm5/pillo/etc/rgb.txt')

  for k in xrange(dim_k):
    outname = outdat + '_' + `k` + '.gif'
    try:
      img = Image.fromstring("I", (dim_ew, dim_ns), arrfield[k].tostring())
    except (ValueError, IOError), e:
      print "Cannot convert to GIF: ", e
      return -1
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = img.transpose(Image.ROTATE_180)
    img = img.convert("L")
    img = img.resize((dim_ew*8, dim_ns*8))
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.putpalette(palette)
    try:
      img.save(outname, "GIF")
    except IOError, e:
      print "Cannot write GIF file: ", e
      return -1

  del field
  del arrfield
  del img

  return 0

__path__ = ''

