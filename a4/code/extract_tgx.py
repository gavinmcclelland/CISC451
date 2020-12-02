import shutil
from os.path import join
data_dir = r"C:\Users\mcunningham\Documents\PythonProjects\CISC451\a4\data"
spark_dir = r"C:\Spark"
downloads_fir = r"C:\Users\mcunningham\Downloads"

# shutil.unpack_archive(join(data_dir, 'reviews.tgz'), data_dir)
shutil.unpack_archive(join(downloads_fir, 'spark-3.0.1-bin-hadoop2.7.tgz'), spark_dir)