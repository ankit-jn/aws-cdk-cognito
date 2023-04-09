import json

from core.utils.datetime import get_current_timestamp_string

def lambda_handler(event, context) -> None:

    print(event)
    
    timestamp = get_current_timestamp_string()
    print(f"Post Authentication Function is triggered at {timestamp}")
    
    ## Logic that we want to execute at post-authentication event

    print("Post Authentication Function is executed successfully.")

    payload = dict(statusCode=200, message = "Post Authentication Function is executed successfully.")

    return json.dumps(payload)