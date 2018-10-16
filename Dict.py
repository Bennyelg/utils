from typing import Dict, Any

class NamedDict(object):

    def __init__(self, anyDict: Dict[Any, Any] = {}):
        self.__dict__.update(**anyDict)
    
    def __setattr__(self, attr, value):
        try:
            self.__dict__.__setattr__(attr, value)
        except AttributeError:
            self.__dict__[attr] = value

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)
    
    def __iter__(self):
        for item, value in self.__dict__.items():
            yield item, value
    
    def union(self, other: Dict[Any, Any]) -> Dict:
        for item, value in other:
            self.__setattr__(item, value)
        return NamedDict(self.__dict__)
    
    def __eq__(self, other: Dict[Any, Any]) -> bool:
        for i in zip(self.__dict__.items(), other.__dict__.items()):
            if i[0] != i[1]:
                return False
        return True
    
    def __len__(self):
        return len(self.__dict__)
    

    

    

if __name__ == '__main__':
    
    def unionTest():
        test = NamedDict({"benny": 10, "elgazar": 1, "age": 89})
        test2 = NamedDict({"first": 5})

        unified = test2.union(test)
        assert NamedDict({'first': 5, 'benny': 10, 'elgazar': 1, 'age': 89}) == unified
    
    def simpleCallTest():
        test = NamedDict()
        test.name = "Benny"
        test.age = 15
        assert test.age == 15 and test.name == "Benny"
    
    def nestedCalls():
        test = NamedDict()
        test.properties = NamedDict()
        test.properties.firstName = "benny"
        assert test.properties.firstName == "benny"


        
    

    simpleCallTest()
    unionTest()
    nestedCalls()