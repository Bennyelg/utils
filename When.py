
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
            except Exception:
                pass

        return self
    
    def then(self, operationToDo, *args, **kwargs):
        if self.state:
            self.used = True
            self.callableObject = (
                operationToDo(self.obj, *args, **kwargs)
                if callable(operationToDo)
                else operationToDo
            )
        return self

    def otherwise(self, operationToDo, *args, **kwargs):
        if not self.state and not self.used:
            return (
                operationToDo(self.obj, *args, **kwargs) 
                if callable(operationToDo)
                else operationToDo
            )
        else:
            return self.callableObject


if __name__ == '__main__':

    def firstTest():
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

        assert value == "just dance"
    
    def secondTest():
        
        myTestArugment = 100

        value = (
            When(myTestArugment)
                .of(25 * 4).then("you got it right.")
                .otherwise("I think you missed the point.")
        )
        assert value == "you got it right."

        value2 = (
            When(10)
            .of(15).then("yep!")
            .otherwise(None)
        )
        assert value2 == None
    
    def thirdTest():
        
        def mutliplyBy(_, value):
            return _ * value
        
        def echoToTheScreen(_):
            return "To the Screen!" + _ 
        
        def castToInt(_):
            return int(_)

        value = (
            When(13.2)
            .of(int).then(mutliplyBy, 10)
            .of(str).then(echoToTheScreen)
            .of(float).then(castToInt)
            .otherwise(None)
        )
        
        assert value == 13
        

    firstTest()
    secondTest()
    thirdTest()
