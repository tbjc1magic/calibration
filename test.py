
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from SlopeFit import SlopeFit
from tbjcSQL import ReadFile2SQL, GetChannelData, CreateFittingTable, GetChannelFit, UpdateChannelFit
from tbjcfitE import returnEverything,ReturnAsymGaussianPeak

from Tkinter import *
import pylab
from pylab import *
import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

#################################################################
##################User Graphic Interface#########################
#################################################################

def _quit():
    global root
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

###########################################################
################### UpdateTextBoxValue ####################
###########################################################

def UpdateTextBoxValue(fitparameters):
    global PeakFitList,farfit, nearfit, SQLextra,bfit

    SQLextra.delete(1.0,END)
    SQLextra.insert(INSERT,fitparameters["SQLextra"])

    farfit.delete(1.0,END)
    farfit.insert(INSERT,fitparameters["farfit"])

    nearfit.delete(1.0,END)
    nearfit.insert(INSERT,fitparameters["nearfit"])

    bfit.delete(1.0,END)
    bfit.insert(INSERT,fitparameters["bfit"])

    PeakFitList_Name = ["A1fit", "xc1fit", "w1fit", "t1fit","A2fit", "xc2fit", "w2fit", "t2fit",'bfit']
    for i in xrange(8):
       PeakFitList[i].delete(1.0,END)
       PeakFitList[i].insert(INSERT,fitparameters[PeakFitList_Name[i]])

def RetrieveTextBoxValue(CurrentID):

    PeakFitList_Name = ["A1fit", "xc1fit", "w1fit", "t1fit","A2fit", "xc2fit", "w2fit", "t2fit",'bfit']

    retrievedict = {}
    txt = SQLextra.get(1.0,END).rstrip('\n')
    retrievedict["SQLextra"]=txt

    txt = farfit.get(1.0,END)
    retrievedict["farfit"]=float(txt)

    txt = nearfit.get(1.0,END)
    retrievedict["nearfit"]=float(txt)

    txt = bfit.get(1.0,END)
    retrievedict["bfit"]=float(txt)

    for i in xrange(8):
        txt = PeakFitList[i].get(1.0,END)
        retrievedict[PeakFitList_Name[i]] = float(txt)

    retrievedict["channelID"]=CurrentID
    return retrievedict

###########################################################
################### UpdateFigure ##########################
###########################################################

def UpdateFigure( fitParameters ):
    global line1,canvas, line2,line2_fit ,ax1, ax2
    channelID = fitParameters["channelID"]
    aa=GetChannelData("test.db",channelID, fitParameters["SQLextra"])
    datalist = tuple((zip(*(row[2:5] for row in aa))))
    slfit = SlopeFit(datalist,[fitParameters["farfit"],fitParameters["nearfit"],0])

    xdata,ydata,popt,newy = returnEverything(datalist[0],(fitParameters["A1fit"],fitParameters["xc1fit"],fitParameters["w1fit"],fitParameters["t1fit"],fitParameters["A2fit"],fitParameters["xc2fit"],fitParameters["w2fit"],fitParameters["t2fit"]))

    fitParameters["A1fit"]    = popt[0]
    fitParameters["xc1fit"]   = popt[1]
    fitParameters["w1fit"]    = popt[2]
    fitParameters["t1fit"]    = popt[3]
    fitParameters["A2fit"]    = popt[4]
    fitParameters["xc2fit"]   = popt[5]
    fitParameters["w2fit"]    = popt[6]
    fitParameters["t2fit"]    = popt[7]
    fitParameters["nearfit"]  = slfit[1]
    fitParameters["farfit"]   = slfit[0]
    fitParameters["bfit"]   = slfit[2]

    #print "fit parameters", fitParameters
    UpdateTextBoxValue(fitParameters)

    datalist1 = [x*slfit[0] for x in datalist[1]]
    datalist2 = [x*slfit[1] for x in datalist[2]]
    line1[0].set_data(datalist1,datalist2)

    xlimit = max(xdata)
    ylimit = max(ydata)

    ax2.set_xlim([0,xlimit*1.2])
    ax2.set_ylim([0,ylimit*1.2])

    line2[0].set_data(xdata,ydata)
    line2_fit[0].set_data(xdata,newy)

    fitpara = GetChannelFit("test.db",channelID)

    canvas.draw()

