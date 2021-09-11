

import sys
sys.path.append('WeatherMeasTrg')

import unittest
import azure.functions as func

from blob import storeMeasurement, createBlobName, storeData
import logging

# Run this way:
# . .local/devenv.sh
# python test/storage_test.py

# Uncomment for debugging
#logging.basicConfig(level=logging.DEBUG)

class TestStorage(unittest.TestCase):

    def testStoreData1(self):
        msg = "{\"messageId\":16, \"Temperature\":24.437500,\"Pressure\":1000,\"Humidity\":56.5}"
        storeData("s1", msg, False);
    def testStoreData2(self):
        msg = "{\"Id\":16, \"t1\":24.437500,\"t2\":25.0,\"p\":1000,\"h\":56.5,\"bat\":2.9}"
        storeData("s2", msg, False);
    def testStoreData3(self):
        msg = "{\"messageId\":16, \"t1\":24.437500,\"p\":1000,\"h\":56.5,\"battery:\":3.3}"
        storeData("DOIT2", msg, True);
if __name__ == '__main__':
    unittest.main()