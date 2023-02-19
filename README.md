# AWS Data Exchange to S3 Data Lake Serverless Ingestion Solution

This is a trivial example of how to automate ingestion from AWS Data Exchange into
an S3 data lake, along with a Glue Job and Step Function trigger to perform basic data
transformation.

## How it works

- CloudFormation template creates some S3 buckets, use Lake Formation to setup governance on
the buckets and manage permissions to the data stored in them
- AWS Data Exchange ingestion lambda function is written in Python using Boto3
- CloudWatch event rule triggers the ingestion based on dataset updates to AWS Data Exchange 
- Step Function will trigger Glue to perform some basic data transformation, and the a Glue crawler
to crawl the data and update any schema definition or tables
