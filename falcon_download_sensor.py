#!/usr/bin/env python3

# Python script to download the most recent sensors
# for multiple operating systems

##############################################
# Requirements:
#   pip3 install crowdstrike-falconpy==0.9.0
##############################################

# Import creds
from secrets import csfalcon
falcon_host, falcon_user, falcon_pass = csfalcon.get(csfalcon)

import os
# Import falcon
from falconpy import SensorDownload

# Globals
# Download sensors for the following operating systems
OPERATING_SYSTEM_FILTER = [
        f"platform: 'windows'", 
        f"platform:'linux'+os:'Ubuntu*'", 
        f"platform: 'mac'"
        ]

# Offset for sensor release
# For this script,
#    0 = most recent
#    1 = second most recent
#    2 = third most recent
#    ...
OFFSET = 0

# The path to save sensor downloads to
# e.g. "/home/foo/falconsensors/"
DOWNLOAD_PATH = os.getcwd()

# Prefix for filename of downloaded sensor
# Leave blank to use default filename
SENSOR_FILE_PREFIX = "crowdstrike-falcon-sensor" # This will save as "crowdstrike-falcon-sensor-windows.exe"
#SENSOR_FILE_PREFIX = ""

# For each filter, download the most recent sensor, n-OFFSET
for ostype in OPERATING_SYSTEM_FILTER:

  print("[INFO] Searching Falcon sensors with pattern, \"{}\"".format(ostype))
  try:
    falcon = SensorDownload(
            client_id=falcon_user,
            client_secret=falcon_pass
            )

    response = falcon.get_sensor_installers_by_query(
            offset=OFFSET,
            filter=ostype
            )
  
  except Exception as msg:
      print("[ERROR] No sensor available for filter: \"{}\"\nError Stack: {}".format(ostype, msg))

  sensor_id = response['body']['resources'][0]
  sensor_info = falcon.get_sensor_installer_entities(ids=sensor_id)
  sensor_desc = sensor_info['body']['resources'][0]['description']
  sensor_file_type = sensor_info['body']['resources'][0]['file_type']
  sensor_os = sensor_info['body']['resources'][0]['platform']
  sensor_version = sensor_info['body']['resources'][0]['version']

  if not SENSOR_FILE_PREFIX or SENSOR_FILE_PREFIX == "":
      sensor_file_name = sensor_info['body']['resources'][0]['name']
  else:
      sensor_file_name = "{}-{}.{}".format(SENSOR_FILE_PREFIX, sensor_os, sensor_file_type)

  print("[INFO] Downloading \"{} v{}\" to {}/{}...".format(
      sensor_desc, 
      sensor_version, 
      DOWNLOAD_PATH + "/", 
      sensor_file_name
      ))
  try:
    download = falcon.download_sensor_installer(
        id=sensor_id,
        download_path=DOWNLOAD_PATH,
        file_name=sensor_file_name
        )
  except Exception as msg:
      print("[ERROR] Failed to download {}\nError Stack: {}".format(sensordownload, msg))

print("Crowdstrike Sensor Downloads Complete")
