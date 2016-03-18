import matplotlib.pyplot as plt
from pylab import *
from scipy.special import erf
from scipy.optimize import curve_fit
import numpy as np
import scipy.optimize


######################################################################################
########################find slopes with  least square fitting########################
######################################################################################




def SlopeModel(parameter, x, y):
    a, b, c = parameter
    return a*x + b*y + c
 
def SlopeResidual(parameter, data, x, y):
    res = []
    datalen = len(data)
    for i in xrange(datalen):
        res.append(data[i]-SlopeModel(parameter,x[i],y[i]))
    return res


#########################################################################################
#######################plot figures######################################################
#########################################################################################



def NFfigs(Nlist,Flist, picname="default.png"):
    plt.clf()
    plt.plot(Nlist,Flist,'o')
    plt.savefig(picname)

def EXfigs(Elist,Xlist, picname="default.png"):

    plt.clf()
    plt.plot(Xlist,Elist,'.')
    plt.ylim(0,7)
    plt.xlim(-1.1,1.1)
    plt.savefig(picname)


def ESUMfigs(processlist, picname="default.png"):
    ziplist = zip(*processlist)
    e = list(ziplist[0])
    fs = list(ziplist[1])
    ns = list(ziplist[2])

    NFsum = [x+y for x,y in zip(ns,fs)]


    plt.clf()
    plt.plot(NFsum,e,'o')
    plt.savefig(picname)


#####################################################################################
#####################fit E vs X with polynomial functions############################
#####################################################################################

def EXpolyfig(e,x,picname="default.png"):
    
    polyterm = 4
    popt = np.polyfit(x,e,polyterm)
    #print popt
    listlen = len(x)

    fitE = []
    for i in xrange(listlen):
        tmpx = 0
        for j in xrange(polyterm+1):
            tmpx = tmpx + popt[j] * x[i]**(polyterm - j)
        fitE = fitE + [tmpx]

    plt.clf()
    plt.plot(x,e,'o')
    plt.plot(x,fitE,'o',c='g')
    plt.savefig(picname)

#####################################################################################
####################find the largest value in the hist on both edges#################
#####################################################################################

def Xhistfind(x,picname="default.png"):

    events, edges, patches = hist(x,100)
    binlength = len(events)
    tmp1 = edges[1:binlength+1]
    tmp2 = edges[0:binlength]
    bincenter = (tmp1+tmp2)/2

    xdata = bincenter
    ydata = events

    datalen = len(xdata)

    leftP  = [-1,0]
    rightP = [1,0] 
    
    for i in xrange(datalen):
        if(xdata[i]<0 and ydata[i]>leftP[1]):
            leftP = [xdata[i],ydata[i]]

        if(xdata[i]>0 and ydata[i]>rightP[1]):
            rightP = [xdata[i],ydata[i]]

    plt.clf()
    plt.plot(xdata,ydata,'o',c='r')
    plt.plot([leftP[0]],[leftP[1]],'o',c='b')
    plt.plot([rightP[0]],[rightP[1]],'o',c='b')

    plt.savefig(picname)
    
    return (leftP[0],rightP[0]) 

######################################################################################
########################E fit models asymmetric gaussian functions####################
######################################################################################



def AsymGaussian(x,A,xc,w,t0):
    tmp1 = exp(0.5*(w/t0)**2+(x-xc)/t0)
    tmp2 = erf((-(x-xc)/w-w/t0)/2**0.5)
    return A/(2*t0)*tmp1*(1+tmp2)

def DoubleAsymGaussian(x,A1,xc1,w1,t01,A2,xc2,w2,t02):
    return AsymGaussian(x,A1,xc1,w1,t01) + AsymGaussian(x,A2,xc2,w2,t02) 

######################################################################################
########################E fit models##################################################
######################################################################################

def EModel(parameter,x):
    return DoubleAsymGaussian(x,parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6],parameter[7])


def EResidual(parameter, data, x):
    res = []
    datalen = len(data)
    for i in xrange(datalen):
        res = res + [data[i] - EModel(parameter,x[i])]
    return res


######################################################################################
##########fit E peaks with least square fit using asymmetric gaussian function########
######################################################################################

def LeastSquareE(processlist, picname = "default.png", __p0=[1,1,1,1,1,1,1,1]):

    events, edges, patches = hist(processlist,100)
    binlength = len(events)
    tmp1 = edges[1:binlength+1]
    tmp2 = edges[0:binlength]
    bincenter = (tmp1+tmp2)/2
    plt.clf()

    xdata = bincenter[int(0.12*binlength):binlength]
    ydata = events[int(0.12*binlength):binlength]

    xlistdata = [x for x in xdata]
    ylistdata = [y for y in ydata]

    #print "p0",__p0
    __p0[0] = __p0[0] - 100
    __p0[1] = __p0[1] - 100

    fitresult = scipy.optimize.leastsq(EResidual,__p0, args = (ylistdata,xlistdata))
    return  fitresult[0]


##########################################################################################
#################fit E peaks using asymmetric gaussian function###########################
##########################################################################################

def fitE(processlist, picname="default.png",__p0=[1,1,1,1,1,1,1,1]):


    events, edges, patches = hist(processlist,100)
    binlength = len(events)
    tmp1 = edges[1:binlength+1]
    tmp2 = edges[0:binlength]
    bincenter = (tmp1+tmp2)/2
    plt.clf()

    xdata = bincenter[int(0.12*binlength):binlength]
    ydata = events[int(0.12*binlength):binlength]


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

########################################################
#############read alpha data############################
########################################################


