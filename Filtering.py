import matplotlib.pyplot as pt
import pandas as pd 
import random 
import math
import re


dtype_spec = {
    'Pincode': str,  
    'Latitude':str,
    'Longitude':str
    
}
completedata=pd.read_csv("clustering_data.csv")

HomeState="ANDHRA PRADESH"
maxlat=20
minlat=12
maxlon=85
minlon=76


# HomeState="TELANGANA"
# maxlat=20
# minlat=15
# maxlon=82
# minlon=77


data=completedata.loc[completedata['StateName']==HomeState]
pincodes=data['Pincode']
data.to_csv('loc.csv')

print(len(data))
for index,location in data.iterrows():
  pattern=r'[a-zA-Z\s]'


  list1=re.split(pattern,str(location['Latitude']))
  check=False
  for element in list1:
    if(re.fullmatch(r'^[-+]?\d*\.?\d+$',element)):
      location['Latitude']=float(element)
      check=True
      break
  if(not check):
    data=data.drop(index)
  else:


    check=False   
    list2=re.split(pattern,str(location['Longitude']))
    for element in list2:
      if(re.fullmatch(r'^[-+]?\d*\.?\d+$',element)):
        location['Longitude']=float(element)
        check=True
        break
    if(not check):
      data=data.drop(index)

print(len(data))
data=data.reset_index()


data.to_csv('Lat.csv')

data['Latitude']=data['Latitude'].astype(float)
data['Longitude']=data['Longitude'].astype(float)

data=data.loc[(data['Latitude']<maxlat) & (data['Longitude']<maxlon) &(data['Latitude']>minlat) & (data['Longitude']>minlon)]

data[['Pincode','Latitude','Longitude']].to_csv('filteredData.csv')

Maxlon=math.ceil(data['Longitude'].max())
Minlon=math.floor(data['Longitude'].min())
Maxlat=math.ceil(data['Latitude'].max())
Minlat=math.floor(data['Latitude'].min())

print(Maxlat,Minlat,Maxlon,Minlon)

latlist=[Minlat]
lonlist=[Minlon]
i=Minlon
while(i<=Maxlon):
  i+=1
  lonlist.append(i)

j=Minlat
while(j<=Maxlat):
  j+=1
  latlist.append(j)




for index,location in data.iterrows():
  pt.plot(location['Longitude'],location['Latitude'],'b.-')
  
pt.xticks(lonlist)
pt.yticks(latlist)
pt.show()