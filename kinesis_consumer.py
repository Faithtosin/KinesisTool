import boto3
import base64
import time
import json
import pprint

my_stream_name = 'eirgrid-stream-develop'

kinesis_client = boto3.client('kinesis', region_name='us-west-2')

response = kinesis_client.describe_stream(StreamName=my_stream_name)

my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=2)

while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=2)

    pprint.pprint(record_response)
    print('----------------------')
    decoded_record_data = [base64.b64decode(record['Data']) for record in record_response['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
    pprint.pprint(deserialized_data)
    print('-------------------------------------------------------------------------------------------')

    # wait for 5 seconds
    time.sleep(5)
