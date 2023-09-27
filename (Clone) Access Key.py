# Databricks notebook source
dbutils.fs.mount(

  source = "wasbs://raw@sanly.blob.core.windows.net",

  mount_point = "/mnt/sanly/raw",

  extra_configs = {"fs.azure.account.key.sanly.blob.core.windows.net":"+wZyMJdwqiETIzCNMc/uvE0AJQ/2+fIGVKKvfx4um7lsUO0EPZjLx3efLhF9OihDdkaV1TBwq77j+AStSZRQ1Q=="})



# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------

# MAGIC %fs/dbfs:/mnt/

# COMMAND ----------



# COMMAND ----------

dbfs:/mnt/


# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/
# MAGIC

# COMMAND ----------

# MAGIC %fs ls 
# MAGIC dbfs:/mnt/sanly/

# COMMAND ----------

# MAGIC %fs ls 
# MAGIC dbfs:/mnt/sanly/raw

# COMMAND ----------

df=spark.read.option('header',True).option('inferschema',True).csv('dbfs:/mnt/sanly/raw/Baby_Names.csv')

# COMMAND ----------

output="dbfs:/mnt/sanly/raw/output"

# COMMAND ----------



df.write.mode("overwrite").parquet(f"{output}/ayush/babyname")

# COMMAND ----------



dbutils.fs.mount(

  source = "wasbs://inputfiles@saunext.blob.core.windows.net",

  mount_point = "/mnt/saunext/inputfiles",

  extra_configs = {"fs.azure.account.key.saunext.blob.core.windows.net":"UUDMjjk8JYIiTwHNyh8WCs3BShkfIL//HM/cUrbOrRmUH+HaoR/J5bM9MlWTYefbkqNo/bQzgs1M+AStEn3dkA=="})

# COMMAND ----------

users_sch="timestamp timestamp, event_type string, user_id string, page_id string"

# COMMAND ----------

df=spark.readStream.schema(users_sch).json("dbfs:/mnt/saunext/inputfiles/inputstream/")

# COMMAND ----------

df.display()

# COMMAND ----------

outputstream="dbfs:/mnt/saunext/inputfiles/outputstream"

# COMMAND ----------

df.writeStream\
.option("checkpointlocation",f"{outputstream}/naval/checkpoint")\
.option("path",f"{outputstream}/ayush/output")\
.table("test.jsonsample")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from test.jsonsample

# COMMAND ----------

for stream in spark.streams.active:

    stream.stop()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from test.jsonsample

# COMMAND ----------

(spark

.readStream

.schema(users_sch)

.json("dbfs:/mnt/saunext/inputfiles/inputstream/")

.writeStream

.option("checkpointlocation",f"{outputstream}/naval/checkpoint")

.option("path",f"{outputstream}/naval/output")

.trigger(once=True)

.table("test.jsonsample")

)

# COMMAND ----------


