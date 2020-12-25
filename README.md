## Azure Function App to handle sensor data 

Process telemetry from Azure IoT HUB, write to Azure Blob, send notifications, do data aggregation

### Other components

https://github.com/bdomokos74/weathersense-device - send sensor data from Arduino, RasPi  to Azure IoT HUB

https://github.com/bdomokos74/weathersense-spa - Single Page Application to display measurements from Azure Blob

### Get started
```bash
python -m venv .venv
. ./bin/activate
pip install -r requirements.txt
```

Note: python3 is needed

### Run tests
```bash
python test/storage_test.py
```

### TODO

* add count for failed connection attemps
* measure the battery voltage, add to telemetry data
* send alert if battery needs charge (this goes to the weathersense-collect)
* alert if no measurement from a sensor in 30 min
* implement loading the arduino prog OTA, triggerd centrally
* change blob format from csv lines to json lines