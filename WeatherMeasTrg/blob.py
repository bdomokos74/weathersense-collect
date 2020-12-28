from datetime import datetime, timedelta
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.core.exceptions import ResourceNotFoundError
import logging, json

def createBlobName(prefix="meas", sensorId="1", extension=".txt"):
        datePart = datetime.now().strftime("%Y%m%d")
        return "-".join([prefix, sensorId, datePart])+extension

def convert(s):
    msg = json.loads(s)
    temp = msg.get("Temperature", "")
    pressure = msg.get("Pressure", "")
    humidity = msg.get("Humidity", "")
    bat = msg.get("bat", "")
    offset = msg.get("offset", 0)
    ret =  [temp, pressure, humidity, bat, offset]
    return ret

def createRecord(eventString):
    msgs = eventString.split("\n")
    print(msgs)
    parsed = list(map(convert, filter( lambda x: x!="", msgs)))
    result = []
    timestamp = datetime.now()-timedelta(milliseconds=parsed[-1][4])
    for p in parsed:
        result.append(f"{(timestamp+timedelta(milliseconds=p[4])).isoformat()},{p[0]},{p[1]},{p[2]},{p[3]}\n")
    return "".join(result)

def storeMeasurement(storageName, containerName, blobName, eventString):

    credential = DefaultAzureCredential()
    oauth_url = "https://{}.blob.core.windows.net".format( storageName )
    blobClient = BlobClient(oauth_url, container_name=containerName, blob_name=blobName, credential=credential)
    
    
    record = createRecord(eventString)

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