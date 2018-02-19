import threading, queue


# TODO add documentation
class ServerTaskQueue:

    def __init__(self, workers_size=4):
        self.task_queue = queue.Queue()
        self.workers_size = workers_size
        self.threads = []

        for i in range(workers_size):
            t = threading.Thread(name="ServerTaskQueue_Thread_"+str(i), target=self.execute_task)
            t.start()
            self.threads.append(t)

    def execute_task(self):
        while True:
            task_description = self.task_queue.get()
            task = task_description['task']
            args = task_description['arguments']
            if task is None:
                break
            task(*args)
            self.task_queue.task_done()

    def put_task(self, task, arguments=None):
        self.task_queue.put({
            'task': task,
            'arguments': arguments
        })

    def stop_queue(self):
        for i in range(self.workers_size):
            self.put_task(None)


# def tst(arg1, arg2):
#     print("Arg1: ", arg1, "Arg2: ", arg2)
#
# q = ServerTaskQueue()
# q.put_task(tst, ("123", "456"))
# print(("123", "456"))
# q.stop_queue()