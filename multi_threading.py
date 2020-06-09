import threading
import time

class MyThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print("Starting", self.name, "\n")
		thread_lock.acquire()
		print_time(self.name, 1, self.counter)
		thread_lock.release()
		print("Exiting", self.name, "\n")

class MyThread2(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print("Starting", self.name, "\n")
		thread_lock.acquire()
		thread_lock.release()
		print_time(self.name, 1, self.counter)
		print("Exiting", self.name, "\n")

def print_time(threadName, delay, counter):
	while counter:
		time.sleep(delay)
		print(f"{threadName}: {time.ctime(time.time())} {counter}")
		counter -= 1


# Lock the thread
thread_lock = threading.Lock()

# Create new Threads
thread1 = MyThread(1, "Payment", 5)
thread2 = MyThread2(2, "Sending Email", 10)
thread3 = MyThread2(3, "Loading Page", 3)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
# This helps you execute loading the page while the email is being sent
# which will save much more time
# And the user won't be upset

thread1.join()
thread2.join()
thread3.join()

print("Exiting Main Thread")