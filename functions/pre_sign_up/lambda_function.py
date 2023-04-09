import json

from core.utils.datetime import get_current_timestamp_string

def lambda_handler(event, context):

    print(event)
    
    timestamp = get_current_timestamp_string()
    print(f"Pre Signup Function is triggered at {timestamp}.")
    
    ## Logic that we want to execute at pre-signup event

    print("Pre Signup Function is executed successfully.")

    payload = dict(statusCode=200, message = "Pre Signup Function is executed successfully.")

    return json.dumps(payload)