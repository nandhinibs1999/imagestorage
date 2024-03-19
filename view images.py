import json
import boto3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # List objects in S3 bucket
        response = s3.list_objects_v2(
            Bucket='bucketname'
        )

        # Extract image URLs
        image_urls = [f"https://imagestorage.s3.amazonaws.com/{obj['Key']}" for obj in response.get('Contents', [])]

        # Return image URLs
        return {
            'statusCode': 200,
            'body': json.dumps(image_urls)
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
