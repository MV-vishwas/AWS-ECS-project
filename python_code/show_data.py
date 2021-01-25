import boto3
from boto3.dynamodb.conditions import Key,Attr
# from boto.dynamodb2.table import Table

table_name='users'
ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table(table_name)

# response = ddb.query(KeyConditionExpression=Key('bookID').eq('1'))

# c=0
# for item in response['Items']:
#     c+=1
#     print(item['bookID'],item['price'])
# print('count',c)
# items = response['Items']
# print(items)

# response= ddb.scan(FilterExpression=Key('users'))

# response= ddb.scan(FilterExpression=Attr('price').between('2000','2001') | Attr('title').begins_with("S") | )

# response= ddb.scan(FilterExpression=Attr('title').begins_with("A") | Attr('title').begins_with("a"))

# response= ddb.scan(FilterExpression=Attr('title').begins_with("B") | Attr('title').begins_with("b"))


# print(type(response['Items']))
# c=0
# for item in response['Items']:
#     c+=1
#     # print(item['bookID'],item['price'])
#     print(item['title'])
# print('count',c)

response = ddb.scan()
print(response['Items'])
# items = response['Items']
# while 'LastEvaluatedKey' in response:
#     print(response['LastEvaluatedKey'])
#     response = ddb.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
#     items.extend(response['Items'])