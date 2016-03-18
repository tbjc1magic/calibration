#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite

SQLmodel_list= [
    ("farfit","double",1),
    ("nearfit","double",1),
    ("bfit","double",1),

    ("A1fit","double",1),
    ("xc1fit","double",1),
    ("w1fit","double",1),
    ("t1fit","double",1),

    ("A2fit","double",1),
    ("xc2fit","double",2),
    ("w2fit","double",1),
    ("t2fit","double",1),

    ("SQLextra","text","\"\"")
]

def ReadFile2SQL(f,DBname):

    con = lite.connect(DBname)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS CalData")
        cur.execute("CREATE TABLE CalData(Id INTEGER PRIMARY KEY, channelID integer,energy integer, far integer, near integer)")
        dataID = 0

        line =""
        while(1):
            dataID = dataID + 1;
            line = f.readline()
            if(line==""): break
            print line
            cf, e, fs, ns = line.split()
            print dataID, cf, e,fs, ns
            cf= int(cf)
            e = float(e)
            fs = float(fs)
            ns = float(ns)
    #        #tbjclist[cf] = tbjclist[cf] + [[e,fs,ns]]
            cur.execute("INSERT INTO CalData VALUES (?,?,?,?,?)",(dataID, cf, e, fs, ns))

def GetChannelData(DBname,channelID,additional=""):
    #print "hello there"
    con = lite.connect(DBname)
    with con:
        cur = con.cursor()
        SQLquery = "select * from CalData where channelID ="+str(channelID)
        SQLquery_extra = SQLquery
        if not (additional.isspace() or additional==''):
            SQLquery_extra = SQLquery+" and "+additional

        try:
            cur.execute(SQLquery_extra)
            while(1):
                row = cur.fetchone()
                if row is None: break
                yield row

        except Exception:
            cur.execute(SQLquery)
            while(1):
                row = cur.fetchone()
                if row is None: break
                yield row
            print "**************************"
            print SQLquery_extra
            print "SQL query error, try again"
            print "**************************"

def CreateFittingTable(DBname):
    con = lite.connect(DBname)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Fitting")

        SQLCreate_query = "CREATE TABLE Fitting(channelID integer primary key"

        for modelkey,modeltype,modelinit in SQLmodel_list:
            SQLCreate_query = SQLCreate_query +", "+modelkey+" "+modeltype

        SQLCreate_query = SQLCreate_query +")"

        cur.execute(SQLCreate_query)

        for cf in xrange(24):
            SQLInsert_query = "insert into fitting values("+str(cf)
            for key,value,init in SQLmodel_list:
                SQLInsert_query = SQLInsert_query + ","+ str(init)

            SQLInsert_query = SQLInsert_query + ")"
            print SQLInsert_query
            cur.execute(SQLInsert_query)

def GetChannelFit(DBname,channelID):
    #print "hello there"
    con = lite.connect(DBname)
    with con:
        cur = con.cursor()
        SQLquery = "select * from Fitting where channelID ="+str(channelID)

        try:
            cur.execute(SQLquery)
            row = cur.fetchone()

            SelectReturn_dict = {"channelID":row[0]}

            for index, (key,value,init) in enumerate(SQLmodel_list):
                SelectReturn_dict[key]=row[index+1]

            return SelectReturn_dict

        except Exception:
            print "**************************"
            print SQLquery
            print "SQL query error, try again"
            print "**************************"

def UpdateChannelFit(DBname,NewFit):
    #print "hello there"
    print NewFit
    con = lite.connect(DBname)
    with con:
        cur = con.cursor()

        SQLUpdate_query = "update Fitting set "

        for index, (key,value,init) in enumerate(SQLmodel_list):
            if index != 0: SQLUpdate_query = SQLUpdate_query + ","
            SQLUpdate_query = SQLUpdate_query + key+"=:"+key
        SQLUpdate_query = SQLUpdate_query +" where channelID=:channelID"

        try:
            cur.execute(SQLUpdate_query,NewFit)

        except Exception:
            print "**************************"
            print SQLUpdate_query
            print "SQL query error, try again"
            print "**************************"
