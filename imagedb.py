import boto3
import uuid  # For generating unique image IDs
from datetime import datetime, timedelta

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Name of your DynamoDB table
table_name = 'Dyname Table name'

# Get reference to the DynamoDB table
table = dynamodb.Table(table_name)

def get_current_ist_time():
    # Get current UTC time
    utc_now = datetime.utcnow()

    # Calculate the time difference for IST (+5:30 hours)
    ist_offset = timedelta(hours=5, minutes=30)

    # Convert UTC time to IST
    ist_now = utc_now + ist_offset

    return ist_now.strftime('%Y-%m-%d %H:%M:%S IST')

def insert_image_metadata(owner_id, image_url):
    try:
        # Generate a unique image ID
        image_id = str(uuid.uuid4())
        
        # Get current IST timestamp
        timestamp = get_current_ist_time()

        # Construct the item to be inserted into DynamoDB
        item = {
            'ImageID': image_id,
            'OwnerID': owner_id,
            'ImageURL': image_url,
            'Timestamp': timestamp,
            # Add other attributes as needed
        }

        # Insert the item into the DynamoDB table
        response = table.put_item(Item=item)

        # Check if the item was successfully inserted
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'Metadata for the image has been successfully inserted into DynamoDB.'
        else:
            return 'Failed to insert metadata into DynamoDB.'
    except Exception as e:
        return f'Error: {str(e)}'

def lambda_handler(event, context):
    if 'owner_id' in event and 'image_url' in event:
        # Call function to insert image metadata
        insert_result = insert_image_metadata(event['owner_id'], event['image_url'])

        return {
            'statusCode': 200 if insert_result.startswith('Metadata') else 500,
            'body': insert_result
        }
    elif 'image_id' in event:
        try:
            # Retrieve image data based on ImageID
            image_id = event['image_id']

            # Query DynamoDB to retrieve image data
            response = table.get_item(
                Key={'ImageID': image_id}
            )

            # Check if the item was found
            if 'Item' in response:
                image_data = response['Item']
                return {
                    'statusCode': 200,
                    'body': image_data
                }
            else:
                return {
                    'statusCode': 404,
                    'body': 'Image not found in DynamoDB.'
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Error: {str(e)}'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid request. Please provide owner_id and image_url or image_id.'
        }
