import json
import os
import boto3
import urllib.request


def distribute_client(event, context):
    generate_client_url = "/".join([os.environ['SWAGGER_API_URL'],
                                    os.environ['GENERATE_CLIENT_URL'],
                                    'java'])
    method = "POST"
    headers = {"Content-Type": "application/json"}

    obj = {"swaggerUrl": event['swaggerUrl']}
    json_data = json.dumps(obj).encode("utf-8")

    request = urllib.request.Request(generate_client_url,
                                     data=json_data,
                                     method=method,
                                     headers=headers)

    with urllib.request.urlopen(request) as res:
        code = json.loads(res.read().decode('utf-8'))['code']
        download_client_url = "/".join([os.environ['SWAGGER_API_URL'],
                                        os.environ['DOWNLOAD_CLIENT_URL'],
                                        code])
        print(download_client_url)
        with urllib.request.urlopen(download_client_url) as client_res:
            s3 = boto3.resource('s3')
            client_bucket = s3.Bucket(os.environ['CLIENT_SDK_BUCKET'])
            client_file = client_bucket.Object(
                event['serviceName'] + '/java/java-generated-client.zip')
            client_file.put(Body=client_res.read())

    response = {
        "statusCode": 200
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
