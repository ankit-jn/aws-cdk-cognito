import json

from core.utils.datetime import get_current_timestamp_string

def lambda_handler(event, context):

    print(event)
    
    timestamp = get_current_timestamp_string()
    print(f"Post Confirmation Function is triggered at {timestamp}.")
    
    ## Logic that we want to execute at post-confirmation event

    print("Post Confirmation Function is executed successfully.")

    payload = dict(statusCode=200, message = "Post Confirmation Function is executed successfully.")

    return json.dumps(payload)