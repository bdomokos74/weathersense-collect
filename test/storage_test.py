import sys, os
sys.path.append('WeatherMeasTrg')

import unittest
import azure.functions as func

from blob import storeMeasurement, createBlobName
import logging
logging.basicConfig(level=logging.DEBUG)

class TestStorage(unittest.TestCase):
    storageName = os.getenv("STORAGE_ACCOUNT_NAME")
    containerName = os.getenv("BLOB_CONTAINER_NAME")
    blobName = createBlobName(sensorId="s1")
    
    def testCreateBlobName(self):
        msg = {"messageId":16, "Temperature":24.437500}
        logging.info("blobname: "+self.blobName)
        storeMeasurement(self.storageName, self.containerName, self.blobName, msg)
    
if __name__ == '__main__':
    unittest.main()