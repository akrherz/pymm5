# ! file mm5_proj.py

##############################################################
#################  University of L'Aquila    #################
#################       PST ABruzzo          #################
################# MM5 python interface V 0.1 #################
##############################################################

" Projection conversion utilities. "

import mm5_class
from math import fabs, ceil, floor, fmod, cos, sin, tan, atan, \
                 atan2, acos, asin, log, log10, sqrt, exp, hypot
from Numeric import shape

def cubic(x):
  """ y = cubic(x)

    http://www.lakeheadu.ca/~forwww/assig2j.html

    Cubic function to be convolved with grid for cubic convolution
    A value for parameter a of -0.5 tends to produce output bands
    with a mean and standard deviation closer to that of the original
    data, in most cases.
  """
  a=-0.5
  mx=fabs(x)
  if (mx <= 1.0):
     return((a+2.0)*mx**3 - (a+3.0)*mx**2 + 1.0)
  elif (mx > 1.0 and mx < 2.0):
     return(a*mx**3 - 5.0*a*mx**2 + 8.0*a*mx - 4.0*a)
  else: return 0.0

def rintf(x):
  """ a = rintf(x)

   Return nearest integer value to x 
  """
  if (int(x) == 0):
    if (x > 0.50): return ceil(x)
    else: return floor(x)
  elif (fmod(x, int(x)) > 0.50): return ceil(x)
  else: return floor(x)

def ispointin(i,j,(maxi,maxj)):
  """ check = ispointin(i,j,(maxi,maxj))

   Checks if point i,j is in (1,maxi), (1,maxj) interval
  """
  if (i < 0.0 or j < 0.0 or i > (maxi-1) or j > (maxj-1)): return 0
  return 1

def cosd(x):
  """ a = cosd(x)

   cos of x, x in degrees
  """
  return(cos(x*0.01745329251994329576))
def sind(x):
  """ a = sind(x)

   sin of x, x in degrees
  """
  return(sin(x*0.01745329251994329576))
def tand(x):
  """ a = tand(x)

   tan of x, x in degrees
  """
  return(tan(x*0.01745329251994329576))

