import asyncio
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import (
    BlobCheckpointStore,
)

# BLOB_STORAGE_CONNECTION_STRING = ""
# BLOB_CONTAINER_NAME = "BLOB_CONTAINER_NAME"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://hrpqqtesteventhubns.servicebus.windows.net/;SharedAccessKeyName=first;SharedAccessKey=EKx/IHO/UFXjc785qV4B2owxJFvOBBXga+AEhGerrIU=;EntityPath=hub1"
EVENT_HUB_NAME = "hub1"

class Consumer:
    def __init__(self) -> None:
        # Create a consumer client for the event hub.
        self.client = EventHubConsumerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR,
            consumer_group="$Default",
            eventhub_name=EVENT_HUB_NAME,
            # checkpoint_store=checkpoint_store,
        )
        self.names = []

    def on_event(self, partition_context, event):
        # Print the event data.
        mess = event.body_as_str(encoding="UTF-8")
        print(
            'Received the event: "{}" from the partition with ID: "{}"'.format(
                mess, partition_context.partition_id
            )
        )
        self.names.append(mess)

        # Update the checkpoint so that the program doesn't read the events
        # that it has already read when you run it next time.
        # await partition_context.update_checkpoint(event)

    def listen(self):
        with self.client:
            self.client.receive(on_event=self.on_event, starting_position="-1")
        # Create an Azure blob checkpoint store to store the checkpoints.
        #checkpoint_store = BlobCheckpointStore.from_connection_string(
        #    BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME
        #)

        # Call the receive method. Read from the beginning of the
        # partition (starting_position: "-1")
        