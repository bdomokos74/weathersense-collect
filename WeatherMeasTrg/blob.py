from datetime import datetime
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.core.exceptions import ResourceNotFoundError
import logging

def createBlobName(prefix="meas", sensorId="1", extension=".txt"):
        datePart = datetime.now().strftime("%Y%m%d")
        return "-".join([prefix, sensorId, datePart])+extension

def createRecord(msg):
    timestamp = datetime.now().isoformat()
    temp = msg.get("Temperature", "")
    pressure = msg.get("Pressure", "")
    humidity = msg.get("Humidity", "")
    return f"{timestamp},{temp},{pressure},{humidity}\n"

def storeMeasurement(storageName, containerName, blobName, msg):
    credential = DefaultAzureCredential()
    oauth_url = "https://{}.blob.core.windows.net".format( storageName )
    blobClient = BlobClient(oauth_url, container_name=containerName, blob_name=blobName, credential=credential)
    record = createRecord(msg)

    logging.info(f"appending to {blobName}: {record}")
    retryCnt = 0
    succ = False
    while not succ and retryCnt<2:
        try:
            ret = blobClient.append_block(record)
            succ = True
        except ResourceNotFoundError:
            retryCnt += 1
            blobClient.create_append_blob()
            logging.info(f"created {blobName}")