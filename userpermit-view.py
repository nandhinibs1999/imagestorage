import json
import boto3

def lambda_handler(event, context):
    # Extract user identity from the incoming request
    user_id = event['requestContext']['authorizer']['claims']['sub']  # Assuming Cognito user ID is stored in 'sub'

    if event['httpMethod'] == 'GET':  # For image retrieval
        image_owner_id = event['pathParameters']['image_owner_id']  # Assuming owner ID is passed as a path parameter
        if user_id == image_owner_id:
            # Generate a pre-signed URL for the image
            s3 = boto3.client('s3')
            bucket_name = 'bucketname'
            image_key = 'images/foldername/imagename.png'  # You need to provide the key of the image to be retrieved
            image_name = image_key.split('/')[-1]  # Extracting the image name from the image_key
            try:
                return {
                    'statusCode': 200,
                    'body': json.dumps({"image_name": image_name})
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({"error": str(e)})
                }
        else:
            # User is not authorized to view the image
            return {
                'statusCode': 403,
                'body': json.dumps({"error": "Unauthorized access"})
            }
