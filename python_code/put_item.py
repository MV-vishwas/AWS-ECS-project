import boto3
from boto3.dynamodb.conditions import Key,Attr

print('Enter email ID(this will be your userID)')
userID=input()
full_name=input('Enter your full name\n')
password=input('Enter your password\n')
re_password=input('Re-Enter your password\n')
if password!= re_password:
    print('Password in not matched.')
else:
    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table('users')
    response = ddb.query(KeyConditionExpression=Key('userID').eq(userID))
    # print(len(response[Items]))
    if len(response['Items'])==0:
        ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table('users')
        input={'userID':userID,
                'full_name':full_name,
                'password':password,
                'favourites':[],
        }
        ddb.put_item(Item=input)
    else:
        print('The email ID is already taken.')
