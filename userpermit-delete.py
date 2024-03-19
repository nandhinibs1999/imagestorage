import json
import boto3

def lambda_handler(event, context):
    # Extract user identity from the incoming request
    user_id = event['requestContext']['authorizer']['claims']['sub']  # Assuming Cognito user ID is stored in 'sub'

    if event['httpMethod'] == 'DELETE':  # For image deletion
        image_owner_id = event['pathParameters']['image_owner_id']  # Assuming owner ID is passed as a path parameter
        if user_id == image_owner_id:
            # Delete the image from storage
            s3 = boto3.client('s3')
            bucket_name = 'bucketname'
            image_key = 'images/foldername/imagename.png'  # You need to provide the key of the image to be deleted
            try:
                s3.delete_object(Bucket=bucket_name, Key=image_key)
                return {
                    'statusCode': 200,
                    'body': json.dumps({"message": "Image deleted successfully"})
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({"error": str(e)})
                }
        else:
            # User is not authorized to delete the image
            return {
                'statusCode': 403,
                'body': json.dumps({"error": "Unauthorized access"})
            }
