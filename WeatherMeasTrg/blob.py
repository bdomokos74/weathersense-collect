from datetime import datetime, timedelta
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.core.exceptions import ResourceNotFoundError
import logging, json
import sys, os

def storeData(sensorId, msg, testDevice):
    data = msg
    containerName = os.getenv("BLOB_CONTAINER_NAME")
    storageName = os.getenv("STORAGE_ACCOUNT_NAME")
    if testDevice:
        storageName = os.getenv("TEST_STORAGE_ACCOUNT_NAME")
        data = msg.strip()+'\n'
    else:
        data = createRecord(msg)

    blobName = createBlobName(sensorId=sensorId)
    client = createClient(storageName, containerName, blobName)
    storeMeasurement(client, blobName, data)

def createBlobName(prefix="meas", sensorId="1", extension=".txt"):
        datePart = datetime.now().strftime("%Y%m%d")
        return "-".join([prefix, sensorId, datePart])+extension

def convert(rows):
    ret = []
    tmp = json.loads(rows[-1])
    #logging.info(tmp)

    timestamp = datetime.now()-timedelta(milliseconds=tmp.get("offset", 0))
    for s in rows:
        msg = json.loads(s)
        offset = msg.get("offset", 0)
        bat = msg.get("bat", "")
        
        if "Temperature" in msg:
            temp = msg.get("Temperature", "")
            pressure = msg.get("Pressure", "")
            humidity = msg.get("Humidity", "")        
            ret.append(f'{(timestamp+timedelta(milliseconds=offset)).isoformat()},{temp:.2f},{pressure:.2f},{humidity:.2f},{bat},{offset}\n')
        else:
            mid = msg.get("Id", "")
            t1 = msg.get("t1", "")
            t2 = msg.get("t2", "")
            pressure = msg.get("p", "")
            humidity = msg.get("h", "")
            temp = (t1+t2)/2.0
            ret.append(f'{(timestamp+timedelta(milliseconds=offset)).isoformat()},{temp:.2f},{pressure:.2f},{humidity:.2f},{bat},{offset},{t1:.2f},{t2:.2f},{mid}\n')
    return ret

def createRecord(eventString):
    msgs = eventString.split("\n")
    #print(msgs)
    result = convert(list(filter(lambda x: x!="", msgs)))
    return "".join(result)


def createClient(storageName, containerName, blobName):
    print(f"storageName={storageName}, containerName={containerName}, blobName={blobName}")
    credential = DefaultAzureCredential()
    oauth_url = "https://{}.blob.core.windows.net".format( storageName )
    blobClient = BlobClient(oauth_url, container_name=containerName, blob_name=blobName, credential=credential)
    return blobClient

def storeMeasurement(blobClient, blobName, record):    
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
