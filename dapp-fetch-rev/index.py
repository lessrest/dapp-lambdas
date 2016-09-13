import boto3
import json
import subprocess
import os
import tempfile

def main(event, context):
    msg = json.loads(event["Records"][0]["Sns"]["Message"])
    origin = msg["origin"]
    rev = msg["rev"]

    cwd = "/var/task"
    os.chdir(cwd)

    os.environ["GIT_EXEC_PATH"] = "{}/git/libexec/git-core".format(cwd)
    os.environ["PATH"] = "{}:{}".format(cwd, os.environ["PATH"])
    os.environ["PATH"] = "{}/git/bin:{}".format(cwd, os.environ["PATH"])

    tmp = tempfile.mkdtemp()
    os.chdir(tmp)

    subprocess.check_call(["fetch-rev", origin, rev])

    boto3.client("s3").upload_file(
        "rev.tgz", "dapp-rev-archives", "{}.tgz".format(rev)
    )

    print "Uploaded dapp-rev-archives/{}.tgz".format(rev)
