class When(object):

    state = None
    used = False
    callableObject = None

    def __init__(self, obj):
        self.obj = obj

    def of(self, item):
        self.state = self.obj == item
        if not self.state:
            try:
                self.state = isinstance(self.obj, item)
            except Exception as e:
                pass

        return self
    
    def then(self, operationToDo):
        if self.state:
            self.used = True
            self.callableObject = operationToDo(self.obj)
        return self

    def otherwise(self, operationToDo):
        if not self.state and not self.used:
            return operationToDo(self.obj)
        else:
            return self.callableObject


testArgument = []

def itsStr(n):
    return "its str"

def itsInt(n):
   return "its int"

def pop(n):
    return "just dance"

def tellMeAboutIt(*arg):
    return "wrong!"

value = ( 
    When(testArgument)
        .of(str).then(itsStr)
        .of(10).then(itsInt)
        .of([]).then(pop)
        .otherwise(tellMeAboutIt)
)
print(value)
