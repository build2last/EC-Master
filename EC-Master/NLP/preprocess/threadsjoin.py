# coding:utf-8
import threading
import time

def eat(food, count):
	print("Now begin to eat %s for %d"%(food, count))
	time.sleep(2)
	print(food + " was eaten")

def have_lunch():
	threads = []
	threads.append(threading.Thread(target=eat, args=("Shit",1)))
	th2 = threading.Thread(target=eat, args=("Eggs",2))
	threads.append(th2)
	for th in threads:
		th.start()
	for th in threads:
		th.join()
	print("You both eat a lot!")

if __name__ == '__main__':
	have_lunch()
