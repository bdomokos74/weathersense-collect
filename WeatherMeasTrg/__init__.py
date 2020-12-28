import logging, os
import azure.functions as func

from . import blob

def main(event: func.EventHubEvent):
    logging.info("called WeatherMeasTrg")
    eventString = event.get_body().decode('utf-8')
    # {"messageId":16, "Temperature":24.437500}
    #logging.info(eventString)

    sensorId = event.metadata.get("SystemProperties", {}).get("iothub-connection-device-id", None)
    if sensorId == None:
        raise Error("Missing device id")

    storageName = os.getenv("STORAGE_ACCOUNT_NAME")
    containerName = os.getenv("BLOB_CONTAINER_NAME")
    blobName = blob.createBlobName(sensorId=sensorId)

    blob.storeMeasurement(storageName, containerName, blobName, eventString)
    
    #logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
