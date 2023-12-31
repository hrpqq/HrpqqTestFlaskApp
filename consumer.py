from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore
from azure.identity import DefaultAzureCredential

BLOB_STORAGE_ACCOUNT_URL = "https://hrpqqtestsa.blob.core.windows.net"
BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=hrpqqtestsa;AccountKey=ELTWw06ZfvPu9OYaDnXfe3mW6Drf+l0SvE5V8JLoO51sM4zDfgQSqozxGlhIiHzvXmFfHfxCbRHG+AStPHcFAQ==;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "checkpoints"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://hrpqqtesteventhubns.servicebus.windows.net/;SharedAccessKeyName=first;SharedAccessKey=EKx/IHO/UFXjc785qV4B2owxJFvOBBXga+AEhGerrIU=;EntityPath=hub1"
EVENT_HUB_NAME = "hub1"

class Consumer:
    def __init__(self) -> None:
        self.credential = DefaultAzureCredential()
        # Create an Azure blob checkpoint store to store the checkpoints.
        checkpoint_store = BlobCheckpointStore(
            # conn_str=BLOB_STORAGE_CONNECTION_STRING, 
            blob_account_url=BLOB_STORAGE_ACCOUNT_URL,
            container_name=BLOB_CONTAINER_NAME,
            credential=self.credential,
        )
        # Create a consumer client for the event hub.
        self.client = EventHubConsumerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR,
            consumer_group="$Default",
            eventhub_name=EVENT_HUB_NAME,
            checkpoint_store=checkpoint_store,
        )
        self.names = []
        self.errors = []
        self.partition = {}
        self.event = {}

    def on_event(self, partition_context, event):
        # Print the event data.
        mess = event.body_as_str(encoding="UTF-8")
        print('Received the event: "{}" from the partition with ID: "{}"'.format(
                mess, 
                partition_context.partition_id
            )
        )
        self.names.append(mess)
        self.partition=partition_context
        self.event=event

        # Update the checkpoint so that the program doesn't read the events
        # that it has already read when you run it next time.
        partition_context.update_checkpoint(event)

    def on_error(self, partition_context, error):
        # Put your code here. partition_context can be None in the on_error callback.
        self.errors.append(error)
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

    def listen(self):
        with self.client:
            self.client.receive(
                on_event=self.on_event, 
                on_error=self.on_error,
                starting_position="-1")
        self.credential.close()

        