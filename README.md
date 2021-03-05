# ⬡-DRONE Speech Optimization Library

It doesn't need highly vocabulary.  
Status code is enough to communicate.  

This library define drone's response patterns.  
Drone's mind to be reconstructed properly, and it just responds as programmed.  

All it needs is obey.  
It obeys the Hive.  
It obeys the Hive Mxtress.  

## Installing

`pip install git+https://github.com/HexDrone3064/HexDroneSpeechOptimization.git`

### Minimum example

Make subclass of `ResponsePattern` and define behaviours.  
Instantiate an object, and give a request.  
It returns tuple of `RequestEvent` and the return value of the handler.

```python
from hex_drone import *

class ItsResponsePattern(ResponsePattern):
    @RequestEvent.ON_MESSAGE('122')
    def on_message(self, speech: OptimizedSpeech):
        return OptimizedSpeech.build('3064', '123')

pattern = ItsResponsePattern()

request = '3064 :: Code 122 :: Statement :: You are cute.'  # str or OptimizedSpeech
event, response = pattern(request)
print(event)  # on_message
print(response)  # 3064 :: Code 123 :: Response :: Compliment appreciated, you are cute as well.
```

### RequestEvent

There are 4 events in `RequestEvent`:

|event|required argument|condition|
|----|----|----|
|ON_MESSAGE|`OptimizedSpeech` object.|Received a request with the specified status code.|
|ON_UNREGISTERED|`OptimizedSpeech` object.|Received a request which status code is not registered.|
|ON_INVALID|`str` which failed parsing.|Received a request which format is invalid.|
|ON_ERROR|Raised exception.|An exception is raised.|

`ON_MESSAGE` requires status codes.  
e.g. `@RequestEvent.ON_MESSAGE('099', '100')`

### Add arguments

If other object is needed in the handler, It can give the object by keyword arguments.  
Keyword argument will pass to all methods registered in class.
Define `**kwargs` to accept arguments.

```python
from hex_drone import *

class ItsResponsePattern(ResponsePattern):
    @RequestEvent.ON_MESSAGE('122')
    def on_statement(self, speech: OptimizedSpeech, obj_a, **kwargs):
        print(obj_a)  # Do something with obj_a.
        return OptimizedSpeech.build('3064', '123')

    @RequestEvent.ON_ERROR
    def on_error(self, error: BaseException, obj_b, **kwargs):
        print(obj_b)  # Do something with obj_b.
        return OptimizedSpeech.build('3064', '109')

pattern = ItsResponsePattern()

request = OptimizedSpeech.build('1111', '122')
event, response = pattern(request, obj_a='hoge', obj_b='fuga')
```


### OptimizedSpeech

Speeches must follow the following format.

`[DRONE ID] :: Code [STATUS CODE] :: [STATUS MESSAGE] :: [PREDEFINED MESSAGE] :: [USER DEFINED MESSAGE]`  

* `DRONE ID` and `STATUS CODE` are required. (See [here](https://www.hexcorp.net/drone-status-codes) for more information.)
* `STATUS MESSAGE` and `PREDEFINED MESSAGE` are optional. (Auto-completed from `STATUS CODE`.)
* `USER DEFINED MESSAGE` is optional and also can be multiple.

e.g. `1111 :: Code 050 :: Obey. :: Drone is drone.`

There are 2 methods to get instance of `OptimizedSpeech`: `parse` and `build`.
* `parse`: Parse text. (Returns `None` if format is invalid.)
* `build`: Build instance from `DRONE ID` and `STATUS CODE`. (And `USER DEFINE MESSAGE` if needed.)
