
import TodoistWrapper
import json
configFilePath = "config.json"
f = open(configFilePath)
config = json.load(f)

api = TodoistWrapper.TodoistWrapper(config["API_KEY"])
tasks = api.getTasksByFilter("Current Sprint")

sortedTasks = []
sortedTasks = sorted(tasks, key=lambda x : x["due"]["date"])

for task in range(len(sortedTasks)):
	print(sortedTasks[task]["content"])
