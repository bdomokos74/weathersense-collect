## Azure Function App to handle sensor data 

Process telemetry from Azure IoT HUB, write to Azure Blob, send notifications, do data aggregation

### Other components

https://github.com/bdomokos74/weathersense-device - send sensor data from Arduino, RasPi  to Azure IoT HUB

https://github.com/bdomokos74/weathersense-spa - Single Page Application to display measurements from Azure Blob

### Get started
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Note: python3 is needed

### Run tests
```bash
. dev.env
python test/blob_test.py
python test/storage_test.py
```
