class Logger:
    def __init__(self):
        self.path: str = None

    def set_file(self, path: str, clear: bool = False):
        self.path = path
        if clear:
            with open(self.path, "w"):
                pass

    def log(self, *args, force_print=False):
        if self.path is None or force_print:
            print(*args)
        if self.path is not None:
            with open(self.path, "a") as f:
                for arg in args:
                    f.write(str(arg) + "\n")

logger = Logger()
