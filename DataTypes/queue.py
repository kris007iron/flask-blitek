class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        return self.queue.pop(0)
    def size(self):
        return len(self.queue)
    def is_empty(self):
        return len(self.queue) == 0
    def __str__(self):
        return str(self.queue)
    def __repr__(self):
        return str(self.queue)
