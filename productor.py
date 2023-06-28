import asyncio

from azure.eventhub import EventData
from azure.eventhub import EventHubProducerClient
from azure.identity import DefaultAzureCredential
from azure.eventhub.exceptions import EventHubError

EVENT_HUB_CONNECTION_STR  = "Endpoint=sb://hrpqqtesteventhubns.servicebus.windows.net/;SharedAccessKeyName=first;SharedAccessKey=EKx/IHO/UFXjc785qV4B2owxJFvOBBXga+AEhGerrIU=;EntityPath=hub1"
EVENT_HUB_NAME = "hub1"

class Productor:
    def __init__(self) -> None:
        # self.credential = DefaultAzureCredential()
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, 
            eventhub_name=EVENT_HUB_NAME
        )

    def send(self, message: str):
        # Create a producer client to send messages to the event hub.
        # Specify a connection string to your event hubs namespace and
        # the event hub name.
        
        # Create a batch.
        event_data_batch = self.producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(message))
        # event_data_batch.add(EventData("Second event"))
        # event_data_batch.add(EventData("Third event"))

        # Send the batch of events to the event hub.
        self.producer.send_batch(event_data_batch)

# asyncio.run(run())    