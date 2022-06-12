# invoke a crawler on object creation
import boto3

glue = boto3.client(service_name='glue', region_name='us-east-1',
              endpoint_url='https://glue.us-east-1.amazonaws.com')

def lambda_handler(event, context):
    try:
       glue.start_crawler(Name='revision')
    except Exception as e:
        print(e)
        print('Error starting crawler')
        raise e