import logging, os
import azure.functions as func

from . import blob

def main(event: func.EventHubEvent):
    eventString = event.get_body().decode('utf-8')

    sensorId = event.metadata.get("SystemProperties", {}).get("iothub-connection-device-id", None)
    props = event.metadata.get("Properties", {})
    testDevice = (props.get("testDevice", "false")=="true");
    logging.info(f"Event properties: {props}, testDevice={testDevice}")
    if sensorId == None:
        raise Error("Missing device id")

    blob.storeData(sensorId, eventString, testDevice)

    #logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
