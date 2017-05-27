# ! file mm5_class.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

"Reads mm5 I/O file extracting informations and meteo fields"

from os import stat
from time import mktime, localtime
from struct import pack, unpack, calcsize
from string import strip, rstrip, lower, replace
from numpy import ravel, shape, resize, array, reshape, transpose, take
import mm5_table


#
# UTILITIES
#
############
#
# INCTIME
#
def inctime(adate, xsec):

  """ ndate =  inctime(adate, xsec)

   Increments a reference date of xsec seconds
  """

  ttup = ( adate['year'], adate['month'], adate['day'], adate['hour'],
           adate['minute'], adate['second'], 0, 0, 1 )

  secs = mktime(ttup) + xsec
  ttup = localtime(secs)

  ndate = {
             'year'    : ttup[0],
             'month'   : ttup[1],
             'day'     : ttup[2],
             'hour'    : ttup[3],
             'minute'  : ttup[4],
             'second'  : ttup[5],
             'msec'    : 0
          }

  return ndate
#
# PDATE
#
def pdate(adate):

  """ fdate = pdate(adate)

   Formats a date string
  """

  fdate = ("%04d:%02d:%02d %02d:%02d:%02d.%04d" %
          (adate['year'], adate['month'], adate['day'], adate['hour'],
           adate['minute'], adate['second'], adate['msec']))

  return fdate
#
# FORTRAN_READ
#
def fortran_read(fp, nbyte):

  """ field = fortran_read(fp, nbyte)

   Reads nbyte from a fortran unformatted file (big endian)
  """

  if (nbyte <= 0): return -1

  big_nbyte = pack(">I", nbyte)

  try:
    check = fp.read(calcsize(">I"))
  except Exception, e:
    print "Error reading ", nbyte, " from file: ", e
    return -1

  if (check != big_nbyte):
    print "Error: block of data size is: ", check
    print "       requested byte are   : ", big_nbyte
    return -1

  try:
    buffer = fp.read(nbyte)
  except (IOError, EOFError), e:
    print "Error reading ", nbyte, " from file"
    return -1

  try:
    check = fp.read(calcsize(">I"))
  except (IOError, EOFError), e:
    print "Error reading ", nbyte, " from file"
    return -1

  if (check != big_nbyte):
    print "Error: File format error or not fortran unformatted file"
    return -1

  return buffer
#
# INTEGER_BIG_READ
#
def integer_big_read(fp):

  """ i = integer_big_read(fp)

   Reads an integer value from a big_endian file
  """

  try:
    value = fp.read(calcsize(">I"))
  except Exception, e:
    print "Error reading ", calcsize(">I"), " from file: ", e
    return -1

  value = unpack(">I", value)
  value = value[0]

  return value
#
# C2D
#
def c2d(c):

  """ f2d = c2d(f2c)

   Cross point to dot point interpolation
  """

  shc = shape(c)
  if (len(shc) < 3): raise RuntimeError, "Dimension error in c2d !"
  nic = shc[1]
  njc = shc[2]
  nid = nic + 1
  njd = njc + 1
  lic = nic - 1
  ljc = njc - 1
  lid = nic
  ljd = njc

  d=resize([1.0], (1, nid, njd))

  for i in xrange(1,nic):
    for j in xrange(1,njc):
      d[0][i][j] = 0.25*(c[0][i][j]+c[0][i-1][j]+c[0][i][j-1]+c[0][i-1][j-1])

  for i in xrange(1,nic):
    d[0][i][0]   = 0.5*(c[0][i][0]+c[0][i-1][0])
    d[0][i][ljd] = 0.5*(c[0][i][ljc]+c[0][i-1][ljc])

  for j in xrange(1,njc):
    d[0][0][j]   = 0.5*(c[0][0][j]+c[0][0][j-1])
    d[0][lid][j] = 0.5*(c[0][lic][j]+c[0][lic][j-1])

  d[0][0][0]       = c[0][0][0]
  d[0][0][ljd]     = c[0][0][ljc]
  d[0][lid][ljd]   = c[0][lic][ljc]
  d[0][lid][0]     = c[0][lic][0]

  return d
############
#
# MM5 Class
#
############

class mm5:

  " Main MM5 I/O format reader routines "

