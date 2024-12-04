# K_mean-Clusttering

## About
- Implemented k means cluttering from scratch using elbow method to identify best k.
- The file clustering_data.csv has location details of post offices through out india , this application is used to filter data of particular state and divide those locations into clusters and show them in map.
## How to Use
- First run filter_data.py , it creates another csv file "filteredData.csv" having details of the state mentioned in filter_data.csv file. 
- Now run bestk_elbowmethod.py , it plots the graph k Vs WCSS , from this graph  we can find best k for clusttering.
- Now run kmeans.py file after changing variable kbest to the value identified previously , this plots graph after clustering locations.


