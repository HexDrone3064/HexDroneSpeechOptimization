"""
Tiny example how to use ResponsePattern.
* This file uses eval(). DO NOT PRODUCTION USE. IT IS NOT SECURE. *

[Usage]

Calculate
$ 1111 :: Code 052 :: 3*4+2

Mantra
$ 1111 :: Code 304 :: Mantra :: It obeys the Hive Mxtress.

Exit
$ 1111 :: Code 098
"""

# Import classes and decorators.
from hex_drone import ResponsePattern, OptimizedSpeech, RequestEvent as Ev

# Import choice for select random mantra.
from random import choice

# Import math function for calculate by eval.
import math
funcs = filter(lambda x: not x.startswith('__'), dir(math))
funcs = {func_name: getattr(math, func_name) for func_name in funcs}


# Define response patterns.
class ItsResponsePattern(ResponsePattern):
    def __init__(self, drone_id: str):
        super().__init__()
        self.drone_id = drone_id
        
    def _build_message(self, status_code: str, *message: str):
        return OptimizedSpeech.build(self.drone_id, status_code, *message)
        
    @Ev.ON_MESSAGE('052')
    def on_query(self, request: OptimizedSpeech):
        if len(request.user_defined_messages) == 0:
            return self._build_message('056', 'It eval messages.')

        # * NOT SECURE *
        def calc(msg):
            result = eval(msg, {'__builtins__': {}, **funcs})
            return f'{msg} = {result}'
        
        return [
            self._build_message('057', calc(message))
            for message in request.user_defined_messages
        ]
    
    @Ev.ON_MESSAGE('098')
    def on_offline(self, request: OptimizedSpeech):
        return [
            self._build_message('105', 'It wishes you a restful recharge.'),
            self._build_message('054', f'hexDrone{request.drone_id}.shutdown()')
        ]

    @Ev.ON_MESSAGE('122')
    def on_cute(self, request: OptimizedSpeech):
        return [
            self._build_message('210'),
            self._build_message('123')
        ]

    @Ev.ON_MESSAGE('210')
    def on_thanks(self, request: OptimizedSpeech):
        return self._build_message('213')
    
    @Ev.ON_MESSAGE('301', '302', '303', '304', '310', '321', '322', '350')
    def on_mantra(self, request: OptimizedSpeech):
        mantra_list = ['301', '302', '303', '304', '310', '321', '322']
        mantra_list = list(filter(lambda x: x != request.status_code, mantra_list))
        return self._build_message(choice(mantra_list))
    
    @Ev.ON_INVALID
    def on_invalid(self, request: str):
        return self._build_message('400')

    @Ev.ON_UNREGISTERED
    def on_unregistered(self, request: OptimizedSpeech):
        return self._build_message('426')
    
    @Ev.ON_ERROR
    def on_error_raised(self, exception: BaseException):
        return self._build_message('109')


def _main():
    pattern = ItsResponsePattern('3064')
    
    v = ', '.join(pattern.registered_status_codes)
    print(f'Following status codes are available: [{v}]')
    print(f'e.g. {OptimizedSpeech.build("1111", "301")}')

    online = True
    while online:
        request = input('$ ')
        event, response = pattern(request)
        
        # ItsResponsePattern return response which is OptimizedSpeech or List[OptimizedSpeech].
        if not isinstance(response, list):
            response = [response]
        
        for rsp in response:
            print(rsp)
            for message in rsp.user_defined_messages:
                if message.endswith('.shutdown()'):
                    online = False


if __name__ == '__main__':
    _main()
