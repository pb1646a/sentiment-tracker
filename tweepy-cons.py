from __future__import print_function
import base64
import json

def lambda_handler(event,context):
    for record in event['Records']:
        payload=base64.b64decode(record["kinesis"]["data"])
        print("decoded payload: "+str(payload))