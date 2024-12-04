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
completedata=pd.read_csv("clustering_data.csv",dtype=dtype_spec)

HomeState="TELANGANA"
data=completedata.loc[completedata['StateName']==HomeState]
pincodes=data['Pincode']

print(len(data))
for index,location in data.iterrows():
  pattern=r'[a-zA-Z]'


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
WCSS=[]
data=data.reset_index()


for k in range(1,10):


  clustters=[] #stores co-ordinates of cluster points
  SD=[[]] #stores square of distances of different points from different clustters -- k lists
  C=[] #stores which clustter the points are nearest

  #initializing clusters
  for i in range(k):
    SD.append([])
    clustters.append({})
    random_index=math.floor(random.random()*len(data))
    clustters[i]['Longitude']=data['Longitude'].iloc[random_index]
    clustters[i]['Latitude']=data['Latitude'].iloc[math.floor(random.random()*len(data))]

  #calculating square of dustance from each clustter
  for i,point in data.iterrows():
    for j in range(k):
      SD[j].append(( float(point['Longitude']) - float(clustters[j]['Longitude'] ))**2+ ( float(point['Latitude']) - float(clustters[j]['Latitude']) )**2)
  
  #saving them to dataframe
  for i in range(k):
    data['SD'+str(i)]=SD[i]
  
  #assigning points to nearest cluster
  for i,point in data.iterrows():
    m=0 #0 to k-1
    for j in range(k):
      if(SD[j][i]<SD[m][i]):
        m=j
    C.append(m)

  #saving assigned clustters to dataframe
  data['C']=C


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
      newClustters[i]['Longitude']=pd.to_numeric(data.loc[data['C']==i]['Longitude']).mean()
      newClustters[i]['Latitude']=pd.to_numeric(data.loc[data['C']==i]['Latitude']).mean()
  
    #calculating square of distance from each newclustter
    for i,point in data.iterrows():
      for j in range(k):
        SD[j].append((float(point['Longitude'])-float(newClustters[j]['Longitude']))**2+ (float(point['Latitude']) -float(newClustters[j]['Latitude']))**2)

    #assigning points to nearest cluster
    for i,point in data.iterrows():
      m=0 #0 to k-1
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
  WCSS.append(sum)
  print(k)
    
array=[1,2,3,4,5,6,7,8,9]
pt.plot(array,WCSS)
pt.show()

# maxlon=math.ceil(data['Longitude'].max())
# minlon=math.floor(data['Longitude'].min())
# maxlat=math.ceil(data['Latitude'].max())
# minlat=math.floor(data['Latitude'].min())

# latlist=[minlat]
# lonlist=[minlon]
# i=minlon
# while(i<=maxlon):
#   i+=2
#   lonlist.append(i)

# j=minlat
# while(j<=maxlat):
#   j+=3
#   latlist.append(j)




# for index,location in data.iterrows():
#   pt.plot(location['Longitude'],location['Latitude'],'b.-')
  
# pt.xticks(lonlist)
# pt.yticks(latlist)
# pt.show()