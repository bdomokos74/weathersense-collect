import sys, os
sys.path.append('WeatherMeasTrg')

import unittest
import azure.functions as func

from blob import createRecord
import logging

# Run this way:
# . .local/devenv.sh
# python test/blob_test.py

# Uncomment for debugging
logging.basicConfig(level=logging.DEBUG)

class TestStorage(unittest.TestCase):

   def testCreateRecord1(self):
       st = createRecord("{\"Temperature\": 23.2, \"Pressure\": 936.6, \"Humidity\": 55.9}")
       print(st)
   def testCreateRecord2(self):
       st = createRecord("{\"Temperature\": 23.2, \"Pressure\": 936.6, \"Humidity\": 55.9,\"bat\":3.23,\"offset\":0}\n{\"Temperature\": 24.2, \"Pressure\": 936.6, \"Humidity\": 55.9,\"offset\":2000}\n{\"Temperature\": 25.2, \"Pressure\": 936.6, \"Humidity\": 55.9,\"offset\":4000}\n")
       print(st)

if __name__ == '__main__':
    unittest.main()
