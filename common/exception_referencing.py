exception_info = None

try:
    1 / 0
except ZeroDivisionError as e:
    print(f"Caught exception: {e}")
    exception_info = e

print(exception_info, type(exception_info)) # division by zero <class 'ZeroDivisionError'>
print(e)  # NameError: name 'e' is not defined
