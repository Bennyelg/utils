
import time
import threading
import copy
from datetime import datetime, timedelta

from threading import Timer
from functools import partial


def seconds(n):
    return n


def minutes(n):
    return n * 60


def hours(n):
    return n * 60 * 60


class Interval(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        """
        Runs the function at a specified interval with given arguments.
        """
        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running  = False 
        self._timer   = None 

    def __call__(self):
        """
        Handler function for calling the partial and continuting. 
        """
        self.running = False  # mark not running
        self.start()          # reset the timer for the next go 
        self.function()       # call the partial function 

    def start(self):
        """
        Starts the interval and lets it run. 
        """
        if self.running:
            # Don't start if we're running! 
            return 
            
        # Create the timer object, start and set state. 
        self._timer = Timer(self.interval, self)
        self._timer.start() 
        self.running = True

    def stop(self):
        """
        Cancel the interval (no more function calls).
        """
        if self._timer:
            self._timer.cancel() 
        self.running = False 
        self._timer  = None


class MiniCache(dict):

    def __init__(self):

        self._cache = {}
        self.watcher = Interval(0.1, self._cleaner)
        self.watcher.start()

    def set(self, key, value, ttl=None):
        if not ttl:
           self._cache[key] = {"value": value} 
        else:
            self._cache[key] = {"value": value, "ttl": datetime.now() + timedelta(seconds=ttl)}
    
    def get(self, key):
        try:
            return self._cache[key]["value"]
        except KeyError:
            return None

    def flush_all(self):
        self._cache = {}
        self.watcher.stop()
    
    def flush_all_temporary_keys(self):
        tempcache = copy.copy(self._cache)
        for key, value in self._cache.items():
            if 'ttl' not in value:
                tempcache[key] = value
        self._cache = tempcache

    def flush_all_parament_keys(self):
        tempcache = copy.copy(self._cache)
        for key, value in self._cache.items():
            if 'ttl' in value:
                tempcache[key] = value
        self._cache = tempcache

    def num_of_temporary_keys(self):
        return sum(1 for _, value in self._cache.items() if 'ttl' in value)
    
    def num_of_parament_keys(self):
        return sum(1 for _, value in self._cache.items() if 'ttl' not in value)

    def num_of_keys(self):
        return len(self._cache)

    def _cleaner(self):
        try:
            for key, value in self._cache.items():
                if "ttl" not in value:
                    continue
                if datetime.now() >= value["ttl"]:
                    del self._cache[key]
        except RuntimeError:
            pass

    
    
if __name__ == '__main__':
    cache = MiniCache()
    cache.set("game", "Oni 2")
    print(cache.num_of_keys())
    cache.set("game2", "Oni 4")
    print(cache.num_of_keys())
    cache.set("expired_key", "Oni 5", ttl=seconds(5))

    cache.flush_all()
