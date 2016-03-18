SQLmodel= {
    "farfit":"double",
    "nearfit":"double",

    "A1fit":"double",
    "xc1fit":"double",
    "w1fit":"double",
    "t1fit":"double",

    "A2fit":"double",
    "xc2fit":"double",
    "w2fit":"double",
    "t2fit":"double"
}

SQLmodel_list= [
    ("farfit","double"),
    ("nearfit","double"),

    ("A1fit","double"),
    ("xc1fit","double"),
    ("w1fit","double"),
    ("t1fit","double"),

    ("A2fit","double"),
    ("xc2fit","double"),
    ("w2fit","double"),
    ("t2fit","double")



]

print SQLmodel_list

SQLCreate_query = "CREATE TABLE Fitting(channelID integer primary key"

for modelkey,modeltype in SQLmodel_list:
    SQLCreate_query = SQLCreate_query +", "+modelkey+" "+modeltype

SQLCreate_query = SQLCreate_query +")"

print "SQLCreate_query"
print SQLCreate_query

cf=3

SQLInsert_query = "insert into fitting values("+str(cf)

for key,value in SQLmodel_list:
    SQLInsert_query = SQLInsert_query + ",1"

SQLInsert_query = SQLInsert_query + ")"

print SQLInsert_query

row=[0,2,3,1,0,0,0,0,0,0,0]
SelectReturn_dict = {"channelID":row[0]}

for index, (key,value) in enumerate(SQLmodel_list):
    print index+1, key
    SelectReturn_dict[key]=row[index+1]

print
print "SelectReturn_dict"
print SelectReturn_dict 


SQLUpdate_query = "update Fitting set "


for index, (key,value) in enumerate(SQLmodel_list):
    if index != 0: SQLUpdate_query = SQLUpdate_query + ","
    SQLUpdate_query = SQLUpdate_query + key+"=:"+key
SQLUpdate_query = SQLUpdate_query +" where channelID=:channelID"


print SQLUpdate_query


