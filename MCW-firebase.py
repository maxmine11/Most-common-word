import pyrebase
import queue


class MostCommonWord:

	def __init__(self, database):
		# Dictionary to keep track of keys and values inputed by the user
		self.data = database
		# Keep track of most-common-word
		self.mcw_dict = {}

	def set_cmnd(self, path, word):
		data = {"data/"+path: word}
		self.data.update(data)
		self.updateWords()


	def del_cmnd(self, path):
		#my_keys = path_to_key.split("/")
		db = self.data.child("data/"+path).remove()
		self.updateWords()


	def updateWords(self):
		self.print_data(self.data.child("data").get(), "")
		item= ["", 0]
		for key, value in self.mcw_dict.items():
			if (item[1] < value):
				item[0] = key
				item[1] = value

		self.mcw_dict.clear()
		if (item[0] is not ""):
			print ("Most common word: %s" % item[0])


	def print_data(self, my_dict, extra):
		for item in my_dict.each():
			key = item.key()
			value = item.val()
			if (not isinstance(value, str)):
				print (extra + "%s+ %s:" % (extra, key))
				self.print_data(value, extra+"+")
			else:
				print ("%s+ %s: %s" % (extra, key, value))
				if (value in self.mcw_dict):
					self.mcw_dict[value] += 1
				else:
					self.mcw_dict[value] = 1


if __name__ == "__main__":
	config = {
	"apiKey": "",
	"databaseURL": "https://most-common-word.firebaseio.com",
	"authDomain": "most-common-word.firebaseapp.com",
	"storageBucket": "most-common-word.appspot.com",
	"serviceAccount": "most-common-word-2f156b647a18.json"

	}

	firebase = pyrebase.initialize_app(config)

	# Get a reference to the database service
	db = firebase.database()
	MCW = MostCommonWord(db)
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




		



