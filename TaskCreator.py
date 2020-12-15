#!/usr/bin/env python3

import json
import TodoistWrapper
import tkinter as tk

class GUI:
	def __init__(self, configFilePath='./.configQuickTodoist.json'):
		self.__loadConfig(configFilePath)
		self.createGUI()
	#end __init__
	
	def __loadConfig(self, configFilePath):
		f = open(configFilePath)
		self.config = json.load(f)
	#end loadConfig
	
	def createTaskAndClose(self):
		api = TodoistWrapper.TodoistWrapper(self.config['API_KEY'])
		api.createTask(self.taskName.get(), self.taskProject.get(), int(self.taskPriority.get()), dueString=self.taskDueString.get())
		self.root.destroy()
	#createTaskAndClose
		
	def clickEvent(self, event):
		self.createTaskAndClose() 
	#end clickEvent
	
	def createGUI(self):
		self.root=tk.Tk()
		self.root.title('Task Creator')

		self.taskName = tk.StringVar(self.root)
		self.taskNameLabel = tk.Label(self.root, text="Task Name: ")
		self.taskNameLabel.grid(row=0,column=0)
		self.taskNameEntry = tk.Entry(self.root,textvariable = self.taskName,bd=3)
		self.taskNameEntry.grid(row=0,column=1)
	
		self.taskProject = tk.StringVar(self.root)
		self.taskProjectLabel = tk.Label(self.root, text="Project: ")
		self.taskProjectLabel.grid(row=1,column=0)
		self.taskProjectEntry = tk.Entry(self.root,textvariable = self.taskProject,bd=3)
		self.taskProjectEntry.grid(row=1,column=1)
		
		self.taskPriority = tk.StringVar(self.root)
		self.taskPriorityLabel = tk.Label(self.root, text="Priority: ")
		self.taskPriorityLabel.grid(row=2,column=0)
		self.taskPriorityEntry = tk.Entry(self.root,textvariable = self.taskPriority,bd=3)
		self.taskPriorityEntry.grid(row=2,column=1)
		
		self.taskDueString = tk.StringVar(self.root)
		self.taskDueStringLabel = tk.Label(self.root, text="Due Date: ")
		self.taskDueStringLabel.grid(row=3,column=0)
		self.taskDueStringEntry = tk.Entry(self.root,textvariable = self.taskDueString,bd=3)
		self.taskDueStringEntry.grid(row=3,column=1)
		
		
		self.button = tk.Button(self.root,text='Create',command=self.createTaskAndClose)
		self.button.grid(row=4,column=0)
		self.button.bind("<Return>", self.clickEvent)
		self.root.mainloop()
	#end creatGUI
	
if __name__ == "__main__":
	GUI(configFilePath="./.configQuickTodoist.json")
#end if