class projection:

  """ MM5 (Terrain) Projection routines """

  def set_proj(self):
    "INTERNAL USE. NO INTERFACE."
    if (self.cenlat > 0): self.sign = 1.0
    else: self.sign = -1.0
    self.xn = 0.0
    self.psi1 = 0.0
    self.pole = self.sign*90.0
    self.psi0 = (self.pole-self.cenlat)*0.01745329251994329576
    if (self.code == 1):
      self.xn = log10(cosd(self.stdlat1)) - log10(cosd(self.stdlat2))
      self.xn = self.xn/(log10(tand(45.0-self.sign*self.stdlat1*0.50)) - \
                         log10(tand(45.0-self.sign*self.stdlat2*0.50)))
      self.psi1 = (90.0-self.sign*self.stdlat1)*0.01745329251994329576
      self.psi1 = self.sign*self.psi1
    elif (self.code == 2):
      self.xn = 1.0
      self.psi1 = (90.0-self.sign*self.stdlat1)*0.01745329251994329576
      self.psi1 = self.sign*self.psi1
    if (self.code != 3):
      psx = (self.pole-self.cenlat)*0.01745329251994329576
      if (self.code == 1):
        cell  = self.radius*sin(self.psi1)/self.xn
        cell2 = tan(psx*0.50) / tan(self.psi1*0.50)
      else:
        cell  = self.radius*sin(psx)/self.xn
        cell2 = (1. + cos(self.psi1))/(1.0 + cos(psx))
      r = cell*(cell2)**self.xn
      self.xcntr = 0.0
      self.ycntr = -r
      self.xc = 0.0
      self.yc = -self.radius/self.xn*sin(self.psi1)* \
                (tan(self.psi0*0.5)/tan(self.psi1*0.5))**self.xn
    else:
      self.c2 = self.radius * cos(self.psi1)
      self.xcntr = 0.0
      phictr = self.cenlat*0.01745329251994329576
      cell = cos(phictr)/(1.0+sin(phictr))
      self.ycntr = -self.c2*log(cell)
      self.xc = self.xcntr
      self.yc = self.ycntr
    return

  def __init__(self,input):
    """ proj = projection(mm5_input)

     Create a projection instance. Input is an mm5 class instance.
    """
    self.code = input.get_val('map_proj')
    self.stdlat1 = input.get_val('stdlat1')
    self.stdlat2 = input.get_val('stdlat2')
    self.stdlon = self.cenlon = input.get_val('coarse_cenlon')
    self.cenlat = input.get_val('coarse_cenlat')
    self.c_dim_i = input.get_val('exp_dim_i')
    self.c_dim_j = input.get_val('exp_dim_j')
    self.dim_i = input.get_val('grid_dim_i')
    self.dim_j = input.get_val('grid_dim_j')
    self.ratio = float(input.get_val('coarse_ratio'))
    self.xsouth = input.get_val('sw_coarse_i')
    self.xwest = input.get_val('sw_coarse_j')
    self.cntri0 = float((self.c_dim_i + 1) * 0.50)
    self.cntrj0 = float((self.c_dim_j + 1) * 0.50)
    self.cntri = (self.cntri0-self.xsouth) * self.ratio + 0.50
    self.cntrj = (self.cntrj0-self.xwest) * self.ratio + 0.50
    self.ds = input.get_val('grid_distance')
    self.cds = input.get_val('coarse_grid_d')
    self.dddd = self.cntrj0 * self.cds
    self.radius = 6370.0

    self.set_proj()

    return

  def latlon_to_ij(self, lat, lon):
    """ (i,j) = proj.latlon_to_ij(lat,lon)

     From latitude/longitude to i,j of the mm5 domain grid
    """
    if (self.code == 3):
      if (lat != -90.0):
        cell = cosd(lat)/(1.0+sind(lat))
        yy = -self.c2*log(cell)
        xx =  self.c2*((lon-self.cenlon)*0.01745329251994329576)
        if (self.cenlon > 0 and xx < -self.dddd):
          xx = xx + 2.0*self.c2*((180.0+self.cenlon)*0.01745329251994329576)
        elif (self.cenlon < 0 and xx > self.dddd):
          xx = xx - self.c2*(360.0*0.01745329251994329576)
    else:
      ylon = lon - self.cenlon
      if (ylon > 180.0): ylon = ylon - 360.0
      if (ylon < -180.0): ylon = ylon + 360.0
      flp = self.xn*(ylon*0.01745329251994329576)
      psx = (self.pole - lat) * 0.01745329251994329576
      r = -self.radius/self.xn*sin(self.psi1)* \
           (tan(psx*0.50)/tan(self.psi1*0.5))**self.xn
      if (self.cenlat < 0):
        xx = r*sin(flp)
        yy = r*cos(flp)
      else:
        xx = -r*sin(flp)
        yy = r*cos(flp)

    i = (xx - self.xc) / self.ds + self.cntrj
    j = (yy - self.yc) / self.ds + self.cntri

    return(j,i)

  def ij_to_latlon(self,i,j):
    """ (lat,lon) = proj.ij_to_latlon(i,j)

     From i,j of the mm5 domain grid to latitude/longitude
    """
    x = self.xcntr+(j-self.cntrj)*self.ds
    y = self.ycntr+(i-self.cntri)*self.ds
    if (self.code != 3):
      if (y == 0.0):
        if (x >= 0.0): flp = 90.0*0.01745329251994329576
        else: flp = -90.0*0.01745329251994329576
      else:
        if (self.cenlat < 0.0):
          flp = atan2(x,y)
        else:
          flp = atan2(x,-y)
      lon = (flp/self.xn)*57.2957795130823208852+self.cenlon
      if (lon < -180.0): lon = lon + 360.0
      if (lon > 180.0): lon = lon - 360.0
      r = sqrt(x*x+y*y)
      if (self.cenlat < 0.0): r = -r
      if (self.code == 1):
        cell = (r*self.xn)/(self.radius*sin(self.psi1))
        rxn = 1.0/self.xn
        cel1 = tan(self.psi1*0.50)*(cell)**rxn
      else:
        cell = r/self.radius
        cel1 = cell/(1.0+cos(self.psi1))
      cel2 = atan(cel1)
      psx = 2.0*cel2*57.2957795130823208852
      lat = self.pole-psx
    else:
      lon = self.cenlon + ((x-self.xcntr)/self.c2)*57.2957795130823208852
      if (lon < -180.0): lon = lon + 360.0
      if (lon > 180.0): lon = lon - 360.0
      cell = exp(y/self.c2)
      lat = 2.0*(57.2957795130823208852*atan(cell))-90.0

    return(lat,lon)

  def nearval(self,lat,lon,grid,offset):
    """ a.nearval(lat,lon,grid,offset)

     Nearest value interpolation of grid at lat,lon point
     Offset is 1.0 for cross variables, 0.5 for dot ones

     Advantages:    Output values are the original input values. Other methods
                    of resampling tend to average surrounding values.
                    Easy to compute and therefore fastest to use.

     Disadvantages: Produces a choppy, "stair-stepped" effect. The image has
                    a rough appearance relative to the original unrectified
                    data. Data values may be lost, while other values may be
                    duplicated.
    """
    (i,j) = self.latlon_to_ij(float(lat),float(lon))
    (i,j) = (rintf(i-offset),rintf(j-offset))
    if (ispointin(rintf(i-1.0),rintf(j-1.0),shape(grid))):
      return grid[int(i)][int(j)]
    else:
