import boto3
import hmac
import hashlib
import base64

PROFILE_NAME = "<Your AWS profile name>" # arjstack-training
COGNITO_IDP_REGION = "<AWS Region Code>" # ap-south-1

USER_POOL_ID = "<Cognito User Pool ID>"
CLIENT_ID = "<Client ID>"
CLIENT_SECRET = "<Client Secret>"

AUTH_FLOW = "ADMIN_NO_SRP_AUTH"

USER_NAME = "<Your User Name>"
PASSWORD = "<Password>"

ERR_RESPONSE_UNAUTHENTICATED = "Username and/or Password is Incorrect."

def get_cognito_idp_client(region: str):
    """
    Get Cognito IDP Client
    """
    session = boto3.Session(profile_name=PROFILE_NAME)
    cognito_idp_client = session.client("cognito-idp", region_name=region)
    return cognito_idp_client

def get_secret_hash(username):
    msg = username + CLIENT_ID 
    digest = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                    msg = str(msg).encode('utf-8'), 
                    digestmod=hashlib.sha256).digest()
    
    secret_hash = base64.b64encode(digest).decode()
    return secret_hash

def initiate_auth(client, username, password):
    """
    Initiate the Authentication
    """
    try:
        secret_hash = get_secret_hash(username)
        response = client.admin_initiate_auth(UserPoolId=USER_POOL_ID, ClientId=CLIENT_ID,
                                                AuthFlow=AUTH_FLOW,
                                                AuthParameters={
                                                    'USERNAME': username,
                                                    'SECRET_HASH': secret_hash,
                                                    'PASSWORD': password,
                                                },
                                                ClientMetadata={
                                                    'username': username,
                                                    'password': password,
                                                })       
    except client.exceptions.NotAuthorizedException as e:
        raise e
    except client.exceptions.UserNotConfirmedException as e:
        raise e
    except Exception as e:
        raise e
    return response

def main():
    try:
        ## Get Cognito IDP Client
        cognito_idp_client = get_cognito_idp_client(COGNITO_IDP_REGION)

        auth_response = initiate_auth(cognito_idp_client, USER_NAME, PASSWORD)
        if auth_response.get("AuthenticationResult"):
            access_token = auth_response["AuthenticationResult"]["AccessToken"]
            if access_token:
                result = dict(authenticated=False, message="success",
                               token={
                                    "id_token": auth_response["AuthenticationResult"]["IdToken"],
                                    "refresh_token": auth_response["AuthenticationResult"]["RefreshToken"],
                                    "access_token": auth_response["AuthenticationResult"]["AccessToken"],
                                    "expires_in": auth_response["AuthenticationResult"]["ExpiresIn"],
                                    "token_type": auth_response["AuthenticationResult"]["TokenType"]
                                })
            else:
                result = dict(authenticated=False, message = ERR_RESPONSE_UNAUTHENTICATED)
        else:
            result = dict(authenticated=False, message = ERR_RESPONSE_UNAUTHENTICATED)
    except Exception as e:
        print(e.__str__())
        result = dict(authenticated=False, message = ERR_RESPONSE_UNAUTHENTICATED)

    print(result)    

if __name__ == "__main__":
    main()