###########################################################
################### InitialCanvas #########################
###########################################################

def GetCurrentChannel():
    global CurrentChannelDisplay
    channelID = int(CurrentChannelDisplay.get()[8:])
    return channelID

###########################################################
################### InitialCanvas #########################
###########################################################

def SetCurrentChannel(newchannelID, replot=True):
    global CurrentChannelDisplay
    channelID = int(CurrentChannelDisplay.get()[8:])
    if(newchannelID == channelID or (not replot)): return
    CurrentChannelDisplay.set('channel '+str(newchannelID))

###########################################################
################### InitialCanvas #########################
###########################################################

def InitialCanvas():
    global canvas, line1,line2,line2_fit,ax1,ax2, root, CurrentChannelDisplay, callback1, SQLextra, farfit, nearfit, farfit, bfit, PeakFitList, saveCallBack, fitCallBack

    root.minsize(width=1000,height =600)
    root.maxsize(width=1000,height =600)
    ############### channel Picker #####################
    CurrentChannelDisplay =  StringVar()
    CurrentChannelDisplay.set("channel 0") # default value
    CurrentChannelDisplay.trace("w",channelchanged)

    channelPick = OptionMenu(root, CurrentChannelDisplay,'0')

    channelPick['menu'].delete(0,'end')
    #CurrentChannelDisplay.set("channel 0") # default value

    channelPick.place( rely=0.00,relx=0.4,relwidth = 0.15, relheight = 0.05)
    for index in range(24):
        channelPick['menu'].add_command( label='channel '+str(index), command=lambda index =index: SetCurrentChannel(index))

    ############### channel Picker #####################
    button = Tkinter.Button(root, text ="readfile", command = pickupfile)
    button.place(relx=0.6, rely=0.00,relwidth = 0.1, relheight =0.05)

    button = Tkinter.Button(root, text ="save fit", command = filefit)
    button.place(relx=0.75, rely=0.00,relwidth = 0.1, relheight =0.05)

    ############## canvas on TkAgg #####################

    figureframe = Frame(root)
    figureframe.pack()

    fig = pylab.figure(1)
    ax1 = fig.add_subplot(121)
    ax1.grid(True)
    ax1.set_title("Near vs Far plot")
    ax1.set_xlabel("Far")
    ax1.set_ylabel("Near")
    ax1.axis([0,2000,0,2000])
    line1=ax1.plot([0], [0],'.')

    ax2 = fig.add_subplot(122)
    ax2.grid(True)
    ax2.set_title("Energy Plot")
    ax2.set_xlabel("Energy")
    ax2.set_ylabel("Counts")
    ax2.axis([0,2000,0,2000])
    line2=ax2.plot([0], [0],'.')
    line2_fit=ax2.plot([0,1000],[0,1000],'-',c='r')
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.show()
    canvas.get_tk_widget().place(  relwidth=0.95, relheight =0.68, relx=0.025, rely=0.05)

    ############# NavigationToolBar #####################
    #toolbar = NavigationToolbar2TkAgg( canvas, root )
    #toolbar.update()
    #canvas._tkcanvas.pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH, expand=1)

    ############ far vs near fit #########################
    nearlabel = Label( root, text="near*", relief=RAISED )
    nearlabel.place(relwidth=0.05,relheight=0.03, relx=0.04, rely=0.06)

    nearfit = Tkinter.Text(root)
    nearfit.insert(INSERT, "")
    nearfit.place(relwidth=0.07,relheight=0.03, relx=0.1, rely=0.06)

    farlabel = Label( root, text="far*", relief=RAISED )
    farlabel.place(relwidth=0.05,relheight=0.03, relx=0.4, rely=0.69)

    farfit = Tkinter.Text(root)
    farfit.insert(INSERT, "")
    farfit.place(relwidth=0.07,relheight=0.03, relx=0.46, rely=0.69)

    blabel = Label( root, text="b", relief=RAISED )
    blabel.place(relwidth=0.05,relheight=0.03, relx=0.04, rely=0.62)

    bfit = Tkinter.Text(root)
    bfit.insert(INSERT, "")
    bfit.place(relwidth=0.07,relheight=0.03, relx=0.04, rely=0.67)

    ############ SQL text extra #########################
    SQLtextlabel = Label( root, text="SQL", relief=RAISED )
    SQLtextlabel.place(relwidth=0.05,relheight=0.03, relx=0.22, rely=0.74)

    SQLextra = Tkinter.Text(root)
    SQLextra.insert(INSERT, "(near + far)>1000")
    #SQLextra.insert(END, "Bye Bye.....")
    SQLextra.place(  relwidth=0.45, relheight =0.2, relx=0.025, rely=0.78)

    ########### put input and buttons #############################

    controlframe = Frame(root)
    controlframe.place(relwidth=0.45, relheight =0.2, relx=0.525, rely=0.75)

    Peak1List_Name = ["A1", "xc1", "w1", "t1"]
    Peak2List_Name = ["A2", "xc2", "w2", "t2"]

    for index in range(len(Peak1List_Name)):
        tmplabel=Label(root, text=Peak1List_Name[index], relief=RAISED)
        tmplabel.place(in_=controlframe,bordermode=OUTSIDE, width=0.08*root.winfo_width(), height=0.03*root.winfo_height(), relx=0., rely=0.05+0.3*index)

        PeakFitList[index] = Tkinter.Text(root)
        #PeakFitList[index].insert(INSERT, "")
        PeakFitList[index].place(in_=controlframe,bordermode=OUTSIDE ,width=0.07*root.winfo_width(),height=0.03*root.winfo_height(), relx=0.2, rely=0.05+0.3*index)

        tmplabel=Label(root, text=Peak2List_Name[index], relief=RAISED)
        tmplabel.place(in_=controlframe,bordermode=OUTSIDE, width=0.08*root.winfo_width(), height=0.03*root.winfo_height(), relx=0.4, rely=0.05+0.3*index)

        PeakFitList[index+4] = Tkinter.Text(root)
        #PeakFitList[index+4].insert(INSERT, "")
        PeakFitList[index+4].place(in_=controlframe,bordermode=OUTSIDE ,width=0.07*root.winfo_width(),height=0.03*root.winfo_height(), relx=0.6, rely=0.05+0.3*index)

    button = Tkinter.Button(root, text ="fit", command = fitCallBack)
    button.place(in_=controlframe,relx=0.8, rely=0.05,relwidth = 0.2, relheight =0.2)

    button = Tkinter.Button(root, text ="save", command = saveCallBack)
    button.place(in_=controlframe,relx=0.8, rely=0.35,relwidth = 0.2, relheight =0.2)

    button = Tkinter.Button(root, text ="copy", command = copyCallBack)
    button.place(in_=controlframe,relx=0.8, rely=0.65,relwidth = 0.2, relheight =0.2)

    button = Tkinter.Button(root, text ="paste", command = pasteCallBack)
    button.place(in_=controlframe,relx=0.8, rely=0.95,relwidth = 0.2, relheight =0.2)

    ########### set the initial page ####################

    CurrentChannelDisplay.set("channel 0") # default value

