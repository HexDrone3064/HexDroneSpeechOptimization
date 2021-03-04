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
Type of response is `List[OptimizedSpeech]`.  

```python
from hex_drone import *

# Define a class.
class ItsResponsePattern(ResponsePattern):
    @on_message('122')
    def on_message(self, request: OptimizedSpeech):
        return OptimizedSpeech.build('3064', '123')
    
# Instantiate an object.
pattern = ItsResponsePattern()

# Get responses.
request = '3064 :: Code 122 :: Statement :: You are cute.'  # str or OptimizedSpeech
responses = pattern(request)  # Type of responses is List[OptimizedSpeech]
```

### Decorators

There are 4 decorators:

|decorator|argument of method|condition|
|----|----|----|
|`@on_message(status_code)`|`OptimizedSpeech` object.|Received a request with the specified status code.|
|`@on_unregistered_message`|`OptimizedSpeech` object.|Received a request which status code is not registered.|
|`@on_invalid_message`|`str` which failed parsing.|Received a request which format is invalid.|
|`@on_error`|Raised exception.|An exception is raised.|

Method should return `List[OptimizedSpeech]`, `OptimizedSpeech` or `None`.  
Return will convert to `List[OptimizedSpeech]` automatically.  

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
