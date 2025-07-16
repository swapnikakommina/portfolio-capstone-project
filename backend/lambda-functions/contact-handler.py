import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ContactMessages')

def lambda_handler(event, context):
    """
    AWS Lambda function to handle contact form submissions
    Stores data in DynamoDB and returns response
    """
    
    # CORS headers for browser requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Accept',
        'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
        'Content-Type': 'application/json'
    }
    
    print(f"Received event: {json.dumps(event)}")
    
    # Handle preflight CORS request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight successful'})
        }
    
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        print(f"Parsed body: {json.dumps(body)}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not body.get(field):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': f'Missing required field: {field}',
                        'success': False
                    })
                }
        
        # Create unique ID for this submission
        submission_id = str(uuid.uuid4())
        
        # Prepare item for DynamoDB
        item = {
            'id': submission_id,
            'name': body['name'][:100],  # Limit length
            'email': body['email'][:100],
            'subject': body['subject'][:200],
            'message': body['message'][:1000],
            'timestamp': body.get('timestamp', datetime.now().isoformat()),
            'created_at': datetime.now().isoformat(),
            'source': body.get('source', 'contact-form'),
            'user_agent': body.get('userAgent', 'Unknown')[:500],
            'status': 'new'
        }
        
        print(f"Saving to DynamoDB: {json.dumps(item, default=str)}")
        
        # Save to DynamoDB
        response = table.put_item(Item=item)
        print(f"DynamoDB response: {json.dumps(response, default=str)}")
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Contact form submitted successfully',
                'id': submission_id,
                'success': True,
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'error': 'Invalid JSON in request body',
                'details': str(e),
                'success': False
            })
        }
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e),
                'success': False
            })
        }