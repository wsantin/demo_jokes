import random
import hmac
import hashlib
from base64 import b64encode
import boto3

class CognitoService():
  AWS_ACCESS_KEY_ID = None
  AWS_SECRET_ACCESS_KEY = None
  AWS_COGNITO_REGION = None
  AWS_COGNITO_USER_POOL_ID = None
  AWS_COGNITO_APP_CLIENT_ID = None
  AWS_COGNITO_APP_CLIENT_SECRET = None

  def __init__(self, servicesEnv):
    self.AWS_ACCESS_KEY_ID = servicesEnv.AWS_ACCESS_KEY_ID
    self.AWS_SECRET_ACCESS_KEY = servicesEnv.AWS_SECRET_ACCESS_KEY
    self.AWS_COGNITO_REGION = servicesEnv.AWS_COGNITO_REGION
    self.AWS_COGNITO_USER_POOL_ID = servicesEnv.AWS_COGNITO_USER_POOL_ID
    self.AWS_COGNITO_APP_CLIENT_ID = servicesEnv.AWS_COGNITO_APP_CLIENT_ID
    self.AWS_COGNITO_APP_CLIENT_SECRET = servicesEnv.AWS_COGNITO_APP_CLIENT_SECRET

  def create_hash_identified(self, username):
    msg = username + self.AWS_COGNITO_APP_CLIENT_ID
    dig = hmac.new(str(self.AWS_COGNITO_APP_CLIENT_SECRET).encode('utf-8'),
        msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = b64encode(dig).decode()
    return d2

  def pagination_cognito(self, method_to_paginate, **params_to_pass):
    response = method_to_paginate(**params_to_pass)
    yield response
    while response.get('PaginationToken', None):
        response = method_to_paginate(PaginationToken=response['PaginationToken'], **params_to_pass)
        yield response

  def cognito_resource(self):
        return boto3.resource('cognito-idp',
          region_name=self.AWS_COGNITO_REGION,
          aws_access_key_id=self.AWS_ACCESS_KEY_ID,
          aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
          # config = config
      )
          
  def cognito_client(self):
    return boto3.client('cognito-idp',
        region_name=self.AWS_COGNITO_REGION,
        aws_access_key_id=self.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        # config = config
    )

  def signIn_cognito(self, username, password):
    return self.cognito_client().initiate_auth(
            ClientId=self.AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': self.create_hash_identified(username)
            },
            ClientMetadata={
                'UserPoolId': self.AWS_COGNITO_USER_POOL_ID
            }
        )

  def signup_cognito(self, username):
    return self.cognito_client().admin_user_global_sign_out(
        UserPoolId=self.AWS_COGNITO_USER_POOL_ID,
        Username=str(username),
    )

  def users_cognito(self, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID    
      
    users = []
    for page in self.pagination_cognito(self.cognito_client().list_users, UserPoolId=UserPoolId):
        users += page['Users']
    return users

  def user_cognito(self, username, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
            
    return self.cognito_client().admin_get_user(
        Username=username,
        UserPoolId=str(UserPoolId)
    )

  def update_user_cognito(self, username, attributes, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID

    ##Status: '1' or '0'
    return self.cognito_client().admin_update_user_attributes(
        UserPoolId= str(UserPoolId),
        Username= str(username).replace(' ',''),
        UserAttributes= attributes
    )
  

  def create_user_cognito_admin(self, data, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
    
    if not data['email']:
        data['email'] = ''
    
    if not data['custom:bunisse_id']: 
        data['custom:bunisse_id'] = ''

    if not data['custom:document']:
        data['custom:document'] = ''
        
    return self.cognito_client().admin_create_user(
        UserPoolId=str(UserPoolId),
        Username= data['username'],
        TemporaryPassword= data['password'],
        UserAttributes=[
            {
                'Name': 'name',
                'Value': data['name']
            },
            {
                'Name': 'phone_number',
                'Value': data['username']
            },
            {
                'Name': 'email',
                'Value': data['email']
            },
            {
                'Name': 'custom:document',
                'Value': data['custom:document']
            },
            {
                'Name': 'custom:bunisse_id',
                'Value': data['custom:bunisse_id']
            },
        ],
        
        # ForceAliasCreation=True|False,
        # MessageAction='RESEND'|'SUPPRESS',
        DesiredDeliveryMediums=['SMS'],   #'EMAIL'
    )
    
  def list_users_in_group(self, group, limit=None, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID

    if not group:
        return False
    
    if limit:
        return self.cognito_client().list_users_in_group( 
            UserPoolId=UserPoolId, 
            GroupName=group,
            Limit=limit,
        )
    else:
        return self.cognito_client().list_users_in_group( 
            UserPoolId=UserPoolId, 
            GroupName=group
        )

  def add_user_to_group(self, username, group, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
    
    if not username:
        return False
    
    if not group:
        return False
    
    return self.cognito_client().admin_add_user_to_group( 
        UserPoolId=UserPoolId, 
        Username=username, 
        GroupName=group 
    )
    
  def delete_user_cognito_admin(self, username, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
    
    if not username:
        return False
    
    return self.cognito_client().admin_delete_user( 
        UserPoolId=UserPoolId, 
        Username=username
    )
    
  def disabled_user_cognito_admin(self, username, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
    
    if not username:
        return False
    
    return self.cognito_client().admin_disable_user( 
        UserPoolId=UserPoolId, 
        Username=username
    )
    
  def enable_user_cognito_admin(self, username, UserPoolId=None):
    if not UserPoolId:
        UserPoolId = self.AWS_COGNITO_USER_POOL_ID
    
    if not username:
        return False
    
    return self.cognito_client().admin_enable_user( 
        UserPoolId=UserPoolId, 
        Username=username
    )