import matplotlib.pyplot as pt
import pandas as pd 
import random 
import math
import re


dtype_spec = {
    'Pincode': int,  
    'Latitude':float,
    'Longitude':float
    
}
data=pd.read_csv("filteredData.csv",dtype=dtype_spec)



# kbest=3 #for  Telangana
kbest=2 #for  AP
# note k best is determined from elbow method
for k in range(kbest,kbest+1):

  clustters=[] #stores co-ordinates of cluster points
  SD=[[]] #stores square of distances of different points from different clustters -- k lists
  C=[] #stores which clustter the points are nearest

  #initializing clusters
  for i in range(k):
    SD.append([])
    clustters.append({})
    random_index=math.floor(random.random()*len(data))
    clustters[i]['Longitude']=(data['Longitude'].iloc[random_index])
    clustters[i]['Latitude']=(data['Latitude'].iloc[math.floor(random.random()*len(data))])

  #calculating square of distance from each clustter
  for i,point in data.iterrows():
    for j in range(k):
      SD[j].append(( (point['Longitude']) - (clustters[j]['Longitude'] ))**2 +( (point['Latitude']) - (clustters[j]['Latitude']) )**2)
  
  #saving them to dataframe
  for i in range(k):
    data['SD'+str(i)]=pd.DataFrame(SD[i])
  
  #assigning points to nearest cluster
  for i,point in data.iterrows():
    m=0 #0 to k-1
    for j in range(k):
      if(point['SD'+str(j)]<point['SD'+str(m)]):
        m=j
    C.append(m)

  #saving assigned clustters to dataframe
  data['C']=pd.DataFrame(C)


  #checks whether actual cluster is formed or not
  check=False


  while(not check):

    newClustters=[]
    SD=[[]]
    C=[]
    #locating new clusters 
    for i in range(k):
      newClustters.append({})
      SD.append([])
      newClustters[i]['Longitude']=data.loc[data['C']==i]['Longitude'].mean()
      newClustters[i]['Latitude']=data.loc[data['C']==i]['Latitude'].mean()
  
    #calculating square of distance from each newclustter
    for i,point in data.iterrows():
      for j in range(k):
        SD[j].append(((point['Longitude'])-(newClustters[j]['Longitude']))**2 +((point['Latitude']) -(newClustters[j]['Latitude']))**2)

    #assigning points to nearest cluster
    for i,point in data.iterrows():
      m=0 #0 to k-1
      # print(i,point)
      for j in range(k):
        if(SD[j][i]<SD[m][i]):
          m=j
      C.append(m)
  
    
    if(list(data['C'])==C):
      check=True
      
  
    clustters=newClustters
    data['C']=pd.DataFrame(C)
    for i in range(k):
      data['SD'+str(i)]=pd.DataFrame(SD[i])


  sum=0
  for i in range(k):
    sum+=data.loc[data['C']==i]['SD'+str(i)].sum()
  
  
    
print("clustering completed")

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

print("plotting Started")
colors=['blue','red','green','black','yellow']
for i in range(kbest):
  pt.scatter(data.loc[data['C']==i]['Longitude'], data.loc[data['C']==i]['Latitude'], color=colors[i], s=1,label='Clustter'+str(i))
  pt.scatter(clustters[i]['Longitude'],clustters[i]['Latitude'],color='yellow',s=20)

 

pt.xlabel('Longitude')
pt.ylabel('Latitude')
pt.title('Scatter Plot of Coordinates')
pt.xticks(lonlist)
pt.yticks(latlist)
pt.legend()
print("plotting completed")
pt.show()

