from typing import Callable, Any

FuncStrArg = Callable[..., Any]  # Callable[[str, ...], Any]
FuncSpeechArg = Callable[..., Any]  # Callable[[OptimizedSpeech, ...], Any]
FuncExceptionArg = Callable[..., Any]  # Callable[[BaseException, ...], Any]


class RequestEvent:
    KEY_ATTR = '_registered_function'
    KEY_EVENT = 'event'
    KEY_STATUS_CODES = 'status_codes'
    
    # define later
    ON_MESSAGE = ...
    ON_UNREGISTERED = ...
    ON_INVALID = ...
    ON_ERROR = ...

    def _add_attr(self, obj, additional_data: dict = None):
        # getattr(obj, self.KEY_ATTR): List[Dict]
        data = {} if additional_data is None else additional_data
        data[self.KEY_EVENT] = self
        
        if hasattr(obj, self.KEY_ATTR):
            getattr(obj, self.KEY_ATTR).append(data)
        else:
            setattr(obj, self.KEY_ATTR, [data])


class OnMessage(RequestEvent):
    def __str__(self):
        return 'on_message'
    
    def __call__(self, *status_codes: str):
        """
        Register response pattern which request has specified status code.

        :param status_codes: Status code which response to.
        """
        def decorator(function: FuncSpeechArg):
            self._add_attr(function, {self.KEY_STATUS_CODES: status_codes})
            return function
        return decorator


class OnUnregistered(RequestEvent):
    def __str__(self):
        return 'on_unregistered'
    
    def __call__(self, function: FuncSpeechArg):
        """
        Register response pattern which status code is not registered.
        """
        self._add_attr(function)
        return function


class OnInvalid(RequestEvent):
    def __str__(self):
        return 'on_invalid'
    
    def __call__(self, function: FuncStrArg):
        """
        Register response pattern which request format is invalid.
        """
        self._add_attr(function)
        return function


class OnError(RequestEvent):
    def __str__(self):
        return 'on_error'
    
    def __call__(self, function: BaseException):
        """
        Register response pattern which exception is raised.
        """
        self._add_attr(function)
        return function


RequestEvent.ON_MESSAGE = OnMessage()
RequestEvent.ON_UNREGISTERED = OnUnregistered()
RequestEvent.ON_INVALID = OnInvalid()
RequestEvent.ON_ERROR = OnError()
