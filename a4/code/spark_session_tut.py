from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.master(
    "local"
    ).appName("Word Count"
    ).config("spark.sql.execution.arrow.pyspark.enabled", "true"
    ).getOrCreate()

reviews = pd.read_csv(
    r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\sampleReviewData.txt',
    names=["MemberID","ProductID","Date","NumHelpfulFeedback","NumFeedback","Rating","Title","Body"],
    sep="\t",
    header=None,
)
print(reviews.head())

reviews = spark.createDataFrame(reviews)
reviews.withColumn("")
print(reviews.collect())
