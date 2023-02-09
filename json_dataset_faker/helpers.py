from mypy_boto3_s3.client import S3Client
from typedefs import JsonList, String, StrList
import boto3
import json


def upload_file(bucket: String, filename: String, label: String):
    client: S3Client = boto3.client('s3')  # type: ignore
    key: String = f'{label}/{filename}'
    client.upload_file(Bucket=bucket, Key=key, Filename=f'/tmp/{filename}')
    return


def write_file(filename: String, synth_data: JsonList) -> None:
    with open(f'/tmp/{filename}', 'w') as f:
        for element in synth_data:
            f.write(f'{json.dumps(element)}\n')
    return


def read_file(bucket: String, key: String) -> StrList:
    client: S3Client = boto3.client('s3')  # type: ignore
    client.download_file(Bucket=bucket, Key=key, Filename='/tmp/src.json')
    with open('/tmp/src.json', 'r') as f:
        file: StrList = f.readlines()
    return file
