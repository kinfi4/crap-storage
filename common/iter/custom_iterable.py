class CustomIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration

        value = self.data[self.index]
        self.index += 1
        return value


class CustomIterable:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return CustomIterator(self.data)