#     print "WARNING : Point is outside grid !"
      return 1e20

  def lwval(self,lat,lon,grid,offset):
    """ a.lwval(lat,lon,grid,offset)

     Liner interpolation distance weighted of grid at lat,lon point

     Offset is 1.0 for cross variables, 0.5 for dot ones
    """
    (i,j) = self.latlon_to_ij(lat,lon)
    (i,j) = (i-offset,j-offset)
    (i0,j0)=(floor(i),floor(j))
    (i1,j1)=(floor(i),ceil(j))
    (i2,j2)=(ceil(i),ceil(j))
    (i3,j3)=(ceil(i),floor(j))
    if (ispointin(i0,j0,shape(grid)) and ispointin(i1,j1,shape(grid)) and \
        ispointin(i2,j2,shape(grid)) and ispointin(i3,j3,shape(grid))):
      d0=1.0/hypot((i-i0),(j-j0)); d1=1.0/hypot((i-i1),(j-j1))
      d2=1.0/hypot((i-i2),(j-j2)); d3=1.0/hypot((i-i3),(j-j3))
      i0=int(i0); j0=int(j0); i1=int(i1); j1=int(j1)
      i2=int(i2); j2=int(j2); i3=int(i3); j3=int(j3)
      value=grid[i0][j0]*d0+grid[i1][j1]*d1+grid[i2][j2]*d2+grid[i3][j3]*d3
      value=value/(d0+d1+d2+d3)
    else:
      value=1e20
#     print "WARNING : Point is outside grid !"
    return value

  def blinval(self,lat,lon,grid,offset):
    """ a.blinval(lat,lon,grid,offset)

     Bilinear interpolation of grid at lat,lon point

     Offset is 1.0 for cross variables, 0.5 for dot ones

     Advantages:    Stair-step effect caused by the nearest neighbour approach
                    is reduced. Image looks smooth.

     Disadvantages: Alters original data and reduces contrast and high
                    frequency component of the image by averaging neighbouring
                    values together. Is computationally more expensive than
                    nearest neighbour. 
    """
    (i,j) = self.latlon_to_ij(lat,lon)
    (i,j) = (i-offset,j-offset)
    (i0,j0)=(floor(i),floor(j))
    (i1,j1)=(floor(i),ceil(j))
    (i2,j2)=(ceil(i),ceil(j))
    (i3,j3)=(ceil(i),floor(j))
    if (ispointin(i0,j0,shape(grid)) and ispointin(i1,j1,shape(grid)) and \
        ispointin(i2,j2,shape(grid)) and ispointin(i3,j3,shape(grid))):
      dx=(i-i0)
      dy=(j-j0)
      i0=int(i0); j0=int(j0); i1=int(i1); j1=int(j1)
      i2=int(i2); j2=int(j2); i3=int(i3); j3=int(j3)
      p12=dx*grid[i2][j2]+(1-dx)*grid[i1][j1]
      p03=dx*grid[i3][j3]+(1-dx)*grid[i0][j0]
      value=dy*p12+(1-dy)*p03
    else:
      value=1e20
