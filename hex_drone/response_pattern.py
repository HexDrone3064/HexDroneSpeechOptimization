"""
Classes and decorators for define ⬡-Drone's response pattern.
"""

from optimized_speech import OptimizedSpeech
from functools import wraps

from typing import Callable, Optional, Union, Dict, List
OptimizedSpeeches = Union[List[OptimizedSpeech], OptimizedSpeech, None]
FuncStrArg = Callable[[str], OptimizedSpeeches]
FuncSpeechArg = Callable[[OptimizedSpeech], OptimizedSpeeches]
FuncExceptionArg = Callable[[BaseException], OptimizedSpeeches]


def return_list(function: Callable[..., OptimizedSpeeches]):
    """
    Convert returned value to list.
    """
    @wraps(function)
    def decorated_func(*args, **kwargs) -> List[OptimizedSpeech]:
        result = function(*args, **kwargs)
        if result is None:
            return []
        elif isinstance(result, list):
            return result
        else:
            return [result]
    return decorated_func


KEY_ATTR = '_registered_function'
KEY_EVENT = 'event'
KEY_STATUS_CODES = 'status_codes'
EVENT_ON_MESSAGE = 'on_message'
EVENT_ON_INVALID_MESSAGE = 'on_invalid_message'
EVENT_ON_UNREGISTERED_MESSAGE = 'on_unregistered_message'
EVENT_ON_ERROR = 'on_error'


def _add_attr(obj, value):
    if hasattr(obj, KEY_ATTR):
        getattr(obj, KEY_ATTR).append(value)
    else:
        setattr(obj, KEY_ATTR, [value])


def on_message(*status_codes: str):
    """
    Register response pattern which request has specified status code.

    :param status_codes: Status code which response to.
    """
    def decorator(function: FuncSpeechArg):
        _add_attr(function, {KEY_EVENT: EVENT_ON_MESSAGE, KEY_STATUS_CODES: status_codes})
        return function
    return decorator


def on_invalid_message(function: FuncStrArg):
    """
    Register response pattern which request format is invalid.
    """
    _add_attr(function, {KEY_EVENT: EVENT_ON_INVALID_MESSAGE})
    return function


def on_unregistered_message(function: FuncSpeechArg):
    """
    Register response pattern which status code is not registered.
    """
    _add_attr(function, {KEY_EVENT: EVENT_ON_UNREGISTERED_MESSAGE})
    return function


def on_error(function: FuncExceptionArg):
    """
    Register response pattern which exception is raised.
    """
    _add_attr(function, {KEY_EVENT: EVENT_ON_ERROR})
    return function


class ResponsePatternMeta(type):
    """
    Metaclass to register response pattern.
    """
    
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._func_name_on_message: Dict[str, str] = {}
        cls._func_name_on_invalid_message: Optional[str] = None
        cls._func_name_on_unregistered_message: Optional[str] = None
        cls._func_name_on_error: Optional[str] = None

        for func_name, func in attrs.items():  # It may not function, but others will be skipped.
            for event_dict in getattr(func, KEY_ATTR, []):
                event = event_dict[KEY_EVENT]
                if event == EVENT_ON_MESSAGE:
                    for code in event_dict[KEY_STATUS_CODES]:
                        cls._func_name_on_message[code] = func_name
                elif event == EVENT_ON_INVALID_MESSAGE:
                    cls._func_name_on_invalid_message = func_name
                elif event == EVENT_ON_UNREGISTERED_MESSAGE:
                    cls._func_name_on_unregistered_message = func_name
                elif event == EVENT_ON_ERROR:
                    cls._func_name_on_error = func_name
    

class ResponsePattern(metaclass=ResponsePatternMeta):
    """
    Class to register response patterns.
    """
    
    def __init__(self):
        def get_func(func_name):
            if func_name is None:
                return None
            return getattr(self, func_name, None)
        
        self._on_message: Dict[str, FuncSpeechArg] = {
            status_code: get_func(func_name)
            for status_code, func_name in self._func_name_on_message.items()
        }
        self._on_invalid_message: Optional[FuncStrArg] = \
            get_func(self._func_name_on_invalid_message)
        self._on_unregistered_message: Optional[FuncSpeechArg] = \
            get_func(self._func_name_on_unregistered_message)
        self._on_error: Optional[FuncExceptionArg] = \
            get_func(self._func_name_on_error)
        
        self.registered_status_codes = self._on_message.keys()
    
    @return_list  # Decorator convert returns from OptimizedSpeeches to List[OptimizedSpeech]
    def __call__(self, request: Union[str, OptimizedSpeech]) -> List[OptimizedSpeech]:
        """
        Get response messages.
        
        :param request: Raw text or parsed speech.
        :return: A list which contains response messages. It might be empty.
        """
        try:
            if isinstance(request, str):
                r = request
                request = OptimizedSpeech.parse(request)
                if request is None:
                    if self._on_invalid_message is None:
                        return []
                    return self._on_invalid_message(r)
            
            func = self._on_message.get(request.status_code)
            if func is None:
                if self._on_unregistered_message is None:
                    return []
                return self._on_unregistered_message(request)
            
            return func(request)
        except BaseException as e:
            if self._on_error is None:
                return []
            return self._on_error(e)
