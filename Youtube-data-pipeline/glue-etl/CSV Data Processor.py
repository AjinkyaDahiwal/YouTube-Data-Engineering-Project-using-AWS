import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

#  Job initialization
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

#  Filter for specific regions only
predicate_pushdown = "region in ('ca','gb','us')"

#  Read CSV data from Glue catalog
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "db_youtube_raw", 
    table_name = "raw_statistics", 
    transformation_ctx = "datasource0", 
    push_down_predicate = predicate_pushdown
)

#  Map and cast data types properly
applymapping1 = ApplyMapping.apply(
    frame = datasource0, 
    mappings = [
        ("video_id", "string", "video_id", "string"), 
        ("trending_date", "string", "trending_date", "string"), 
        ("title", "string", "title", "string"), 
        ("channel_title", "string", "channel_title", "string"), 
        ("category_id", "long", "category_id", "long"), 
        ("publish_time", "string", "publish_time", "string"), 
        ("tags", "string", "tags", "string"), 
        ("views", "long", "views", "long"), 
        ("likes", "long", "likes", "long"), 
        ("dislikes", "long", "dislikes", "long"), 
        ("comment_count", "long", "comment_count", "long"), 
        ("thumbnail_link", "string", "thumbnail_link", "string"), 
        ("comments_disabled", "boolean", "comments_disabled", "boolean"), 
        ("ratings_disabled", "boolean", "ratings_disabled", "boolean"), 
        ("video_error_or_removed", "boolean", "video_error_or_removed", "boolean"), 
        ("description", "string", "description", "string"), 
        ("region", "string", "region", "string")
    ], 
    transformation_ctx = "applymapping1"
)

#  Handle schema conflicts
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")

#  Remove rows with null values
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")

#  Optimize file size and partitioning
datasink1 = dropnullfields3.toDF().coalesce(1)
df_final_output = DynamicFrame.fromDF(datasink1, glueContext, "df_final_output")

# Write final data with region partitioning
datasink4 = glueContext.write_dynamic_frame.from_options(
    frame = df_final_output, 
    connection_type = "s3", 
    connection_options = {
        "path": "s3://de-on-youtube-cleansed-useast1-dev/youtube/raw_statistics/", 
        "partitionKeys": ["region"]
    }, 
    format = "parquet", 
    transformation_ctx = "datasink4"
)

job.commit()

# What this job does:

# Processes the CSV video statistics files from multiple regions
# Filters data to focus on Canada, Great Britain, and United States only
# Standardizes data types and resolves schema conflicts
# Removes incomplete records with null values
# Partitions the output by region for faster queries
# Saves optimized Parquet files to the analytics bucket