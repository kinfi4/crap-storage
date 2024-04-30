import sys
import weakref


class Obj:
    def __del__(self):
        print("The object is being destroyed")


def show_case():
    obj = Obj()

    print(f"Number of references: {sys.getrefcount(obj)}")

    ref = weakref.ref(obj)

    print(f"Number of references: {sys.getrefcount(obj)}")  # doesn't count weak references !!!

    print(ref)
    print(ref())
    del obj
    print(ref())  # None, because the object was destroyed


def circular_references():
    obj = Obj()
    obj.obj = obj  # making a circular reference
    print(obj.obj.obj.obj.obj)
    obj = None  # the object is not destroyed, because of the circular reference :(((

    import gc; gc.collect()  # collect garbage

    obj = Obj()
    obj.obj = weakref.proxy(obj)  # making a circular weak reference
    print(obj.obj.obj.obj.obj)
    obj = None  # the object is destroyed, because of the weak reference :))


if __name__ == "__main__":
    show_case()
    circular_references()
