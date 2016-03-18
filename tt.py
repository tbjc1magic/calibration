
from tbjcfitE import *
import numpy as np
import matplotlib.pylab as plt

#def AsymGaussian(x,A,xc,w,t0):
def main():
    x = np.linspace(-10,10,1000)
    y = AsymGaussian(x,1.0,2.0,1.0,1.0)
    print ReturnAsymGaussianPeak( 1.0,2.0,1.0,1.0)

    #y = yfunc(x,1.0,1.0)

    #print y

    plt.plot(x,y)
    plt.show()

main()
