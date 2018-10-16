class Try(object):

    def __init__(self, action):
        self.action = action
        self.result = None
        self.failedDueToTheRightException = False

    def inCaseOfFailureBy(self, exceptionType):
        
        if self.failedDueToTheRightException or self.result:
            return self

        try:

            return self.action()

        except Exception as err:

            if isinstance(err, exceptionType):
                self.failedDueToTheRightException = True
                return self

        return self

    
    def doThis(self, operation):
        
        if self.result:
            return self
        
        if self.failedDueToTheRightException:
            
            self.result = operation()
            return self
        
        else:
            return self
    
    @property
    def getResult(self):
        return self.result


if __name__ == '__main__':
    def do():
        return 5 / 0

    def doFix():
        return 1

    def sleep():
        import time
        time.sleep(5)
        return "Done"

    def read():
        rdr = open("xxx.xxx", "rb")
        return rdr

    print("Test #1")
    assert (
        Try(read)
            .inCaseOfFailureBy(ZeroDivisionError)
            .doThis(doFix)
            .inCaseOfFailureBy(FileNotFoundError)
            .doThis(sleep)
        ).getResult == "Done"

    print("Test #2")
    assert (
        Try(do)
            .inCaseOfFailureBy(ZeroDivisionError)
            .doThis(doFix)
            .inCaseOfFailureBy(FileNotFoundError)
            .doThis(sleep)
        ).getResult == 1
    