#     print "WARNING : Point is outside grid !"
    return value

  def cubconval(self,lat,lon,grid,offset):
    """ a.cubconval(lat,lon,grid,offset)

     Cubic convolution of grid at lat,lon point

     Offset is 1.0 for cross variables, 0.5 for dot ones

     Advantages:    Stair-step effect caused by the nearest neighbour approach
                    is reduced. Image looks smooth. 

     Disadvantages: Alters original data and reduces contrast by averaging
                    neighbouring values together. Is computationally more
                    expensive than nearest neighbour or bilinear interpolation. 
    """
    (ix,jx)=self.latlon_to_ij(lat,lon)
    (ix,jx) = (ix-1,jx-1)
    (id,jd)=(rintf(ix),rintf(jx))
    (i0,j0)=(id-1.0,jd-1.0);   (i1,j1)=(id,jd-1.0);
    (i2,j2)=(id+1.0,jd-1.0);   (i3,j3)=(id+2.0,jd-1.0);
    (i4,j4)=(id-1.0,jd);       (i5,j5)=(id,jd);
    (i6,j6)=(id+1.0,jd);       (i7,j7)=(id+2.0,jd);
    (i8,j8)=(id-1.0,jd+1.0);   (i9,j9)=(id,jd+1.0);
    (i10,j10)=(id+1.0,jd+1.0); (i11,j11)=(id+2.0,jd+1.0);
    (i12,j12)=(id-1.0,jd+2.0); (i13,j13)=(id,jd+2.0);
    (i14,j14)=(id+1.0,jd+2.0); (i15,j15)=(id+2.0,jd+2.0);
    if (ispointin(i0,j0,shape(grid))   and ispointin(i1,j1,shape(grid))   and \
        ispointin(i2,j2,shape(grid))   and ispointin(i3,j3,shape(grid))   and \
        ispointin(i4,j4,shape(grid))   and ispointin(i5,j5,shape(grid))   and \
        ispointin(i6,j6,shape(grid))   and ispointin(i7,j7,shape(grid))   and \
        ispointin(i8,j8,shape(grid))   and ispointin(i9,j9,shape(grid))   and \
        ispointin(i10,j10,shape(grid)) and ispointin(i11,j11,shape(grid)) and \
        ispointin(i12,j12,shape(grid)) and ispointin(i13,j13,shape(grid)) and \
        ispointin(i14,j14,shape(grid)) and ispointin(i15,j15,shape(grid))):
      f0=cubic(hypot((ix-i0),(jx-j0))); f1=cubic(hypot((ix-i1),(jx-j1)));
      f2=cubic(hypot((ix-i2),(jx-j2))); f3=cubic(hypot((ix-i3),(jx-j3)));
      f4=cubic(hypot((ix-i4),(jx-j4))); f5=cubic(hypot((ix-i5),(jx-j5)));
      f6=cubic(hypot((ix-i6),(jx-j6))); f7=cubic(hypot((ix-i7),(jx-j7)));
      f8=cubic(hypot((ix-i8),(jx-j8))); f9=cubic(hypot((ix-i9),(jx-j9)));
      f10=cubic(hypot((ix-i10),(jx-j10))); f11=cubic(hypot((ix-i11),(jx-j11)));
      f12=cubic(hypot((ix-i12),(jx-j12))); f13=cubic(hypot((ix-i13),(jx-j13)));
      f14=cubic(hypot((ix-i14),(jx-j14))); f15=cubic(hypot((ix-i15),(jx-j15)));
      i0=int(i0); j0=int(j0); i1=int(i1); j1=int(j1);
      i2=int(i2); j2=int(j2); i3=int(i3); j3=int(j3);
      i4=int(i4); j4=int(j4); i5=int(i5); j5=int(j5);
      i6=int(i6); j6=int(j6); i7=int(i7); j7=int(j7);
      i8=int(i8); j8=int(j8); i9=int(i9); j9=int(j9);
      i10=int(i10); j10=int(j10); i11=int(i11); j11=int(j11);
      i12=int(i12); j12=int(j12); i13=int(i13); j13=int(j13);
      i14=int(i14); j14=int(j14); i15=int(i15); j15=int(j15);
      v1=grid[i0][j0]*f0+grid[i1][j1]*f1+grid[i2][j2]*f2+grid[i3][j3]*f3
      v2=grid[i4][j4]*f4+grid[i5][j5]*f5+grid[i6][j6]*f6+grid[i7][j7]*f7
      v3=grid[i8][j8]*f8+grid[i9][j9]*f9+grid[i10][j10]*f10+grid[i11][j11]*f11
      v4=grid[i12][j12]*f12+grid[i13][j13]*f13+\
         grid[i14][j14]*f14+grid[i15][j15]*f15
      div=f0+f1+f2+f3+f4+f5+f6+f7+f8+f9+f10+f11+f12+f13+f14+f15
      value=(v1+v2+v3+v4)/div
    else:
      value=1e20
#     print "WARNING : Point is outside grid !"
    return value
#

__path__ = ''

