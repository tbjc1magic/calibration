
import matplotlib.pylab as plt
import numpy as np
from math import *
######################################################################################
########################E fit models asymmetric gaussian functions####################
######################################################################################

def AsymGaussian(x,A,xc,w,t0):
    print 0.5*(w/t0)**2+(x-xc)/t0
    tmp1 = exp(0.5*(w/t0)**2+(x-xc)/t0)
    tmp2 = erf((-(x-xc)/w-w/t0)/2**0.5)
    return A/(2*t0)*tmp1*(1+tmp2)

def DoubleAsymGaussian(x,A1,xc1,w1,t01,A2,xc2,w2,t02):
    return AsymGaussian(x,A1,xc1,w1,t01) + AsymGaussian(x,A2,xc2,w2,t02)

def main():

    A1=10000.0
    xc1 = 900.0
    w1=1.0
    t01=3.0

    A2=5000.0
    xc2 = 1900.0
    w2=1.0
    t02=3.0

    xlist = []
    rlist = []
    for one in range(1,2000):
        xlist.append(one)
        r = DoubleAsymGaussian(one, A1,xc1,w1,t01, A2,xc2, w2, t02)
        rlist.append(r)

    plt.plot(xlist, rlist)
    plt.show()
main()
