import awswrangler as wr
import pandas as pd
import urllib.parse
import os

# Added by Ajinkya - Environment variables for configuration
os_input_s3_cleansed_layer = os.environ['s3_cleansed_layer']
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name']
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name']
os_input_write_data_operation = os.environ['write_data_operation']

def lambda_handler(event, context):
    # Added by Ajinkya - Extract bucket and file info from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        # Added by Ajinkya - Read JSON file from S3
        df_raw = wr.s3.read_json('s3://{}/{}'.format(bucket, key))
        
        # Added by Ajinkya - Extract nested 'items' array from JSON structure
        df_step_1 = pd.json_normalize(df_raw['items'])
        
        # Added by Ajinkya - Convert to Parquet and save to cleansed bucket
        wr_response = wr.s3.to_parquet(
            df=df_step_1,
            path=os_input_s3_cleansed_layer,
            dataset=True,
            database=os_input_glue_catalog_db_name,
            table=os_input_glue_catalog_table_name,
            mode=os_input_write_data_operation
        )
        return wr_response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

# What this function does:

# Triggers automatically when JSON files are uploaded to the raw S3 bucket
# Reads the JSON category files (like CA_category_id.json) that contain YouTube category mappings
# Extracts the nested data from the "items" field in the JSON structure
# Converts to Parquet format for better performance and smaller file size
# Saves to the transformed bucket with proper catalog registration
