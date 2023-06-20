from contextlib import contextmanager

class GlobalContext:
    def __init__(self, on_search=None):
        self.on_search = on_search

@contextmanager
def global_context(on_search=None):
    context = GlobalContext(on_search=on_search)
    yield context