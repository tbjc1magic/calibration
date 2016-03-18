from scipy.special import erf
from scipy.optimize import curve_fit
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

##################################################################
############################fit the slope#########################
##################################################################
def SlopeFit(inputlist,Slopeparams0=[1,1,1]):
#    print inputlist
    fitresult = scipy.optimize.leastsq(SlopeResidual, Slopeparams0, inputlist)
    FSlope = fitresult[0][0]
    NSlope = fitresult[0][1]
    b = fitresult[0][2]

    return FSlope, NSlope,b
