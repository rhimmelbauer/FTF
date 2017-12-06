import Queue 

class OneQueue():
	__q = None
	@staticmethod
	def getOneQueue():
		if not OneQueue.__q:
			OneQueue.__q = Queue.Queue()
		return OneQueue.__q