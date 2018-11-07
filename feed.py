#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Main imports
import sys
try:
	import requests
except ImportError as e:
	print("\'requests\' module is required.\nYou can install it with \'pip install requests\'")
	sys.exit(1)
import json
import os
import argparse

# Arguments parser
arguments_parser = argparse.ArgumentParser(description="Trello-Clockify connector")
arguments_parser.add_argument("--config",dest="config",action="store",default="config.json",help="JSON configuration file (default: config.json)")
arguments_parser.add_argument("-trello",dest="trello",action="store_true",help="Run help with Trello configuration (not implemented yet)")
arguments_parser.add_argument("-clockify",dest="clockify",action="store_true",help="Run help with Clockify configuration (not implemented yet)")
arguments_parser.add_argument("-configure",dest="configure",action="store_true",help="Run configration generator (not implemented yet)")
arguments = arguments_parser.parse_args()

# Assert config.json existence
if not os.path.exists(arguments.config):
	print("\'%s\' config file was not found.\nConsult README.md to find out how to create one"%arguments.config)
	sys.exit(1)

# Read config
with open(arguments.config,"r") as config_file:
	try:
		config = json.load(config_file)
	except json.decoder.JSONDecodeError as e:
		print("\'%s\' is an invalid JSON file."%arguments.config)
		sys.exit(1)

# Load Trello tasks
params = {"key": config["trello"]["api-key"], "token": config["trello"]["access-token"], "fields": ["name", "labels"]}
r = requests.get("https://api.trello.com/1/boards/%s/cards/"%config["trello"]["dashboard"],params=params)
try:
	data = r.json()
except Exception as e:
	# ToDo: Give help
	print(e)
	sys.exit(1)

# Get formatted name of a task
trello_tasks = []
for trello_card in data:
	if len(trello_card["labels"])==0 and config["config"]["skip-tagless"]:
		print("Skipping",repr(trello_card["name"]),"- no tags")
		continue
	current_card = {"name": trello_card["name"], "tags": ", ".join([l["name"] for l in trello_card["labels"]])}
	trello_tasks.append(config["config"]["format"]%current_card)

# Get existing Clockify.me tasks
cme_conf = {"workspaceId": config["clockify"]["workspace"], "projectId": config["clockify"]["project"]}
cme_headers = {"X-Api-Key": config["clockify"]["api-key"], "Content-type": "application/json"}
r = requests.get("https://api.clockify.me/api/workspaces/%(workspaceId)s/projects/%(projectId)s/tasks/"%cme_conf,headers=cme_headers)

try:
	data = r.json()
except Exception as e:
	# ToDo: Give help
	print(e)
	sys.exit(1)

cme_tasks = [t["name"] for t in data]

# Push all tasks that do not exist on the server
for task in trello_tasks:
	if task in cme_tasks:
		print("Skipping",repr(task),"- already exists")
		continue
	data = {"name": task, "projectId": cme_conf["projectId"]}
	r = requests.post("https://api.clockify.me/api/workspaces/%(workspaceId)s/projects/%(projectId)s/tasks/"%cme_conf,headers=cme_headers,json=data)
	print(r.url)
	print(r.text)