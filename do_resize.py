#!/usr/bin/env python3

import requests
import json
import argparse
import time
import sys

parser = argparse.ArgumentParser(description='This script can resize a Digital Ocean droplet. It is intended to be used for scheduling a droplet resize at a specific time using cron, but can be used at any event trigger.')
parser.add_argument('--resize' , nargs='?', help='Specify the droplet size')
parser.add_argument('--expand', help='Expand to larger droplet',action='store_true')
parser.add_argument('--contract', help='Resize to smaller droplet',action='store_true')
parser.add_argument('-v','--verbose', help='Turn on output',action='store_true')
args = parser.parse_args()

verbose = args.verbose

try:
	with open('config.json', 'r') as f:
	    config = json.load(f)
	if verbose is True:
		print("Configuration file loaded.")
except Exception as e:
	print("Configuration file config.json could not be found or loaded. Error: "+str(e))
	sys.exit(1)

try:
	if args.resize:
		size = args.resize
	elif args.expand:
		size = config["lgsize"]
	else:
		size = config["smsize"]
	if verbose is True:
		print("Target droplet size set to "+size)
except Exception as e:
	print("Target droplet resize could not be set. Exiting. Error: "+str(e))
	sys.exit(2)

headers= {"Content-Type":"application/json","Authorization":"Bearer "+config["apikey"]}
shutdowndata = {'type':'shutdown'}
resizedata = {'type':'resize','disk':False,'size':size}
powerondata = {'type':'power_on'}

apiurl = config["url"]+config["dropletID"]

try:
	if verbose is True:
		print("Sending shutdown signal to droplet "+config["dropletID"])
	res_json = requests.post(apiurl+"/actions",headers=headers,data=json.dumps(shutdowndata))
except Exception as e:
	print("Error sending shutdown signal. Error: "+str(e))
	print(res_json.json())
	sys.exit(3)

try:
	if verbose is True:
		print("Checking the status of the droplet")
	while True:
		res = requests.get(apiurl,headers=headers)
		res_json = res.json()	
		if res_json['droplet']['status'] == 'off':
			if verbose is True:
				print("Status: "+res_json['droplet']['status'])
				print("Sending resize request for "+size)
			res = requests.post(apiurl+"/actions",headers=headers,data=json.dumps(resizedata))
			break
		else:
			if verbose is True:
				print(res_json['droplet']['status'])
			time.sleep(10)
except Exception as e:
	print("Error getting droplet status. Error: "+str(e))
	print(res.json())
	sys.exit(4)

try:
	if verbose is True:
		print("Waiting for droplet resize confirmation")
	while True:
		res = requests.get(apiurl,headers=headers)
		res_json = res.json()
		if verbose is True:
			print(res_json['droplet']['size']['slug'])
		if size == res_json['droplet']['size']['slug']:
			if verbose is True:
				print("Droplet resized to "+size)
				print("Sending the power on request.")
			res = requests.post(apiurl+"/actions",headers=headers,data=json.dumps(powerondata))
			break
		else:
			if verbose is True:
				print("Droplet size: "+res_json['droplet']['size']['slug'])
			time.sleep(10)

except Exception as e:
	print("Error resizing the droplet. Error: "+str(e))

