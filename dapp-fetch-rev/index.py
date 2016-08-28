import boto3
import json
import subprocess
import os
import tempfile

def main(event, context):
    msg = json.loads(event["Records"][0]["Sns"]["Message"])
    origin = msg["origin"]
    rev = msg["rev"]

    os.chdir("/var/task")
    os.environ["GIT_EXEC_PATH"] = "{}/git/libexec/git-core".format(os.getcwd())
    os.environ["PATH"] = "{}:{}".format(os.getcwd(), os.environ["PATH"])
    os.environ["PATH"] = "{}/git/bin:{}".format(os.getcwd(), os.environ["PATH"])
    os.chdir(tempfile.mkdtemp())

    subprocess.check_call(["fetch-rev", origin, rev])

    boto3.client("s3").upload_file(
        "rev.tgz", "dapp-rev-archives", "{}.tgz".format(rev)
    )

    print "Uploaded dapp-rev-archives/{}.tgz".format(rev)
