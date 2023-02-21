import os
import boto3

# Set up the AWS credentials
session = boto3.Session(
    aws_access_key_id='AKIAVD4EYQ336MEOGM4G',
    aws_secret_access_key='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'
)
s3 = session.resource('s3')

# Set up the S3 bucket and directory path
bucket_name = 'my-s3-bucket-malligo2'
directory_path = '/root/slave1work/localfileuploadpath'

# Loop through the files and directories in the directory
for root, dirs, files in os.walk(directory_path):
    for file in files:
        # Construct the full local path of the file
        local_path = os.path.join(root, file)

        # Construct the S3 key (i.e. the remote path of the file)
        # by removing the local directory path from the local path
        s3_key = os.path.relpath(local_path, directory_path)

        # Upload the file to S3
        s3.meta.client.upload_file(local_path, bucket_name, s3_key)

    for dir in dirs:
        # Construct the full local path of the directory
        local_path = os.path.join(root, dir)

        # Construct the S3 key (i.e. the remote path of the directory)
        # by removing the local directory path from the local path and
        # adding a trailing slash
        s3_key = os.path.relpath(local_path, directory_path) + '/'

        # Upload an empty object to represent the directory in S3
        s3.Object(bucket_name, s3_key).put(Body='')

