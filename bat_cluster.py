from __future__ import print_function

from numpy import array
from math import sqrt
import csv

from pyspark import SparkContext

from pyspark.mllib.clustering import KMeans, KMeansModel
cluster_no = 6
if __name__ == "__main__":
    sc = SparkContext(appName="KMeansExample")  # SparkContext
    
    
  
    
    data = sc.textFile("/home/bsnova/Desktop/assignment/bat11.csv")
    parsedData=data.map(lambda line: array([float(x) for x in line.split(',')]))

    # Build the model (cluster the data)
    clusters = KMeans.train(parsedData,cluster_no, maxIterations=16000, initializationMode="random")

    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))

    WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)

    
    print ("\n\n\n\n\n\n")
    cluster_ind =clusters.predict(parsedData)
    x=cluster_ind.collect()
    print (x)

    cluster_sizes = cluster_ind.countByValue().items()
    print (cluster_sizes)
    print("Within Set Sum of Squared Error = " + str(WSSSE))
    print ("\n\n\n\n\n\n")

    clusters = []
    for i in range(0,cluster_no):
        clusters.append([])
    with open('/home/bsnova/Desktop/assignment/bat1.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            temp = x[line_count]
            temp2=[row[0],row[1],row[2]]
            clusters[temp].append(temp2)
            line_count=line_count+1
    csv_file.close()
    with open('/home/bsnova/Desktop/assignment/batc.csv', 'w') as File:
        writer = csv.writer(File)
        for i in range(0,len(clusters)):
            for j in range(0,len(clusters[i])):
                row=[clusters[i][j][0],i,clusters[i][j][1],clusters[i][j][2]]
                writer.writerow(row)
    File.close()
    print (clusters)
    
    
    # Save and load model
    clusters.save(sc, "target/project1")
    sameModel = KMeansModel.load(sc, "target/project1")
    sc.stop()