#
# CONSTRUCTOR
#
  def __init__(self, filename):

    """ a = mm5_class.mm5(filename)

     Opens a binary MM5 file checking version
    """

    self.filename = filename
    self.ctab = mm5_table.table()

    # Open file for binary reading

    try:
      self.fp = open(filename, "rb", 0)
    except IOError, e:
      print e
      raise RuntimeError, "Error opening mm5 binary file !!"

    # Check first word for version 

    check = integer_big_read(self.fp)
    if (check == -1):
      raise RuntimeError, "Error opening mm5 binary file !!"

    if (check == 3360000L):
      self.version = 2
      self.headersize = 3360000L
    elif (check == 4L):
      self.version = 3
      self.headersize = 117600L
    else:
      print "Version check error"
      raise RuntimeError, "Error opening mm5 binary file !!"

    if (self.extract_header() == -1):
      print "Cannot read mm5 header"
      raise RuntimeError, "Error opening mm5 binary file !!"

    if (self.extract_field_list() == -1):
      print "Cannot read field list"
      raise RuntimeError, "Error opening mm5 binary file !!"

    self.extract_reftime()
    self.extract_timeincrement()

    flen = stat(self.filename)
    flen = flen[6]
    if (self.version == 2):
      self.tsteps = int(flen / self.timesize)
    else:
      offset = (5*calcsize(">I")+self.headersize)
      flen = flen - offset
      self.tsteps = int(flen / (self.timesize - offset))

    self.extract_vertcoord()

    if (self.version == 2 and (self.prog_id == 6 or self.prog_id == 5)):
      self.extract_psdot()

    return
#
# EXTRACT_HEADER
#
  def extract_header(self):

    """ a.extract_header()

      Extracts MM5 header information storing them in a dictionary
    """

    # Go to file beginning

    self.fp.seek(0, 0)

    # Branch on version number

    if (self.version == 2):

      header = fortran_read(self.fp, self.headersize)
      if (header == -1): return -1

      # Unpack V2 header

      sizemif = 1000*20*calcsize("i")
      sizemrf = 1000*20*calcsize("f")
      sizemifc = 1000*20*80*calcsize("c")

      mif = unpack(">20000i", header[0:sizemif])
      mrf = unpack(">20000f", header[sizemif:sizemif+sizemrf])

      start = sizemif+sizemrf
      stop = sizemif+sizemrf+2*sizemifc
      lowcase = lower(header[start:stop])

      del header

      self.mm5_header = { "filename" : self.filename }

      start=0
      my_head   = self.mm5_header

      for i in xrange(20):
        for j in xrange(1000):
          ms = unpack(">80s", lowcase[start:start+80])
          sm = strip(ms[0])
          if (mif[i*1000+j] != -999):
            key = ('mif', j + 1, i + 1)
            my_head[key] = (sm , mif[i*1000+j])
          start = start + 80

      for i in xrange(20):
        for j in xrange(1000):
          ms = unpack(">80s", lowcase[start:start+80])
          sm = strip(ms[0])
          if (mrf[i*1000+j] != -999):
            key = ('mrf', j + 1, i + 1)
            my_head[key] = (sm , mrf[i*1000+j])
          start = start + 80

      del lowcase
      del mif
      del mrf

    elif (self.version == 3):

      # Check big header flag

      flag = fortran_read(self.fp, calcsize(">I"))
      if (flag == -1): return -1
      flag = unpack(">i", flag)
      flag = flag[0]

      if (flag == 0):
        header = fortran_read(self.fp, self.headersize)
        if (header == -1): return -1
      else:
        print "Error opening mm5 binary file !!"
        print "Format read error."
        return -1

      # Unpack V3 header

      sizebhi = 50*20*calcsize("i")
      sizebhr = 20*20*calcsize("f")
      sizebhic = 50*20*80*calcsize("c")
      sizebhrc = 20*20*80*calcsize("c")

      bhi = unpack(">1000i", header[0:sizebhi])
      bhr = unpack(">400f", header[sizebhi:sizebhi + sizebhr])

      start = sizebhi + sizebhr
      stop = sizebhi + sizebhr + sizebhic + sizebhrc
      lowcase = lower(header[start:stop])

      del header

      self.mm5_header = { "filename" : self.filename }

      start=0
      my_head   = self.mm5_header

      for i in xrange(20):
        for j in xrange(50):
          ms = unpack(">80s", lowcase[start:start+80])
          sm = strip(ms[0])
          if (bhi[i*50+j] != -999):
            key = ('bhi', j + 1, i + 1)
            my_head[key] = (sm , bhi[i*50+j])
          start = start + 80

      for i in xrange(20):
        for j in xrange(20):
          ms = unpack(">80s", lowcase[start:start+80])
          sm = strip(ms[0])
          if (bhr[i*20+j] != -999):
            key = ('bhr', j + 1, i + 1)
            my_head[key] = (sm , bhr[i*20+j])
          start = start + 80

      del lowcase
      del bhi
      del bhr

    else: return -1

    self.prog_id = self.get_val('prog_id')

    return 0
