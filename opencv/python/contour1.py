#!/usr/bin/python
#\file    contour1.py
#\brief   certain python script
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Apr.16, 2020
import numpy as np
import six.moves.cPickle as pickle
import copy
import cv2
#import matplotlib.pyplot as plt

def FindMultilevelContours(img, vmin, vmax, step):
  contours= []
  for v in np.arange(vmin, vmax, step):
    img2= img.astype('uint8')
    #print img2.shape, img2.dtype
    img2[img<v]= 0
    img2[img>=v]= 1
    cnts,_= cv2.findContours(copy.deepcopy(img2), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)>0:  contours.append((v,cnts))
    #img2= cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    #cv2.drawContours(img2, cnts, -1, (0,0,255), 1)
    #cv2.imshow('debug',img2)
    #cv2.waitKey()
  return contours

def DrawMultilevelContours(img):
  print 'min:',np.min(img)
  print 'max:',np.max(img)
  contours= FindMultilevelContours(img, np.min(img), np.max(img), 2)
  #contours= FindMultilevelContours(img, 370, 390, 2)
  img_viz= cv2.cvtColor(img.astype('uint8')*255, cv2.COLOR_GRAY2BGR)
  print len(contours)
  for v,cnts in contours:
    col= (0,min(255,max(10,v-100)),0)
    thickness= 1
    cv2.drawContours(img_viz, cnts, -1, col, thickness)
  return img_viz

if __name__=='__main__':
  img_depth= pickle.load(open('../../python/data/depth001.dat','rb'))['img_depth']
  print img_depth.shape, img_depth.dtype

  img_viz= DrawMultilevelContours(img_depth)

  #data= img_depth.reshape(img_depth.shape[0],img_depth.shape[1])
  #plt.contour(data)
  #plt.show()

  cv2.imshow('depth',img_viz)
  #cv2.imshow('localmax',localmax)
  cv2.waitKey()
