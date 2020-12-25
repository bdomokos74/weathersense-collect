import logging
import json, os
import azure.functions as func

from . import blob

def main(event: func.EventHubEvent):
    logging.info("called WeatherMeasTrg")
    eventString = event.get_body().decode('utf-8')
    msg = json.loads(eventString)
    # {"messageId":16, "Temperature":24.437500}
    
    logging.info(msg)

    sensoreId = "default"
    sensoreId = event.metadata.get("SystemProperties", {}).get("iothub-connection-device-id", None)
    if sensoreId == None:
        raise Error("Missing device id")

    storageName = os.getenv("STORAGE_ACCOUNT_NAME")
    containerName = os.getenv("BLOB_CONTAINER_NAME")
    blob_name = blob.createBlobName(sensoreId=sensoreId)

    blob.storeMeasurement(storageName, containerName, blobName, msg)
    
    #logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