#
# EXTRACT_FIELD_LIST
#
  def extract_field_list(self):

    """ a.extract_field_list()

     Extracts MM5 fields information storing them in a dictionary
    """

    # Initialise

    self.fields = {}
    fp = self.fp

    # Branch on version number

    if (self.version == 2):

      start = self.headersize + 2 * calcsize(">I")
      fp.seek(start, 0)
      header = self.mm5_header

      pgi = self.prog_id
      num3d = header[('mif', 201, pgi)][1]
      num2d = header[('mif', 202, pgi)][1]
      num1d = header[('mif', 203, pgi)][1]
      num0d = header[('mif', 204, pgi)][1]
      total_num = num3d + num2d + num1d + num0d
      fstarti = ( 1, 1, 1, 1 )

      for i in xrange(total_num):

        # Extracts field information from V2 header

        fname = header[('mif', 205 + i, pgi)][0][0:8]
        fname = rstrip(fname)
        fname = replace(fname, " ", "_")
        funit = header[('mif', 205 + i, pgi)][0][9:25]
        funit = rstrip(funit)
        fdesc = header[('mif', 205 + i, pgi)][0][26:65]
        fdesc = rstrip(fdesc)
        fcoupl = header[('mif', 205 + i, pgi)][1] % 10
        fcross = header[('mif', 205 + i, pgi)][1] < 10
        fdims = 3
        if (pgi == 5 or pgi == 6):
          forder = 'YXS'
        else:
          forder = 'YXP'
        if (i > num3d): fdims = 2
        if (i > num3d + num2d): fdims = 1
        if (i > num3d + num2d + num1d): fdims = 0
        if (fdims > 1):
          dim_i = header[('mif', 104, 1)][1]
          dim_j = header[('mif', 105, 1)][1]
        else:
          dim_i = 1
          dim_j = 1

        # Walk first timestep and extract field positions

        fsize = integer_big_read(fp)
        if (fsize == -1):
          print "Format error in mm5 file: Error on record %d (%s)" % \
                i, fname
          return -1

        dim_k = int(fsize / (dim_i * dim_j * calcsize(">f")))

        fpos = fp.tell() - calcsize(">I")

        try:
          fp.seek(fsize, 1)
        except (IOError, EOFError), e:
          print "Format error in mm5 file: Error on record %d (%s)" % \
                i, fname
          print "Error :", e
          return -1

        check = integer_big_read(fp)
        if (check == -1):
          print "Format error in mm5 file: Error on record %d (%s)" % \
                i, fname
          return -1

        if (fsize != check):
          print "Format error in mm5 file: Error on record %d (%s)" % \
                i, fname
          return -1

        fstopj = ( dim_i, dim_j, dim_k, 1 )

        # Fill field dictionary

        self.fields[fname] = {'description' : fdesc,
                              'unit'        : funit,
                              'coupled'     : fcoupl,
                              'cross'       : fcross,
                              'position'    : fpos,
                              'size'        : fsize,
                              'ndims'       : fdims,
                              'start'       : fstarti,
                              'stop'        : fstopj,
                              'ordering'    : forder }

      self.timesize = fp.tell()

    elif (self.version == 3):

      # Reposition after Big Header

      start = self.headersize + 5 * calcsize(">I")
      fp.seek(start, 0)

      flag = fortran_read(fp, calcsize(">I"))
      if (flag == -1):
        print "Format error in mm5 file"
        return -1
      flag = unpack(">I", flag)
      flag = flag[0]

      subhsize = 9 * calcsize("i") + calcsize("f") + \
               112 * calcsize("c")

      # Loop on reading V3 subheaders
      # Walk first timestep and extract field positions

      while (flag == 1):

        subh = fortran_read(fp, subhsize)
        if (subh == -1):
          print "Format error in mm5 file"
          return -1

        subh = unpack(">i4i4if4s4s24s9s25s46s", subh)

        fsize = integer_big_read(fp)
        if (fsize == -1):
          print "Format error in mm5 file"
          return -1

        fpos = fp.tell() - calcsize(">I")

        try:
          fp.seek(fsize, 1)
        except (IOError, EOFError), e:
          print "Format error in mm5 file"
          return -1

        check =  integer_big_read(fp)
        if (check == -1):
          print "Format error in mm5 file"
          return -1

        if (fsize != check):
          print "Format error in mm5 file"
          return -1

        # Extract field information from subheader

        fname = replace(lower(rstrip(subh[13])), " ", "_")
        fdate = subh[12]
        fdesc = lower(rstrip(subh[15]))
        funit = rstrip(subh[14])
        fdims = subh[0]
        fstarti = (subh[1], subh[2], subh[3], subh[4])
        fstopj  = (subh[5], subh[6], subh[7], subh[8])
        forder  = rstrip(subh[11])
        fcoupl = 0
        fcross = (rstrip(subh[11]) == 'C')

        # Fill field dictionary

        self.fields[fname] = {'description' : fdesc,
                              'unit'        : funit,
                              'coupled'     : fcoupl,
                              'cross'       : fcross,
                              'position'    : fpos,
                              'time'        : fdate,
                              'size'        : fsize,
                              'ndims'       : fdims,
                              'start'       : fstarti,
                              'stop'        : fstopj,
                              'ordering'    : forder }

        flag = fortran_read(fp, calcsize(">I"))
        if (flag == -1):
          print "Format error in mm5 file"
          return -1
        flag = unpack(">I", flag)
        flag = flag[0]

      self.timesize = fp.tell()

    else:
      print "??? No version information ???"
      return

    return
