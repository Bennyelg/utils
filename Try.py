class Try(object):

    def __init__(self, action):
        self.action = action
        self.result = None
        self.failedDueToTheRightException = False

    def inCaseOf(self, exceptionType):
        
        if self.failedDueToTheRightException or self.result:
            return self

        try:

            self.result = self.action if not callable(self.action) else self.action()

        except Exception as err:

            if isinstance(err, exceptionType):
                self.failedDueToTheRightException = True
                return self

        return self

    
    def then(self, operation):
        if self.result:
            return self
        
        if self.failedDueToTheRightException:
            self.result = operation() if callable(operation) else operation
            return self
        
        else:
            return self
    
    @property
    def getResult(self):
        return self.result


if __name__ == '__main__':
    def then():
        return 5 / 0

    def thenFix():
        return 1

    def sleep():
        import time
        time.sleep(5)
        return "thenne"

    def read():
        rdr = open("xxx.xxx", "rb")
        return rdr

    print("Test #1")
    assert (
        Try(read)
            .inCaseOf(ZeroDivisionError)
            .then(thenFix)
            .inCaseOf(FileNotFoundError)
            .then(sleep)
        ).getResult == "thenne"

    print("Test #2")
    assert (
        Try(then)
            .inCaseOf(ZeroDivisionError)
            .then("hello")
            .inCaseOf(FileNotFoundError)
            .then(sleep)
        ).getResult == "hello"

