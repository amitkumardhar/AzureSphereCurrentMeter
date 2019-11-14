#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub partition.
"""
import os
from azure.eventhub import EventPosition,EventHubConsumerClient
import pymongo

CONNECTION_STR = "Endpoint=eventhub-compatible_endpoint_from_azure_iothub"
EVENT_HUB = "eventhub_compatible_name_from_azure_iothub"

EVENT_POSITION = EventPosition("-1")
PARTITION = "0"

total = 0
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["currentMeter"]
mycol = mydb["readings"]


def do_operation(event):
    # do some operations on the event, avoid time-consuming ops
    mydict = json.loads(event['body'])
    mydict['timestamp']=event['enqueued_time']
    x = mycol.insert_one(mydict)
    print(event)


def on_partition_initialize(partition_context):
    # put your code here
    print("Partition: {} has been intialized".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # put your code here
    print("Partition: {} has been closed, reason for closing: {}".format(partition_context.partition_id,
                                                                         reason))


def on_error(partition_context, error):
    # put your code here
    print("Partition: {} met an exception during receiving: {}".format(partition_context.partition_id,
                                                                       error))


def on_events(partition_context, events):
    # put your code here
    global total

    print("received events: {} from partition: {}".format(len(events), partition_context.partition_id))
    total += len(events)
    for event in events:
        do_operation(event)


if __name__ == '__main__':
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        event_hub_path=EVENT_HUB
    )
    
    try:
        with consumer_client:
            consumer_client.receive(on_events=on_events, consumer_group='$Default',
                                    on_partition_initialize=on_partition_initialize,
                                    on_partition_close=on_partition_close,
                                    on_error=on_error,track_last_enqueued_event_properties=True)
    except KeyboardInterrupt:
        print('Stop receiving.')