#
# EXTRACT_REF_TIME
#
  def extract_reftime(self):

    """ a.extract_reftime()

     Extracts reference date from MM5 header
    """

    pgi = self.prog_id
    header = self.mm5_header

    if (self.version == 2):
      if (pgi == 1):
        self.reftime = { 'year' : 2000, 'month' : 1, 'day' : 1,
                         'hour' : 0, 'minute' : 0, 'second' : 0 , 'msec' : 0}
      elif (pgi < 5):
        self.reftime = { 'year' : header[('mif', 21, pgi)][1],
                         'month' : header[('mif', 22, pgi)][1],
                         'day' : header[('mif', 23, pgi)][1],
                         'hour' : header[('mif', 24, pgi)][1],
                         'minute' : header[('mif', 25, pgi)][1],
                         'second' : 0 , 'msec' : 0}
      elif (pgi == 5):
        self.reftime = { 'year' : header[('mif', 21, 2)][1],
                         'month' : header[('mif', 22, 2)][1],
                         'day' : header[('mif', 23, 2)][1],
                         'hour' : header[('mif', 24, 2)][1],
                         'minute' : header[('mif', 25, 2)][1],
                         'second' : 0 , 'msec' : 0}
      else:
        year = header[('mif', 16, pgi)][1] * 100 + \
               header[('mif', 15, pgi)][1]
        self.reftime = { 'year' : year,
                         'month' : header[('mif', 14, pgi)][1],
                         'day' : header[('mif', 13, pgi)][1],
                         'hour' : header[('mif', 12, pgi)][1],
                         'minute' : header[('mif', 11, pgi)][1],
                         'second' : 0 , 'msec' : 0}
    elif (self.version == 3):
      if (pgi == 1):
        self.reftime = { 'year' : 2000, 'month' : 1, 'day' : 1,
                         'hour' : 0, 'minute' : 0, 'second' : 0 , 'msec' : 0}
      else:
        self.reftime = { 'year' : header[('bhi', 5, pgi)][1],
                         'month' : header[('bhi', 6, pgi)][1],
                         'day' : header[('bhi', 7, pgi)][1],
                         'hour' : header[('bhi', 8, pgi)][1],
                         'minute' : header[('bhi', 9, pgi)][1],
                         'second' : header[('bhi', 10, pgi)][1],
                         'msec' : header[('bhi', 11, pgi)][1] }
    return
