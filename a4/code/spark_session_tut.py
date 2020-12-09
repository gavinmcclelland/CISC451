from pyspark.sql import SparkSession
# from pyspark.sql.functions import count, udf, explode, array, sum, col, abs, countDistinct, split
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType, Row, FloatType

POSITIVE_PATH = r"C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\positive.txt"
NEGATIVE_PATH = r"C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\negative.txt"

def determine_review_sentiment(positive_file_path, negative_file_path, reviews_file_path, output_dir):

    with open(positive_file_path, "r") as f:
        positive_words = [line.strip() for line in f.readlines() if line[0] != ";" and line.strip() != ""]

    with open(negative_file_path, "r") as f:
        negative_words = [line.strip() for line in f.readlines() if line[0] != ";" and line.strip() != ""]


    def classify_review(body):
        pos = 0
        neg = 0
        for word in body.split(" "):
            if word in positive_words:
                pos += 1
            elif word in negative_words:
                neg += 1
        if pos > neg:
            return 1
        else:
            return -1


    def get_label(review_score):
        if review_score > 0:
            return "positive"
        elif review_score < 0:
            return "negative"
        else:
            return "neutral"


    def get_percentage(parameter_array):
        num_reviews = parameter_array[0]
        margin = abs(parameter_array[1])
        return (((num_reviews - margin) /2) + margin) / num_reviews * 100


    # Convert to a udf functions
    get_label_udf = F.udf(get_label, StringType())
    get_percentage_udf = F.udf(get_percentage, FloatType())
    classify_review_udf = F.udf(classify_review, IntegerType())

    spark = SparkSession.builder.master("local")\
        .config("spark.executor.memory", "3g")\
        .config("spark.driver.memory", "2g")\
        .appName("Review Classifier").getOrCreate()
    # spark.conf.set("spark.sql.files.maxPartitionBytes", '10m')
    # spark.conf.set("spark.default.parallelism", 4)
    # spark.conf.set("spark.sql.shuffle.partitions", 500)
    # spark.conf.set("spark.executor.memory", "2g")

    schema = StructType() \
        .add("MemberID",StringType(),True) \
        .add("ProductID",StringType(),True) \
        .add("Date",StringType(),True) \
        .add("NumHelpfulFeedback",StringType(),True) \
        .add("NumFeedback",StringType(),True) \
        .add("Rating",StringType(),True) \
        .add("Title",StringType(),True) \
        .add("Body",StringType(),True)

    reviews = spark.read.csv(
        reviews_file_path,
        sep="\t",
        schema=schema
        ).select(
            "ProductID",
            "Body",
        ).dropna().repartition(1000, "ProductID")
    print(reviews.count())

    # partition_mapping = {}
    # for index, product_id in enumerate(reviews.select("ProductID").distinct().collect()):
    #     partition_mapping[product_id["ProductID"]] = index
    # print(partition_mapping)
    # num_partitions = index + 1

    # def product_group_partitioner(key):
    #     return partition_mapping[key]

    # reviews = reviews.rdd.map(lambda row: (row[0], row))
    # reviews = reviews.partitionBy(num_partitions, product_group_partitioner)
    # reviews = spark.createDataFrame(reviews.map(lambda row: row[1]))

    # reviews = reviews.withColumn("Classification", classify_review_udf("Body"))
    reviews = reviews.withColumn("Body", F.split(F.trim(F.col("Body"))), " ")
    reviews = reviews.groupby(
        ['ProductID']
        ).agg(
            F.count("Classification").alias('NumReviews'),
            F.sum("Classification").alias("ReviewScore")
        )
    # reviews.createOrReplaceTempView("REVIEWS")
    # reviews = spark.sql(
    #     "SELECT ProductID, NumReviews,"
    #     " CASE"
    #     "   WHEN ReviewScore > 0 THEN 'positive'"
    #     "   WHEN ReviewScore < 0 THEN 'negative'"
    #     "   ELSE 'neutral'"
    #     " END AS Label,"
    #     " (((NumReviews - abs(ReviewScore)) / 2) + abs(ReviewScore)) / NumReviews * 100.0 AS Percentage"
    #     " FROM REVIEWS"
    # )
            # ).withColumn("Label", get_label_udf("ReviewScore")
            # ).withColumn(
            #     "Percentage",
            #     ((((col('NumReviews') - abs(col("ReviewScore"))) / 2) + abs(col("ReviewScore"))) / col('NumReviews') * 100.0))
            # ).withColumn("Percentage", get_percentage_udf(array("NumReviews", "ReviewScore")))

    reviews.write.csv(output_dir)


if __name__ == "__main__":
    determine_review_sentiment(
        POSITIVE_PATH,
        NEGATIVE_PATH,
        r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\reviews.txt',
        'SENTAMENT_RESULTS'
    )