##########################################################
################### global savedict#######################
##########################################################
fitcache = None

###########################################################
################### copycallback ###########################
###########################################################

def copyCallBack(*args):
    global fitcache
    fitcache = RetrieveTextBoxValue(100)
    return
###########################################################
################### pastecallback ###########################
###########################################################

def pasteCallBack(*args):
    global fitcache
    if fitcache is not None:
        UpdateTextBoxValue(fitcache)
    return

###########################################################
################### fitcallback ###########################
###########################################################

def fitCallBack(*args):
    CurrentChannel = GetCurrentChannel()
    fitdict = RetrieveTextBoxValue(CurrentChannel)
    UpdateFigure(fitdict)

###########################################################
################### fitcallback ###########################
###########################################################

from tkFileDialog import askopenfilename

def pickupfile(*args):

    CurrentChannel = GetCurrentChannel()
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    if(filename==""): return
    with open(filename) as f:
        ReadFile2SQL(f,"test.db")
        CreateFittingTable("test.db")
        SetCurrentChannel(CurrentChannel,replot=False)
        fitdict=GetChannelFit("test.db",CurrentChannel)
        print fitdict
        UpdateFigure(fitdict)

###########################################################
################### fitcallback ###########################
###########################################################

from tkFileDialog import asksaveasfile

