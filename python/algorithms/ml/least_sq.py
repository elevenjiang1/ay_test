#!/usr/bin/python
from gaussian_rbf import Sq, Vec, FeaturesG, FeaturesNG, ConstructRBF
import numpy as np
import numpy.linalg as la
import math
import random

#Features= FeaturesG
Features= FeaturesNG

def Func(x):
  return x[0]*math.sin(3.0*x[1])
  #return 3.0-(x[0]*x[0]+x[1]*x[1])
  #return 3.0-(x[0]*x[0]+Sq(math.sin(3.0*x[1])))
  #return 1.0 if x[0]*x[0]+x[1]*x[1] < 0.25 else 0.0

def Rand(xmin, xmax):
  return (xmax-xmin)*random.random()+xmin

def GenerateSample(xmin, xmax, N_sample):
  data_x= [[Rand(xmin[0],xmax[0]), Rand(xmin[1],xmax[1])] for i in range(N_sample)]
  data_f= [Func(x) for x in data_x]
  return data_x, data_f

#f_reg: regularization
def GetWeightByLeastSq(data_x, data_f, func_feat, f_reg=0.1):
  dim= len(data_x[0])
  fdim= len(func_feat(data_x[0]))
  V= Vec(data_f)
  Theta= Vec([[0.0]*fdim]*len(data_x))
  for i in range(len(data_x)):
    Theta[i][:]= func_feat(data_x[i])
  w= la.inv(Theta.T.dot(Theta)+f_reg*np.eye(fdim)).dot(Theta.T).dot(V)
  return w


#def PrintEq(s):  print '%s= %r' % (s, eval(s))

if __name__=='__main__':
  xmin= [-1.,-1.]
  xmax= [2.,3.]
  n_units= [10,10]
  mu, invSig= ConstructRBF(xmin, xmax, n_units)

  data_x, data_f= GenerateSample(xmin, xmax, N_sample=300)
  w= GetWeightByLeastSq(data_x, data_f, func_feat=lambda x: Features(x,mu,invSig))


  fp= file('res/data.dat','w')
  for x,f in zip(data_x, data_f):
    fp.write('%f %f %f\n' % (x[0],x[1], f))

  fp= file('res/approx.dat','w')
  for x0 in np.arange(xmin[0],xmax[0],(xmax[0]-xmin[0])/50.0):
    for x1 in np.arange(xmin[1],xmax[1],(xmax[1]-xmin[1])/50.0):
      x= Vec([x0,x1])
      f= w.T.dot(Features(x, mu, invSig))
      fp.write('%f %f %f\n' % (x0,x1, f))
    fp.write('\n')

  print 'qplot -x -3d res/approx.dat w l res/data.dat'