#
# EXTRACT_TIMEINCREMENT
#
  def extract_timeincrement(self):

    """ a.extract_timeincrement()

     Extract time increment information from header
    """

    pgi = self.prog_id
    header = self.mm5_header

    if (self.version == 2):
      if (pgi == 1): self.timeincrement = 0
      elif (pgi < 5):
        self.timeincrement = header[('mif', 5, pgi)][1] * 3600
      elif (pgi == 5):
        if (header.has_key(('mif', 5, 3))):
          self.timeincrement = header[('mif', 5, 3)][1] * 3600
        else:
          self.timeincrement = header[('mif', 5, 2)][1] * 3600
      else:
        self.timeincrement = int(header[('mrf', 302, pgi)][1]) * 60
    elif (self.version == 3):
      if (pgi == 1): self.timeincrement = 0
      else:
        self.timeincrement = int(header[('bhr', 1, pgi)][1])
    else:
      self.timeincrement = 0
    return
#
# EXTRACT_VERTCOORD
#
  def extract_vertcoord(self):

    """ a.extract_vertcoord()

      Extracts vertical level informations
    """

    self.vertcoord = {}
    pgid = self.prog_id
    header = self.mm5_header

    if (pgid == 1 or pgid == 4 or (self.version == 3 and pgid == 6)):
      lvf = {  'name'        : 'surface',
               'description' : 'surface variables',
               'unit'        : 'Pa',
               'nlevs'       : 1,
               'values'      : (1013,) }
    else:
      if (self.version == 2):
        if (pgid == 5 or pgid == 6):
          nlevs = int(header[('mrf', 101, pgid)][1])
          lvf = {  'name'        : 'sigma',
                   'description' : 'sigma coordinate',
                   'unit'        : 'sigma',
                   'nlevs'       : nlevs }
          levs = []
          for i in xrange(nlevs):
            levs.append(header[('mrf', 102 + i, pgid)][1])
          lvf['values'] = levs
        else:
          nlevs = header[('mif', 101, pgid)][1]
          lvf = {  'name'        : 'pressure',
                   'description' : 'pressure coordinate',
                   'unit'        : 'Pa',
                   'nlevs'       : nlevs }
          levs = []
          for i in xrange(nlevs):
            pval = float(header[('mif', 102 + i, pgid)][1]) * 100.0
            levs.append(pval)
          lvf['values'] = levs
      elif (self.version == 3):
        name = 'sigma'
        xlvf = self.get_field('sigmah', 0)
        if (xlvf == -1):
          name = 'pressure'
          xlvf = self.get_field('pressure', 0)
        lvf = {  'name'        : name,
                 'description' : xlvf['description'],
                 'unit'        : xlvf['units'],
                 'nlevs'       : xlvf['dim_ns'],
                 'values'      : ravel(xlvf['values']) }

    self.vertcoord = lvf

    return
#
# EXTRACT_PSDOT
#
  def extract_psdot(self):

    """ a.extract_psdot()

     For V2 and mm5 id 5 or 6, calculate pstar on dot point for decoupling
    """

    ps = self.get_field('pstarcrs', 0)
    self.pstarcrs = ps['values']
    self.pstardot = c2d(self.pstarcrs)
    del ps
    return
#
# GET_VERSION
#
  def get_version(self):

    """ vers = a.get_version()

      Return MM5 version number
    """

    return self.version
#
# GET_PROGRAM_ID
#
  def get_program_id(self):

    """ pgid = a.get_program_id()

     Return MM5 program id
    """

    return self.prog_id
#
# GET_VAL
#
  def get_val(self, key):

    """ val = a.get_val(key)

     Retrieve mm5 header information
     See class mm5_table for key informations
    """

    key_h = self.ctab.get_key(key, self.version)
    try:
      value = self.mm5_header[key_h][1]
    except Exception:
      value = 'absent'

    return value
#
# GET_FIELD_LIST
#
  def get_field_list(self):

    """ dict = get_field_list()

     Returns MM5 field list for the file
    """

    return self.fields
#
# GET_REF_TIME
#
  def get_reftime(self):

    """ rftime = a.get_reftime()

     Returns MM5 reference time for the file
    """

    return self.reftime
