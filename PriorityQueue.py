import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def put2(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)[1]

    def get2(self):
        return heapq.heappop(self.elements)

    def exists(self, item):
        return item in (x[1] for x in self.elements)

    def __len__(self):
        return len(self.elements)


if __name__ == "__main__":
    cue = PriorityQueue()
    cue.put("highValue", 10)
    cue.put("lowValue", 0)
    cue.put("midValue", 5)

    print(cue.get())
    print(cue.get())
    print(cue.get())
