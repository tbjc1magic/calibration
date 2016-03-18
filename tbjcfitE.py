from matplotlib.pyplot import *
from scipy.special import erf
from scipy.optimize import curve_fit
import numpy as np
import scipy.optimize

from pylab import *

import math

from scipy.optimize import fsolve

######################################################################################
########################E fit models asymmetric gaussian functions####################
######################################################################################

def AsymGaussian(x,A,xc,w,t0):
    tmp1 = exp(0.5*(w/t0)**2+(x-xc)/t0)
    tmp2 = erf((-(x-xc)/w-w/t0)/2**0.5)
    return A/(2*t0)*tmp1*(1+tmp2)

def DoubleAsymGaussian(x,A1,xc1,w1,t01,A2,xc2,w2,t02):
    return AsymGaussian(x,A1,xc1,w1,t01) + AsymGaussian(x,A2,xc2,w2,t02)

def erfcx(z):
    return np.exp(z*z)*(1-erf(z))

def yfunc(y,t0,w):
    return erfcx(y)-t0/w*math.sqrt(2/math.pi)

def ReturnAsymGaussianPeak(A,xc,w,t0):

    rts = fsolve(yfunc,x0=0,args=(t0,w))

    peakP = xc + rts[0]*w*math.sqrt(2) -w*w/t0

    return peakP

##########################################################################################
#################fit E peaks using asymmetric gaussian function###########################
##########################################################################################

def fitE(xdata, ydata, __p0=[1,1,1,1,1,1,1,1]):

    xdatal = []
    ydatal = []

    for onex, oney in zip(xdata,ydata):
        if oney>5:
            xdatal.append(onex)
            ydatal.append(oney)

    xdata= np.array(xdatal)
    ydata= np.array(ydatal)

    sigmalist = []

    for one in ydata.astype(float):
        if one> 1:
            sigmaone = 1/math.sqrt(one)
        else:
            sigmaone = 100000.0

        sigmalist.append(sigmaone)

    sigma = np.array(sigmalist)

    popt, pcov = curve_fit(DoubleAsymGaussian, xdata, ydata,sigma=sigma,p0=__p0)

    #y = DoubleAsymGaussian(xdata,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7] )

    return popt

##########################################################################################
############################### return the whole set #####################################
##########################################################################################

def returnEverything(processlist,poptguess=[1,1,1,1,1,1,1,1]):

    xdata,ydata =returnXY(processlist)
    popt = fitE(xdata, ydata,poptguess)

    y = DoubleAsymGaussian(xdata,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7] )

    return xdata,ydata,popt,y

##########################################################################################
##################################return x and y data#####################################
##########################################################################################

def returnXY(processlist):

    events,edges = np.histogram(processlist, bins=range(0,max(processlist)+200,10), density=False)

    #events, edges, patches = hist(processlist,100)
    binlength = len(events)
    tmp1 = edges[1:binlength+1]
    tmp2 = edges[0:binlength]
    bincenter = (tmp1+tmp2)/2

    xdata = bincenter[int(0.12*binlength):binlength]
    ydata = events[int(0.12*binlength):binlength]

    return xdata,ydata,

    popt, pcov = curve_fit(DoubleAsymGaussian, xdata, ydata,p0=__p0)
    #print popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7]

    y = DoubleAsymGaussian(xdata,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7] )

    #histplot.scatter(xdata,y,c="red")
    plt.plot(xdata,ydata,'o',xdata,y)

    #plt.show()
    plt.savefig(picname)
    plt.close()
    plt.clf()
    return popt
