import threading
import time

ls = []

def func(n):
	for i in range(1, n+1):
		ls.append(i)
		time.sleep(0.5)
def func2(n):
	for i in range(1, n+1):
		ls.append(i)
		time.sleep(0.5)
x = threading.Thread(target=func, args=(5,))
x.start()

# Switch back to the other thread
# Which means switch for x thread to y thread
y = threading.Thread(target=func2, args=(5,))
y.start()

print(threading.active_count())

x.join()
y.join()
#  Donnot Print ls: -> List Until you synchronize and finish both x and y

print(ls)