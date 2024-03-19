import json
import boto3

# Initialize the Amazon Cognito client
client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    # Parameters for user authentication
    params = {
        'AuthFlow': 'USER_PASSWORD_AUTH',  # Specify the authentication flow
        'ClientId': 'clientid',  # Replace 'your-app-client-id' with your app client ID
        'AuthParameters': {
            'USERNAME': 'username',  # Replace with the user's username/email
            'PASSWORD': 'password'  # Replace with the user's password
        }
    }

    try:
        # Authenticate the user
        response = client.initiate_auth(**params)
        
        # Access token obtained after successful authentication
        access_token = response['AuthenticationResult']['AccessToken']
        print('Access Token:', access_token)
        
        # You can perform additional actions here, such as returning the access token
        return {
            'statusCode': 200,
            'body': json.dumps({'accessToken': access_token})
        }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error occurred while authenticating user'})
        }
