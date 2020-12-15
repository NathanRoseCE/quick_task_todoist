#!/usr/bin/env python3

import json
import TodoistWrapper
import tkinter as tk

class TaskPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		sortedTasks = controller.getSortedTasks()
		for i in range(len(sortedTasks)):
			button = tk.Button(self, text=sortedTasks[i]['content'], command=lambda taskId=sortedTasks[i]["id"]: controller.closeTask(taskId))
			button.bind("<Return>", lambda event, taskId=sortedTasks[i]["id"]: controller.closeTask(taskId))
			button.grid(row=i, column=0, sticky="nesw")
		#end for
		
		button = tk.Button(self, text="Close", command=controller.close)
		button.bind("<Return>", lambda event: controller.close())
		button.grid(row=len(sortedTasks)+1, column=0, sticky="nesw")
		
		button = tk.Button(self, text="Change Filter", command=lambda pageName=FilterPage : controller.showFrame(pageName))
		button.bind("<Return>",  lambda event, pageName=FilterPage : controller.showFrame(pageName))
		button.grid(row=len(sortedTasks)+2, column=0, sticky="nesw")
	#end init
#end TaskPage

class FilterPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent) 
		filters = controller.getFilters()
		for i  in range(len(filters)):
			button = tk.Button(self, text=filters[i]['name'], command=lambda name=filters[i]['name']: controller.loadFilter(name))
			button.bind("<Return>", lambda event, name=filters[i]['name']: controller.loadFilter(name))
			button.grid(row=i, column=0, sticky="nesw")
		#end for
		button = tk.Button(self, text="Close", command=controller.close)
		button.bind("<Return>", lambda event: controller.close())
		button.grid(row=len(filters)+1, column=0, sticky="nesw")
		
		button = tk.Button(self, text="View tasks", command=lambda pageName=TaskPage : controller.showFrame(pageName))
		button.bind("<Return>",  lambda event, pageName=FilterPage : controller.showFrame(pageName))
		button.grid(row=len(filters)+2, column=0, sticky="nesw")
	#end __init__
	
class SaveAsDefault(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent) 
		self.nextFrame = TaskPage
		self.controller = controller
		label = tk.Label(self, text="Save Filter As Default?")
		label.grid(row=0,column=0,columnspan=2)
		
		button = tk.Button(self, text="Yes", command=self.saveAsDefault)
		button.bind("<Return>", lambda event: self.saveAsDefault())
		button.grid(row=1, column=0, sticky="nesw")
		
		#impliment this
		button = tk.Button(self, text="No", command=lambda pageName=TaskPage : controller.showFrame(pageName))
		button.bind("<Return>",  lambda event, pageName=self.nextFrame : controller.showFrame(pageName))
		button.grid(row=1, column=1, sticky="nesw")
	#end __init__
	
	def saveAsDefault(self):
		self.controller.saveFilterAsDefault()
		self.controller.showFrame(self.nextFrame)
#end SaveAsDefault
class Application(tk.Tk):
	def __init__(self, configFilePath='./.configQuickTodoist.json', *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.configFilePath = configFilePath
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)
		self.container.grid_rowconfigure(0, weight = 1) 
		self.container.grid_columnconfigure(0, weight = 1) 
		self.__loadConfig(configFilePath)
		
		self.currentFrame = None
		self.showFrame(TaskPage)
	#end __init__
	
	def showFrame(self, cont):
		if self.currentFrame is not None:
			self.currentFrame.destroy()
			
		self.currentFrame= cont(self.container, self)
		self.currentFrame.grid(row = 0, column = 0, sticky = "nsew")

	#end showFrame
	def loadFilter(self, filterName):
		self.filter = filterName
		self.showFrame(SaveAsDefault)
	#end loadFilter
	
	def saveFilterAsDefault(self):
		self.config["FILTER_NAME"] = self.filter
		with open(self.configFilePath, "w+") as f:
			f.write(json.dumps(self.config, indent=4))
			f.truncate()
		#end context manager
	#end saveFilterAsDefault
	def __loadConfig(self, configFilePath):
		f = open(configFilePath)
		self.config = json.load(f)
		self.api = TodoistWrapper.TodoistWrapper(self.config['API_KEY'])
		self.filter = self.config["FILTER_NAME"]
		f.close()
	#end loadConfig
	
	def closeTask(self, taskID):
		self.api.closeTask(taskID)
		self.close()
	#createTaskAndClose
	
	def getSortedTasks(self):
		tasks = self.api.getTasksByFilter(self.filter)
		datelessTasks = []
		taskCpys = tasks.copy()
		for task in taskCpys:
			date = None
			try:
				task["due"]["date"]
			except KeyError:
				datelessTasks.append(task)
				tasks.remove(task)
			#end try
			
		sortedTasks = sorted(tasks, key=lambda x : x["due"]["date"])
		for item in datelessTasks:
			sortedTasks.append(item)
		#end for
		return sortedTasks
	#end getSOrtedTasks
	
	def getFilters(self):
		return self.api.getAllFilters()
	def close(self):
		self.destroy()
	#end close
#end Application

if __name__ == "__main__":
	app = Application(configFilePath="./config.json")
	app.mainloop()
#end if
