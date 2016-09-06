import boto3
import os
import subprocess
import tempfile

def main(event, context):
  record = event["Records"][0]
  assert record["eventName"] == "ObjectCreated:Put"

  src_json_key = record["s3"]["object"]["key"]
  src_json_bucket = record["s3"]["bucket"]["name"]

  rev = os.path.splitext(src_json_key)[0]

  os.chdir(tempfile.mkdtemp())

  boto3.client("s3").download_file(
    src_json_bucket, src_json_key, "src.json"
  )

  os.environ["PATH"] = "/var/task:{}".format(os.environ["PATH"])
  subprocess.check_call(["dapple-test"])
  
  boto3.client("s3").upload_file(
      "result.json", "dapp-rev-results", "{}.json".format(rev)
  )

  print "Uploaded {}.json".format(rev)
