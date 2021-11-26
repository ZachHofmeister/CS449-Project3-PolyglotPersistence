import boto3

def regenPollsTable(dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

	table = None
	try:
		dynamodb.Table('Polls').delete()
		table = dynamodb.create_table(
			TableName='Polls',
			KeySchema=[
				{
					'AttributeName': 'username',
					'KeyType': 'HASH' #partition key
				},
				{
					'AttributeName': 'question',
                	'KeyType': 'RANGE'  #sort key
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'username',
					'AttributeType': 'S' #number
				},
				{
					'AttributeName': 'question',
					'AttributeType': 'S' #string
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 10,
				'WriteCapacityUnits': 10
			}
		)
	except Exception as e:
		print(f'exception in createPollsTable: {str(e)}')
		# table = dynamodb.Table('Polls')
	
	return table

if __name__ == '__main__':
	table = regenPollsTable()
	if table:
		print(f'Table status: {table.table_status}')