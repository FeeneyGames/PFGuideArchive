from threading import Lock


# print exceptions nicely and thread safe
def print_exception(msg, identifier, exception):
    with _print_exception_lock:
        print(msg + "\n" + identifier)
        print(exception)
        print()


_print_exception_lock = Lock()