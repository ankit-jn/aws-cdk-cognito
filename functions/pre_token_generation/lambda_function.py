import json

from core.utils.datetime import get_current_timestamp_string

def lambda_handler(event, context):

    print(event)
    
    timestamp = get_current_timestamp_string()
    print(f"Pre Token Generattion Function is triggered at {timestamp}.")
    
    ## Logic that we want to execute at pre-token-generation event

    print("Pre Token Generattion Function is executed successfully.")

    payload = dict(statusCode=200, message = "Pre Token Generattion Function is executed successfully.")

    return json.dumps(payload)