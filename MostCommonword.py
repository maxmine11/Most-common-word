import queue

class MostCommonWord:

	def __init__(self):
		# Dictionary to keep track of keys and values inputed by the user
		self.data = {}
		# Priority Queue to keep track of the repeated words in order
		self.mostCmmnWord = queue.PriorityQueue()
		# Dictionary to keep track of repeated words 
		self.noRepeats = {}


	def set_cmnd(self, path_to_key, word):
		replaced_words = []
		my_keys = path_to_key.split("/")
		my_dict = self.data
		index = 0
		for key in my_keys:
			if (key in my_dict):
				value = my_dict[key]
				if (index < len(my_keys) - 1):
					if (type(value) is dict):
						my_dict = value
						index += 1
					else:
						# Need to replace a value for a dictionary
						replaced_words.append(value)
						value = {}
						my_dict[key] = value
						my_dict = value
						index +=1
				else: 
					my_dict[key] = word

			else:
				if (index < len(my_keys) - 1):
					value = {}
					my_dict[key] = value
					my_dict = value
					index +=1

				else: 
					my_dict[key] = word
		#Update noRepeats and Priority Queue  for word 
		#need to add an extra repetition to the word
		if (word in self.noRepeats):
			self.noRepeats[word] += 1
		else:
			self.noRepeats[word] = 1

		self.mostCmmnWord.put((-self.noRepeats[word], word))
		self.updateWords(replaced_words)
		return 


	def del_cmnd(self, path_to_key):
		my_keys = path_to_key.split("/")
		deleted_words = []
		my_dict = self.data
		index = 0
		for key in my_keys:
			if (key in my_dict):
				value = my_dict[key]
				if (index < len(my_keys) - 1):
					if (type(value) is dict):
						my_dict = value
						index += 1
					else:
						print ("%s already does not exist" % (path_to_key))
						return
				else: 
					if (type(value) is dict):
						deleted_words = value.values()
					else:
						deleted_words.append(value)

					del my_dict[key]
			else:
				print ("%s already does not exist" % (path_to_key))
				return
		self.updateWords(deleted_words)
		return

	def updateWords(self, words):
		#Update noRepeats and Priority Queue  for deleted words
		for word in words:
			self.noRepeats[word] -= 1
			self.mostCmmnWord.put((-self.noRepeats[word], word))

		if (len(self.data) != 0):
			self.print_data(self.data, "")
		if (self.mostCmmnWord.empty()):
			return

		item = self.mostCmmnWord.queue[0]
		while (True):
			if (item[1] not in self.noRepeats):
				self.mostCmmnWord.get()
				if (self.mostCmmnWord.empty()):
					item = (0, "")
					break
				else:
					item = self.mostCmmnWord.queue[0]

			elif (item[0] != -self.noRepeats[item[1]]):
				if (self.noRepeats[item[1]] == 0):
					del self.noRepeats[item[1]]
				self.mostCmmnWord.get()
				if (self.mostCmmnWord.empty()):
					item = (0, "")
					break
				else:
					item = self.mostCmmnWord.queue[0]
			else:
				break

		if (item[0] != 0):
			print ("Most common word: %s" % item[1])


	def print_data(self, my_dict, extra):
		for key, value in my_dict.items():
			if (type(value) is dict):
				print (extra + "%s+ %s:" % (extra, key))
				self.print_data(value, extra+"+")
			else:
				print ("%s+ %s: %s" % (extra, key, value))


if __name__ == "__main__":
	MCW = MostCommonWord()
	ON = True
	while (ON):
		command_word = input("Enter command: ")
		command_lst = command_word.split(" ")
		if (command_lst[0].lower() == "set"):
			if (len(command_lst) != 3):
				print ("missing command arguments")
			else:
				MCW.set_cmnd(command_lst[1], command_lst[2])
		elif (command_lst[0].lower() == "del"):
			if (len(command_lst) != 2):
				print ("missing command arguments")
			else:
				MCW.del_cmnd(command_lst[1])
		else:
			print("command not found")




		



