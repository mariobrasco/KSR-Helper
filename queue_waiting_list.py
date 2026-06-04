class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, mahasiswa):
        self.items.append(mahasiswa)

    def dequeue(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)

    def display(self):
        if len(self.items) == 0:
            print("Waiting list kosong")
            return

        print("Waiting List:")
        for i, mhs in enumerate(self.items, start=1):
            print(f"{i}. {mhs}")