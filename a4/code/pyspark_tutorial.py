import pyspark

sc = pyspark.SparkContext('local[*]')

sample = sc.textFile(r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\sampleReviewData.txt')
negative = sc.textFile(r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\negative.txt')
positive = sc.textFile(r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\positive.txt')

negative_words = negative.flatMap(
    lambda line: line if line and line[0] != ";" else ['']
)
print(negative_words.collect())

positive_words = positive.flatMap(
    lambda line: line if line and line[0] != ";" else ['']
)
print(positive_words.collect())

word_counts = sample.map(
    lambda line: (line.split("\t"))
)

print(word_counts.reduceByKey(lambda a, b: a + b).collect())

positive_word_counts = word_counts.intersection(
    positive_words
).reduceByKey(lambda a, b: a + b)
print(positive_word_counts.collect())

negative_word_counts = negative_words.intersection(
    positive_words
).reduceByKey(lambda a, b: a + b)
print(negative_word_counts.collect())

# word_counts.saveAsTextFile(r'C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data\sampleResults.txt')