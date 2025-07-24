# YouTube-Data-Engineering-Project-using-AWS
Hey there! I built this project to show how I can handle real-world data challenges using AWS cloud services. This pipeline takes messy YouTube trending data and transforms it into something useful for business decisions.

# What This Project Does
Imagine you're working for a marketing company that wants to understand what makes YouTube videos go viral. They need to analyze trending patterns across different countries to plan their ad campaigns better. This project solves exactly that problem by building a complete data pipeline that processes YouTube trending data automatically.
#The Dataset I Used
I downloaded the "Trending YouTube Video Statistics" dataset from Kaggle. This dataset contains daily information about trending YouTube videos from different countries. Each country has its own CSV file with video details like views, likes, comments, and a separate JSON file that explains what each category ID means (like "Gaming" or "Music").

Link: https://www.kaggle.com/datasets/datasnaek/youtube-new

# Architecture : 
![Image Alt](https://github.com/AjinkyaDahiwal/YouTube-Data-Engineering-Project-using-AWS/blob/3645ad3fcb0d0e7d8f2341f8b0c76b3f0b87a0f3/Youtube-data-pipeline/architecture/Architecture%20Diagram%20Final.png)


# My Three-Layer Data Storage Strategy
I designed my data lake with three separate S3 buckets, each serving a specific purpose:
Layer 1 - Raw Data Bucket (de-on-youtube-raw-useast1-dev)
This is where I first uploaded all the original files from Kaggle. I kept everything exactly as I downloaded it from my desktop. I wanted to preserve the original data in case I needed to reprocess it differently later. Having this raw layer means I can always go back to the source if something goes wrong in my transformations. I organized the CSV files using region-based folders (like region=ca/, region=us/) to make them easier to work with later.

Layer 2 - Transformed Data Bucket (de-on-youtube-transformed-useast1-dev)
Here's where my smart automation kicks in. I built a Lambda function that automatically watches the raw bucket. Whenever I upload a JSON file (those category mapping files), the Lambda function immediately converts it from JSON to Parquet format. I did this because Parquet files are much smaller and way faster to read than JSON files. The Lambda function also extracts the important "items" data from the nested JSON structure and saves it in a clean, organized way. This happens automatically without me having to manually convert each file.

Layer 3 - Analytics Data Bucket (de-on-youtube-analytics-useast1-dev)
This is my final, business-ready data. Here I used a powerful PySpark job that combines the video statistics with the category information. I also filtered the data to focus only on Canada, Great Britain, and United States since those were the markets my hypothetical client cared about. The job fixes data type mismatches, removes incomplete records, and creates perfectly partitioned tables that analysts can query super fast. It's like having a final, polished dataset ready for any business question.

Technologies I Used
Amazon S3: Cloud storage for all my data files across three buckets

AWS Glue Crawler: Automatically scans my data and builds a searchable catalog

AWS Lambda: Runs my JSON conversion code instantly when files are uploaded

AWS Glue ETL: Heavy-duty data processing using PySpark for complex transformations

Amazon Athena: Lets me and others query the data using regular SQL

AWS CLI: Command-line tools for uploading data and automation

How My Pipeline Works Step by Step
Step 1: Organized Data Upload
I used AWS CLI commands to upload my Kaggle dataset in a smart way. All JSON category files went to a reference data folder, and each country's CSV file went to its own region folder. This organization makes everything downstream work smoothly.

Step 2: Automatic Schema Discovery
AWS Glue Crawler scanned all my uploaded files and automatically figured out what columns and data types I had. This saved me hours of manual work defining database schemas.

Step 3: Smart JSON Processing (Lambda Function)
The moment I upload a JSON file, my Lambda function springs into action. It reads the file, extracts the nested category data, converts everything to efficient Parquet format, and saves it to the transformed bucket. This happens in seconds without any manual intervention.

Step 4: Powerful CSV Processing (PySpark ETL)
My Glue ETL job handles the heavy lifting. It processes all the video statistics CSV files, but only keeps data from the regions I care about (CA, GB, US). It standardizes data types, removes bad records, and creates perfectly partitioned output files optimized for fast queries.

Step 5: Business-Ready Analytics
The final data lands in my analytics bucket, organized by region and ready for any business question. Analysts can now write simple SQL queries in Athena to get insights like "Which video categories trend most in the US?" or "What's the average engagement rate by country?"

# Key Technical Features: 
Event-Driven Architecture: My pipeline processes new data immediately when it arrives, making it feel real-time to users.

Cost Optimization: Using Parquet format and smart partitioning reduces query costs by up to 70% compared to scanning raw CSV files.

Error Handling: Built comprehensive logging and error handling so the pipeline doesn't break when it encounters bad data.

Scalable Design: Can handle growing data volumes without needing infrastructure changes or manual intervention.

Production Ready: Includes proper IAM security, environment variables, and monitoring.

# Real Business Problems This Solves
Campaign Planning: "Which video categories should we target for ads in different countries?"

Trend Analysis: "How do engagement patterns differ between regions?"

Content Strategy: "What type of content gets the most views in our target markets?"

Performance Benchmarking: "How do our video metrics compare to trending content?"


# Since this is a learning project so :
I Stopped all services after project completion to prevent ongoing costs.
Set up Lambda with appropriate memory settings to avoid over-provisioning





# What I Learned Building This
 Technical Skills:

How to design scalable data lake architectures

Event-driven programming with AWS Lambda

Advanced data transformations using PySpark

Optimizing cloud costs while maintaining performance

Working with different file formats and their trade-offs

Business Skills:

Understanding real-world data quality challenges
Designing systems that non-technical users can easily work with
Building pipelines that scale with business growth


# Why This Project Stands Out
This isn't just a simple ETL tutorial - it's a production-grade data pipeline that demonstrates:

Real-world problem solving with messy, multi-format data

Cloud-native architecture using serverless technologies

Cost optimization strategies for business environments

Scalable design patterns that grow with data volume

End-to-end thinking from raw data to business insights

This project shows I can build data infrastructure that actually helps businesses make better decisions. The code is clean, the architecture is sound, and the results speak for themselves. Ready to discuss how I can bring these skills to your data team!
