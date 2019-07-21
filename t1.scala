import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.Vectors
import sqlContext.implicits._
import org.apache.spark.sql.types._

var rdd = sc.textFile("/home/bsnova/Desktop/assignment/bat1.csv")

def stoDouble (s : String): Double = {
return s.map(_.toByte.doubleValue()).reduceLeft( (x,y) => x + y)
}

case class StateCode(State:String, Code:Double)
var lines = rdd.map(l => l.split(","))
var states = lines.map(l => StateCode(l(0),stoDouble(l(0)))).toDF()
states.show()
states.createOrReplaceTempView("states")

def makeDouble (s: String): Array[Double] = {
var str = s.split(",")
var a = stoDouble(str(0))
return Array(a,str(2).toDouble,str(3).toDouble)
}
var crime = rdd.map(m => makeDouble(m))

val crimeVector = crime.map(a => Vectors.dense(a(0),a(1),a(2)))
val clusters = KMeans.train(crimeVector,5,10)

case class Crime (Code:Double, Murder:Double, Assault:Double, UrbanPop:Double,Rape:Double, PredictionVector:org.apache.spark.mllib.linalg.Vector, Prediction:Double)
val crimeClass = crimeVector.map(a => Crime(a(0), a(1), a(2), a ,clusters.predict(a))).toDF()
crimeClass.show()
crimeClass.createOrReplaceTempView("crimes")