def filefit():
    f = asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return

    text2save = ""

    for channelID in xrange(24):
        fitdict = GetChannelFit("test.db",channelID)
        text2save = text2save+ str(channelID)+" "+str(fitdict["farfit"]) + " " + str(fitdict["nearfit"])+ " "+str(fitdict['bfit'])+" ""\n"
    text2save = text2save + "\n"

    AlphaE1 = 3.1828
    AlphaE2 = 5.8048

    for channelID in xrange(24):
        fitdict = GetChannelFit("test.db",channelID)
        xc1 = fitdict["xc1fit"]
        A1 = fitdict["A1fit"]
        w1 = fitdict["w1fit"]
        t1 = fitdict["t1fit"]

        xc2 = fitdict["xc2fit"]
        A2 = fitdict["A2fit"]
        w2 = fitdict["w2fit"]
        t2 = fitdict["t2fit"]

        P1 = ReturnAsymGaussianPeak( A1, xc1, w1, t1)
        P2 = ReturnAsymGaussianPeak( A2, xc2, w2, t2)

        print P1, P2,xc1,xc2
        Ea = (AlphaE1-AlphaE2)/(P1-P2)
        Eb = (AlphaE2*P1-AlphaE1*P2)/(P1-P2)

        text2save =  text2save+ str(channelID)+" "+str(Ea)+" "+ str(Eb)+"\n"
    text2save = text2save + "\n"

    f.write(text2save)
    f.close()

###########################################################
################### savecallback ##########################
###########################################################

def saveCallBack(*args):
    CurrentChannel = GetCurrentChannel()
    savedict = RetrieveTextBoxValue(CurrentChannel)
    UpdateFigure(savedict)
    savedict = RetrieveTextBoxValue(CurrentChannel)
    UpdateChannelFit("test.db",savedict)

###########################################################
###################### channelchanged #####################
###########################################################

def channelchanged(*args):
    global  SQLextra,PeakFitList,farfit, nearfit
    channelID = GetCurrentChannel()
    fitparameters = GetChannelFit("test.db",channelID)
    UpdateTextBoxValue(fitparameters)
    UpdateFigure(fitparameters)

###################################################################
############### Global CurrentChannelDisplays Definition ##########
###################################################################

root = Tkinter.Tk()
canvas = None
ax1 = None
ax2 = None
line1 = None
line2 = None
line2_fit = None
CurrentChannelDisplay = None
SQLextra = None
farfit = None
nearfit = None
bfit = None
PeakFitList = [None for i in range(8)]

InitialCanvas()

root.wm_title("Extended Realtime Plotter")
root.protocol("WM_DELETE_WINDOW", _quit)  #thanks aurelienvlg

Tkinter.mainloop()
