# ! file mm5_table.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Table for MM5 metadata informations. "

class table:

  """ Table for MM5 metadata informations. """

  def __init__(self):

    """ a = mm5_table.table()

     Constructor
    """

    self.table = {
            'prog_id'            : (('mif', 1, 1),   ('bhi', 1, 1)),
            'coarse_dim_i'       : (('mif', 2, 1),   ('bhi', 5, 1)),
            'coarse_dim_j'       : (('mif', 3, 1),   ('bhi', 6, 1)),
            'map_proj'           : (('mif', 4, 1),   ('bhi', 7, 1)),
            'exp_flag'           : (('mif', 5, 1),   ('bhi', 8, 1)),
            'exp_dim_i'          : (('mif', 6, 1),   ('bhi', 9, 1)),
            'exp_dim_j'          : (('mif', 7, 1),   ('bhi', 10, 1)),
            'exp_off_i'          : (('mif', 8, 1),   ('bhi', 11, 1)),
            'exp_off_j'          : (('mif', 9, 1),   ('bhi', 12, 1)),
            'usgs_wat'           : (('mif', 11, 1),  ('bhi', 23, 1)),
            'dom_id'             : (('mif', 101, 1), ('bhi', 13, 1)),
            'mother_id'          : (('mif', 102, 1), ('bhi', 14, 1)),
            'nest_lvl'           : (('mif', 103, 1), ('bhi', 15, 1)),
            'grid_dim_i'         : (('mif', 104, 1), ('bhi', 16, 1)),
            'grid_dim_j'         : (('mif', 105, 1), ('bhi', 17, 1)),
            'sw_mother_i'        : (('mif', 106, 1), ('bhi', 18, 1)),
            'sw_mother_j'        : (('mif', 107, 1), ('bhi', 19, 1)),
            'coarse_ratio'       : (('mif', 108, 1), ('bhi', 20, 1)),
            'mother_ratio'       : (('mif', 109, 1), ('bhi', 21, 1)),
            'tw_flag'            : (('mif', 110, 1), ('bhi', 24, 1)),
            'smoother_flag'      : (('mif', 111, 1), ('bhi', 22, 1)),
            'emisphere_flag'     : (('mif', 112, 1), ('absent')),
            'coarse_grid_d'      : (('mrf', 1, 1),   ('bhr', 1, 1)),
            'coarse_cenlat'      : (('mrf', 2, 1),   ('bhr', 2, 1)),
            'coarse_cenlon'      : (('mrf', 3, 1),   ('bhr', 3, 1)),
            'conefac'            : (('mrf', 4, 1),   ('bhr', 4, 1)),
            'stdlat1'            : (('mrf', 5, 1),   ('bhr', 5, 1)),
            'stdlat2'            : (('mrf', 6, 1),   ('bhr', 6, 1)),
            'polepos_lat'        : (('mrf', 7, 1),   ('bhr', 7, 1)),
            'approx_exp'         : (('mrf', 8, 1),   ('bhr', 8, 1)),
            'grid_distance'      : (('mrf', 101, 1), ('bhr', 9, 1)),
            'sw_coarse_i'        : (('mrf', 102, 1), ('bhr', 10, 1)),
            'sw_coarse_j'        : (('mrf', 103, 1), ('bhr', 11, 1)),
            'ne_coarse_i'        : (('mrf', 104, 1), ('bhr', 12, 1)),
            'ne_coarse_j'        : (('mrf', 105, 1), ('bhr', 13, 1)),
            'terdata_res'        : (('mrf', 106, 1), ('bhr', 14, 1)),
            'landdata_res'       : (('mrf', 107, 1), ('bhr', 15, 1)),
            'ifirst'             : (('mif', 6, 2),   'absent'),
            'sstsrc'             : (('mif', 7, 2),   'absent'),
            'ihemis'             : (('mif', 8, 2),   'absent'),
            'ptop'               : (('mrf', 1, 2),   ('bhr', 2, 2)),
            'ifac'               : ('absent',        ('bhi', 13, 3)),
            'iwtscm'             : (('mif', 7, 3),   ('bhi', 14, 3)),
            'iwind'              : (('mif', 8, 3),   ('bhi', 15, 3)),
            'iwt'                : (('mif', 9, 3),   ('bhi', 16, 3)),
            'smooth'             : (('mif', 10, 3),  ('bhi', 17, 3)),
            'noblnd'             : (('mif', 11, 3),  ('bhi', 18, 3)),
            'rwsubm'             : (('mif', 12, 3),  ('bhi', 19, 3)),
            'isfc'               : (('mif', 13, 3),  ('bhi', 20, 3)),
            'fddasf'             : (('mif', 14, 3),  ('bhi', 21, 3)),
            'intf4d'             : ('absent',        ('bhi', 22, 3)),
            'lagtem'             : (('mif', 16, 3),  ('bhi', 23, 3)),
            'fddauwindflag'      : (('mif', 6, 4),   'absent'),
            'fddavwindflag'      : (('mif', 7, 4),   'absent'), 
            'fddatflag'          : (('mif', 8, 4),   'absent'), 
            'fddaqflag'          : (('mif', 9, 4),   'absent'), 
            'fddapsflag'         : (('mif', 10, 4),  'absent'), 
            'fddarhflag'         : (('mif', 11, 4),  'absent'), 
            'fddapslvflag'       : (('mif', 12, 4),  'absent'), 
            'fddatobboxflag'     : (('mif', 13, 4),  'absent'), 
            'hydroflag'          : (('mif', 5, 5),   'absent'), 
            'basestateslp'       : (('mrf', 2, 5),   ('bhr', 2, 5)), 
            'basestateslt'       : (('mrf', 3, 5),   ('bhr', 3, 5)), 
            'basestatelapserate' : (('mrf', 4, 5),   ('bhr', 4, 5)), 
            'basestatestratot'   : ('absent',        ('bhr', 5, 5)),
            'idry'               : (('mif', 3, 6),   'absent'), 
            'imoist'             : (('mif', 4, 6),   'absent'), 
            'inhyd'              : (('mif', 5, 6),   'absent'), 
            'itgflg'             : (('mif', 6, 6),   'absent'), 
            'iice'               : (('mif', 7, 6),   'absent'), 
            'inav'               : (('mif', 8, 6),   'absent'), 
            'iiceg'              : (('mif', 9, 6),   'absent'), 
            'maxmv'              : (('mif', 10, 6),  ('bhi', 3, 14)), 
            'ifrest'             : (('mif', 301, 6), ('bhi', 1, 12)), 
            'ixtimr'             : (('mif', 302, 6), ('bhi', 2, 12)), 
            'ifsave'             : (('mif', 303, 6), ('bhi', 3, 12)), 
            'iftape'             : (('mif', 304, 6), ('bhi', 4, 12)), 
            'maschk'             : (('mif', 305, 6), ('bhi', 5, 12)), 
            'ifrad'              : (('mif', 306, 6), ('bhi', 1, 13)), 
            'icustb'             : (('mif', 307, 6), ('bhi', 24, 13)), 
            'iexice'             : (('mif', 308, 6), 'absent'), 
            'ifdry'              : (('mif', 309, 6), ('bhi', 14, 13)), 
            'imvdif'             : (('mif', 310, 6), ('bhi', 7, 13)), 
            'ibmoist'            : (('mif', 311, 6), ('bhi', 26, 13)), 
            'ifogmd'             : ('absent',        ('bhi', 27, 13)),
            'icor3d'             : (('mif', 312, 6), ('bhi', 12, 13)), 
            'ifupr'              : (('mif', 313, 6), ('bhi', 13, 13)), 
            'iboudy'             : (('mif', 314, 6), ('bhi', 15, 13)), 
            'ibltyp'             : (('mif', 315, 6), ('bhi', 4, 13)), 
            'idry'               : (('mif', 316, 6), 'absent'), 
            'imoist'             : (('mif', 317, 6), 'absent'), 
            'icupa'              : (('mif', 318, 6), ('bhi', 2, 13)), 
            'issflx'             : (('mif', 319, 6), ('bhi', 17, 13)), 
            'itgflg'             : (('mif', 320, 6), ('bhi', 18, 13)), 
            'isfpar'             : (('mif', 321, 6), ('bhi', 19, 13)), 
            'icloud'             : (('mif', 322, 6), ('bhi', 20, 13)), 
            'icdcon'             : (('mif', 323, 6), ('bhi', 21, 13)), 
            'ifsnow'             : (('mif', 324, 6), ('bhi', 16, 13)), 
            'imoiav'             : (('mif', 325, 6), ('bhi', 25, 13)), 
            'ivmixm'             : (('mif', 326, 6), ('bhi', 22, 13)), 
            'ievap'              : (('mif', 327, 6), ('bhi', 23, 13)), 
            'ishallo'            : (('mif', 328, 6), ('bhi', 6, 13)), 
            'ioverw'             : (('mif', 329, 6), ('bhi', 1, 14)), 
            'imove'              : (('mif', 330, 6), ('bhi', 4, 14)), 
            'imovco'             : (('mif', 331, 6), ('bhi', 5, 14)), 
            'ifeed'              : (('mif', 332, 6), ('bhi', 2, 14)), 
            'iabsor'             : (('mif', 333, 6), 'absent'), 
            'i4d3d'              : (('mif', 334, 6), ('bhi', 1, 16)), 
            'iwind3d'            : (('mif', 335, 6), ('bhi', 2, 16)), 
            'itemp3d'            : (('mif', 336, 6), ('bhi', 3, 16)), 
            'imois3d'            : (('mif', 337, 6), ('bhi', 4, 16)), 
            'irot'               : (('mif', 338, 6), ('bhi', 5, 16)), 
            'i4dsfc'             : (('mif', 339, 6), ('bhi', 6, 16)), 
            'iwindsfc'           : (('mif', 340, 6), ('bhi', 7, 16)), 
            'itempsfc'           : (('mif', 341, 6), ('bhi', 8, 16)), 
            'imoissfc'           : (('mif', 342, 6), ('bhi', 9, 16)), 
            'inonblu'            : (('mif', 343, 6), ('bhi', 10, 16)), 
            'inonblv'            : (('mif', 344, 6), ('bhi', 11, 16)), 
            'inonblt'            : (('mif', 345, 6), ('bhi', 12, 16)), 
            'inonblmr'           : (('mif', 346, 6), ('bhi', 13, 16)), 
            'i4di'               : (('mif', 347, 6), ('bhi', 14, 16)), 
            'iswind'             : (('mif', 348, 6), ('bhi', 15, 16)), 
            'istemp'             : (('mif', 349, 6), ('bhi', 16, 16)), 
            'ismois'             : (('mif', 350, 6), ('bhi', 17, 16)), 
            'ionf'               : (('mif', 351, 6), ('bhi', 18, 16)), 
            'imphys'             : (('mif', 353, 6), ('bhi', 3, 13)), 
            'itpdif'             : (('mif', 354, 6), ('bhi', 11, 13)), 
            'isoil'              : (('mif', 355, 6), ('bhi', 5, 13)), 
            'ivqadv'             : (('mif', 356, 6), ('bhi', 8, 13)), 
            'ivtadv'             : (('mif', 357, 6), ('bhi', 9, 13)), 
            'idynin'             : (('mif', 358, 6), ('bhi', 19, 16)), 
            'ithadv'             : (('mif', 359, 6), ('bhi', 10, 13)), 
            'imovet0'            : (('mif', 401, 6), ('bhi', 6, 14)), 
            'imovet1'            : (('mif', 402, 6), ('bhi', 7, 14)), 
            'imovet2'            : (('mif', 403, 6), ('bhi', 8, 14)), 
            'imovet3'            : (('mif', 404, 6), ('bhi', 9, 14)), 
            'imovet4'            : (('mif', 405, 6), ('bhi', 10, 14)), 
            'imovet5'            : (('mif', 406, 6), ('bhi', 11, 14)), 
            'imovet6'            : (('mif', 407, 6), ('bhi', 12, 14)), 
            'imovet7'            : (('mif', 408, 6), ('bhi', 13, 14)), 
            'imovet8'            : (('mif', 409, 6), ('bhi', 14, 14)), 
            'imovet9'            : (('mif', 410, 6), ('bhi', 15, 14)), 
            'imovei0'            : (('mif', 411, 6), ('bhi', 16, 14)), 
            'imovei1'            : (('mif', 412, 6), ('bhi', 17, 14)), 
            'imovei2'            : (('mif', 413, 6), ('bhi', 18, 14)), 
            'imovei3'            : (('mif', 414, 6), ('bhi', 19, 14)), 
            'imovei4'            : (('mif', 415, 6), ('bhi', 20, 14)), 
            'imovei5'            : (('mif', 416, 6), ('bhi', 21, 14)), 
            'imovei6'            : (('mif', 417, 6), ('bhi', 22, 14)), 
            'imovei7'            : (('mif', 418, 6), ('bhi', 23, 14)), 
            'imovei8'            : (('mif', 419, 6), ('bhi', 24, 14)), 
            'imovei9'            : (('mif', 420, 6), ('bhi', 25, 14)), 
            'imovej0'            : (('mif', 421, 6), ('bhi', 26, 14)), 
            'imovej1'            : (('mif', 422, 6), ('bhi', 27, 14)), 
            'imovej2'            : (('mif', 423, 6), ('bhi', 28, 14)), 
            'imovej3'            : (('mif', 424, 6), ('bhi', 29, 14)), 
            'imovej4'            : (('mif', 425, 6), ('bhi', 30, 14)), 
            'imovej5'            : (('mif', 426, 6), ('bhi', 31, 14)), 
            'imovej6'            : (('mif', 427, 6), ('bhi', 32, 14)), 
            'imovej7'            : (('mif', 428, 6), ('bhi', 33, 14)), 
            'imovej8'            : (('mif', 429, 6), ('bhi', 34, 14)), 
            'imovej9'            : (('mif', 430, 6), ('bhi', 35, 14)), 
            'p0'                 : (('mrf', 2, 6),   'absent'),
            'ts0'                : (('mrf', 3, 6),   'absent'),
            'tlp'                : (('mrf', 4, 6),   'absent'),
            'savfrq'             : (('mrf', 301, 6), ('bhr', 3, 12)),
            'tapfrq'             : (('mrf', 302, 6), ('bhr', 4, 12)),
            'buffrq'             : ('absent',        ('bhr', 5, 12)),
            'radfrq'             : (('mrf', 303, 6), ('bhr', 1, 13)),
            'hydpre'             : (('mrf', 304, 6), ('bhr', 2, 13)),
            'xmoist'             : (('mrf', 305, 6), 'absent'),
            'xstnes'             : (('mrf', 306, 6), ('bhr', 1, 14)),
            'xennes'             : (('mrf', 307, 6), ('bhr', 2, 14)),
            'timax'              : (('mrf', 308, 6), ('bhr', 1, 12)),
            'tistep'             : (('mrf', 309, 6), ('bhr', 2, 12)),
            'zzlnd'              : (('mrf', 310, 6), ('bhr', 1, 15)),
            'zzwtr'              : (('mrf', 311, 6), ('bhr', 2, 15)),
            'alblnd'             : (('mrf', 312, 6), ('bhr', 3, 15)),
            'thinld'             : (('mrf', 313, 6), ('bhr', 4, 15)),
            'xmava'              : (('mrf', 314, 6), ('bhr', 5, 15)),
            'conf'               : (('mrf', 315, 6), ('bhr', 6, 15)),
            'fdasta'             : (('mrf', 316, 6), ('bhr', 1, 16)),
            'fdaend'             : (('mrf', 317, 6), ('bhr', 2, 16)),
            'diftim3d'           : (('mrf', 318, 6), ('bhr', 3, 16)),
            'diftimsfc'          : (('mrf', 319, 6), ('bhr', 4, 16)),
            'gv3d'               : (('mrf', 320, 6), ('bhr', 5, 16)),
            'gt3d'               : (('mrf', 321, 6), ('bhr', 6, 16)),
            'gq3d'               : (('mrf', 322, 6), ('bhr', 7, 16)),
            'gr3d'               : (('mrf', 323, 6), ('bhr', 8, 16)),
            'gvsfc'              : (('mrf', 324, 6), ('bhr', 9, 16)),
            'gtsfc'              : (('mrf', 325, 6), ('bhr', 10, 16)),
            'gqsfc'              : (('mrf', 326, 6), ('bhr', 11, 16)),
            'rinblw'             : (('mrf', 327, 6), ('bhr', 12, 16)),
            'giv'                : (('mrf', 328, 6), ('bhr', 13, 16)),
            'git'                : (('mrf', 329, 6), ('bhr', 14, 16)),
            'giq'                : (('mrf', 330, 6), ('bhr', 15, 16)),
            'rinxy'              : (('mrf', 331, 6), ('bhr', 16, 16)),
            'rinsig'             : (('mrf', 332, 6), ('bhr', 17, 16)),
            'twindo'             : (('mrf', 333, 6), ('bhr', 18, 16)),
            'dtramp'             : ('absent',        ('bhr', 19, 16))
    }
    return

  def get_key(self, name, version):

    """ key = a.get_key(name, version)

     Returns a key
    """

    try:
      key = self.table[name][version - 2]
    except Exception, e:
      return 'absent'

    return key

  def get_keys(self):

    """ keys = a.get_keys()

      Returns all keys
    """

    keys = self.table.keys()

    return keys

  def print_keys(self):

    """ a.print_keys()

     Prints out keys
    """

    keys = self.table.keys()

    for i in xrange(len(keys)):
      print keys[i]

    return

  def __del__(self):
    """ a.del()

     Destructor 
    """
    del self.table

__path__ = ''

