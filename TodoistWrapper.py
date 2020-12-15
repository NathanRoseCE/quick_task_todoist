from todoist.api import TodoistAPI
import json, requests
class TodoistWrapper:

	def __init__(self, key):
		self.key = key
		self.api = TodoistAPI(key)
	#end __init__
	
	def getProjectFromName(self, projectName):
		self.api.sync()
		projects = self.api.state['projects']
		
		for project in projects:
			if project.__getitem__("name") == projectName:
				return project
			#end if
		#end for
		return None
	#end getProjectWithName

	def getTasksByFilter(self, filterName):
		self.api.sync()
		f = [f for f in self.api.state['filters'] if f['name'] == filterName][0]
		
		tasks = requests.get(
    		"https://api.todoist.com/rest/v1/tasks",
    		params={
        		"filter": f['query']
    		},
    		headers={
     		   "Authorization": "Bearer %s" % self.key
    		}).json()
		return tasks
	#end getTasksByFilter
	def getProjectIDFromName(self, projectName):
		project = self.getProjectFromName(projectName)
		if project is not None:
			return project.__getitem__("id")
		#end if
		print("Project " + projectName + " not found")
		return None
	#end getIDFromName
	
	def getAllLabels(self):
		self.api.sync()
		return self.api.state['labels']
	#end getAllLabels
	
	def getLabelFromName(self, labelName):
		self.api.sync()
		labels = self.api.state['labels']
		for label in labels:
			if label.__getitem__('name') == labelName:
				return label
			#end if
		#end for
		print("Label " + labelName + " not found")
		return None
	#end getLabelFromName
	
	def getLabelIDFromName(self, labelName):
		label = self.getLabelFromName(labelName)
		if label is not None:
			return label.__getitem__("id")
		#end if
		return None
	#end getLabelIDFromName
		
	def getAllFilters(self):
		self.api.sync()
		return self.api.state['filters']
	#end getAllLabels
	
	def getFilterFromName(self, filterName):
		self.api.sync()
		filters = self.api.state['filters']
		for filter in filters:
			if filter.__getitem__('name') == filterName:
				return filter
			#end if
		#end for
		return None
	#end getLabelFromName
	
	def getFilterIDFromName(self, filterName):
		filter = self.getFilterFromName(filterName)
		if filter is not None:
			return filter.__getitem__("id")
		#end if
		return None
	#end getLabelIDFromName
	
	def createTask(self, taskName, projectName, priority=3, comment=None, labels=[], dueString=None):
		if priority > 4:
			priority = 4
		elif priority <= 0:
			priority = 1
		#end if
		
		#For whatever reason this number needs to be inverted idk y
		prio = priority
		if priority == 4:
			prio = 1
		elif priority == 3:
			prio = 2
		elif priority == 2:
			prio = 3
		else:
			prio = 4
		#end if
		
		
		# get ID's
		labelIds = []
		for labelName in labels:
			labelId = self.getLabelIDFromName(labelName.strip())
			if labelId is not None:
				labelIds.append(labelId)
			else:
				print("Label " + labelName + " not found")
			#end if
		#end for
		
		projectId = self.getProjectIDFromName(projectName.strip())
		if projectId is None:
			print("Project Name: " + projectName + " not found")
			return
		#end if
		
		args = {}
		args['priority'] = prio
		if projectId is not None:
			args['project_id'] = projectId
		#end if
		if labelIds is not None:
			args['labels'] = labelIds
		#end if
		if dueString is not None:
			args['due'] = {'string': dueString}
		#end if
		
		task = self.api.items.add(taskName, **args)
		if comment is not None:
			comment3 = api.notes.add(task['id'], comment)
			#end if
		self.api.commit()
	#end createTask
	
	def closeTask(self, taskID):
		requests.post("https://api.todoist.com/rest/v1/tasks/%s/close" % taskID, headers={"Authorization": "Bearer %s" % self.key})
	#end closeTask

#end Project_Wrapper
