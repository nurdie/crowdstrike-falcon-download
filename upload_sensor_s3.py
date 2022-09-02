#!/usr/bin/env python3

from secrets import s3aws
bucket, keyid, accesskey = s3aws.get(s3aws)
import boto3
import os, fnmatch

# Globals
# Upload sensors for the following operating systems
OPERATING_SYSTEM_FILTER = [
        "windows",
        "centos",
        "ubuntu",
        "mac"
        ]

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

session = boto3.Session(
    aws_access_key_id=keyid,
    aws_secret_access_key=accesskey,
)
s3 = session.resource('s3')
# Filename - File to upload
# Bucket - Bucket to upload to (the top level directory under AWS S3)
# Key - S3 object name (can contain subdirectories). If not specified then file_name is used
for ostype in OPERATING_SYSTEM_FILTER:
  try:
    sensor = os.path.basename(str(find("crowdstrike-falcon-sensor-{}*".format(ostype), "./")[0]))
  except Exception as msg:
    print("Error retrieving file: ")
    print(msg)
    continue
  print("Found {} - Uploading...".format(sensor))
  try:
    s3.meta.client.upload_file(Filename=sensor, Bucket=bucket, Key=sensor)
    aws_sensor = s3.Bucket(bucket).Object(sensor)
    aws_sensor.Acl().put(ACL='public-read')
  except Exception as msg:
    print("Error uploading file: ")
    print(msg)
    continue