fname="alphatbjc.dat"
lineindex=0
tbjclist = [[] for x in xrange(24)]
with open(fname) as readfile:
    content = readfile.readlines()
    
    for line in content:
        lineindex += 1
        cf, e, fs, ns = line.split()
        print lineindex, cf, e,fs, ns        
        cf= int(cf)
        e = float(e)
        fs = float(fs)
        ns = float(ns)
        
        if((fs<5)or(ns<5)):
            continue

        tbjclist[cf] = tbjclist[cf] + [[e,fs,ns]]



########################################################
#############read alpha E parameter estimates###########
########################################################
Eoutf = open("Efactors.dat","w")
Slopeoutf = open("Slopefactors.dat","w")
Xoutf = open("Xfactors.dat","w")


Eoptsf="alphaEopt.csv"
tbjcEopts = [[] for x in xrange(24)]
with open(Eoptsf) as readfile:
    content = readfile.readlines()

    for line in content:
        c, p0, p1, p2, p3, p4, p5, p6, p7 = line.split()
        c = int(c)
        p0 = float(p0)
        p1 = float(p1)
        p2 = float(p2)
        p3 = float(p3)
        p4 = float(p4)
        p5 = float(p5)
        p6 = float(p6)
        p7 = float(p7)
        tbjcEopts[c] = tbjcEopts[c] + [p0,p1,p2,p3,p4,p5,p6,p7]


AlphaE1 = 3.1828
AlphaE2 = 5.8048


##################################################################
################process the analysis##############################
##################################################################
print "process the analysis"

for i in xrange(24):
    picname = "efit_"+str(i)
    print i,

    ziplist = zip(*tbjclist[i])
    e = list(ziplist[0])
    fs = list(ziplist[1])
    ns = list(ziplist[2])
    #EXfigs(tbjclist[i],"EX_"+str(i))
    #NFfigs(ns,fs,"NF_"+str(i))

##################################################################
############################fit the slope#########################
##################################################################
    Slopeparams0 = [1., 1.,1.]
    fitresult = scipy.optimize.leastsq(SlopeResidual, Slopeparams0, (e,fs,ns))
    FSlope = fitresult[0][0]
    NSlope = fitresult[0][1]
    Slopeoutf.write(str(i)+" "+str(FSlope)+" "+str(NSlope)+"\n")
    


##################################################################
#################apply the slope factors to energies##############
##################################################################
   
    for index in xrange(len(tbjclist[i])):
        tbjclist[i][index][0] = tbjclist[i][index][0]
        tbjclist[i][index][1] = tbjclist[i][index][1] * FSlope
        tbjclist[i][index][2] = tbjclist[i][index][2] * NSlope


    ziplist = zip(*tbjclist[i])
    e = list(ziplist[0])
    fs = list(ziplist[1])
    ns = list(ziplist[2])
    x = [(xns-yfs)/(xns+yfs) for xns,yfs in zip(*[ns,fs])]
    NFfigs(ns,fs,"NF_"+str(i))


    anotherX = []
    for index in xrange(len(tbjclist[i])):
        anotherX = anotherX + [(fs[index]-ns[index])/e[index]]


    ESUMfigs(tbjclist[i],"ESUM_"+str(i))



##################################################################
#####################find peaks in x histogram####################
##################################################################
    newx = []
    newe = []
    listlen = len(x)
    for tmpi in xrange(listlen):
        if(e[tmpi]>1400):
            newx = newx + [x[tmpi]]
            newe = newe + [e[tmpi]]

    
    leftP, rightP = Xhistfind(newx,"x_"+str(i)) 

    Xa = 2/(rightP - leftP)
    Xb = -(rightP + leftP)/(rightP - leftP)

    Xoutf.write(str(i)+" "+str(Xa)+" "+str(Xb)+"\n")
##################################################################
##########################apply X factors#########################
##################################################################

    for tmpi in xrange(listlen):
        x[tmpi] = Xa * x[tmpi] +Xb

##################################################################
########################fit the energy peaks######################
##################################################################
    popt = fitE(e,picname,tbjcEopts[i])
    print "popt",popt
    #print "lsqE",LeastSquareE(e,picname,tbjcEopts[i]) 
    P1 = popt[1]
    P2 = popt[5]

    Ea = (AlphaE1-AlphaE2)/(P1-P2)
    Eb = (AlphaE2*P1-AlphaE1*P2)/(P1-P2) 
   

    Eoutf.write(str(i)+" "+str(Ea)+" "+str(Eb)+"\n")
    

##################################################################
################apply the energy factors to energies##############
##################################################################
  
    for index in xrange(len(tbjclist[i])):
        tbjclist[i][index][0] = tbjclist[i][index][0] * Ea + Eb
        tbjclist[i][index][1] = tbjclist[i][index][1]
        tbjclist[i][index][2] = tbjclist[i][index][2]

    ziplist = zip(*tbjclist[i])
    e = list(ziplist[0])
    fs = list(ziplist[1])
    ns = list(ziplist[2])


    EXfigs(e,x,"EX_"+str(i))

##################################################################
################fit the lower line with polynomial################
##################################################################
################I will  not use it for alphas#####################
##################################################################

    newx = []
    newe = []
    for tmpi in xrange(len(x)):
        if(x[tmpi]>-0.7 and x[tmpi]<0.7 and e[tmpi]>2.7 and e[tmpi]<3.4):
            newx = newx + [x[tmpi]]
            newe = newe + [e[tmpi]]
    EXpolyfig(newe,newx, "newEX_"+str(i))
