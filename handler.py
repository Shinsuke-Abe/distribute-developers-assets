import json
import os
import boto3
import urllib.request
s3 = boto3.resource('s3')


def generate_client_api(swagger_url, language):
    api_base = {
        "url": "/".join([os.environ['SWAGGER_API_URL'],
                        os.environ['GENERATE_CLIENT_URL'],
                        language]),
        "method": "POST",
        "headers": {"Content-Type": "application/json"}
    }
    obj = {"swaggerUrl": swagger_url}
    json_data = json.dumps(obj).encode("utf-8")

    return urllib.request.Request(api_base['url'],
                                  data=json_data,
                                  method=api_base['method'],
                                  headers=api_base['headers'])


def download_client_api(code):
    return "/".join([os.environ['SWAGGER_API_URL'],
                     os.environ['DOWNLOAD_CLIENT_URL'],
                     code])


def distribute_client(event, context):
    request = generate_client_api(event['swaggerUrl'], event['language'])

    with urllib.request.urlopen(request) as res:
        code = json.loads(res.read().decode('utf-8'))['code']
        with urllib.request.urlopen(download_client_api(code)) as client_res:
            client_bucket = s3.Bucket(os.environ['CLIENT_SDK_BUCKET'])
            client_file = client_bucket.Object(
                event['serviceName'] +
                '/{0}/{0}-generated-client.zip'.format(event['language']))
            client_file.put(Body=client_res.read())

    response = {
        "statusCode": 200
    }

    return response
