import boto3
 
s3 = boto3.client('s3')
 
def lambda_handler(event, context):
    # Extract image key from event
    image_key = event['key']
    try:
        # Delete image from S3 bucket
        s3.delete_object(
            Bucket='bucket name',
            Key=image_key
        )
 
        return {
            'statusCode': 200,
            'body': 'Image deleted successfully'
        }
    except Exception as e:
        # Handle errors
        return {
            'statusCode': 500,
            'body': f'Error deleting image: {str(e)}'
        }