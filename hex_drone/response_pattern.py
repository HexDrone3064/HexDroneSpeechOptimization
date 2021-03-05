"""
Classes and decorators for define ⬡-Drone's response pattern.
"""

from .optimized_speech import OptimizedSpeech
from .request_event import RequestEvent
from .logs import get_logger
from logging import Logger
from typing import Callable, Optional, Union, Dict, Tuple, List, Any

FuncStrArg = Callable[..., Any]  # Callable[[str, ...], Any]
FuncSpeechArg = Callable[..., Any]  # Callable[[OptimizedSpeech, ...], Any]
FuncExceptionArg = Callable[..., Any]  # Callable[[BaseException, ...], Any]


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
            events: List[dict] = getattr(func, RequestEvent.KEY_ATTR, [])
            for event_dict in events:
                event = event_dict[RequestEvent.KEY_EVENT]
                if event == RequestEvent.ON_MESSAGE:
                    for code in event_dict[RequestEvent.KEY_STATUS_CODES]:
                        cls._func_name_on_message[code] = func_name
                elif event == RequestEvent.ON_INVALID:
                    cls._func_name_on_invalid_message = func_name
                elif event == RequestEvent.ON_UNREGISTERED:
                    cls._func_name_on_unregistered_message = func_name
                elif event == RequestEvent.ON_ERROR:
                    cls._func_name_on_error = func_name
    

class ResponsePattern(metaclass=ResponsePatternMeta):
    """
    Class to register response patterns.
    """
    
    def __init__(self, logger: Logger = None):
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
        
        self._logger = get_logger(__name__) if logger is None else logger

    @property
    def registered_status_codes(self):
        return self._on_message.keys()
    
    def __call__(self, request: Union[str, OptimizedSpeech], **kwargs) -> Tuple[RequestEvent, Any]:
        """
        Get response messages.
        Note that *option_args and **option_kwargs are given to all registered methods.
        
        :param request: Raw text or parsed speech.
        :param kwargs: Arguments to be given to the registered method.
        :return: A list which contains response messages. It might be empty.
        """

        def _try_call(event: RequestEvent, func: Optional[Callable], *args) -> Tuple[RequestEvent, Any]:
            if func is None:
                self._logger.debug(f'The function for {event} is None.')
                return event, None
    
            try:
                self._logger.debug(f'Invoke the function for {event}')
                return event, func(*args, **kwargs)
            except BaseException as e:
                self._logger.exception(f'An exception raised while handling {event}.')
                if self._on_error is None:
                    self._logger.debug(f'The function for {RequestEvent.ON_ERROR} is None.')
                    return RequestEvent.ON_ERROR, None
                try:
                    self._logger.debug(f'Invoke the function for {RequestEvent.ON_ERROR}')
                    return RequestEvent.ON_ERROR, self._on_error(e, **kwargs)
                except BaseException as e2:
                    self._logger.exception(f'An exception raised while handling {RequestEvent.ON_ERROR}.')
                    return RequestEvent.ON_ERROR, None

        if isinstance(request, str):
            r = request
            request = OptimizedSpeech.parse(request)
            if request is None:
                return _try_call(RequestEvent.ON_INVALID, self._on_invalid_message, r)
            
        request: OptimizedSpeech

        func = self._on_message.get(request.status_code)
        if func is None:
            return _try_call(RequestEvent.ON_UNREGISTERED, self._on_unregistered_message, request)
        
        return _try_call(RequestEvent.ON_MESSAGE, func, request)
