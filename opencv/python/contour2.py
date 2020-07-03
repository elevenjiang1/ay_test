#!/usr/bin/python
#\file    contour2.py
#\brief   certain python script
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Apr.16, 2020
import numpy as np
import six.moves.cPickle as pickle
import copy
import cv2
import scipy.ndimage
#import matplotlib.pyplot as plt

'''
Find multi-level contours in image img.
  contours: Multi-level contours.
  contours= <list>[contours[i]|i=0,1,...]
    contours[i]= <tuple>(level, subcontours)
      level: Level (height) at i.
      subcontours: Contours at level.
      subcontours= <list>[subcontours[j]|j=0,1,...]
        subcontours[j]: A contour; set of contour points.
        subcontours[j]= <np.array>[[[x0,y0]], [[x1,y1]], ...]
'''
def FindMultilevelContours(img, vmin, vmax, step, v_smaller=0, v_larger=1, approx_epsilon=1.5):
  contours= []
  #img= cv2.blur(copy.deepcopy(img),(3,3))
  for v in np.arange(vmin, vmax, step):
    img2= copy.deepcopy(img)
    img2[img<v]= v_smaller
    img2[img>=v]= v_larger
    img2= img2.astype('uint8')
    #print img2.shape, img2.dtype
    cnts,_= cv2.findContours(img2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if approx_epsilon is not None and approx_epsilon>0.0:
      cnts_approx= []
      for curve in cnts:
        #print len(curve),'-->',
        curve2= cv2.approxPolyDP(curve, approx_epsilon, closed=True)
        #print len(curve2)
        if len(curve2)>3:  cnts_approx.append(curve2)
      cnts= cnts_approx
    if len(cnts)>0:  contours.append((v,cnts))
    #img2= cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    #cv2.drawContours(img2, cnts, -1, (0,0,255), 1)
    #cv2.imshow('debug',img2)
    #cv2.waitKey()
  return contours

#Visualize multi-level contours.
def DrawMultilevelContours(img, step=2, v_smaller=0, v_larger=1):
  print 'min:',np.min(img)
  print 'max:',np.max(img)
  contours= FindMultilevelContours(img, np.min(img), np.max(img), step, v_smaller, v_larger)
  pickle.dump(contours,open('/tmp/contours1.dat','w'))
  img_viz= cv2.cvtColor(img.astype('uint8'), cv2.COLOR_GRAY2BGR)
  print '# of levels, contours, points:', len(contours), sum(len(cnts) for v,cnts in contours), sum(sum(len(cnt) for cnt in cnts) for v,cnts in contours)
  for v,cnts in contours:
    #col= (0,min(255,max(10,v-100)),0)
    col= (0,min(255,max(1,255-0.5*v)),0)
    thickness= 1
    cv2.drawContours(img_viz, cnts, -1, col, thickness)
  return img_viz

if __name__=='__main__':
  #img_depth,v_s,v_l= pickle.load(open('../../python/data/depth001.dat','rb'))['img_depth'],0,1
  img_depth,v_s,v_l= cv2.cvtColor(cv2.imread('../cpp/sample/test_depth1.png'), cv2.COLOR_BGR2GRAY).astype(np.uint16),1,0
  #img_depth,v_s,v_l= cv2.cvtColor(cv2.imread('../cpp/sample/nprdepth001.png'), cv2.COLOR_BGR2GRAY).astype(np.uint16),1,0
  #img_depth,v_s,v_l= cv2.cvtColor(cv2.imread('../cpp/sample/nprdepth002.png'), cv2.COLOR_BGR2GRAY).astype(np.uint16),1,0
  #img_depth,v_s,v_l= cv2.cvtColor(cv2.imread('../cpp/sample/nprdepth003.png'), cv2.COLOR_BGR2GRAY).astype(np.uint16),1,0
  print img_depth.shape, img_depth.dtype, [np.min(img_depth), np.max(img_depth)]

  img_depth[img_depth==0]= np.max(img_depth)
  #img_depth= scipy.ndimage.gaussian_filter(img_depth, sigma=7)
  #cv2.imshow('filtered',img_depth*155)


  img_viz= DrawMultilevelContours(img_depth,v_smaller=v_s,v_larger=v_l)*1

  #data= img_depth.reshape(img_depth.shape[0],img_depth.shape[1])
  #plt.contour(data)
  #plt.show()

  cv2.imshow('depth',img_viz)
  #cv2.imshow('localmax',localmax)
  while cv2.waitKey() not in map(ord,[' ','q']):  pass
