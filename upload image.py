import boto3
import urllib.request
import urllib.error
import os

s3 = boto3.client('s3')
def lambda_handler(event, context):
    try:
        # Extract the URL of the image from the event
        image_url = event['imageUrl']
        # Create a User-Agent header to mimic a web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        # Download the image from the URL
        request = urllib.request.Request(image_url, headers=headers)
        with urllib.request.urlopen(request) as response:
            image_data = response.read()
        # Extract the file name from the URL and create a new file name
        file_name = image_url.split('/')[-1]
        new_file_name = 'imagename.jpg'  # Change this to the desired new file name
        # Upload the image data to S3 with the new file name
        s3.put_object(
            Bucket='bucketname',
            Key=new_file_name,
            Body=image_data
        )
        # Return success response
        return {
            'statusCode': 200,
            'body': 'Image uploaded successfully with new file name: {}'.format(new_file_name)
        }
    except urllib.error.HTTPError as e:
        # Return error response for HTTP errors
        return {
            'statusCode': e.code,
            'body': 'HTTP Error: {}'.format(e.reason)
        }
    except Exception as e:
        # Return error response for other exceptions
        return {
            'statusCode': 500,
            'body': 'Error: {}'.format(str(e))
        }
 
 