class Iterable:
    def __init__(self):
        self.collection = [1, 2, 3]

    def generate(self):
        for item in self.collection:
            yield item

    def __iter__(self):
        return self.generate()


iterable = Iterable()
for item in iterable:
    print(item)
