import threading
import time
x = 0 # global variable x

def increment():
    # function to increment global variable x
    global x
    temp = x
    time.sleep(0.0)
    temp = temp + 1
    x = temp

def thread_task():
    # task for thread
    for _ in range(100000):
        increment()

def main_task():
    global x
    x = 0 # setting global variable x as 0

    # creating threads
    t1 = threading.Thread(target=thread_task)
    t2 = threading.Thread(target=thread_task)

    # start threads
    t1.start()
    t2.start()

    # wait until threads finish their job
    t1.join()
    t2.join()

if __name__ == "__main__":
    for i in range(10):
        main_task()
        print("Iteration {0}: x = {1}".format(i,x))