#
# GET_TIMEINCREMENT
#
  def get_timeincrement(self):

    """ timeinc = a.get_timeincrement()

     Returns MM5 time increment between timesteps for the file
    """

    return self.timeincrement
#
# GET_HEADER
#
  def get_header(self):

    """ head = a.get_header()

      Returns MM5 header information for the file
    """

    return self.mm5_header
#
# GET_FIELD
#
  def get_field(self, fname, timestep):

    """ field = a.get_field(fname, timestep)

     Retrieves meteo field from MM5 file
    """

    fp=self.fp

    try:
      finfo = self.fields[fname]
    except Exception:
      return -1

    if (timestep < 0):
      print "Negative timestep ?"
      return -1

    if (timestep > self.tsteps - 1):
      print "Start date is: ", pdate(self.reftime) 
      print "Total number of timesteps is:  ", self.tsteps, \
            "(from 0 to", self.tsteps - 1, ")"
      return -1

    position = finfo['position']
    size     = finfo['size']
    start    = position + timestep * self.timesize

    if (self.version == 3 and timestep > 0):
      start = start - timestep * (5*calcsize(">I")+self.headersize)

    try:
      fp.seek(start, 0)
    except (IOError, EOFError):
      print "Format error in mm5 file: Error on timestep ", timestep
      return -1

    field = fortran_read(fp, size)
    if (field == -1):
      print "Format error in mm5 file: Error on timestep ", timestep
      return -1

    format   = size / calcsize(">f")
    format   = ">%df" % format
    try:
      field    = unpack(format, field)
    except Exception:
      print "Format error or beyond file limits"
      return -1

    dim_ns   = 1 + finfo['stop'][0] - finfo['start'][0]
    dim_ew   = 1 + finfo['stop'][1] - finfo['start'][1]
    dim_z    = 1 + finfo['stop'][2] - finfo['start'][2]
    act_time = inctime(self.reftime, self.timeincrement * timestep)

    xfield = { 'name'        : fname,
               'description' : finfo['description'],
               'units'       : finfo['unit'],
               'refdate'     : self.reftime,
               'date'        : pdate(act_time),
               'cross'       : finfo['cross'],
               'dim_z'       : dim_z  }
    if (self.version == 2):
      xfield['fullsigma'] = dim_z > self.vertcoord['nlevs']
    else:
      xfield['fullsigma'] = 0

    # Transpose output

    xvalue = reshape(array(field), (dim_z, dim_ew, dim_ns))
    xvalue = transpose(xvalue, (0, 2, 1))

    # Remove last line and last row for cross fields

    if (finfo['cross']):
      dim_ns = dim_ns - 1
      dim_ew = dim_ew - 1
      xvalue = take(xvalue, xrange(0,dim_ns), 1)
      xvalue = take(xvalue, xrange(0,dim_ew), 2)

    xfield['dim_ns'] = dim_ns
    xfield['dim_ew'] = dim_ew

    if (finfo['coupled']):
      xfield['units'] = xfield['units'][4:]
      if (finfo['cross']):
        for k in xrange(dim_z):
          xvalue[k] = xvalue[k]/self.pstarcrs[0]
      else:
        for k in xrange(dim_z):
          xvalue[k] = xvalue[k]/self.pstardot[0]

    xfield['values'] = xvalue

    del field
    return xfield
#
# GET_VERTCOORD
#
  def get_vertcoord(self):

    """ levels = a.get_vertcoord()

     Returns vertical coordinate
    """

    return self.vertcoord
#
# PRINT_HEADER
#
  def print_header(self):

    """ a.print_header()

     Prints out MM5 header informations
    """

    item = self.mm5_header.items()
    item.sort()
    for i in xrange(len(self.mm5_header)):
     print item[i]
    del item
    return
#
# PRINT_FIELD_LIST
#
  def print_field_list(self):

    """ a.print_field_list()

     Prints out MM5 field list informations
    """

    item = self.fields.items()
    item.sort()
    for i in xrange(len(self.fields)):
     print item[i]
    del item
    return

#
# DESTRUCTOR
#
  def __del__(self):

    """ a.del()

     Close a binary mm5 file
    """

    try:
      del self.mm5_header
      del self.fields
      del self.ctab
      self.fp.close()
    except:
      pass

__path__ = ''

