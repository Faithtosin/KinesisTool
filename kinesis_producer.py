
import boto3
import json
from datetime import datetime
import calendar
import random
import time

my_stream_name = 'mykinesis'

kinesis_client = boto3.client('kinesis', region_name='us-west-2')

def put_to_stream(thing_id, property_value, property_timestamp,moxa_index,port_no,kw_reading_value):
    payload = {
                'recordId': str(property_value),
                'timestamp': str(property_timestamp),
                'signal_name': 'AE1 DR Achieved',
                'signal_type': 'dr_achieved',
                'moxa_index': str(moxa_index), 
                'ip_address': '1.1.1.1',
                'port': str(port_no),
                'username': 'username',
                'password': 'moxa123!',
                'kw_reading_value': str(kw_reading_value)
              }

    print(payload)
    print('------------------------------------------------------------------------------------')

    put_response = kinesis_client.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey=thing_id)

while True:
    property_value = random.randint(40, 120)
    moxa_index = random.randint(1, 4)
    port_no = random.randint(300, 955)
    kw_reading_value = random.randint(100, 50000)
    property_timestamp = calendar.timegm(datetime.utcnow().timetuple())
    thing_id = 'aa-bb'
    put_to_stream(thing_id, property_value, property_timestamp,moxa_index,port_no,kw_reading_value)

    #wait for 5 second
    time.sleep(5)
