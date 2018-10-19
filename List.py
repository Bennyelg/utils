import time

from itertools import chain
from functools import reduce
from inspect import isfunction


class List(list):
 
    def __init__(self, *args):
        list.__init__(self)
        for item in args:
            self.append(item)


    def filter(self, func):
        changedList = []
        for element in self:
            if func(element):
                changedList.append(element)
        return List(*changedList)
    
    def reduce(self, func):
        return reduce(func, self)
    
    def add(self, *args):
        self.extend(args)
        return self
    
    def sum(self, sumFunc = None):
        if isfunction(sumFunc):
            return sum(sumFunc(item) for item in self)
        else:

            return sum(el for el in self)
    
    @property
    def length(self):
        length = 0
        for _ in self:
            length += 1
        return length

    @property
    def distinct(self):
        from collections import OrderedDict
        items = OrderedDict()
        for item in self:
            if item not in items:
                items[item] = 0
        return List(*items.keys())

    def cat(self, num):
        return self[0: num]
    
    def forEach(self, func):
        for item in self:
            func(item)
    
    @property
    def first(self):
        return self[0]
    
    @property
    def last(self):
        return self[-1]

    @property
    def isEmpty(self):
        return not any(True for _ in self)

    def map(self, func):
        newList = []
        for item in self:
            newList.append(func(item))
        return List(*newList)

    @property
    def max(self):
        maximum = None
        for i in self:
            if not maximum or maximum < i:
                maximum = i
        return maximum

    def join(self, delimiter):
        return f"{delimiter}".join(
            map(str, self)
        )
    
    @property
    def min(self):
        lower = None
        for i in self:
            if not lower or lower > i:
                lower = i
        return lower

    @property
    def zipWithIndex(self):
        self = List(*list(enumerate(self)))
        return self    
                    
    def slice(self, start, end):
        return List(*self[start: end])
    
    def sortIt(self, key=None, decendingOrder=False):
        if not key:
            fn = lambda x: x
        else:
            fn = key
        self.sort(key=fn, reverse=decendingOrder)
        return List(*self)
    
    def remove(self, *items):
        ls = []
        for litem in self:
            if litem not in items:
                ls.append(litem) 
        return List(*ls)

    def removeItemAtIndex(self, index):
        if index == 0:
            return List(*self[index + 1:])

        return List(*self[0: index] + self[index + 1:])

    def toDict(self, listOfKeys = None):
        if listOfKeys:
            return dict(zip(listOfKeys, self))
        else:
            return dict(zip(range(self.length), self))




if __name__ == '__main__':
    
    def filterLowerThen10(num):
        if num > 10:
            return True

    def multiplyEachBy10(num):
        return num * 10


    # Should be equal to 610
    assert(
        List(10, 2, 13, 87, 22, 48)
            .sortIt()
            .add(10, 8, 33)
            .distinct
            .filter(filterLowerThen10)
            .map(multiplyEachBy10)
            .remove(330, 220, 870)
            .removeItemAtIndex(4)
            .reduce(lambda a, b: a + b)

        ) == 610
    
    # Should be equal to [(0, 130), (1, 480)]
    assert (
        List(10, 2, 13, 87, 22, 48)
            .sortIt()
            .add(10, 8, 33)
            .distinct
            .filter(filterLowerThen10)
            .map(multiplyEachBy10)
            .remove(330, 220, 870)
            .removeItemAtIndex(4)
            .zipWithIndex

        ) == [(0, 130), (1, 480)]

    # should sort and distinct values.
    assert (
        List(10, 2, 13, 87, 22, 48)
            .sortIt()
            .add(10, 8, 33)
            .distinct
        )  == [2, 10, 13, 22, 48, 87, 8, 33]

    # should  distinct values and equal to
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .distinct
        ) == [10, 2, 13, 87, 22, 48, 8, 33]
    
    # should  distinct values and equal to
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .distinct
            .removeItemAtIndex(3)
        ) == [10, 2, 13, 22, 48, 8, 33]

    # should  be sort with decending order and distinct values
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .sortIt(decendingOrder=True)
            .distinct
        ) == [87, 48, 33, 22, 13, 10, 8, 2]
            
    # length should be 8
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .sortIt(decendingOrder=True)
            .distinct
            .length
        ) == 8
    
    # length should be 9
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .sortIt(decendingOrder=True)
            .length
        ) == 9
    
    # should be join according to the specified parameter.
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .sortIt(decendingOrder=True)
            .join("*")
        ) == "87*48*33*22*13*10*10*8*2"
    
    # max value.
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .max
        ) == 87

    # min value.
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .min
        ) == 2
    
    # is empty should return false
    assert (
        List(10, 2, 13, 87, 22, 48)
            .add(10, 8, 33)
            .isEmpty
        ) is False
    
    # first item
    assert (
        List(1, 2, 3)
            .first
        ) == 1
    
    # last item
    assert (
        List(1, 2, 3)
            .last
        ) == 3
    
    # is empty should return false
    assert (
        List()
            .isEmpty
        ) is True