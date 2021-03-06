#!/usr/bin/python
#\file    polygon_area.py
#\brief   Obtaining area of polygon in 2D.
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    May.19, 2017

#Calculate area of a polygon in 2D.
# http://mathworld.wolfram.com/PolygonArea.html
# http://stackoverflow.com/questions/451426/how-do-i-calculate-the-area-of-a-2d-polygon
def PolygonArea(points):
  if len(points)<3:  return 0.0
  return 0.5*abs(sum(x0*y1-x1*y0
                     for ((x0,y0), (x1,y1)) in zip(points, points[1:]+[points[0]])))

def Main():
  polygon1= [[0.729,0.049],[0.723,0.082],[0.702,0.125],[0.682,0.124],[0.654,0.106],[0.656,0.101],[0.647,0.081],[0.652,0.078],[0.651,0.071],[0.655,0.071],[0.673,0.031]]
  polygon2= [[0.722,0.219],[0.717,0.220],[0.712,0.229],[0.693,0.235],[0.681,0.227],[0.672,0.230],[0.649,0.211],[0.637,0.213],[0.629,0.208],[0.626,0.216],[0.620,0.202],[0.616,0.203],[0.617,0.207],[0.609,0.200],[0.603,0.201],[0.601,0.191],[0.587,0.181],[0.589,0.175],[0.580,0.166],[0.585,0.133],[0.593,0.121],[0.605,0.113],[0.626,0.113],[0.645,0.121],[0.644,0.127],[0.651,0.123],[0.661,0.135],[0.669,0.134],[0.675,0.140],[0.702,0.148],[0.715,0.159],[0.717,0.150],[0.720,0.149],[0.721,0.167],[0.727,0.167],[0.730,0.195],[0.724,0.204]]
  polygon3= [[0.820,0.156],[0.793,0.154],[0.812,0.154],[0.812,0.150],[0.803,0.149],[0.806,0.134],[0.802,0.139],[0.796,0.133],[0.786,0.140],[0.779,0.139],[0.772,0.131],[0.774,0.126],[0.782,0.127],[0.779,0.134],[0.789,0.130],[0.788,0.115],[0.794,0.109],[0.773,0.111],[0.769,0.124],[0.755,0.143],[0.749,0.144],[0.753,0.150],[0.750,0.153],[0.737,0.147],[0.731,0.149],[0.738,0.141],[0.722,0.144],[0.722,0.124],[0.726,0.126],[0.729,0.123],[0.725,0.118],[0.733,0.107],[0.733,0.090],[0.738,0.086],[0.738,0.077],[0.740,0.082],[0.744,0.080],[0.749,0.041],[0.757,0.039],[0.758,0.032],[0.763,0.034],[0.762,0.040],[0.769,0.037],[0.769,0.008],[0.781,0.024],[0.778,0.034],[0.788,0.043],[0.828,0.144],[0.819,0.150]]
  polygon4= [[0.6,0.05],[0.65,0.05],[0.65,0.1],[0.6,0.1]]
  polygon5= [[0.6,0.15],[0.6,0.2],[0.65,0.15],[0.65,0.2]]
  polygon6= [[0.65,0.05],[0.7,0.05],[0.7,0.1]]

  def Print(eq,g=globals(),l=locals()): print eq+'= '+str(eval(eq,g,l))
  Print('PolygonArea(polygon1)')
  Print('PolygonArea(polygon2)')
  Print('PolygonArea(polygon3)')
  Print('PolygonArea(polygon4)')
  Print('PolygonArea(polygon5)')  #NOTE incorrect!
  Print('PolygonArea(polygon6)')

  def write_polygon(fp,polygon):
    if len(polygon)>0:
      for pt in polygon+[polygon[0]]:
        fp.write('%s\n'%' '.join(map(str,pt)))
    fp.write('\n')

  fp= open('/tmp/polygons.dat','w')
  write_polygon(fp,polygon1)
  write_polygon(fp,polygon2)
  write_polygon(fp,polygon3)
  write_polygon(fp,polygon4)
  write_polygon(fp,polygon5)
  write_polygon(fp,polygon6)
  fp.close()


def PlotGraphs():
  print 'Plotting graphs..'
  import os
  commands=[
    '''qplot -x2 aaa
        /tmp/polygons.dat u 1:2:'(column(-1)+1)' lc var w l
        &''',
        #/tmp/polygons.dat u 1:2:-1 lc var w l
    '''''',
    '''''',
    ]
  for cmd in commands:
    if cmd!='':
      cmd= ' '.join(cmd.splitlines())
      print '###',cmd
      os.system(cmd)

  print '##########################'
  print '###Press enter to close###'
  print '##########################'
  raw_input()
  os.system('qplot -x2kill aaa')

if __name__=='__main__':
  import sys
  if len(sys.argv)>1 and sys.argv[1] in ('p','plot','Plot','PLOT'):
    PlotGraphs()
    sys.exit(0)
  Main()
